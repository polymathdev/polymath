head.ready(function(){


$(document).ready(function(){
	
	$("#dim").css("height", $(document).height());
	
	$('#smelly').appear(function() {
		$("#howitworkscall").delay(1800).fadeIn();
		$(".messages").delay(1500).fadeOut();
		$("#nextbutton").delay(1500).fadeOut();
		$("#coda-nav-1").delay(1500).fadeIn();
	});
	
	
	$('#coda-slider-1').codaSlider({
				dynamicTabs: false, 
				dynamicArrows: false,
				slideEaseDuration: 200,
			});
		
		/*
			$("#nextbutton").click(function(){
				$(this).hide();
				setTimeout(function(){
				     var height = $("#coda-slider-1").height();
					console.log("height of panel is %s", height);
					height = height/2;
					console.log("new height is %s", height);
					$("#nextbutton").css("margin-top", height);
					$("#nextbutton").show();
				},800);
			});
			
			
			$(".previewimages a").click(function(){
				$("nextbutton").hide();
				setTimeout(function(){
				     var height = $("#coda-slider-1").height();
					console.log("height of panel is %s", height);
					height = height/2;
					console.log("new height is %s", height);
					$("#nextbutton").css("margin-top", height);
					$("#nextbutton").show();
				},800);

				
			});*/
	
		
	
	
		
});




});

