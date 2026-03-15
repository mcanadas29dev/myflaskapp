/**
 * HEALTHWANA — MAIN JAVASCRIPT
 * Handles: scroll animations, navbar, form validation, mobile menu
 */

'use strict';

/* ============================================
   SCROLL FADE-UP ANIMATION
   ============================================ */
function initScrollAnimations() {
  const targets = document.querySelectorAll('.fade-up');
  if (!targets.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );

  targets.forEach((el) => observer.observe(el));
}

/* ============================================
   NAVBAR: ACTIVE SECTION HIGHLIGHTING
   ============================================ */
function initNavHighlight() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('#menu_nav .uk-navbar-nav a[href^="#"]');

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          navLinks.forEach((link) => {
            link.classList.toggle(
              'uk-text-bold',
              link.getAttribute('href') === `#${entry.target.id}`
            );
          });
        }
      });
    },
    { threshold: 0.4 }
  );

  sections.forEach((s) => observer.observe(s));
}

/* ============================================
   SMOOTH MOBILE OFF-CANVAS CLOSE ON NAV CLICK
   ============================================ */
function initMobileMenuClose() {
  const mobileLinks = document.querySelectorAll('#mobile-menu a');
  mobileLinks.forEach((link) => {
    link.addEventListener('click', () => {
      // UIkit off-canvas close
      const el = document.getElementById('mobile-menu');
      if (el && window.UIkit) {
        UIkit.offcanvas(el).hide();
      }
    });
  });
}

/* ============================================
   CONTACT FORM — CLIENT-SIDE VALIDATION
   (Server-side validation must always be implemented too)
   ============================================ */
function initContactForm() {
  const form = document.getElementById('consultation-form');
  if (!form) return;

  const feedback = document.getElementById('form-feedback');

  function showMessage(message, isError = false) {
    if (!feedback) return;
    feedback.textContent = message;
    feedback.className = isError
      ? 'form-feedback form-feedback--error'
      : 'form-feedback form-feedback--success';
    feedback.hidden = false;
  }

  function sanitize(str) {
    // Basic XSS prevention — strip HTML tags before display
    const temp = document.createElement('div');
    temp.textContent = str;
    return temp.innerHTML;
  }

  function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  function validatePhone(phone) {
    // Allow empty or valid international format
    return phone === '' || /^\+?[\d\s\-().]{7,20}$/.test(phone);
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name    = form.elements['name'].value.trim();
    const email   = form.elements['email'].value.trim();
    const phone   = form.elements['phone'] ? form.elements['phone'].value.trim() : '';
    const goal    = form.elements['goal'].value.trim();
    const message = form.elements['message'] ? form.elements['message'].value.trim() : '';

    // Validation
    if (!name || name.length < 2) {
      showMessage('Please enter your full name.', true);
      return;
    }
    if (!validateEmail(email)) {
      showMessage('Please enter a valid email address.', true);
      return;
    }
    if (!validatePhone(phone)) {
      showMessage('Please enter a valid phone number.', true);
      return;
    }
    if (!goal) {
      showMessage('Please tell us about your primary goal.', true);
      return;
    }

    // Disable submit button during request
    const submitBtn = form.querySelector('[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending…';
    }

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name:    sanitize(name),
          email:   sanitize(email),
          phone:   sanitize(phone),
          goal:    sanitize(goal),
          message: sanitize(message),
        }),
      });

      if (response.ok) {
        showMessage(
          'Thank you! Your consultation request has been received. We will contact you within 24 hours.',
          false
        );
        form.reset();
      } else {
        const data = await response.json().catch(() => ({}));
        showMessage(data.error || 'Something went wrong. Please try again.', true);
      }
    } catch {
      showMessage('Network error. Please check your connection and try again.', true);
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Book your consultation';
      }
    }
  });
}

/* ============================================
   NAVBAR SCROLL SHADOW
   ============================================ */
function initNavbarShadow() {
  const nav = document.getElementById('menu_nav');
  if (!nav) return;

  window.addEventListener('scroll', () => {
    nav.style.boxShadow = window.scrollY > 10
      ? '0 2px 20px rgba(0,0,0,0.08)'
      : 'none';
  }, { passive: true });
}

/* ============================================
   INIT
   ============================================ */
document.addEventListener('DOMContentLoaded', () => {
  initScrollAnimations();
  initNavHighlight();
  initMobileMenuClose();
  initContactForm();
  initNavbarShadow();
});