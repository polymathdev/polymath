$(document).ready(function(){

	$('.profilecourseBlock').mouseenter(function(){
		$(this).toggleClass("highlight");
		});

	$('.profilecourseBlock').mouseleave(function(){
		$(this).toggleClass("highlight");
	});

	$(".lessonCreatedBlock").click(function(){
		if( $(this).find(".coursename").attr("href") ){
	     window.location=$(this).find(".coursename").attr("href");
	     return false;
		} else {
			
		}
	});
//	$('.subject').tipsy({fade: false, gravity: 's', opacity:0.6});
	
//	$('.lessonCreatedBlock').tipsy({fade: false, gravity: 's', opacity:0.6});
	
}); 