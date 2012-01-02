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
	
});