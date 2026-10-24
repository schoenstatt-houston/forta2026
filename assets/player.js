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

  // Si activan el sonido desde los controles del reproductor, oculta el botón.
  video.addEventListener("volumechange", function () {
    if (!video.muted) hideButton();
  });
})();
