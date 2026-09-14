/* The sea is a native navigation dialog; motion only follows visitor input. */
(() => {
  const dialog = document.querySelector("#project-index");
  const opener = document.querySelector("[data-index-open]");
  if (!dialog || !opener) return;
  if (typeof dialog.showModal !== "function") {
    opener.hidden = true;
    document.querySelector(".no-script-nav").style.display = "flex";
    return;
  }

  const root = document.documentElement;
  const map = dialog.querySelector("[data-sea-map]");
  const islands = [...dialog.querySelectorAll("[data-island]")];
  const vessel = dialog.querySelector("[data-sea-vessel]");
  const course = dialog.querySelector("[data-sea-course]");
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
  const animations = new Set();
  let voyage = null;
  let departure = null;
  let activeIsland = null;
  const quiet = () => reducedMotion.matches || root.dataset.motion === "paused";
  const transform = (x, y, angle) => `translate(${x}px, ${y}px) rotate(${angle}deg)`;

  function play(element, frames, options) {
    const animation = element.animate(frames, options);
    animations.add(animation);
    animation.finished.then(
      () => animations.delete(animation),
      () => animations.delete(animation),
    );
    return animation;
  }

  function stopBoat() {
    // Capture its actual position before cancelling so a new course never jumps.
    const matrix = new DOMMatrixReadOnly(getComputedStyle(vessel).transform);
    const state = { x: matrix.e, y: matrix.f, angle: Math.atan2(matrix.b, matrix.a) * 180 / Math.PI };
    vessel.style.transform = transform(state.x, state.y, state.angle);
    voyage?.cancel();
    voyage = null;
    vessel.classList.remove("is-moving");
    return state;
  }

  function waterMap() {
    const bounds = map.getBoundingClientRect();
    const point = (x, y) => ({ x: x - bounds.x, y: y - bounds.y });
    const regions = islands.map(island => {
      const art = island.querySelector("[data-shoreline]");
      const box = art.getBoundingClientRect();
      const label = island.querySelector(".island-label-name").getBoundingClientRect();
      const labelBottom = Math.max(label.bottom, island.querySelector(".island-here")?.getBoundingClientRect().bottom || label.bottom);
      return {
        id: island.dataset.island,
        shore: JSON.parse(art.dataset.shoreline).map(([x, y]) => point(box.x + x * box.width, box.y + y * box.height)),
        label: [point(label.left, label.top), point(label.right, label.top), point(label.right, labelBottom), point(label.left, labelBottom)],
      };
    });
    return Astro90SeaRoutes.build(regions, bounds.width, bounds.height, vessel.clientWidth * .44);
  }

  function sailTo(island) {
    if (quiet() || !dialog.open) return;
    const start = stopBoat();
    const bounds = map.getBoundingClientRect();
    const dock = island.querySelector("[data-island-dock]").getBoundingClientRect();
    const path = Astro90SeaRoutes.plan(waterMap(), start, island.dataset.island, { x: dock.x - bounds.x, y: dock.y - bounds.y });
    course.removeAttribute("d");
    // Keep the vessel in open water if an unusually small layout has no route.
    if (!path || path.length < 2) return;
    const points = [path[0]];
    for (let i = 1; i < path.length; i++) {
      const a = path[i - 1], b = path[i];
      const steps = Math.max(1, Math.ceil(Astro90SeaRoutes.distance(a, b) / 8));
      for (let j = 1; j <= steps; j++) points.push({ x: a.x + (b.x - a.x) * j / steps, y: a.y + (b.y - a.y) * j / steps });
    }
    let total = 0;
    const lengths = points.map((p, i) => { if (i) total += Astro90SeaRoutes.distance(points[i - 1], p); return total; });
    if (total < 2) return;
    course.setAttribute("d", points.map((p, i) => `${i ? "L" : "M"}${p.x.toFixed(2)} ${p.y.toFixed(2)}`).join(" "));
    let angle = start.angle;
    const frames = points.map((p, i) => {
      const next = points[i + 1] || p;
      const heading = Math.atan2(next.y - p.y, next.x - p.x) * 180 / Math.PI;
      if (i && i < points.length - 1) angle += (((heading - angle + 540) % 360) - 180) * .35;
      return { transform: transform(p.x, p.y, angle), offset: lengths[i] / total };
    });
    vessel.classList.add("is-moving");
    const trip = play(vessel, frames, { duration: Math.min(1800, Math.max(700, total * 2.2)), easing: "cubic-bezier(.2,.6,.25,1)", fill: "forwards" });
    voyage = trip;
    trip.finished.then(() => {
      if (voyage !== trip) return;
      vessel.style.transform = frames.at(-1).transform;
      trip.cancel();
      voyage = null;
      vessel.classList.remove("is-moving");
    }, () => {});
  }

  function select(island) {
    if (activeIsland === island || departure !== null) return;
    activeIsland?.removeAttribute("data-active");
    activeIsland = island;
    if (island) {
      island.setAttribute("data-active", "");
      map.dataset.activeIsland = island.dataset.island;
      sailTo(island);
    } else {
      delete map.dataset.activeIsland;
    }
  }

  function cancelDeparture() {
    clearTimeout(departure);
    departure = null;
    dialog.classList.remove("is-departing");
    islands.forEach(island => island.classList.remove("is-sailing"));
  }

  function settle() {
    stopBoat();
    animations.forEach(animation => animation.cancel());
    animations.clear();
  }

  function reset() {
    cancelDeparture();
    settle();
    select(null);
    course.removeAttribute("d");
    const preferred = { x: map.clientWidth * .55, y: map.clientHeight * .51 };
    const berth = dialog.open ? waterMap().safePoint(preferred) || preferred : preferred;
    vessel.style.transform = transform(berth.x, berth.y, -24);
  }

  function prepareImages() {
    dialog.querySelectorAll(".island-land img").forEach(image => { image.loading = "eager"; });
  }
  opener.addEventListener("pointerenter", prepareImages, { once: true });
  opener.addEventListener("focus", prepareImages, { once: true });
  opener.addEventListener("click", () => {
    if (dialog.open) return;
    prepareImages();
    dialog.showModal();
    opener.setAttribute("aria-expanded", "true");
    dialog.scrollTop = 0;
    reset();
    if (quiet()) return;
    play(dialog.querySelector(".sea-water"), [{ opacity: .35 }, { opacity: 1 }], { duration: 320 });
    islands.forEach((island, i) => {
      play(island.querySelector(".island-arrival"), [
        { opacity: 0, transform: "translateY(18px)" },
        { opacity: 1, transform: "translateY(0)" },
      ], { duration: 420, delay: i * 35, easing: "cubic-bezier(.16,1,.3,1)", fill: "backwards" });
    });
  });

  islands.forEach(island => {
    island.addEventListener("pointerenter", event => {
      if (event.pointerType !== "touch") select(island);
    });
    island.addEventListener("pointerdown", () => select(island));
    island.addEventListener("focus", () => select(island));
    island.addEventListener("pointerleave", () => {
      if (activeIsland === island && !island.matches(":focus-visible")) select(null);
    });
    island.addEventListener("blur", () => {
      if (activeIsland === island) select(null);
    });
    island.addEventListener("click", event => {
      // A new click replaces any pending departure, including modified clicks.
      cancelDeparture();
      // Preserve native links, modified clicks, new tabs and reduced-motion navigation.
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || island.hasAttribute("download") || (island.target && island.target !== "_self") || quiet()) return;
      event.preventDefault();
      select(island);
      island.classList.add("is-sailing");
      dialog.classList.add("is-departing");
      play(island.querySelector(".island-tide"), [
        { transform: "scale(1.16, 1.04) translateY(5%)", opacity: .6 },
        { transform: "scale(1.45, 1.25) translateY(5%)", opacity: 0 },
      ], { duration: 240, easing: "ease-out" });
      // A brief response, never a loading gate. Escape and Close can cancel it.
      departure = setTimeout(() => {
        departure = null;
        location.assign(island.href);
      }, 240);
    });
  });

  dialog.querySelector("[data-index-close]").addEventListener("click", () => dialog.close());
  dialog.addEventListener("keydown", event => {
    if (event.key !== "Tab" || event.altKey || event.ctrlKey || event.metaKey) return;
    const controls = [...dialog.querySelectorAll("a[href], button:not(:disabled)")];
    const first = controls[0];
    const last = controls.at(-1);
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
  dialog.addEventListener("cancel", cancelDeparture);
  dialog.addEventListener("close", () => {
    reset();
    opener.setAttribute("aria-expanded", "false");
    opener.focus({ preventScroll: true });
  });
  addEventListener("pagehide", () => {
    cancelDeparture();
    if (dialog.open) dialog.close();
  });
  addEventListener("pageshow", () => {
    if (dialog.open) dialog.close();
    opener.setAttribute("aria-expanded", "false");
  });
  addEventListener("resize", () => { if (dialog.open) reset(); }, { passive: true });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden && dialog.open) { cancelDeparture(); settle(); }
  });
  const respectMotion = () => {
    if (dialog.open && quiet()) { cancelDeparture(); settle(); }
  };
  new MutationObserver(respectMotion).observe(root, { attributes: true, attributeFilter: ["data-motion"] });
  reducedMotion.addEventListener("change", respectMotion);
})();
