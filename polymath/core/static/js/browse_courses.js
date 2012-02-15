head.ready(function(){
	
	
	jQuery.expr[":"].containsNoCase = function(el, i, m) {
	             var search = m[3];
	             if (!search) return false;
	             return eval("/" + search + "/i").test($(el).text());
	         };
	


$(document).ready(function(){
	
	var arr = new Array();

	$('lessonCreatedBlock.browse').each(function() { 
	  arr.push(this.innerHTML); 
	})

	$(".lessonCreatedBlock.browse").show();

	$("body").attr("id","learn");
	
	$('.categoryli').click(function(){
		$('.selectedtags').show();
	});
	
	$("#browsecourselist").jCarouselLite({
		btnPrev:"#previous",
		btnNext: "#next",
		visible: 0,
		circular: "true",
    });

/*
	var stickyHeaderTop = $('.aboutsidebar.browse').offset().top;

	 $(window).scroll(function(){
		if( $(window).scrollTop() > stickyHeaderTop - 30) {
			$('.aboutsidebar.browse').css({position: 'fixed', top: '30px'});
		} else {
			$('.aboutsidebar.browse').css({position: 'static', top: '30px'});
		}
	});
	
	*/

	var stickyHeaderTop = $('.browsing').offset().top;

	 $(window).scroll(function(){
		if( $(window).scrollTop() > stickyHeaderTop - 30) {
			$('.browsing').css({position: 'fixed', top: '30px'});
		} else {
			$('.browsing').css({position: 'static', top: '30px'});
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

		
		
		// user removes "filter by tag", show the entire list of content
		$('.closetagfilter').click(function(){
			window.location.href="/courses/browse/";
		});
		
		
		// search functionality
		$("#txtSearch").keyup(function(){
			if ($('#txtSearch').val().length > 2) {
				$(".browseBlock").hide();
				$('.browseBlock:containsNoCase(\'' + $('#txtSearch').val() + '\')').show();	
//				$(".lessonCreatedBlock.browse").parent().hide();
//				$('.lessonCreatedBlock.browse:containsNoCase(\'' + $('#txtSearch').val() + '\')').parent().show();	
				$(".lessonCreatedBlock.browse").parent().hide();
				$('.lessonCreatedBlock.browse:containsNoCase(\'' + $('#txtSearch').val() + '\')').parent().show();
			} else if ($('#txtSearch').val().length == 0){
				resetSearch();
			}
			
			if ($('.browseBlock:visible').length == 0){
				$(".emptycourselist").show(); // if search results in no lessons, show message
			}
			
			if($('.lessonCreatedBlock.browse:visible').parent().length == 0){
				// if search results in no courses, show message, hide nav buttons, and resize course block
				$(".nocourses").show();
				$("#next").hide();
				$("#previous").hide();
				$("#browsecourselist").css("height","40");
			}
			
			
			
		});
		
		function resetSearch() {
		    // clear the textbox
		    $('#txtSearch').val('');
		    // show all lessons and courses
		    $('.browseBlock').show();
			$('.lessonCreatedBlock.browse').parent().show();
			// remove empty views
			$(".emptycourselist").hide();
			$(".nocourses").hide();
			//show next and previous nav buttons
			$("#next").show();
			$("#previous").show();
			//reset height of courses block
			$("#browsecourselist").css("height","");
		
	
		    // make sure we re-focus on the textbox for usability
		    $('#txtSearch').focus();
		
		}
		
		
	
}); // end jquery ready


}); // end head ready