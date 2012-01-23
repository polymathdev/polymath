$(document).ready(function(){
	
		
		$('.submit-post').click( function(){
			if ($('#id_comment').val().length == 0) {
			  return false;
			
			}
		});
	
	var remainderLessons = lessons - 2;
	
	if (remainderLessons <= 0){
		$('#loginmore').hide();
		$('#loginmore').parent().hide();
		
	} else if (remainderLessons == 1){
		$('#loginmore').text('Log in to see ' + remainderLessons + ' more lesson');
	} else {
		$('#loginmore').text('Log in to see ' + remainderLessons + ' more lessons');
	}

	
	console.log('completed lessons: %s and the user is %s', completed_lessons, isLoggedIn);
	
		$('.vote_link').click(function() {

			if (isLoggedIn){

				 	lesson_id = $(this).closest('.lessonBlock').find('.lesson_id').val();
			        is_up = $(this).attr('rel');
			        vote_status_span = $(this).closest('.lessonBlock').find('.vote_status');


					var donebutton = $(this);
					var otherbutton = $(this).siblings(".done");
					var currentscore = parseInt(donebutton.closest('.lessonBlock').find('#scorecounthidden').text());
					var newscore;
					
					if (donebutton.is(".done")){
						 is_up = !(is_up);
						 $.post(
				                from_server['vote_lesson_url'],
				                {
				                lesson_id: lesson_id,
				                is_up: is_up
				                },
				                function(response) {
				                if( response['vote_successful'] ) {
									donebutton.removeClass("done");
				                    vote_status_span.html('Vote = ' + response['vote_result']);
									if (is_up == 1){
										// decrement the vote count
										newscore = currentscore - 1;
										donebutton.attr('original-title', 'You liked this');
										otherbutton.attr('original-title', 'Didn\'t like this?');
									} else {
										// increment the vote count
										newscore = currentscore + 1;
										donebutton.attr('original-title', 'You didn\'t like this');
										otherbutton.attr('original-title', 'Liked this?');
									}

									donebutton.closest('.lessonBlock').find('#scorecounthidden').text( newscore );	
									if ( newscore == 1){
										donebutton.closest('.lessonBlock').find('#score').text( newscore  + ' like');
									} else {
										donebutton.closest('.lessonBlock').find('#score').text( newscore  + ' likes');
									}

				               }
				            }
				       	);
					} else {
					

			            $.post(
			                from_server['vote_lesson_url'],
			                {
			                lesson_id: lesson_id,
			                is_up: is_up
			                },
			                function(response) {
			                if( response['vote_successful'] ) {
								donebutton.addClass("done");
								otherbutton.removeClass("done");
			                    vote_status_span.html('Vote = ' + response['vote_result']);
								if (is_up == 1){
									// increment the vote count
									newscore = currentscore + 1;
									donebutton.attr('original-title', 'You liked this');
									otherbutton.attr('original-title', 'Didn\'t like this?');
								} else {
									// decrement the vote count
									newscore = currentscore - 1;
									donebutton.attr('original-title', 'You didn\'t like this');
									otherbutton.attr('original-title', 'Liked this?');
								}
								
								donebutton.closest('.lessonBlock').find('#scorecounthidden').text( newscore );	
								if ( newscore == 1){
									donebutton.closest('.lessonBlock').find('#score').text( newscore  + ' like');
								} else {
									donebutton.closest('.lessonBlock').find('#score').text( newscore  + ' likes');
								}
								
			               }
			            }
			       	);
			}

			} else { //if not logged in
				$.colorbox({
					width:"500px",
					height:"350px",
					inline: true,
					href:"#logindivnewcourse",
					opacity:'0.6',
					top:"10%",
					returnFocus:false,
				});
			}

	    });
	
        
	// set the current value of the progress bar
	$('#progressbar').progressbar({
		value: (completed_lessons/lessons) *100			
	});
	
	////
	
	$('.checkb').click(function(){ // when the done button is clicked...
		
		var checkbox = $(this);
		
		if ( $(this).hasClass('done')){ // don't do anything if it's already done
		
		} else {
			
			if (isLoggedIn){
			
				$(this).toggleClass("done"); // mark the checkbox as done
	
				var val = $("#progressbar").progressbar("option", "value"); // set current value of progress bar
		
				var pGress = setInterval(function() { // loop to animate progress bar action
		        	var pVal = $('#progressbar').progressbar('option', 'value');
		        	var pCnt = !isNaN(pVal) ? (pVal + 1) : (completed_lessons/lessons) *100;
		        	if (pCnt > val + (100/lessons) + 1) { //animate progress bar to number of currently completed lesson
		            	clearInterval(pGress);
		        	} else {
		            	$('#progressbar').progressbar({value: pCnt});
		        	}
		    	}, 10);


				lesson_id = $(this).closest('.lessonBlock').find('.lesson_id').val();
	        		$.post(
	            		from_server['complete_lesson_url'],
	            		{ lesson_id: lesson_id },
	            		function(response) {
	                		if( response['complete_successful'] ) {
								$("#numbercompleted").text(+($("#numbercompleted").text()) + 1); // increment the number of completed lessons
//								checkbox.closest('.lessonBlock').animate({backgroundPosition: '0px 0px'}, {duration: 1300});
								checkbox.closest('.lessonBlock').toggleClass("completedBlock");
								console.log("%s", checkbox);
	               			}
	            		}
	        		);
	
				} else {
						$.colorbox({
						width:"500px",
						height:"350px",
						inline: true,
						href:"#logindivnewcourse",
						opacity:'0.6',
						top:"10%",
						returnFocus:false,
					});
				}

			} // endif
			
		}); // end done animation
	
	
	
	
	
	///

    
    $('#test_btn').click(function() {
        $('.lesson_div').each(function(i) {
            console.log(i + ':' + $(this).find('input[name$="-name"]').attr('name'));  
        });
    });

    // remove lesson
    $('#lesson_list_ul').on('click', '.complete_lesson_lnk', function() {
        complete_spn = $(this).parent();
        lesson_id = $(this).closest('.lesson_li').find('.lesson_id').val();

        $.post(
            from_server['complete_lesson_url'],
            { lesson_id: lesson_id },
            function(response) {
                alert(response['result_message']);
                if( response['complete_successful'] ) {
                    complete_spn.css('color','green');
                    complete_spn.html(' You\'ve done this ');
                }
            }
        );

    });

	// lesson completed
    $('.complete_lesson_lnk').click(function() {
        complete_spn = $(this).parent();
        lesson_id = $(this).closest('.lessonBlock').find('.lesson_id').val();

        $.post(
            from_server['complete_lesson_url'],
            { lesson_id: lesson_id },
            function(response) {
                alert(response['result_message']);
                if( response['complete_successful'] ) {
                    complete_spn.css('color','green');
                    complete_spn.html(' You\'ve done this ');
                }
            }
        );


    });


	//toggle lessonBlock view
	$('.lessonBlock').mouseenter(function(){
		$(this).toggleClass("highlight");
	});
			
	$('.lessonBlock').mouseleave(function(){
		$(this).toggleClass("highlight");
	});

	//tooltips
	$('.checkb').tipsy({fade: false, gravity: 'se', opacity:0.8});

	$('.checkb.done').tipsy({fade: false, gravity: 'sw', opacity:0.8});

	$('.takecourse').tipsy({fade: false, gravity: 's', opacity:0.8});
	
	$('.votescore').tipsy({fade: false, gravity: 'se', opacity:0.8});

	$('.lessonname').tipsy({fade: false, gravity: 'w', opacity:0.8, offset:10});
	
	$('.vote_link').tipsy({fade: false, gravity: 's', opacity:0.8, offset:0});
	
		$('.completed').tipsy({fade: false, gravity: 's', opacity:0.8});


/*
  $('.vote_link').click(function() {
        lesson_id = $(this).closest('.lessonBlock').find('.lesson_id').val();
        is_up = $(this).attr('rel');
        vote_status_span = $(this).parent().find('.vote_status');
            $.post(
                from_server['vote_lesson_url'],
                {
                lesson_id: lesson_id,
                is_up: is_up
                },
                function(response) {
                if( response['vote_successful'] ) {
                    vote_status_span.html('Vote = ' + response['vote_result']);
               }
            }
       	);


    }); */



	$('.takecourse').click(function(){
		if(isLoggedIn){
			
		} else {
			$.colorbox({
				width:"500px",
				inline: true,
				href:"#logindivnewcourse",
				opacity:'0.6',
				top:"10%",
				returnFocus:false,
			});
			
		}
	});
	
	
/*	$('.embedclass').embedly({
        maxWidth: 450,
        wmode: 'transparent',
        method: 'after',
        key: '93c670123dda11e1927d4040d3dc5c07'
      });
*/

	var apiKey = 'QM09p1Gqmv1n';
	
	$('.embedclass a').each(function(){
	        // Grab the URL from our link
	        var url = encodeURIComponent( $(this).attr('href') ),
	

	        // Create image thumbnail using Websnapr thumbnail service
	        thumbnail = $('<img />').attr({
	            src: 'http://images.websnapr.com/?url=' + url + '&key=' + apiKey + '&hash=' + encodeURIComponent(websnapr_hash),
//				src: 'http://images.websnapr.com/?size=S' + '&key=' + apiKey + '&url=' + url,
	            alt: 'Loading thumbnail...',
	            width: 202,
	            height: 152
	        });

	        // Setup the tooltip with the content
	        $(this).qtip({
	          	content: thumbnail,
	
	            position: {
	                corner: {
	                    tooltip: 'leftMiddle',
	                    target: 'leftMiddle'
	                }
	            },
	            style: {
	                tip: false, // Give it a speech bubble tip with automatic corner detection
	                name: 'light'
	            }, 
				show: { ready: true },
	        });
	});
	
	
	
	
	
	
	$('.votescore').click(function(){
	//	$(this).hide();
		$(this).closest('.lessonBlock').find('.thumbsbuttons').show();
	});
	
	
	
	
	$('#seemorecourses').colorbox({
		width:"500px",
		height:"350px",
		inline: true,
		href:"#logindivnewcourse",
		opacity:'0.6',
		top:"10%",
		returnFocus:false,
	});
	
	
    
}); 


