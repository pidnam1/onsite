



!(function($) {
  "use strict"; // Start of use strict

   // Preloader
  $(window).on('load', function() {
    if ($('#preloader').length) {
      $('#preloader').delay(150).fadeOut('slow', function() {
        $(this).remove();
      });
    }
  });

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 56)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

    // Toggle nav bar to transparent and dark when page is scrolled
  $(window).scroll(function() {
    if ($(this).scrollTop() > 650) {
    $('#mainNav').removeClass('navbar-transparent');
       $('#mainNav').addClass('navbar-dark');
       $('#mainNav').removeClass('bg-transparent');
       $('#mainNav').addClass('bg-dark');
    } else {
       $('#mainNav').addClass('navbar-transparent');
       $('#mainNav').removeClass('navbar-dark');
       $('#mainNav').addClass('bg-transparent');
       $('#mainNav').removeClass('bg-dark');
    }
  });

  if ($(window).scrollTop() > 100) {
      $('#mainNav').addClass('navbar-transparent');
       $('#mainNav').removeClass('navbar-dark');
       $('#mainNav').addClass('bg-transparent');
       $('#mainNav').removeClass('bg-dark');
  }

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 56
  });

  // Testimonials carousel (uses the Owl Carousel library)
  $(".testimonials-carousel").owlCarousel({
    autoplay: true,
    dots: true,
    loop: true,
    items: 1
  });

  // Activate smooth scroll on page load with hash links in the url
  $(document).ready(function() {
    if (window.location.hash) {
      var initial_nav = window.location.hash;
      if ($(initial_nav).length) {
        var scrollto = $(initial_nav).offset().top - scrolltoOffset;
        $('html, body').animate({
          scrollTop: scrollto
        }, 1500, 'easeInOutExpo');
      }
    }
  });

   // Navigation active state on scroll
  var nav_sections = $('section');
  var main_nav = $('.nav-menu, .mobile-nav');

  $(window).on('scroll', function() {
    var cur_pos = $(this).scrollTop() + 200;

    nav_sections.each(function() {
      var top = $(this).offset().top,
        bottom = top + $(this).outerHeight();

      if (cur_pos >= top && cur_pos <= bottom) {
        if (cur_pos <= bottom) {
          main_nav.find('li').removeClass('active');
        }
        main_nav.find('a[href="#' + $(this).attr('id') + '"]').parent('li').addClass('active');
      }
      if (cur_pos < 300) {
        $(".nav-menu ul:first li:first, .mobile-menu ul:first li:first").addClass('active');
      }
    });
  });

  // jQuery counterUp
  $('[data-toggle="counter-up"]').counterUp({
    delay: 10,
    time: 1000
  });

  // Init AOS
  function aos_init() {
    AOS.init({
      duration: 1000,
      easing: "ease-in-out",
      once: true,
      mirror: false
    });
  }
  $(window).on('load', function() {
    aos_init();
  });


})(jQuery); // End of use strict

