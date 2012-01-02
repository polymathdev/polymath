$(document).ready(function(){


$('#ticker').jCarouselLite({  
        vertical: true,  
        visible: 1,  
        auto:1700,  
        speed:100 ,
		hoverPause : true,
 });



$('.featuredblock').mouseenter(function(){
	$(this).toggleClass("highlight");
	$(this).css('cursor', 'pointer');
});

$('.featuredblock').mouseleave(function(){
	$(this).toggleClass("highlight");
});

$('.featuredblock.1').click(function(){
	document.location.href='course1.html'; 
});

$('.featuredblock.2').click(function(){
	document.location.href='course2.html'; 
});

$('.featuredblock.3').click(function(){
	document.location.href='course3.html'; 
});


	$(function(){
	        // Check the initial Poistion of the Sticky Header
	        var stickyHeaderTop = $('.fbsignin').offset().top;

	        $(window).scroll(function(){
	                if( $(window).scrollTop() > stickyHeaderTop ) {
	                        $('.fbsignin').css({position: 'fixed', top: '45px'});
	                } else {
	                        $('.fbsignin').css({position: 'static', top: '45px'});
	                }
	        });
	  });




});