$(document).ready(function(){

	$('.profilecourseBlock').mouseenter(function(){
		$(this).toggleClass("highlight");
		});

	$('.profilecourseBlock').mouseleave(function(){
		$(this).toggleClass("highlight");
	});

//	$('.subject').tipsy({fade: false, gravity: 's', opacity:0.6});
	
//	$('.lessonCreatedBlock').tipsy({fade: false, gravity: 's', opacity:0.6});
	
}); 