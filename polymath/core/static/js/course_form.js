head.ready(function(){
	



$(document).ready(function(){

	
// 	$("#id_category option:eq(0)").text("Course Category");
	$("select").sb();

	$('#id_tags').tagsInput({
		'width':'280px',
		'height':'75px',
		'defaultText':'Add a tag',
		'onAddTag': updatehiddendiv,			// when a new tag is added, update the hidden div that the validate function checks
	});
	
	
	function updatehiddendiv(){
		var value = $('#id_tags').val();
		$("#tagsexist").val(value);
		$("#new_course_form").validate().element("#tagsexist");
	}
	

    
    $('#test_btn').click(function() {
        $('.lesson_div').each(function(i) {
            console.log(i + ':' + $(this).find('input[name$="-name"]').attr('name'));  
        });
    });
    reorder_lessons();

    // add lesson
    $('#add_lesson_btn').click(function(){
        // increment total # of forms
        new_lesson_num = parseInt($('input[name$="TOTAL_FORMS"]').val()) + 1;
        $('input[name$="TOTAL_FORMS"]').val(new_lesson_num);

        // create HTML for new form by inserting the new # in for __prefix__ (created by Django's formset.emptyform)
        new_form_html = $('#empty_lesson_form_div').html().replace(/__prefix__/g, (new_lesson_num-1));

        // create a new div containing the new form HTML
        new_lesson_div = $('<div>').addClass('lesson_div').addClass('extra').html(new_form_html);
        new_lesson_div.find('.lesson_num_spn').html(new_lesson_num);
        new_lesson_div.appendTo('#lesson_list_div');
    });
    
	$('#lesson_list_div').sortable({
		tolerance : 'intersect',
		opacity: 0.8,
		forcePlaceholderSize: true,
		placeholder: "ui-state-highlight",
	//	connectWith: '#lesson_list_div',
		helper: function(event, element) {
		        return element.clone().appendTo("body");
		    }
	});
	
	
//	$('.lessonlink').tipsy({fade: false, gravity: 'e', opacity:0.6});
	

    // move lesson up
    $('#lesson_list_div').on('click', '.move_up_lnk', function() {
        // take this lesson and move the previous one after it (i.e. move this one up)
        $(this).parent('.lesson_div').after($(this).parent('.lesson_div').prev('.lesson_div'));
        reorder_lessons();
    });


    // move lesson down
    $('#lesson_list_div').on('click', '.move_down_lnk', function() {
        // take this lesson and move the next one before it (i.e. move this one down)
        $(this).parent('.lesson_div').before($(this).parent('.lesson_div').next('.lesson_div')); 
        reorder_lessons();
    });

    
    // remove lesson
    $('#lesson_list_div').on('click', '.remove_lesson_lnk', function() {
        this_lesson_div = $(this).parent('.lesson_div');

        function remove_the_form(is_initial) {
            // decrement total/initial forms values in management form
            if( is_initial ) {
                $('input[name$="INITIAL_FORMS"]').val(parseInt($('input[name$="INITIAL_FORMS"]').val()) - 1);    
            }
            $('input[name$="TOTAL_FORMS"]').val(parseInt($('input[name$="TOTAL_FORMS"]').val()) - 1);
            this_lesson_div.remove();
            reorder_lessons(is_initial);
        }

        if( ! this_lesson_div.hasClass('extra') ) {
            // the way i formatted the below $.post() might look extremely ugly...haven't decided yet
            $.post(
                from_server['delete_lesson_url'],
                {lesson_id: $(this).parent('.lesson_div').find('input[id$="-id"]').val() },
                function(response) {
                    alert(response['result_message']);
                    if( response['delete_successful'] ) {
                        remove_the_form(true);
                    }
                }
            );
        } else {
            remove_the_form(false);
        }

    });
    
    
    // re-writes Lesson # headings and more importantly updates the formset order fields and input name prefixes
    function reorder_lessons(reorder_initial) {

        valid_lesson_count = 1
        
        // update order fields for all lessons
        $('.lesson_div').each(function(index) {
            $(this).find('.lesson_num_spn').html(index+1);
            $(this).find('input[name$="order"]').val(valid_lesson_count);  
            valid_lesson_count++;
        });

        // re-order input names for the initial forms if necessary (i.e. when an initial form was deleted)
        if( reorder_initial ) {
            $('.lesson_div:not(.extra)').each(function(index) {
                // TODO: should refactor this since i do it again below...
                $(this).find(':input').each(function(i) { 
                    new_input_name = $(this).attr('name').replace(/(.*-)\d+(-.*)/,'$1' + index + '$2'); 
                    $(this).attr('name', new_input_name);
                });
            });
        }

        num_initial_forms = parseInt($('input[name$="INITIAL_FORMS"]').val());

        // re-order extra lesson input names to play nicely with Django
        $('.extra').each(function(index) {

            // go through all input fields in this .lesson_div and replace the input name index with the one from the loop so we get a consecutive sequence of these overall when combined with the initial ones
            // (needed to place nice with Django) 
            $(this).find(':input').each(function(i) {
                new_input_name = $(this).attr('name').replace(/(.*-)\d+(-.*)/,'$1' + (parseInt(num_initial_forms)+index) + '$2');
                $(this).attr('name', new_input_name);
            });
        });
    }

  //  $('#new_course_form').submit(function() {
    //    $('#new_course_form :submit').attr('disabled','true');
      //  reorder_lessons()
//    });



	$('#editimage').click(function(){
		$('#photouploaddiv').toggle();
	});
	
	$('#sim_save_course').click(function(){
		$('#save_course').trigger('click');
	});
	
	$('#sim_add_lesson_btn').click(function(){
		$('#add_lesson_btn').trigger('click');
	});
	
	
/*
	var stickyHeaderTop = $('#sim_save_course').offset().top;

	 $(window).scroll(function(){
		if( $(window).scrollTop() > stickyHeaderTop - 40) {
			$('#sim_save_course').css({position: 'fixed', top: '40px', left:'20px'});
		} else {
			$('#sim_save_course').css({position: 'static', top: '40px'});
		}
	});*/
	
	
	
	// COURSE PHOTO JAVASCRIPT
	
	$('#editimage').colorbox({
		width:"350px",
		height:"250px",
		inline: true,
		href:"#uploadphoto",
		opacity:'0',
		top:"10%",
		returnFocus:false,
		onLoad:function(){
			$('#cboxClose').remove();
		}
	});
	
	var intervalFunc = function () {	// update our custom span with the value of the default, hidden id_photo div
		$("#file-name").show();
		var filename = $('#id_photo').val().replace(/^.*[\\\/]/, '')
//		var shorttext = $.trim(filename).substring(0, 30).split(" ").slice(0, -1).join(" ") + "...";
        $('#file-name').html(filename);
    };


	$("#browsephoto").unbind("click").bind("click", function () { // bind our custom browse button to the default id_photo functionality
	   $("#id_photo").click();
	   setInterval(intervalFunc, 1);
       return false;
	});
		
	
	$('#id_photo').change(function(){	
			var val = $(this).val();

			    switch(val.substring(val.lastIndexOf('.') + 1).toLowerCase()){
			        case 'gif': case 'jpg': case 'png': case 'jpeg':
						handleFiles(this.files)  // if file select input was changed, trigger the store & image preview function
			            break;
			        default:
			            $(this).val('');
			            // error message here
			            alert("Please upload an image file.");
			            break;
			    }
		
	  });
	
	

	function handleFiles(files){		// use HTML5 filereader api to preview the image, and hide any existing images
		for (var i = 0; i < files.length; i++) {  
	    var file = files[i];  
	    var imageType = /image.*/;  

	    if (!file.type.match(imageType)) {  
	      continue;  
	    }  

	    var img = document.createElement("img");  
	    img.classList.add("obj");  
	    img.file = file;  
		img.height = 60;
		img.width =60;
	
		var box = document.getElementById('imageBox');
		
		if ( box.hasChildNodes() )					// loop to remove any existing images
		{
		    while ( box.childNodes.length >= 1 )
		    {
		        box.removeChild( box.firstChild );	       
		    } 
		}
		
		box.appendChild(img);  				//add preview image to the DOM
		
		$('#existingphoto').hide(); 			// hide old photo and delete button
		$('#deletephotobutton').hide();
	
		img.setAttribute('id', 'previewImage');		// #previewImage

	    	var reader = new FileReader();  
	    	reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(img);  
	    	reader.readAsDataURL(file);  
		
	  }
	
	}
	
	
	
	var blankPhoto = $("#hiddenblankphoto").attr("src");
	var originalimage = $("#courseLogo").attr("src");
	
	$("#savephoto").click(function(){		// when the save/okay button is clicked...
		
		
		$('#editimage').colorbox.close();	
		
		var newfile = $("#id_photo").val();   // save the value of the new file input, whether empty (no image) or new image
		var filename = newfile.replace(/^.*[\\\/]/, '')
		$("#photourl").text("New photo: " + filename);  // update span on front-end on course form
		
		var newimage = $("#previewImage").attr('src');    // store preview image value
		
		
		if (newfile.length > 0){	// check if new image or not
			$("#courseLogo").attr("src", newimage);			// update front-end with this image preview
			$('#photo-clear_id').removeAttr("checked");    // override the default behavior of the ClearableInput field
		} else {
			$("#courseLogo").attr("src", blankPhoto);		// if no image, update front-end with the default "blank" image
		}
		

	});
	
	
	
	$("#deletephotobutton").click(function(){
		$('#photo-clear_id').trigger('click'); // check the Django ClearableInput checkbox to remove the file
		$('#existingphoto').hide(); // hide the current photo
		$(this).hide(); // hide the X button
		$("#file-name").text("No image currently selected.");	// hide the filename
	});
	



	$("#photocancel").click(function(){  // when cancelled, reset all properties
		
		$('#editimage').colorbox.close();			// hide the colorbox
		
		$("#existingphoto").attr("src", originalimage); // return photo to last saved image on course form
		$('#existingphoto').show(); 				// show the latest photo
		$("#photourl").text("");  // update span on front-end on course form
		
		
		$('#deletephotobutton').show(); 			// show the delete button
		$("#file-name").show();						// show the file name
		$('#photo-clear_id').removeAttr("checked");    // reset clearableinput to default
		$("#previewImage").remove();				// remove the preview image in the photo div
		
		$("#id_photo").replaceWith($("#id_photo").clone(true));	// since we can't edit the form instance, we create a new one
		$("#id_photo").val("");	// the form will take a blank value
		
		$("#courseLogo").attr("src", originalimage);
	});
	
	
	
	
	
	
	// SUBMIT COURSE FORM
	
		$("#save_course").click(function(){
			updatehiddendiv();
			
		});
	

		$("#new_course_form").validate({
			submitHandler: function(form){
				$('#new_course_form :submit').attr('disabled','true');
		        reorder_lessons()
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
				tagsexist : {
					required: true
				}
			}, 		
		});
		
		
		
		
	

}); 




});