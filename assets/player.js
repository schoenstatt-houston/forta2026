// Inicia el video en cuanto abre la página.
// Los navegadores solo permiten autoplay con sonido en algunos casos;
// si lo bloquean, arranca en silencio y muestra un botón para activar el sonido.
(function () {
  var video = document.getElementById("video");
  var button = document.getElementById("unmute");
  if (!video || !button) return;

  function showButton() { button.hidden = false; }
  function hideButton() { button.hidden = true; }

  function startMuted() {
    video.muted = true;
    var p = video.play();
    if (p && p.catch) p.catch(function () {});
    showButton();
  }

  // Primero intenta con sonido.
  video.muted = false;
  var attempt = video.play();
  if (attempt && attempt.then) {
    attempt.then(hideButton).catch(startMuted);
  } else if (video.paused) {
    startMuted();
  }

  // Al tocar el botón: desde el inicio y con sonido.
  button.addEventListener("click", function () {
    video.currentTime = 0;
    video.muted = false;
    video.play();
    hideButton();
  });

  // Lleva la pantalla al video para que no tengan que desplazarse.
  // Siempre deja el video arriba, con una franja de la foto y el nombre
  // de la pareja visibles, sin importar si el video es cuadrado u horizontal.
  var userScrolled = false;
  window.addEventListener("touchstart", function () { userScrolled = true; }, { once: true, passive: true });
  window.addEventListener("wheel", function () { userScrolled = true; }, { once: true, passive: true });
  function focusVideo() {
    if (userScrolled) return;
    var vh = window.innerHeight;
    var rect = video.getBoundingClientRect();
    // Deja el video centrado si cabe; si es corto (horizontal), lo sube igual
    // que en los demás, dejando ~22% de la pantalla para el encabezado.
    var topGap = Math.min(Math.max((vh - rect.height) / 2, 0), vh * 0.22);
    var target = window.scrollY + rect.top - topGap;
    if (target <= 0) return;
    // Si la página no es lo bastante alta para desplazarse, agrega espacio abajo.
    var doc = document.documentElement;
    var missing = target + vh - doc.scrollHeight;
    if (missing > 0) document.body.style.paddingBottom = Math.ceil(missing) + "px";
    window.scrollTo({ top: target, behavior: "smooth" });
  }
  if (video.readyState >= 1) setTimeout(focusVideo, 700);
  else video.addEventListener("loadedmetadata", function () { setTimeout(focusVideo, 700); }, { once: true });

  // Si activan el sonido desde los controles del reproductor, oculta el botón.
  video.addEventListener("volumechange", function () {
    if (!video.muted) hideButton();
  });
})();
