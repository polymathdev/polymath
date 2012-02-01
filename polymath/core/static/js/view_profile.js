$(document).ready(function(){
	
	// 
	
/*
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
	}); */
	
	$('.lessoncount').tipsy({fade: false, gravity: 's', opacity:0.8});
	$('.numfollowers').tipsy({fade: false, gravity: 's', opacity:0.8});
	
	 $('#editblurb textarea').addClass('blurbbox');
	
	
	// make sure the user can't submit an empty blurb
	//$('#profile_edit_form').submit(function() 
	
	$("#editprofilesubmit").click(function(){
        if ( $.trim( $(this).closest('form').find('.blurbbox').val()  ) == "" ) {
            return false;
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
	
	// old picture edit js
	
	$('#saveorcancel1 a').click(function(){
		$('#pictureeditdiv').hide();
	});
	
//	$('#editimageprofile').click(function(){
//		$('#pictureeditdiv').show();
//	}); 
	
	
	var stickyHeaderTop = $('#leftsidediv').offset().top;

	 $(window).scroll(function(){
		if( $(window).scrollTop() > stickyHeaderTop - 30) {
			$('#leftsidediv').css({position: 'fixed', top: '30px'});
		} else {
			$('#leftsidediv').css({position: 'static', top: '30px'});
		}
	});
	
	
	
	// PROFILE PHOTO JAVASCRIPT
	
	$('#editimageprofile').colorbox({
		width:"350px",
		height:"250px",
		inline: true,
		href:"#uploadprofilephoto",
		opacity:'0.4',
		top:"10%",
		returnFocus:true,
		onLoad:function(){
//			$('#cboxClose').remove();
		}
	});
	
	



	var intervalFunc = function () {	// update our custom span with the value of the default, hidden id_photo div
		$("#file-name").show();
	    $('#file-name').html($('#id_profile_pic').val());
	    $('#urlname').html($('#id_profile_pic').val());
	};


	$("#browsephoto").unbind("click").bind("click", function () {   // bind custom browse button to the default form
	   $("#id_profile_pic").click();
	   setInterval(intervalFunc, 1);
	   return false;
	});
	

	$('#id_profile_pic').change(function(){

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

		$("#previewImage").show();
		
		if (typeof FileReader !== "undefined"){
			img.src = window.URL.createObjectURL(file);
			$('#existingphoto').hide();
		} else {
	    	var reader = new FileReader();  
	    	reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(img);  
	    	reader.readAsDataURL(file);  
		}
		
		if (newfile.length > 0){	// check if new image or not
			$('#photo-clear_id').removeAttr("checked");    // override the default behavior of the ClearableInput field
		}

	  }

	}

/*
	$("#savephoto").unbind("click").bind("click", function () {   // bind custom browse button to the default form

		$('#uploadprofilephoto').colorbox.close();
	  	$("#editpicturesubmit").trigger('click');
	   	setInterval(intervalFunc, 1);
	   	return false;
	});

*/


	$("#deletephotobutton").click(function(){
		$('#profile_pic-clear_id').trigger('click'); // check the Django ClearableInput checkbox to remove the file
		
		$("#existingphoto").hide(); // hide the current photo
		
		$(this).hide(); // hide the X button
		
		$("#file-name").text("No image currently selected.");	// hide the filename
	});


	$("#photocancel").click(function(){	 // reset all properties -- this is ideal but couldn't get the functionality right
				
//		$("#id_profile_pic").replaceWith($("#id_profile_pic").clone(true));	// since we can't edit the form instance, we create a new one		
		$('#uploadprofilephoto').colorbox.close(); // close colorbox
	});
	
	/*
	
	$(document).bind('cbox_closed', function() {
		$('#existingphoto').show(); 			// show existing photo and delete button
		$('#deletephotobutton').show();
	});
	
	
	$(document).bind('cbox_cleanup', function(){
		$("#file-name").hide(); // remove the preview image and value
		$("#previewImage").hide();
	//	$("#id_profile_pic").replaceWith("<input type='file' id='id_profile_pic' />");	// since we can't edit the form instance, we create a new one
		$("#id_profile_pic").reset();
	});
	
*/



	

	
}); 