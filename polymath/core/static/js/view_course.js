head.ready(function(){


$(document).ready(function(){
	
	var lessonheight = $('.lessonsBlock').height();
	
	$('.lessonspine.loggedin').css("height",lessonheight-10);
	
	if (lessons > 2){
		$('.lessonspine.loggedout').css("height",lessonheight);		
	} else {
		$('.lessonspine.loggedout').css("height", lessonheight-60);
	}
	

	
	$('.thatsit').css("margin-top", lessonheight-52);
	$('.endcircle').css("margin-top", lessonheight-20);
	
    $('.addcomment textarea').addClass('commentbox');

    // don't submit the post comment form if the comment box is blank
    $('.comment_form').submit(function() {
        if ( $.trim( $(this).find('.commentbox').val() ) == "" ) {
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
					

				 	lesson_id = $(this).closest('.lessonmetablock').find('.lesson_id').val();
					console.log(lesson_id);
			        is_up = $(this).attr('rel');
			        vote_status_span = $(this).closest('.lessonmetablock').find('.vote_status');


					var donebutton = $(this);
					var otherbutton = $(this).siblings(".done");
					var currentscore = parseInt(donebutton.closest('.border-callout').find('#scorecounthidden').text());
				
					var newscore;
					
					if (donebutton.is(".done")){ // if a button is already selected
						if ( is_up == 0 ){
								is_up = 1;
							} else {
								is_up = 0;
						}
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
											newscore = currentscore + 1;
											donebutton.attr('original-title', 'You liked this');
											otherbutton.attr('original-title', 'Didn\'t like this?');
										} else {
											// increment the vote count
											newscore = currentscore - 1;
											donebutton.attr('original-title', 'You didn\'t like this');
											otherbutton.attr('original-title', 'Liked this?');
										}

										donebutton.closest('.lessonmetablock').find('#scorecounthidden').text( newscore );	
										if ( newscore == 1){
											donebutton.closest('.lessonmetablock').find('.score').text( newscore  + ' like');
										} else {
											donebutton.closest('.lessonmetablock').find('.score').text( newscore  + ' likes');
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
								if(otherbutton.is(".done")){
									otherbutton.removeClass("done");
									donebutton.removeClass("done");
								} else {
									donebutton.addClass("done");
									otherbutton.removeClass("done");
								}

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
								
								donebutton.closest('.lessonmetablock').find('#scorecounthidden').text( newscore );	
								if ( newscore == 1){
									donebutton.closest('.lessonmetablock').find('.score').text( newscore  + ' like');
								} else {
									donebutton.closest('.lessonmetablock').find('.score').text( newscore  + ' likes');
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
	
	$('.donethis').click(function(){ // when the done button is clicked...
		
		var checkbox = $(this);
		
		if ( $(this).hasClass('done')){ // don't do anything if it's already done
			
		
		} else {
			
			if (isLoggedIn){
	
	
				var val = $("#progressbar").progressbar("option", "value"); // set current value of progress bar


				lesson_id = $(this).closest('.lessonBlock').find('.lesson_id').val();
	        		$.post(
	            		from_server['complete_lesson_url'],
	            		{ lesson_id: lesson_id },
	            		function(response) {
	                		if( response['complete_successful'] ) {
								checkbox.toggleClass("done"); // mark the checkbox as done
								$("#numbercompleted").text(+($("#numbercompleted").text()) + 1); // increment the number of completed lessons
								checkbox.closest('.lessonBlock').toggleClass("completedBlock");
								checkbox.closest('.lessonBlock').find('.numberdone').text(+(checkbox.closest('.lessonBlock').find('.numberdone').text()) + 1);
								checkbox.attr('original-title', 'You\'ve done this!');
								var pGress = setInterval(function() { // loop to animate progress bar action
						        	var pVal = $('#progressbar').progressbar('option', 'value');
						        	var pCnt = !isNaN(pVal) ? (pVal + 1) : (completed_lessons/lessons) *100;
						        	if (pCnt > val + (100/lessons) + 1) { //animate progress bar to number of currently completed lesson
						            	clearInterval(pGress);
						        	} else {
						            	$('#progressbar').progressbar({value: pCnt});
						        	}
						    	}, 10);
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
	
	
	
		$('.savethis').click(function(){ // when the done button is clicked...

			var savebutton = $(this);

			if ( $(this).hasClass('done')){ // don't do anything if it's already done


			} else {

				if (isLoggedIn){
					lesson_id = $(this).closest('.lessonBlock').find('.lesson_id').val();
		        		$.post(
		            		from_server['save_lesson_url'],
		            		{ lesson_id: lesson_id },
		            		function(response) {
		                		if( response['save_successful'] ) {
									savebutton.toggleClass("done"); // change the class of the saved button to done
									savebutton.find('span').text("Saved");
									savebutton.attr('original-title', 'You\'ve saved this!');
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
	$('.donethis').tipsy({fade: false, gravity: 's', offset: 2, opacity:0.8});
	
	$('.savethis').tipsy({fade: false, gravity: 's', offset: 2, opacity:0.8});

	$('.donethis.done').tipsy({fade: false, gravity: 's', opacity:0.8});
	
	$('.donecount').tipsy({fade: false, gravity: 's', offset: 7, opacity:0.8});
	
	$('.vote_link').tipsy({fade: false, gravity: 's', opacity:0.8, offset:0});
	
	$('.completed').tipsy({fade: false, gravity: 's', opacity:0.8});
	
	$('.takingimage').tipsy({fade: false, gravity: 's', opacity:0.8});
	
	$('.lessoncount').tipsy({fade: false, gravity: 's', opacity:0.8});
	
	$('.followercount').tipsy({fade: false, gravity: 's', opacity:0.8});
	


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


	$('.score').click(function(){
		var relattr = $(this).closest(".lessonmetablock").find(".lessonmetaname").text(); 
		var url = ".usersliked[rel=" + relattr + "]";
		
		$(".score").colorbox({
				width:"500px",
				height:"350px",
				inline: true,
				href:url,
				opacity:'0.6',
				top:"10%",
				returnFocus:false,
		}); 
	});

	
	var stickyHeaderTop = $('#leftinfoblock').offset().top;

	 $(window).scroll(function(){
//		if( $(window).scrollTop() > stickyHeaderTop - 30) {
//			$('#leftinfoblock').css({position: 'fixed', top: '30px'});
//		} else {
//			$('#leftinfoblock').css({position: 'static', top: '30px'});
//		}
	});

	

	
    
}); 


});