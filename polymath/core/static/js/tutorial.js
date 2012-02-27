head.ready(function(){
	



$(document).ready(function(){


	
	$('#fbsignup').tipsy({fade: true, gravity: 's', offset: 2, opacity:0.8});	
	
	var stickyHeaderTop = $('#leftinfoblocktutorial').offset().top;

	 $(window).scroll(function(){
		if( $(window).scrollTop() > stickyHeaderTop - 30) {
			$('#leftinfoblocktutorial').css({position: 'fixed', top: '30px'});
		} else {
			$('#leftinfoblocktutorial').css({position: 'static', top: '30px'});
		}
	});
	

	
	var lessonheight = $('.lessonsBlock').height();
	
	$('.lessonspine.loggedin').css("height",lessonheight-10);
	
	if (lessons > 2){
		$('.lessonspine.loggedout').css("height",lessonheight);		
	} else {
		$('.lessonspine.loggedout').css("height", lessonheight-60);
	}
	

	
	$('.thatsit').css("margin-top", lessonheight-52);
	$('.endcircle').css("margin-top", lessonheight-20);





});


});