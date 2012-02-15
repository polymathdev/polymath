head.ready(function(){
	


$(document).ready(function(){
	



	$("body").attr("id","learn");
	
	$('.categoryli').click(function(){
		$('.selectedtags').show();
	});
	
	$("#browsecourselist").jCarouselLite({
		btnPrev:"#previous",
        btnNext: "#next", 
		visible: 0,
    });


	var stickyHeaderTop = $('.aboutsidebar.browse').offset().top;

	 $(window).scroll(function(){
		if( $(window).scrollTop() > stickyHeaderTop - 30) {
			$('.aboutsidebar.browse').css({position: 'fixed', top: '30px'});
		} else {
			$('.aboutsidebar.browse').css({position: 'static', top: '30px'});
		}
	});
	
	
	
		// store url for current page as global variable
		current_page = window.location.href
		
		console.log("%s", current_page);
		
		
		// apply selected states depending on current page
		if (current_page.match(/programming/)) {
			$(".aboutsidebar li:eq(1)").addClass('selected');
		} else if (current_page.match(/design/)) {
				$(".aboutsidebar li:eq(2)").addClass('selected');
		} else if (current_page.match(/entrepreneurship/)) {
				$(".aboutsidebar li:eq(3)").addClass('selected');
		}  else if (current_page.match()) {
				$(".aboutsidebar li:eq(0)").addClass('selected');
		} else { // don't mark any nav links as selected
			$(".aboutsidebar li:eq(0)").addClass('selected');
		};
	
	
		$('.lessoncount').tipsy({fade: false, gravity: 's', opacity:0.8});
		$('.numfollowers').tipsy({fade: false, gravity: 's', opacity:0.8});
		$('.browsepageheading').tipsy({fade: false, gravity: 'e', opacity:0.9});

		
		$('.closetagfilter').click(function(){
			window.location.href="/courses/browse/";
		});
	
});


});