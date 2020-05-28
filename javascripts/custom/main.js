/*
* EGO - A premium portfolio template from designova
* Author: Designova, http://www.designova.net
* Copyright (C) 2015 Designova
* This is a premium product. For licensing queries please contact info@designova.net
*/

/*global $:false */
/*global window: false */

(function(){
  "use strict";


$(function ($) {


//Detecting viewpot dimension
    var vH = $(window).height();
    var vW = $(window).width();


//Adjusting Intro Components Spacing based on detected screen resolution
    $('.fullwidth').css('width',vW);
    $('.fullheight').css('height',vH);
    $('.halfwidth').css('width',vW/2);
    $('.halfheight').css('height',vH/2);
    $('.menu-panel').css('height',vH);

//PRELOADER
        $('div#preloader.fluidview').css('width', vW);
        $('div#preloader.fluidview').css('height', vH);
        $('body, html').addClass('preloader-running');
        $('#mastwrap').css('visibility', 'hidden');
        $(window).load(function() {
            $("#status").delay(800).fadeOut();
            $("#preloader").delay(1000).fadeOut(1000);
            $('body, html').removeClass('preloader-running');
            $('body, html').addClass('preloader-done');
            $("#mastwrap").delay(1000).css('visibility', 'visible');
});

//Equal Heights Trigger
        $('.equal-height').setAllToMaxHeight();
        $('.team-01-image, .team-01-info').setAllToMaxHeight();

//Featured Side Panel View
            $('.cd-btn').on('click', function(event) {
                event.preventDefault();
                $('.cd-panel').addClass('is-visible');
            });
            //close the lateral panel
            $('.cd-panel').on('click', function(event) {
                if ($(event.target).is('.cd-panel') || $(event.target).is('.cd-panel-close')) {
                    $('.cd-panel').removeClass('is-visible');
                    event.preventDefault();
                }
            });
             //close the lateral panel on close-btn click
            $('.menu-close-trigger').on('click', function(event) {
                event.preventDefault();
                    $('.cd-panel').removeClass('is-visible');
            });


//Sub Menu Trigger
        $('.main-menu li a.sub-menu-trigger').on('mouseenter', function(){
            $(this).next('.sub-menu').stop().slideDown();
        });
        $('.main-menu li').on('mouseleave', function(){
            $('.sub-menu').stop().slideUp();
        });


//Inner Sticky Navigation
        $('.mastwrap section:nth-child(2)').waypoint(function (direction) {
              if (direction === 'down') {
                 $('header.masthead').addClass('header-highlighted');
                 $('div#preloader').css('top',50);
              } 
              else {
                 $('header.masthead').removeClass('header-highlighted');
                 $('div#preloader').css('top',120);
              }
        }, { offset: 50 });


//Misc UX
        $('.rev_slider_wrapper').waypoint(function (direction) {
              if (direction === 'down') {
                $('.tp-bullets').fadeOut('slow');
              } 
              else {
                $('.tp-bullets').fadeIn('slow');
              }
        }, { offset: 50 });

        

//Filter Panel Trigger
        $('.works-container').waypoint(function (direction) {
              if (direction === 'down') {
                 $('.filter-notification').fadeIn();
              } 
              else {
                 $('.filter-notification').fadeOut();
              }
        }, { offset: 200 });
        $('.filter-notification a').on('click', function(){
            $('.works-filter-panel').slideDown();
        });
        $('.works-filter li a').on('click', function(){
            $('.works-filter-panel').slideUp();
            $('html, body').animate({
                scrollTop: $("#works-container").offset().top-100
            }, 2000);
        });


 //PARALLAX
        //Initialize Each Parallax Layer  
        function parallaxInit() {
            $.stellar({
                positionProperty: 'transform'
            });
        }

        if (!device.tablet() && !device.mobile()) {

            //Activating Parallax effect if non-mobile device is detected
            $(window).bind('load', function() {
                parallaxInit();
            });


        } else {

            //Dectivate Parallax effect if mobile device is detected (bg image is displayed)
            $('.parallax, .parallax-layer').addClass('no-parallax');

        }

//ISOTOPE
        
        //ISOTOPE GLOBALS
        var $container1 = $('.works-container');


        //ISOTOPE INIT
        $(window).load(function() {
            $container1.isotope({
                // options
                itemSelector: '.works-item',
                layoutMode: 'masonry',
                transitionDuration: '0.8s'
            });
            //forcing a perfect masonry layout after initial load
            setTimeout(function() {
            $container1.isotope('layout');
            }, 100);
            // filtering
            $('.works-filter li a').on('click', function() {
                $('.works-filter li a').removeClass('active');
                $(this).addClass('active');

                var selector = $(this).attr('data-filter');
                $('.works-container').isotope({
                    filter: selector
                });
                return false;
            });
        });

        //Isotope ReLayout on Window Resize event.
        $(window).on('resize', function() {
            $container1.isotope('layout');
        });

        //Isotope ReLayout on device orientation changes
        window.addEventListener("orientationchange", function() {
            $container1.isotope('layout');
        }, false);



//VENOBOX
    $('.venobox, .image-lightbox-link').venobox({
        numeratio: true,
        infinigall: true
    });   
        
   
});
// $(function ($)  : ends

})();
//  JSHint wrapper $(function ($)  : ends







  

