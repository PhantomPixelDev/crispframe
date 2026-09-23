(function () {
  'use strict';
  function init() {
    document.querySelectorAll('[data-pricing]').forEach(function (section) {
      var toggle = section.querySelector('[data-pricing-toggle]');
      if (!toggle || !section.querySelector('[data-price-year]')) return;
      toggle.hidden = false;
      toggle.addEventListener('click', function (event) {
        var button = event.target.closest('[data-pricing-period]');
        if (!button || !toggle.contains(button)) return;
        var year = button.dataset.pricingPeriod === 'year';
        toggle.querySelectorAll('[data-pricing-period]').forEach(function (choice) {
          choice.setAttribute('aria-pressed', String(choice === button));
        });
        section.querySelectorAll('[data-price-month], [data-suffix-month]').forEach(function (value) { value.hidden = year; });
        section.querySelectorAll('[data-price-year], [data-suffix-year]').forEach(function (value) { value.hidden = !year; });
      });
    });
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
