/* ============ ENHANCEMENTS JS ============ */
/* Feature enhancements for The Visionaries website */

(function () {
  'use strict';

  // Wait for DOM to be fully loaded
  document.addEventListener('DOMContentLoaded', function () {

    // ======================================================
    // 1. SCROLL PROGRESS BAR
    // ======================================================
    var progressBar = document.getElementById('scrollProgress');

    function updateScrollProgress() {
      if (!progressBar) return;
      var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      var docHeight = document.documentElement.scrollHeight - window.innerHeight;
      var scrollPercent = (scrollTop / docHeight) * 100;
      progressBar.style.width = scrollPercent + '%';
    }

    // ======================================================
    // 2. BACK-TO-TOP BUTTON
    // ======================================================
    var backToTopBtn = document.getElementById('backToTop');

    function toggleBackToTop() {
      if (!backToTopBtn) return;
      var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      if (scrollTop > 400) {
        backToTopBtn.classList.add('visible');
      } else {
        backToTopBtn.classList.remove('visible');
      }
    }

    if (backToTopBtn) {
      backToTopBtn.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }

    // ======================================================
    // 3. NAVBAR SHRINK ON SCROLL
    // ======================================================
    var header = document.querySelector('header');

    function handleNavShrink() {
      if (!header) return;
      var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      if (scrollTop > 80) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    }

    // ======================================================
    // 4. ACTIVE NAV INDICATOR
    // ======================================================
    var navLinks = document.querySelectorAll('.nav-links a');
    var sections = [];

    // Build section list from nav links
    navLinks.forEach(function (link) {
      var href = link.getAttribute('href');
      if (href && href.startsWith('#') && href.length > 1) {
        var section = document.getElementById(href.substring(1));
        if (section) {
          sections.push({ el: section, link: link });
        }
      }
    });

    function updateActiveNav() {
      var scrollTop = window.pageYOffset + 200; // offset for header
      var currentSection = null;

      sections.forEach(function (item) {
        var top = item.el.offsetTop;
        var bottom = top + item.el.offsetHeight;
        if (scrollTop >= top && scrollTop < bottom) {
          currentSection = item;
        }
      });

      navLinks.forEach(function (link) {
        link.classList.remove('active');
      });

      if (currentSection) {
        currentSection.link.classList.add('active');
      }
    }

    // ======================================================
    // COMBINED SCROLL LISTENER (efficient)
    // ======================================================
    var ticking = false;

    window.addEventListener('scroll', function () {
      if (!ticking) {
        window.requestAnimationFrame(function () {
          updateScrollProgress();
          toggleBackToTop();
          handleNavShrink();
          updateActiveNav();
          ticking = false;
        });
        ticking = true;
      }
    });

    // Initial calls
    updateScrollProgress();
    toggleBackToTop();
    handleNavShrink();
    updateActiveNav();

    // ======================================================
    // 5. ANIMATED COUNTER STATS
    // ======================================================
    function animateCounter(element) {
      var text = element.textContent.trim();
      // Parse the number, prefix, and suffix
      var match = text.match(/^([^\d]*)([\d,]+)(.*)$/);
      if (!match) return; // Skip non-numeric like "Type-C"

      var prefix = match[1]; // e.g., "₹"
      var numStr = match[2].replace(/,/g, ''); // remove commas
      var suffix = match[3]; // e.g., "cm", "+"
      var target = parseInt(numStr, 10);

      if (isNaN(target) || target === 0) return;

      var duration = 2000; // 2 seconds
      var startTime = null;
      element.textContent = prefix + '0' + suffix;

      function step(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = Math.min((timestamp - startTime) / duration, 1);
        // Ease out cubic
        var eased = 1 - Math.pow(1 - progress, 3);
        var current = Math.floor(eased * target);

        // Format with commas if original had them
        var formatted = current.toLocaleString();
        element.textContent = prefix + formatted + suffix;

        if (progress < 1) {
          requestAnimationFrame(step);
        }
      }

      requestAnimationFrame(step);
    }

    // Use IntersectionObserver to trigger counters
    var counterObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          counterObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    // Observe all stat numbers
    var statNums = document.querySelectorAll('.stat .num, .win-stat .num');
    statNums.forEach(function (el) {
      el.setAttribute('data-original', el.textContent.trim());
      counterObserver.observe(el);
    });

    // ======================================================
    // 6. TYPING EFFECT ON HERO SUBTITLE
    // ======================================================
    var heroSub = document.querySelector('.hero .sub');

    if (heroSub) {
      var fullText = heroSub.textContent.trim();
      heroSub.textContent = '';

      // Add cursor span
      var cursorSpan = document.createElement('span');
      cursorSpan.className = 'typing-cursor';
      heroSub.appendChild(cursorSpan);

      var charIndex = 0;
      var typingSpeed = 35; // ms per character

      function typeChar() {
        if (charIndex < fullText.length) {
          // Insert character before cursor
          var textNode = document.createTextNode(fullText.charAt(charIndex));
          heroSub.insertBefore(textNode, cursorSpan);
          charIndex++;
          setTimeout(typeChar, typingSpeed);
        } else {
          // Remove cursor after a delay
          setTimeout(function () {
            cursorSpan.style.animation = 'none';
            cursorSpan.style.opacity = '0';
            cursorSpan.style.transition = 'opacity 0.5s ease';
          }, 2000);
        }
      }

      // Start typing after a short delay
      setTimeout(typeChar, 800);
    }

    // ======================================================
    // 7. PARTICLE NETWORK BACKGROUND (Hero)
    // ======================================================
    var canvas = document.getElementById('particleCanvas');

    if (canvas) {
      var ctx = canvas.getContext('2d');
      var particles = [];
      var numParticles = 25;
      var connectionDistance = 150;
      var animFrameId = null;

      function resizeCanvas() {
        var heroVisual = canvas.parentElement;
        if (heroVisual) {
          canvas.width = heroVisual.offsetWidth;
          canvas.height = heroVisual.offsetHeight;
        }
      }

      function Particle() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.radius = Math.random() * 2 + 1;
      }

      Particle.prototype.update = function () {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
      };

      Particle.prototype.draw = function () {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(212, 175, 55, 0.5)';
        ctx.fill();
      };

      function initParticles() {
        particles = [];
        for (var i = 0; i < numParticles; i++) {
          particles.push(new Particle());
        }
      }

      function drawConnections() {
        for (var i = 0; i < particles.length; i++) {
          for (var j = i + 1; j < particles.length; j++) {
            var dx = particles[i].x - particles[j].x;
            var dy = particles[i].y - particles[j].y;
            var dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < connectionDistance) {
              var opacity = (1 - dist / connectionDistance) * 0.3;
              ctx.beginPath();
              ctx.moveTo(particles[i].x, particles[i].y);
              ctx.lineTo(particles[j].x, particles[j].y);
              ctx.strokeStyle = 'rgba(212, 175, 55, ' + opacity + ')';
              ctx.lineWidth = 0.5;
              ctx.stroke();
            }
          }
        }
      }

      function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach(function (p) {
          p.update();
          p.draw();
        });

        drawConnections();
        animFrameId = requestAnimationFrame(animateParticles);
      }

      resizeCanvas();
      initParticles();
      animateParticles();

      window.addEventListener('resize', function () {
        resizeCanvas();
        initParticles();
      });
    }

    // ======================================================
    // 8. 3D TILT EFFECT ON FEATURE CARDS
    // ======================================================
    var featureCards = document.querySelectorAll('.feature');

    featureCards.forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var rect = card.getBoundingClientRect();
        var x = e.clientX - rect.left; // x within card
        var y = e.clientY - rect.top;  // y within card

        var centerX = rect.width / 2;
        var centerY = rect.height / 2;

        var rotateX = ((y - centerY) / centerY) * -8; // max 8 degrees
        var rotateY = ((x - centerX) / centerX) * 8;

        card.style.transform = 'rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg) scale(1.02)';
      });

      card.addEventListener('mouseleave', function () {
        card.style.transform = 'rotateX(0) rotateY(0) scale(1)';
      });
    });

  }); // end DOMContentLoaded
})();
