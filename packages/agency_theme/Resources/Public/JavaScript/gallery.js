(function () {
  'use strict';
  function init() {
  document.querySelectorAll('[data-gallery]').forEach(function (gallery) {
    var links = Array.from(gallery.querySelectorAll('[data-gallery-open]'));
    var dialog = gallery.querySelector('.gallery-lightbox');
    if (!dialog || !dialog.showModal || !links.length) return;
    var image = dialog.querySelector('[data-gallery-image]');
    var caption = dialog.querySelector('[data-gallery-caption]');
    var counter = dialog.querySelector('[data-gallery-counter]');
    var active = 0;
    var opener = null;
    function show(index) {
      active = (index + links.length) % links.length;
      var link = links[active];
      image.src = link.href;
      image.alt = link.dataset.galleryAlt || '';
      caption.textContent = link.dataset.galleryCaption || '';
      counter.textContent = (active + 1) + ' / ' + links.length;
    }
    gallery.addEventListener('click', function (event) {
      var link = event.target.closest('[data-gallery-open]');
      if (link && gallery.contains(link)) {
        event.preventDefault();
        opener = link;
        show(links.indexOf(link));
        dialog.showModal();
        dialog.querySelector('[data-gallery-close]').focus();
      }
    });
    dialog.querySelector('[data-gallery-close]').addEventListener('click', function () { dialog.close(); });
    dialog.querySelector('[data-gallery-prev]').addEventListener('click', function () { show(active - 1); });
    dialog.querySelector('[data-gallery-next]').addEventListener('click', function () { show(active + 1); });
    dialog.addEventListener('keydown', function (event) {
      if (event.key === 'ArrowLeft') { event.preventDefault(); show(active - 1); }
      if (event.key === 'ArrowRight') { event.preventDefault(); show(active + 1); }
    });
    dialog.addEventListener('close', function () { image.removeAttribute('src'); if (opener) opener.focus(); });
  });
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
