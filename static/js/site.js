/* Static presentation: input-led artwork, project index and image viewer. */
(() => {
  const root = document.documentElement;
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
  const finePointer = matchMedia("(pointer: fine)");
  const buttons = [...document.querySelectorAll("[data-motion-toggle]")];
  const scenes = [...document.querySelectorAll("[data-scene]")];
  const depthElements = [
    ...document.querySelectorAll(
      "[data-depth], .project-card, .project-hero-art, .feature, .screenshot, .brand-chapter, .studio-line",
    ),
  ];
  const host = document.querySelector("[data-brand-film]");
  const landscape = document.querySelector("[data-night-landscape]");
  const landscapeImage = landscape?.querySelector("[data-night-image]");
  let landscapeMetrics = null;
  let landscapePointer = false;
  let beamAngle = 186;
  let manuallyPaused = false;
  try {
    manuallyPaused =
      sessionStorage.getItem("astro90-spatial-motion") === "paused";
  } catch {}
  let paused = false;
  let film = null;
  let filmStarted = false;
  let frame = 0;
  let lastTime = 0;
  let measurementsDirty = true;
  let sceneMeasurements = [];
  const target = { x: 0, y: 0, scroll: scrollY };
  const current = { ...target };
  const clamp = (v, min = 0, max = 1) => Math.min(max, Math.max(min, v));
  const ease = (value) => {
    const t = clamp(value);
    return t * t * (3 - 2 * t);
  };

  function measureScenes() {
    // Scene containers never transform. Cache their document coordinates so
    // scrolling does not interleave layout reads with style writes per scene.
    sceneMeasurements = scenes.map((scene) => {
      const bounds = scene.getBoundingClientRect();
      const next =
        scene.dataset.nextScene &&
        document.getElementById(scene.dataset.nextScene);
      const nextBounds = next?.getBoundingClientRect();
      const overlap = nextBounds
        ? Math.max(0, bounds.bottom - nextBounds.top)
        : 0;
      return {
        scene,
        top: bounds.top + scrollY,
        nextTop: nextBounds ? nextBounds.top + scrollY : null,
        distance: Math.max(1, bounds.height - innerHeight - overlap),
      };
    });
    if (landscape && landscapeImage) {
      const width = landscape.clientWidth;
      const height = landscape.clientHeight;
      const sourceWidth = landscapeImage.naturalWidth || 1643;
      const sourceHeight = landscapeImage.naturalHeight || 957;
      const scale = Math.max(width / sourceWidth, height / sourceHeight);
      const focus = parseFloat(
        getComputedStyle(landscape).getPropertyValue("--landscape-focus"),
      );
      // Keep the light attached to the painted lantern as object-fit crops
      // the panorama differently on desktop, tablet and portrait phones.
      const beaconX =
        (width - sourceWidth * scale) * focus + sourceWidth * scale * 0.745;
      const beaconY =
        (height - sourceHeight * scale) / 2 + sourceHeight * scale * 0.45;
      landscapeMetrics = { width, height, beaconX, beaconY };
      landscape.style.setProperty("--beacon-x", `${beaconX.toFixed(2)}px`);
      landscape.style.setProperty("--beacon-y", `${beaconY.toFixed(2)}px`);
    }
    measurementsDirty = false;
  }
  function invalidateMeasurements() {
    measurementsDirty = true;
    schedule();
  }

  function schedule() {
    if (!frame && !document.hidden) frame = requestAnimationFrame(render);
  }
  function updateFilm() {
    if (!host) return;
    if (paused) {
      film?.remove();
      film = null;
      host.classList.remove("is-playing");
      return;
    }
    if (filmStarted || !host.dataset.brandFilm) return;
    filmStarted = true;
    film = new Image(720, 720);
    film.className = "brand-film";
    film.alt = "";
    film.setAttribute("aria-hidden", "true");
    film.decoding = "async";
    film.fetchPriority = "high";
    const playingFilm = film;
    film.addEventListener(
      "load",
      () => {
        // The WebP plays once. Release its decoded frames after the sequence and
        // leave the identically framed, higher-resolution Blender still in place.
        setTimeout(() => {
          if (film !== playingFilm) return;
          film.remove();
          film = null;
          host.classList.remove("is-playing");
        }, 3400);
      },
      { once: true },
    );
    film.addEventListener(
      "error",
      () => {
        film?.remove();
        film = null;
        host.classList.remove("is-playing");
      },
      { once: true },
    );
    film.src = host.dataset.brandFilm;
    host.append(film);
    host.classList.add("is-playing");
  }
  function updateLandscape(damping) {
    if (!landscapeMetrics || paused) return false;
    const { width, height, beaconX, beaconY } = landscapeMetrics;
    let angle = 186 - clamp(current.scroll / (height * 0.8)) * 24;
    if (landscapePointer) {
      const aimX = Math.min(
        ((current.x + 1) / 2) * width,
        beaconX - width * 0.2,
      );
      const aimY = ((current.y + 1) / 2) * height;
      angle = (Math.atan2(aimY - beaconY, aimX - beaconX) * 180) / Math.PI;
      if (angle < 0) angle += 360;
      angle = clamp(angle, 138, 218);
    }
    beamAngle += (angle - beamAngle) * damping;
    landscape.style.setProperty("--beam-angle", `${beamAngle.toFixed(3)}deg`);
    return Math.abs(angle - beamAngle) > 0.02;
  }
  function render(time) {
    frame = 0;
    const delta = Math.min(64, time - (lastTime || time - 16));
    lastTime = time;
    const damping = 1 - Math.exp(-delta / 85);
    current.x += (target.x - current.x) * damping;
    current.y += (target.y - current.y) * damping;
    current.scroll += (target.scroll - current.scroll) * damping;
    if (measurementsDirty) measureScenes();
    const x = paused ? 0 : current.x;
    const y = paused ? 0 : current.y;
    root.style.setProperty("--pointer-x", x.toFixed(4));
    root.style.setProperty("--pointer-y", y.toFixed(4));
    const landscapeSettling = updateLandscape(damping);
    for (const { scene, top, nextTop, distance } of sceneMeasurements) {
      const p = paused ? 0 : clamp((current.scroll - top) / distance);
      // Overlap follows the native scroll position, keeping the outgoing view
      // registered with the next section while its contents ease out.
      const handoff = paused
        ? 0
        : nextTop === null
          ? clamp((p - 0.55) / 0.45)
          : clamp((scrollY + innerHeight - nextTop) / innerHeight);
      scene.style.setProperty("--progress", p.toFixed(4));
      scene.style.setProperty("--outro", ease(handoff).toFixed(4));
      scene.style.setProperty(
        "--outro-content",
        ease(handoff / 0.6).toFixed(4),
      );
      scene.style.setProperty(
        "--arrival",
        (paused
          ? 1
          : clamp((scrollY + innerHeight - top) / innerHeight)
        ).toFixed(4),
      );
    }
    for (const element of depthElements) {
      const bounds = element.getBoundingClientRect();
      // Neutral at the viewport center; approach/departure has signed depth.
      const depth = paused
        ? 0
        : clamp(
            (bounds.top + bounds.height / 2 - innerHeight / 2) / innerHeight,
            -1,
            1,
          );
      element.style.setProperty("--depth", depth.toFixed(4));
    }
    const settling =
      landscapeSettling ||
      Math.abs(current.x - target.x) + Math.abs(current.y - target.y) > 0.001 ||
      Math.abs(current.scroll - target.scroll) > 0.2;
    if (settling && !paused) schedule();
  }

  function updateMotion() {
    paused = manuallyPaused || reducedMotion.matches;
    root.dataset.motion = paused ? "paused" : "running";
    buttons.forEach((button) => {
      const label = reducedMotion.matches
        ? "Reduced motion enabled by your device"
        : paused
          ? "Enable full motion"
          : "Reduce motion";
      button.setAttribute("aria-label", label);
      button.setAttribute("aria-pressed", String(paused));
      button.disabled = reducedMotion.matches;
      button.querySelector("span").textContent = reducedMotion.matches
        ? "Reduced motion"
        : paused
          ? "Full motion"
          : "Reduce motion";
      button
        .querySelector("path")
        ?.setAttribute("d", paused ? "m9 5 11 7-11 7V5Z" : "M8 5v14M16 5v14");
    });
    if (paused) {
      target.x = target.y = current.x = current.y = 0;
      landscapePointer = false;
    }
    updateFilm();
    target.scroll = current.scroll = scrollY;
    measurementsDirty = true;
    schedule();
  }
  buttons.forEach((button) =>
    button.addEventListener("click", () => {
      manuallyPaused = !manuallyPaused;
      try {
        sessionStorage.setItem(
          "astro90-spatial-motion",
          manuallyPaused ? "paused" : "running",
        );
      } catch {}
      updateMotion();
    }),
  );
  reducedMotion.addEventListener("change", updateMotion);
  addEventListener(
    "pointermove",
    (event) => {
      if (paused || !finePointer.matches || event.pointerType === "touch")
        return;
      target.x = clamp((event.clientX / innerWidth) * 2 - 1, -1, 1);
      target.y = clamp((event.clientY / innerHeight) * 2 - 1, -1, 1);
      landscapePointer = true;
      schedule();
    },
    { passive: true },
  );
  document.addEventListener("pointerleave", () => {
    target.x = target.y = 0;
    landscapePointer = false;
    schedule();
  });
  addEventListener(
    "scroll",
    () => {
      target.scroll = scrollY;
      if (!finePointer.matches) landscapePointer = false;
      schedule();
    },
    { passive: true },
  );
  addEventListener(
    "resize",
    () => {
      target.scroll = scrollY;
      invalidateMeasurements();
    },
    { passive: true },
  );
  addEventListener("astro90:render", schedule);
  landscapeImage?.addEventListener("load", invalidateMeasurements);
  landscape?.addEventListener(
    "pointerdown",
    (event) => {
      if (paused || event.pointerType !== "touch" || event.target.closest("a"))
        return;
      landscapePointer = true;
      target.x = clamp((event.clientX / innerWidth) * 2 - 1, -1, 1);
      target.y = clamp((event.clientY / innerHeight) * 2 - 1, -1, 1);
      schedule();
    },
    { passive: true },
  );
  addEventListener("pageshow", () => {
    target.scroll = current.scroll = scrollY;
    invalidateMeasurements();
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      cancelAnimationFrame(frame);
      frame = 0;
    } else {
      lastTime = 0;
      schedule();
    }
  });
  root.classList.add("spatial-ready");
  updateMotion();
  const sceneObserver = new ResizeObserver(invalidateMeasurements);
  scenes.forEach((scene) => sceneObserver.observe(scene));
  document.fonts?.ready.then(invalidateMeasurements);

  const index = document.querySelector("#project-index");
  const indexOpener = document.querySelector("[data-index-open]");
  if (index && indexOpener && typeof index.showModal === "function") {
    const map = index.querySelector(".atlas-map");
    indexOpener.addEventListener("click", () => {
      index.showModal();
      index.scrollTop = 0;
    });
    index
      .querySelector("[data-index-close]")
      .addEventListener("click", () => index.close());
    index.addEventListener("close", () =>
      indexOpener.focus({ preventScroll: true }),
    );
    index.querySelectorAll("[data-project]").forEach((link) => {
      const preview = () => {
        map.dataset.activeProject = link.dataset.project;
      };
      link.addEventListener("pointerenter", preview);
      link.addEventListener("focus", preview);
    });
  }

})();
