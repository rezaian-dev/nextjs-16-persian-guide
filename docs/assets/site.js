(() => {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".menu-toggle");
  const drawer = document.querySelector("#mobile-menu");
  const scrim = document.querySelector("#m-scrim");
  const closeBtn = document.querySelector("#m-x");
  if (!header) return;

  let lastFocus = null;

  const closeMenu = () => {
    if (!drawer || drawer.hidden) return;
    header.classList.remove("is-open");
    drawer.hidden = true;
    if (scrim) scrim.hidden = true;
    document.body.style.overflow = "";
    if (toggle) {
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "بازکردن منو");
    }
    lastFocus?.focus?.();
  };

  const openMenu = () => {
    if (!drawer) return;
    lastFocus = document.activeElement;
    header.classList.add("is-open");
    drawer.hidden = false;
    if (scrim) scrim.hidden = false;
    document.body.style.overflow = "hidden";
    toggle.setAttribute("aria-expanded", "true");
    toggle.setAttribute("aria-label", "بستن منو");
    drawer.querySelector(".m-row")?.focus?.();
  };

  if (toggle && drawer) {
    toggle.addEventListener("click", () => (drawer.hidden ? openMenu() : closeMenu()));
    closeBtn?.addEventListener("click", closeMenu);
    scrim?.addEventListener("click", closeMenu);
    drawer.addEventListener("click", (e) => {
      if (e.target.closest("a")) closeMenu();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeMenu();
    });
    // a resize into the desktop layout must not leave the body locked
    matchMedia("(min-width: 768px)").addEventListener("change", (e) => {
      if (e.matches) closeMenu();
    });
  }

  const updateHeader = () => header.classList.toggle("is-scrolled", window.scrollY > 10);
  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });

  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const nodes = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    nodes.forEach((el) => el.classList.add("is-visible"));
    return;
  }
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
  );
  nodes.forEach((el) => io.observe(el));
})();
