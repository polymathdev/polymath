$(document).ready(function(){

	$('.categoryli').click(function(){
		$('.selectedtags').show();
		});

		$('.courseBlock').mouseenter(function(){
			$(this).toggleClass("highlight");
			});

		$('.courseBlock').mouseleave(function(){
			$(this).toggleClass("highlight");
		});



});