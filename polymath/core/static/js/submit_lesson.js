head.ready(function(){
	



$(document).ready(function(){


	$("select").sb();
	
	$('#id_tags').tagsInput({
		'width':'275px',
		'height':'70px',
		'defaultText':'Add a tag',
		'onAddTag': updatehiddendiv,	// when a new tag is added, update the hidden div that the validate function checks
	});
	
	function updatehiddendiv(tag){
		var value = $('#id_tags').val();
		$("#tagsexist").val(value);
		$("#submit_lesson_form").validate().element("#tagsexist");
	}
	
	
	$("#submitlesson").click(function(){
		updatehiddendiv();
		
	});


	$("#submit_lesson_form").validate({
		submitHandler: function(form){
			$('#submit_lesson_form :submit').attr('disabled','true');
			// Get the current value of the contents within the text box
			var val = $('#id_tags').val().toLowerCase();
           	// Reset the current value to the Upper Case Value
           	$('#id_tags').val(val);
			form.submit();
		},
		rules: {
			name: {
				required: true,
				maxlength: 40
			},
			description: {
				required: true
			},
			category: {
				required: true
			}, 
			link :{
				required: true
			}, 
			type: {
				required: true
			}, 
			tagsExist:{
				required: true
			}
		}, 		
	});
	
	
	
}); 




});