/* ============================================================
   Majed Namous — site behaviour.
   No libraries. Everything runs off one rAF loop and writes
   CSS custom properties; the CSS does the rendering.
   ============================================================ */
(function () {
  "use strict";

  var root = document.documentElement;
  root.classList.remove("no-js");

  var reduce =
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- current year ---------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-year]"), function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  /* ---------- visual-asset protection ----------
     Front-end deterrence only. It stops casual right-click / drag /
     "open image in new tab" from the page itself. It does NOT prevent
     anyone from pulling the files out of the network tab or DevTools —
     the images are still ordinary HTTP resources. -------------------- */
  (function protectAssets() {
    var MEDIA = { IMG: 1, PICTURE: 1, SVG: 1, VIDEO: 1, CANVAS: 1 };

    var mark = function (root) {
      var imgs = (root || document).querySelectorAll ?
        (root || document).querySelectorAll("img") : [];
      Array.prototype.forEach.call(imgs, function (img) {
        img.setAttribute("draggable", "false");
      });
    };
    mark(document);

    /* cover anything rendered later */
    if ("MutationObserver" in window) {
      new MutationObserver(function (records) {
        records.forEach(function (r) {
          Array.prototype.forEach.call(r.addedNodes, function (n) {
            if (n.nodeType !== 1) return;
            if (n.tagName === "IMG") n.setAttribute("draggable", "false");
            else mark(n);
          });
        });
      }).observe(document.documentElement, { childList: true, subtree: true });
    }

    /* images are pointer-events:none, so the event target is their
       wrapper — test what is actually under the cursor instead. */
    var overMedia = function (e) {
      if (e.target && MEDIA[e.target.tagName]) return true;
      if (typeof document.elementsFromPoint !== "function") return false;
      var stack = document.elementsFromPoint(e.clientX, e.clientY) || [];
      for (var i = 0; i < stack.length; i++) {
        if (MEDIA[stack[i].tagName]) return true;
      }
      return false;
    };

    document.addEventListener("contextmenu", function (e) {
      if (overMedia(e)) e.preventDefault();
    });

    document.addEventListener("dragstart", function (e) {
      var t = e.target;
      if (t && (MEDIA[t.tagName] || (t.closest && t.closest("picture, figure, svg")))) {
        e.preventDefault();
      }
    });
  })();

  /* ---------- navigation ---------- */
  var nav = document.querySelector("[data-nav]");
  var toggle = document.querySelector("[data-nav-toggle]");
  var menu = document.querySelector("[data-nav-menu]");

  if (nav && toggle && menu) {
    var setOpen = function (open) {
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      menu.setAttribute("aria-hidden", open ? "false" : "true");
    };
    toggle.addEventListener("click", function () {
      setOpen(!nav.classList.contains("is-open"));
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        setOpen(false);
        toggle.focus();
      }
    });
    document.addEventListener("click", function (e) {
      if (nav.classList.contains("is-open") && !e.target.closest("[data-nav]")) {
        setOpen(false);
      }
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth >= 900) setOpen(false);
    });
    setOpen(false);
  }

  /* ---------- reveal on scroll ---------- */
  var items = document.querySelectorAll(".reveal, .img-reveal, .tile");

  if (items.length) {
    if (reduce || !("IntersectionObserver" in window)) {
      Array.prototype.forEach.call(items, function (el) { el.classList.add("is-in"); });
    } else {
      var io = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-in");
              io.unobserve(entry.target);
            }
          });
        },
        { rootMargin: "0px 0px -6% 0px", threshold: 0.05 }
      );
      Array.prototype.forEach.call(items, function (el) { io.observe(el); });
    }
  }

  /* ---------- contact form ----------
     The success state is only ever shown for a real 2xx response from a
     configured endpoint. With no endpoint set the form says so plainly
     rather than pretending the message was sent. -------------------- */
  var form = document.querySelector("[data-form]");
  if (form) {
    var statusEl = form.querySelector("[data-form-status]");
    var button = form.querySelector("button[type=submit]");
    var endpoint = (form.getAttribute("data-endpoint") || "").trim();

    var say = function (text, state) {
      if (!statusEl) return;
      statusEl.textContent = text;
      if (state) statusEl.setAttribute("data-state", state);
      else statusEl.removeAttribute("data-state");
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      if (!endpoint) {
        say(form.getAttribute("data-msg-unconfigured") || "", "info");
        return;
      }

      if (button) { button.disabled = true; }
      say(form.getAttribute("data-msg-sending") || "", "info");

      fetch(endpoint, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(form)
      })
        .then(function (res) {
          if (!res.ok) throw new Error(String(res.status));
          form.reset();
          say(form.getAttribute("data-msg-ok") || "", "ok");
        })
        .catch(function () {
          say(form.getAttribute("data-msg-fail") || "", "info");
        })
        .then(function () {
          if (button) button.disabled = false;
        });
    });
  }

  if (reduce) return;

  /* ---------- one animation loop -----------------------------
     writes --sv (scroll velocity), --prog (page progress)
     and --px / --py (pointer position) on <html>.
     ---------------------------------------------------------- */
  var lastY = window.pageYOffset;
  var vel = 0;
  var progress = 0;
  var pxTarget = 0, pyTarget = 0, px = 0, py = 0;
  var hasPointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var hero = document.querySelector("[data-hero]");
  var running = true;

  if (hasPointer && hero) {
    window.addEventListener(
      "pointermove",
      function (e) {
        pxTarget = (e.clientX / window.innerWidth) * 2 - 1;
        pyTarget = (e.clientY / window.innerHeight) * 2 - 1;
      },
      { passive: true }
    );
  }

  document.addEventListener("visibilitychange", function () {
    running = !document.hidden;
    if (running) {
      lastY = window.pageYOffset;
      requestAnimationFrame(frame);
    }
  });

  var clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };

  function frame() {
    if (!running) return;

    var y = window.pageYOffset;
    var delta = y - lastY;
    lastY = y;

    /* eased, decaying scroll velocity — drives the tile rotation */
    vel += (delta - vel) * 0.16;
    vel *= 0.9;
    if (Math.abs(vel) < 0.02) vel = 0;
    root.style.setProperty("--sv", clamp(vel, -34, 34).toFixed(2));

    /* page progress for the navbar hairline */
    var max = document.documentElement.scrollHeight - window.innerHeight;
    var p = max > 0 ? clamp(y / max, 0, 1) : 0;
    if (Math.abs(p - progress) > 0.001) {
      progress = p;
      root.style.setProperty("--prog", progress.toFixed(4));
    }

    /* pointer parallax for the hero field */
    if (hasPointer && hero) {
      px += (pxTarget - px) * 0.05;
      py += (pyTarget - py) * 0.05;
      root.style.setProperty("--px", px.toFixed(3));
      root.style.setProperty("--py", py.toFixed(3));
    }

    requestAnimationFrame(frame);
  }

  requestAnimationFrame(frame);
})();
