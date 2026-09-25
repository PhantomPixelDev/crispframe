/* Crispframe — main.js | adaptive nav, skip-link, year, sticky | vanilla defer-safe */
(function () {
    'use strict';

    document.documentElement.classList.add('has-js');

    function ready(callback) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', callback);
        } else {
            callback();
        }
    }

    ready(function () {
        var reducedMotion = false;
        try {
            reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
        } catch (error) {
            reducedMotion = false;
        }

        var header = document.getElementById('site-header');
        var toggle = document.getElementById('nav-toggle');
        var mobileMenu = document.getElementById('mobile-menu');
        var closeMenu = null;

        document.querySelectorAll('[data-announcement]').forEach(function (announcement) {
            var keySource = announcement.getAttribute('data-announcement-key') || '';
            var hash = 0;
            for (var index = 0; index < keySource.length; index += 1) {
                hash = ((hash << 5) - hash) + keySource.charCodeAt(index);
                hash |= 0;
            }
            var storageKey = 'crispframe-announcement-' + String(hash);
            try {
                if (localStorage.getItem(storageKey) === 'dismissed') {
                    announcement.hidden = true;
                }
            } catch (error) {
                // Storage can be unavailable in strict privacy modes; the notice stays usable.
            }
            var dismiss = announcement.querySelector('[data-announcement-dismiss]');
            if (dismiss) {
                dismiss.addEventListener('click', function () {
                    announcement.hidden = true;
                    try {
                        localStorage.setItem(storageKey, 'dismissed');
                    } catch (error) {
                        // Dismissing for the current page still works without storage.
                    }
                });
            }
        });

        var submenuToggles = Array.prototype.slice.call(document.querySelectorAll('.nav__submenu-toggle'));
        function setSubmenu(toggleButton, open, restoreFocus) {
            var item = toggleButton.closest('.has-children');
            if (!item) {
                return;
            }
            item.classList.toggle('is-open', open);
            toggleButton.setAttribute('aria-expanded', String(open));
            if (!open && restoreFocus) {
                toggleButton.focus();
            }
        }
        function closeSiblingSubmenus(toggleButton) {
            var navigation = toggleButton.closest('.site-nav');
            submenuToggles.forEach(function (candidate) {
                if (candidate !== toggleButton && candidate.closest('.site-nav') === navigation) {
                    setSubmenu(candidate, false, false);
                }
            });
        }
        submenuToggles.forEach(function (submenuToggle) {
            submenuToggle.addEventListener('click', function () {
                var willOpen = submenuToggle.getAttribute('aria-expanded') !== 'true';
                closeSiblingSubmenus(submenuToggle);
                setSubmenu(submenuToggle, willOpen, false);
            });
        });
        document.addEventListener('keydown', function (event) {
            if (event.key !== 'Escape') {
                return;
            }
            var openToggle = document.querySelector('.nav__submenu-toggle[aria-expanded="true"]');
            if (openToggle) {
                setSubmenu(openToggle, false, true);
            }
        });
        document.addEventListener('click', function (event) {
            submenuToggles.forEach(function (submenuToggle) {
                var item = submenuToggle.closest('.has-children');
                if (item && !item.contains(event.target)) {
                    setSubmenu(submenuToggle, false, false);
                }
            });
        });

        if (toggle && mobileMenu) {
            var openIcon = toggle.querySelector('.nav-toggle__icon--open');
            var closeIcon = toggle.querySelector('.nav-toggle__icon--close');
            var previousFocus = null;

            function isOpen() {
                return toggle.getAttribute('aria-expanded') === 'true';
            }

            function setOpen(open) {
                toggle.setAttribute('aria-expanded', String(open));
                mobileMenu.hidden = !open;
                mobileMenu.classList.toggle('is-open', open);
                if (header) {
                    header.classList.toggle('is-open', open);
                }
                if (openIcon) {
                    openIcon.hidden = open;
                }
                if (closeIcon) {
                    closeIcon.hidden = !open;
                }
                if (open) {
                    previousFocus = document.activeElement;
                    var firstItem = mobileMenu.querySelector('a,button');
                    if (firstItem) {
                        firstItem.focus();
                    }
                } else {
                    mobileMenu.hidden = true;
                    if (previousFocus && document.contains(previousFocus)) {
                        previousFocus.focus();
                    } else {
                        toggle.focus();
                    }
                }
            }

            closeMenu = function () {
                if (isOpen()) {
                    setOpen(false);
                }
            };

            toggle.addEventListener('click', function () {
                setOpen(!isOpen());
            });
            document.addEventListener('keydown', function (event) {
                if (event.key === 'Escape' && isOpen()) {
                    setOpen(false);
                }
            });
            mobileMenu.addEventListener('click', function (event) {
                if (event.target.closest && event.target.closest('a')) {
                    setOpen(false);
                }
            });
            document.addEventListener('click', function (event) {
                if (isOpen() && !mobileMenu.contains(event.target) && !toggle.contains(event.target)) {
                    setOpen(false);
                }
            });
        }

        if (header) {
            var headerInner = header.querySelector('.site-header__inner');
            var brand = header.querySelector('.site-header__brand');
            var navigation = header.querySelector('.site-header__nav');
            var actions = header.querySelector('.site-header__actions');
            var narrowHeader = matchMedia('(max-width: 69.99rem)');
            var resizeFrame = 0;

            function fitNavigation() {
                if (!headerInner || !brand || !navigation || !actions) {
                    return;
                }

                header.classList.remove('is-nav-condensed');
                var shouldCondense = narrowHeader.matches;

                if (!shouldCondense) {
                    var innerStyle = getComputedStyle(headerInner);
                    var gap = parseFloat(innerStyle.columnGap || innerStyle.gap) || 0;
                    var requiredWidth = brand.getBoundingClientRect().width
                        + navigation.scrollWidth
                        + actions.getBoundingClientRect().width
                        + (gap * 2)
                        + 8;
                    shouldCondense = requiredWidth > headerInner.clientWidth;
                }

                header.classList.toggle('is-nav-condensed', shouldCondense);
                if (!shouldCondense && closeMenu) {
                    closeMenu();
                }
            }

            function scheduleNavigationFit() {
                if (resizeFrame) {
                    cancelAnimationFrame(resizeFrame);
                }
                resizeFrame = requestAnimationFrame(function () {
                    resizeFrame = 0;
                    fitNavigation();
                });
            }

            addEventListener('resize', scheduleNavigationFit, {passive: true});
            header.querySelectorAll('img').forEach(function (image) {
                if (!image.complete) {
                    image.addEventListener('load', scheduleNavigationFit, {once: true});
                }
            });
            if (document.fonts && document.fonts.ready) {
                document.fonts.ready.then(scheduleNavigationFit);
            }
            fitNavigation();
        }

        document.querySelectorAll('a.skip-link').forEach(function (anchor) {
            anchor.addEventListener('click', function (event) {
                var selector = anchor.getAttribute('href');
                var target = selector && document.querySelector(selector);
                if (!target) {
                    return;
                }
                event.preventDefault();
                if (!target.hasAttribute('tabindex')) {
                    target.setAttribute('tabindex', '-1');
                }
                try {
                    target.scrollIntoView({behavior: reducedMotion ? 'auto' : 'smooth', block: 'start'});
                } catch (error) {
                    target.scrollIntoView();
                }
                target.focus({preventScroll: true});
            });
        });

        document.querySelectorAll('[data-section-navigation]').forEach(function (navigation) {
            var links = Array.prototype.slice.call(navigation.querySelectorAll('a[href^="#"]'));
            var targets = links.map(function (link) {
                return document.querySelector(link.getAttribute('href'));
            }).filter(Boolean);
            if (!('IntersectionObserver' in window) || targets.length === 0) {
                return;
            }
            var observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (!entry.isIntersecting) {
                        return;
                    }
                    links.forEach(function (link) {
                        var current = link.getAttribute('href') === '#' + entry.target.id;
                        link.classList.toggle('is-active', current);
                        if (current) {
                            link.setAttribute('aria-current', 'location');
                        } else {
                            link.removeAttribute('aria-current');
                        }
                    });
                });
            }, {rootMargin: '-20% 0px -65% 0px', threshold: 0});
            targets.forEach(function (target) {
                observer.observe(target);
            });
        });

        var year = String(new Date().getFullYear());
        document.querySelectorAll('[data-current-year]').forEach(function (element) {
            element.textContent = year;
        });

        if (header) {
            var scrollFrame = 0;
            function updateStickyState() {
                header.classList.toggle('is-sticky', (window.scrollY || document.documentElement.scrollTop) > 8);
                scrollFrame = 0;
            }
            addEventListener('scroll', function () {
                if (!scrollFrame) {
                    scrollFrame = requestAnimationFrame(updateStickyState);
                }
            }, {passive: true});
            updateStickyState();
        }
    });
}());
