$(document).ready(function(){
    
    $('#test_btn').click(function() {
        $('.lesson_div').each(function(i) {
            console.log(i + ':' + $(this).find('input[name$="-name"]').attr('name'));  
        });
    });

    // complete lesson
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
    
}); 
