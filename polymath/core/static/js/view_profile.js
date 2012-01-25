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
	
	
	$('#editprofile').click(function(){
		$('#editblurb').show();
		$('#editprofilesubmit').show();
		$('#saveorcancel').show();
		$(this).hide();
		$('#userblurb').hide();
	});
	
	$('#saveorcancel a').click(function(){
			$('#editblurb').hide();
			$('#editprofilesubmit').hide();
			$('#saveorcancel').hide();
			$('#userblurb').show();
			$('#editprofile').show();
	});
	
	
	$('#profile').click(function(){
		$('#pictureeditdiv').show();
	});
	
	$('#saveorcancel1 a').click(function(){
		$('#pictureeditdiv').hide();
	});
	
	$('#editimageprofile').click(function(){
		$('#pictureeditdiv').show();
	});
	
	
	var stickyHeaderTop = $('#leftsidediv').offset().top;

	 $(window).scroll(function(){
		if( $(window).scrollTop() > stickyHeaderTop - 30) {
			$('#leftsidediv').css({position: 'fixed', top: '30px'});
		} else {
			$('#leftsidediv').css({position: 'static', top: '30px'});
		}
	});
	
	
	
//	$('.subject').tipsy({fade: false, gravity: 's', opacity:0.6});
	
//	$('.lessonCreatedBlock').tipsy({fade: false, gravity: 's', opacity:0.6});
	
}); 