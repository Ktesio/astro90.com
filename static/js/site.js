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
  const host = document.querySelector("[data-brand-scene]");
  let manuallyPaused = false;
  try {
    manuallyPaused =
      sessionStorage.getItem("astro90-spatial-motion") === "paused";
  } catch {}
  let paused = false;
  let brandScene = null;
  let loadingScene = false;
  let frame = 0;
  let lastTime = 0;
  const target = { x: 0, y: 0, scroll: scrollY };
  const current = { ...target };
  const clamp = (v, min = 0, max = 1) => Math.min(max, Math.max(min, v));

  function schedule() {
    if (!frame && !document.hidden) frame = requestAnimationFrame(render);
  }
  async function loadScene() {
    if (!host || brandScene || loadingScene || paused) return;
    loadingScene = true;
    try {
      const { createBrandScene } = await import(host.dataset.sceneModule);
      if (!paused) brandScene = createBrandScene(host);
      schedule();
    } catch {
      // The authored Blender poster remains if the module or WebGL is unavailable.
    } finally {
      loadingScene = false;
    }
  }
  function render(time) {
    frame = 0;
    const delta = Math.min(64, time - (lastTime || time - 16));
    lastTime = time;
    const damping = 1 - Math.exp(-delta / 85);
    current.x += (target.x - current.x) * damping;
    current.y += (target.y - current.y) * damping;
    current.scroll += (target.scroll - current.scroll) * damping;
    const x = paused ? 0 : current.x;
    const y = paused ? 0 : current.y;
    root.style.setProperty("--pointer-x", x.toFixed(4));
    root.style.setProperty("--pointer-y", y.toFixed(4));
    let identityProgress = 0;
    for (const scene of scenes) {
      const bounds = scene.getBoundingClientRect();
      const top = bounds.top + scrollY - current.scroll;
      const distance = Math.max(1, bounds.height - innerHeight);
      const p = paused ? 0 : clamp(-top / distance);
      scene.style.setProperty("--progress", p.toFixed(4));
      scene.style.setProperty(
        "--arrival",
        clamp(1 - top / innerHeight).toFixed(4),
      );
      if (scene.dataset.scene === "identity") identityProgress = p;
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
    if (host && !paused) {
      const bounds = host.getBoundingClientRect();
      if (bounds.bottom > 0 && bounds.top < innerHeight) {
        if (!brandScene) loadScene();
        brandScene?.render({ x, y, progress: identityProgress });
      }
    }
    const settling =
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
      brandScene?.dispose();
      brandScene = null;
      target.x = target.y = current.x = current.y = 0;
    }
    target.scroll = current.scroll = scrollY;
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
      schedule();
    },
    { passive: true },
  );
  document.addEventListener("pointerleave", () => {
    target.x = target.y = 0;
    schedule();
  });
  addEventListener(
    "scroll",
    () => {
      target.scroll = scrollY;
      schedule();
    },
    { passive: true },
  );
  addEventListener(
    "resize",
    () => {
      target.scroll = scrollY;
      schedule();
    },
    { passive: true },
  );
  addEventListener("astro90:render", schedule);
  addEventListener("pageshow", () => {
    target.scroll = current.scroll = scrollY;
    schedule();
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

  const gallery = document.querySelector(".gallery-dialog");
  if (gallery && typeof gallery.showModal === "function") {
    const image = gallery.querySelector(".gallery-large");
    const title = gallery.querySelector("#gallery-title");
    let opener;
    document.querySelectorAll("[data-gallery-src]").forEach((button) => {
      button.addEventListener("click", () => {
        opener = button;
        image.src = button.dataset.gallerySrc;
        image.alt = button.querySelector("img").alt;
        title.textContent = button.dataset.galleryTitle;
        gallery.showModal();
        gallery.scrollTop = 0;
      });
    });
    gallery
      .querySelector("[data-gallery-close]")
      .addEventListener("click", () => gallery.close());
    gallery.addEventListener("click", (event) => {
      if (event.target !== gallery) return;
      const bounds = gallery.getBoundingClientRect();
      if (
        event.clientX < bounds.left ||
        event.clientX > bounds.right ||
        event.clientY < bounds.top ||
        event.clientY > bounds.bottom
      )
        gallery.close();
    });
    gallery.addEventListener("close", () =>
      opener?.focus({ preventScroll: true }),
    );
  }
})();
