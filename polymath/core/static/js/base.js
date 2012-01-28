$(document).ready(function(){
	
	$(".messages").animate({
	  opacity:"show"
	  }, 700 );
	
	
//	$('.messages').slideDown('fast', function() {
//	    // Animation complete.
//	  });
	

	$('#close').click(function(){
			$(".messages").animate({
			  opacity:"hide"
			  }, 200 );
	});

	$('.nav li').click(function(){
		$(this).toggleClass("selected");
	});
	
	$('#loginnav').colorbox({
		width:"500px",
		inline: true,
		href:"#logindivnew",
		opacity:'0.6',
		top:"10%",
		returnFocus:false,
	});
	
	
	$('#homevideo').colorbox({
		width:"522px",
		height:"335px",
		inline: true,
		href:"#videolightbox",
		opacity:'0.7',
		top:"10%",
		returnFocus:false,
	});
	
	
	
});