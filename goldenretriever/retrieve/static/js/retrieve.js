$(document).ready(function() {
    $('#inpterror').html('').hide();
    $('#loader').hide();

    $('#retrbttn').click(function(e) {
        e.preventDefault();

        /* Clearing previous state before retrieving
           new data. */
        $('#titleretr').html('');
        $('#imgretr').attr('src', '').hide();
        $('#inpterror').html('').hide();

        var baseUrl = '/retrieve/?url='
        var siteurl = baseUrl + $('#url_input').val();

        if (siteurl == baseUrl) {
            /* Happens when text input field is empty. */
            $('#inpterror').html('Enter a valid URL').show();
            return
        }
        
        $('#loader').show();

        $.ajax({
            success: function(data) {
            	$('#loader').hide();
                if (data.error == 'true') {
                    $('#inpterror').html(data.msg).show();	
                }

                else {
                    /* Updates fields with information inside the
                       returned JSON. */
                    $('#imgretr').attr('src', data.imgsrc).show();
                    $('#titleretr').html(data.title);
                }
            },
            error: function(data) {
            	$('#loader').hide();
                $('#inpterror').html('An error occurred').show();	
            },
            url: siteurl
        });
    });
});

