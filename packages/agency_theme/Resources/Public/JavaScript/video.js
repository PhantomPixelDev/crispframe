/* The embed URL is created only after an explicit click. */
(function () {
  'use strict';
  function init() {
    document.querySelectorAll('.video-facade').forEach(function (facade) {
      var button = facade.querySelector('.video-facade__button');
      var provider = facade.dataset.videoProvider;
      var id = facade.dataset.videoId || '';
      var valid = provider === 'youtube' ? /^[A-Za-z0-9_-]{11}$/.test(id) : provider === 'vimeo' && /^\d{6,12}$/.test(id);
      if (!button || !valid) {
        if (button) { button.disabled = true; button.setAttribute('aria-label', 'Video unavailable'); }
        return;
      }
      button.addEventListener('click', function () {
        var frame = document.createElement('iframe');
        frame.src = provider === 'youtube'
          ? 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0'
          : 'https://player.vimeo.com/video/' + id + '?autoplay=1&dnt=1';
        frame.title = facade.dataset.videoTitle || 'Video';
        frame.loading = 'eager';
        frame.referrerPolicy = 'strict-origin-when-cross-origin';
        frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
        frame.allowFullscreen = true;
        facade.replaceChildren(frame);
        frame.focus();
      }, { once: true });
    });
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
