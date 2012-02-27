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
	






});


});