head.ready(function(){


$(document).ready(function(){

	$('#coda-slider-1').codaSlider({
				dynamicTabs: false, 
				dynamicArrows: false,
				slideEaseDuration: 200,
			});
		
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

				
			});
	
		
});


});

