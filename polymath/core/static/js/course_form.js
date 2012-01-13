$(document).ready(function(){
	
	
	$('#id_tags').placeHolder({
		"text":"Enter tags, separated by a comma"
	});
    
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
	});
	
	
	$('.lessonlink').tipsy({fade: false, gravity: 'e', opacity:0.6});
	

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

    $('#new_course_form').submit(function() {
        $('#new_course_form :submit').attr('disabled','true');
        reorder_lessons()
    });



	$('#editimage').click(function(){
		$('#photouploaddiv').toggle();
	});
	
	$('#sim_save_course').click(function(){
		$('#save_course').trigger('click');
	});
	
	$('#sim_add_lesson_btn').click(function(){
		$('#add_lesson_btn').trigger('click');
	});
	
	

}); 


