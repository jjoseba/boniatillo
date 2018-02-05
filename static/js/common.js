$(function(){

    var menu = $('#navbar-menu');

    $('[data-toggle="tooltip"]').tooltip();

    $(".link-row").click(function() {
        window.location = $(this).data("href");
    });

    $('.gallery-form').on('submit', function(event ){
        var order = 0;

        $('.gallery-form-photo').each(function(){
            var $question = $(this);
            $question.find('input[id$="order"]').val(order);
            order++;
        });
    });

     $(".gallery-form").on('change', '.form-photo input[type="file"]', function(){
        var input = this;
        var target = $(input).siblings('.thumb');
        var imgTarget = $(input).parents('.file-field').attr('data-img-target');
        if (imgTarget){
            target = $(imgTarget);
        }
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                if (imgTarget){
                    target.attr('src', e.target.result);
                }
                else{
                    target.css('background-image', 'url(' + e.target.result + ')');
                    target.parent().addClass('uploaded');
                }
            }
            reader.readAsDataURL(input.files[0]);
        }
    });

    $('.btn-fab-photo').on('click', function(e){
        $(this).parents('.form-photo').find('input[type="file"]').click();
    })

    $('.popup-gallery').magnificPopup({
		delegate: 'a',
		type: 'image',
		mainClass: 'mfp-img-mobile',
		gallery: {
			enabled: true,
			navigateByImgClick: true,
			preload: [0,1] // Will preload 0 - before current, and 1 after the current image
		}
	});


});
