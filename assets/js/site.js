(function () {
  var root = document.documentElement;
  var c = document.getElementById("contrast");
  var b = document.getElementById("menu-btn");
  var m = document.getElementById("menu");
  function sync() { c.setAttribute("aria-pressed", String(root.classList.contains("hc"))); }
  sync();
  c.addEventListener("click", function () {
    var on = root.classList.toggle("hc");
    sync();
    try { localStorage.setItem("contrast", on ? "high" : "normal"); } catch (e) {}
  });
  function menu(open) { b.setAttribute("aria-expanded", String(open)); m.classList.toggle("open", open); }
  b.addEventListener("click", function () { menu(b.getAttribute("aria-expanded") !== "true"); });
  m.addEventListener("click", function (e) { if (e.target.closest("a")) menu(false); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && m.classList.contains("open")) { menu(false); b.focus(); }
  });
  // PT | EN: leva à seção que está na tela, mesmo que o endereço não tenha âncora.
  function current() {
    var id = "";
    document.querySelectorAll("main > section[id]").forEach(function (s) {
      if (s.getBoundingClientRect().top <= window.innerHeight * 0.35) id = s.id;
    });
    if (window.scrollY > 0 && window.innerHeight + window.scrollY >= root.scrollHeight - 2) {
      var h = location.hash.slice(1), t = h && document.getElementById(h);
      if (t && t.matches("main > section") && t.getBoundingClientRect().top < window.innerHeight) id = h;
    }
    return id === "inicio" ? "" : id;
  }
  // Marca no menu a seção que está na tela.
  var items = m.querySelectorAll("a");
  function mark() {
    var id = current() || "inicio";
    items.forEach(function (a) {
      if (a.getAttribute("href") === "#" + id) a.setAttribute("aria-current", "true");
      else a.removeAttribute("aria-current");
    });
  }
  var wait = false;
  window.addEventListener("scroll", function () {
    if (wait) return;
    wait = true;
    requestAnimationFrame(function () { wait = false; mark(); });
  }, { passive: true });
  mark();
  document.querySelectorAll("[data-lang-link]").forEach(function (a) {
    var base = a.getAttribute("href");
    function set() { var id = current(); a.href = base + (id ? "#" + id : ""); }
    ["click", "focus", "pointerdown", "auxclick"].forEach(function (ev) { a.addEventListener(ev, set); });
  });
  // Eventos: o que já passou vai para o histórico, mesmo sem nova publicação do site.
  var prox = document.getElementById("ev-prox"), hist = document.getElementById("ev-hist");
  if (prox && hist) {
    var d = new Date();
    var hoje = d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2);
    prox.querySelectorAll("li").forEach(function (li) {
      if (li.getAttribute("data-fim") < hoje) hist.querySelector("ol").prepend(li);
    });
    hist.hidden = !hist.querySelector("li");
    if (!prox.querySelector("li")) { prox.hidden = true; hist.open = true; }
  }
  // Vídeo em destaque: só carrega o YouTube depois do clique.
  document.querySelectorAll("[data-video]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault();
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + a.getAttribute("data-video") + (a.getAttribute("data-video").indexOf("?") > -1 ? "&" : "?") + "autoplay=1";
      f.title = a.getAttribute("data-title") || a.querySelector(".video-t").textContent;
      f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
      f.className = "video";
      f.referrerPolicy = "strict-origin-when-cross-origin";
      a.replaceWith(f);
      f.focus();
    });
  });
})();
