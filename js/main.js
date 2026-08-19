(function () {
  const header = document.getElementById("site-header");
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".site-nav");
  const typed = document.getElementById("typed-text");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  requestAnimationFrame(function () {
    if (header) header.classList.add("is-in");
  });

  window.addEventListener("scroll", function () {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 12);
  }, { passive: true });

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      const open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open menu");
      });
    });
  }

  const phrases = [
    "Computer Engineering & Marketing",
    "Technology and Management at HKUST",
    "Internships across AI, software, and marketing",
  ];

  if (typed) {
    if (reduceMotion) {
      typed.textContent = phrases[0];
    } else {
      let phraseIndex = 0;
      let charIndex = 0;
      let deleting = false;

      function tick() {
        const current = phrases[phraseIndex];
        typed.textContent = current.slice(0, charIndex);

        if (!deleting && charIndex < current.length) {
          charIndex += 1;
          window.setTimeout(tick, 48);
          return;
        }
        if (!deleting && charIndex === current.length) {
          deleting = true;
          window.setTimeout(tick, 1600);
          return;
        }
        if (deleting && charIndex > 0) {
          charIndex -= 1;
          window.setTimeout(tick, 28);
          return;
        }
        deleting = false;
        phraseIndex = (phraseIndex + 1) % phrases.length;
        window.setTimeout(tick, 280);
      }

      tick();
    }
  }

  const reveals = document.querySelectorAll(".reveal");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) {
      el.classList.add("is-visible");
    });
  } else {
    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.14, rootMargin: "0px 0px -8% 0px" }
    );
    reveals.forEach(function (el) {
      observer.observe(el);
    });
  }

  const sections = ["about", "education", "experience", "awards", "skills", "hobbies", "resume", "contact"]
    .map(function (id) {
      return document.getElementById(id);
    })
    .filter(Boolean);

  function setActiveNav() {
    if (!nav) return;
    let current = sections[0];
    sections.forEach(function (section) {
      if (section.getBoundingClientRect().top <= 120) current = section;
    });
    nav.querySelectorAll("a").forEach(function (link) {
      const href = link.getAttribute("href") || "";
      link.classList.toggle("is-active", current && href === "#" + current.id);
    });
  }

  window.addEventListener("scroll", setActiveNav, { passive: true });
  setActiveNav();

  const form = document.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const name = document.getElementById("name").value.trim();
      const email = document.getElementById("email").value.trim();
      const subject = document.getElementById("subject").value.trim();
      const message = document.getElementById("message").value.trim();
      const body = [message, "", "-", name + (email ? " (" + email + ")" : "")].join("\n");
      window.location.href =
        "mailto:waimingjanicetai@gmail.com?subject=" +
        encodeURIComponent(subject || "Website enquiry") +
        "&body=" +
        encodeURIComponent(body);
    });
  }

  document.querySelectorAll("[data-print]").forEach(function (button) {
    button.addEventListener("click", function () {
      window.print();
    });
  });
})();
