head.ready(function(){
	
	
$(document).ready(function(){
	
$('#webdesign').hide();

$('#ticker').show();

$('#ticker').jCarouselLite({  
        vertical: true,  
        visible: 1,  
        auto:1700,  
        speed:200 ,
		hoverPause : true,
		easing: "easeOutBounce"
 });



$('.featuredblock').mouseenter(function(){
	$(this).toggleClass("highlight");
	$(this).css('cursor', 'pointer');
});

$('.featuredblock').mouseleave(function(){
	$(this).toggleClass("highlight");
});


$(".featuredBlock").click(function(){
	if( $(this).find(".coursename").attr("href") ){
     window.location=$(this).find(".coursename").attr("href");
     return false;
	} else {
		
	}
})


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



});