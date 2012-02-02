head.ready(function(){
	


$(document).ready(function(){
	

	
	// store url for current page as global variable
	current_page = document.location.href

	// apply selected states depending on current page
	if (current_page.match(/about/)) {
	$(".aboutsidebar ul li:eq(0)").addClass('selected');
	} else if (current_page.match(/beliefs/)) {
	$(".aboutsidebar ul li:eq(2)").addClass('selected');
	} else if (current_page.match(/howitworks/)) {
	$(".aboutsidebar ul li:eq(1)").addClass('selected');
	}  else if (current_page.match(/welcome/)) {
	$(".aboutsidebar ul li:eq(1)").addClass('selected');
	} else if (current_page.match(/contact/)) {
	$(".aboutsidebar ul li:eq(3)").addClass('selected');
	} else { // don't mark any nav links as selected
	$("ul#navigation li").removeClass('selected');
	};
	
	
	
});

});