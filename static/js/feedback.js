/* Presentation feedback: real image requests, a native gallery, and email copy. */
(() => {
  function mediaController(host) {
    const image = host.querySelector("[data-media-image]");
    const status = host.querySelector("[data-media-status]");
    const label = host.querySelector("[data-media-label]");
    const retry = host.querySelector("[data-media-retry]");
    let version = 0;
    let timer;
    let active = true;

    function state(value, message = "") {
      clearTimeout(timer);
      host.dataset.mediaState = value;
      image.setAttribute("aria-busy", String(value === "pending"));
      status.hidden = value === "ready" || value === "idle";
      label.textContent = message;
      if (retry) retry.hidden = value !== "error";
      // A retry control must not disappear while still holding keyboard focus.
      if (retry === document.activeElement && value === "ready") {
        const target = host.querySelector("[data-gallery-src]") || host;
        if (target === host) host.tabIndex = -1;
        target.focus({ preventScroll: true });
      }
    }
    function armTimeout() {
      clearTimeout(timer);
      if (host.dataset.mediaState !== "pending") return;
      const request = version;
      timer = setTimeout(() => {
        if (active && request === version) state("error", "This preview is taking longer than expected.");
      }, 20000);
    }
    function ready() {
      if (!active || !image.complete || !image.naturalWidth) return;
      // WebKit can defer decode() indefinitely for hidden lazy images. The load
      // event and current-image dimensions let native painting proceed normally.
      state("ready");
    }
    function check() {
      if (!image.getAttribute("src")) return;
      if (image.complete) {
        if (image.naturalWidth) ready();
        else state("error", "Preview unavailable.");
      }
    }
    image.addEventListener("load", ready);
    image.addEventListener("error", () => {
      if (active && image.getAttribute("src")) state("error", "Preview unavailable.");
    });

    const controller = {
      load(src, alt, width, height) {
        active = true;
        version += 1;
        state("pending", "Loading preview…");
        image.alt = alt;
        image.width = width;
        image.height = height;
        image.src = src;
        armTimeout();
        check();
      },
      stop() {
        active = false;
        version += 1;
        state("idle");
        image.removeAttribute("src");
      },
    };
    retry?.addEventListener("click", () => {
      const source = image.currentSrc || image.src;
      const url = new URL(source, document.baseURI);
      // Only an explicit retry bypasses a cached failed response.
      url.searchParams.set("preview-retry", Date.now().toString());
      image.removeAttribute("srcset");
      controller.load(url.href, image.alt, image.width, image.height);
      // Keep focus within the image area while the retry control is hidden.
      const target = host.querySelector("[data-gallery-src]") || host;
      if (target === host) host.tabIndex = -1;
      target.focus({ preventScroll: true });
    });
    if (image.getAttribute("src")) {
      state("pending", "Loading preview…");
      check();
      // Lazy images outside the viewport are not slow or failed requests.
      if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => {
          if (entries.some((entry) => entry.isIntersecting)) {
            armTimeout();
            observer.disconnect();
          }
        }, { rootMargin: "300px" });
        observer.observe(host);
      } else armTimeout();
    }
    return controller;
  }

  document.querySelectorAll("[data-media]").forEach(mediaController);

  const gallery = document.querySelector(".gallery-dialog");
  const shots = [...document.querySelectorAll("[data-gallery-src]")];
  if (gallery && shots.length && typeof gallery.showModal === "function") {
    const media = mediaController(gallery.querySelector("[data-gallery-media]"));
    const title = gallery.querySelector("#gallery-title");
    const original = gallery.querySelector("[data-gallery-original]");
    const count = gallery.querySelector("[data-gallery-count]");
    const previous = gallery.querySelector("[data-gallery-prev]");
    const next = gallery.querySelector("[data-gallery-next]");
    let selected = 0;
    let opener;
    function show(index) {
      selected = (index + shots.length) % shots.length;
      const shot = shots[selected];
      const thumbnail = shot.querySelector("img");
      title.textContent = shot.dataset.galleryTitle;
      original.href = shot.href;
      original.hidden = false;
      count.textContent = `${selected + 1} / ${shots.length}`;
      previous.disabled = next.disabled = shots.length < 2;
      media.load(shot.dataset.gallerySrc, thumbnail.alt, Number(thumbnail.getAttribute("width")), Number(thumbnail.getAttribute("height")));
      gallery.scrollTop = 0;
    }
    shots.forEach((shot, index) => {
      shot.addEventListener("click", (event) => {
        // Preserve normal image links, including modified clicks and no-JS use.
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        opener = shot;
        show(index);
        gallery.showModal();
      });
    });
    previous.addEventListener("click", () => show(selected - 1));
    next.addEventListener("click", () => show(selected + 1));
    gallery.querySelector("[data-gallery-close]").addEventListener("click", () => gallery.close());
    gallery.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
        event.preventDefault();
        show(selected + (event.key === "ArrowRight" ? 1 : -1));
      }
    });
    gallery.addEventListener("click", (event) => {
      if (event.target !== gallery) return;
      const bounds = gallery.getBoundingClientRect();
      if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) gallery.close();
    });
    gallery.addEventListener("close", () => {
      media.stop();
      opener?.focus({ preventScroll: true });
    });
  }

  document.querySelectorAll("[data-copy-email]").forEach((button) => {
    const status = button.parentElement.querySelector("[data-copy-status]");
    const label = button.querySelector("span");
    button.hidden = false;
    button.addEventListener("click", async () => {
      if (button.getAttribute("aria-disabled") === "true") return;
      button.setAttribute("aria-disabled", "true");
      label.textContent = "Copying…";
      status.textContent = "";
      try {
        await navigator.clipboard.writeText(button.dataset.copyEmail);
        label.textContent = "Copied";
        status.textContent = "Email address copied.";
      } catch {
        label.textContent = "Copy email address";
        status.textContent = "Couldn’t copy. Select the address above, or open the email link.";
      } finally {
        button.removeAttribute("aria-disabled");
      }
    });
  });
})();
