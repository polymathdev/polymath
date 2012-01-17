$(document).ready(function(){
	
	console.log('completed lessons: %s and the user is %s', completed_lessons, isLoggedIn);
	
	$('.vote_link').click(function() {
		
		if (isLoggedIn){
			
			if( $(this).closest('.lessonBlock').hasClass('.done') ){
			
			 lesson_id = $(this).closest('.lessonBlock').find('.lesson_id').val();
		        is_up = $(this).attr('rel');
		        vote_status_span = $(this).closest('.lessonBlock').find('.vote_status');

				var donebutton = $(this);
				var otherbutton = $(this).siblings(".done");

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
							alert('got it!');
		                    vote_status_span.html('Vote = ' + response['vote_result']);
		               }
		            }
		       	);
			} else {
				alert("Complete the lesson first!");
			}
		
		} else {
			alert("You have to log in first, fool!");
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
					alert("You gotta log in, fool!");
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
	$('.checkb').tipsy({fade: false, gravity: 's', opacity:0.6});

	$('.checkb.done').tipsy({fade: false, gravity: 's', opacity:0.6});

	$('.takecourse').tipsy({fade: false, gravity: 's', opacity:0.6});

	$('.lessonname').tipsy({fade: false, gravity: 'w', opacity:0.6, offset:10});
	
	$('.vote_link').tipsy({fade: false, gravity: 's', opacity:0.6, offset:0});



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


    });



	$('.takecourse').click(function(){
		if(isLoggedIn){
			
		} else {
			alert("Log in first!");
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
	
    
}); 
