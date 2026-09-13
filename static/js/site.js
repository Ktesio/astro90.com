/* Presentation only: navigation, motion preferences, and screenshot viewing. */
(() => {
  const root = document.documentElement;
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const motionButton = document.querySelector("[data-motion-toggle]");
  let manuallyPaused = false;
  try {
    manuallyPaused = sessionStorage.getItem("astro90-motion") === "paused";
  } catch {}

  const updateMotion = () => {
    const paused = reducedMotion.matches || manuallyPaused;
    root.dataset.motion = paused ? "paused" : "running";
    motionButton?.setAttribute("aria-pressed", String(paused));
    motionButton?.setAttribute(
      "aria-label",
      reducedMotion.matches
        ? "Reduced motion enabled by your device"
        : paused
          ? "Resume ambient motion"
          : "Pause ambient motion",
    );
    if (motionButton) {
      motionButton.disabled = reducedMotion.matches;
      const path = motionButton.querySelector("path");
      path?.setAttribute("d", paused ? "m9 5 11 7-11 7V5Z" : "M8 5v14M16 5v14");
    }
  };
  motionButton?.addEventListener("click", () => {
    manuallyPaused = !manuallyPaused;
    try {
      sessionStorage.setItem(
        "astro90-motion",
        manuallyPaused ? "paused" : "running",
      );
    } catch {}
    updateMotion();
  });
  reducedMotion.addEventListener("change", updateMotion);
  updateMotion();

  const revealElements = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reducedMotion.matches) {
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      },
      { threshold: 0.07, rootMargin: "0px 0px 35px 0px" },
    );
    revealElements.forEach((element) => observer.observe(element));
    root.classList.add("enhanced");
  }

  const menuButton = document.querySelector("[data-menu-toggle]");
  const menu = document.querySelector("#mobile-nav");
  const setMenu = (open, returnFocus = false) => {
    if (!menu || !menuButton) return;
    menu.hidden = !open;
    menuButton.setAttribute("aria-expanded", String(open));
    menuButton.setAttribute(
      "aria-label",
      open ? "Close navigation" : "Open navigation",
    );
    menuButton
      .querySelector("path")
      ?.setAttribute("d", open ? "m6 6 12 12M6 18 18 6" : "M4 8h16M4 16h16");
    if (returnFocus) menuButton.focus();
  };
  menuButton?.addEventListener("click", () => setMenu(menu.hidden));
  menu
    ?.querySelectorAll("a")
    .forEach((link) => link.addEventListener("click", () => setMenu(false)));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menu && !menu.hidden) setMenu(false, true);
  });
  document.addEventListener("click", (event) => {
    if (menu && !menu.hidden && !event.target.closest(".site-header"))
      setMenu(false);
  });
  window
    .matchMedia("(min-width: 651px)")
    .addEventListener("change", (event) => {
      if (event.matches) setMenu(false);
    });

  let scrollScheduled = false;
  const updateProgress = () => {
    const range = root.scrollHeight - window.innerHeight;
    root.style.setProperty(
      "--page-progress",
      range > 0 ? Math.min(1, Math.max(0, window.scrollY / range)) : 0,
    );
    scrollScheduled = false;
  };
  const scheduleProgress = () => {
    if (!scrollScheduled) {
      scrollScheduled = true;
      requestAnimationFrame(updateProgress);
    }
  };
  window.addEventListener("scroll", scheduleProgress, { passive: true });
  window.addEventListener("resize", scheduleProgress, { passive: true });
  updateProgress();

  const gallery = document.querySelector(".gallery-dialog");
  if (gallery && typeof gallery.showModal === "function") {
    const largeImage = gallery.querySelector(".gallery-large");
    const title = gallery.querySelector("#gallery-title");
    let opener;
    document.querySelectorAll("[data-gallery-src]").forEach((button) => {
      button.addEventListener("click", () => {
        opener = button;
        largeImage.src = button.dataset.gallerySrc;
        largeImage.alt = button.querySelector("img").alt;
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
