calendarLocale = {
    "format": "DD/MM/YYYY",
    "weekLabel": "W",
    "daysOfWeek": [
        "Dom",
        "Lun",
        "Mar",
        "Mié",
        "Jue",
        "Vie",
        "Sáb"
    ],
    "monthNames": [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre"
    ],
     "firstDay": 1
};
var TOAST_DELAY = 1200;


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

(function( $ ) {
    function loadResults(resultsContainer, url, keepUrl){
        if (url == null || url == '' || url.startsWith('#')){
            return;
        }
        resultsContainer.addClass('loading-container');
        $.get(url, {}, function(data){
            resultsContainer.find('.results').html(data);
            resultsContainer.find('[data-toggle="tooltip"]').tooltip();
            resultsContainer.find(".link-row").click(function() {
                window.location = $(this).data("href");
            });
            resultsContainer.removeClass('loading-container');
            if (!keepUrl){
                var preserveHistory = resultsContainer.attr('data-preservehistory');
                if (!preserveHistory || preserveHistory != 'true')
                    window.history.replaceState({}, '', url);
            }

        });
    }

    $.fn.ajaxLoader = function( url_or_action ) {
        var self = this;
        var initialUrl = self.attr('data-initial');
        var keepUrl = (self.attr('data-keepurl') != null) && (self.attr('data-keepurl')!='');
        
        if ( url_or_action != null) {

            if (url_or_action === 'reload'){
                var current = self.find('.pagination .page-item.active > a').attr('href');
                loadResults(self, current, keepUrl);
                return self;
            }

            loadResults(self, url);
            return self;
        }

        if ((initialUrl != null) && (initialUrl!='')){
            loadResults(self, initialUrl, keepUrl);
        }

        self.on('click', '.pagination a', function(e){
            e.preventDefault();
            if ($(this).parent().hasClass('active'))
                return;
            var url = $(this).attr('href')
            loadResults(self, url, keepUrl);
        });

    };

}( jQuery ));

function showToast(message, messageClasses){
    var toast = $('<div class="toast"></div>').text(message).addClass(messageClasses);
    toast.appendTo('#main-toasts');
    setTimeout(function(){ toast.fadeOut(); }, TOAST_DELAY);
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
            var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(function(){
    var menu = $('#navbar-menu');

    $('[data-toggle="tooltip"]').tooltip();
    $('.modal.show-on-load').modal();
    $('.ajax-load').ajaxLoader();

    $(".link-row").click(function() {
        window.location = $(this).data("href");
    });

    $('.tag-select').each(function(){
        var select = $(this).find('select').addClass('form-control');
        $(this).find('.tags_declaration > li').each(function(){
            var tag = $(this);
            select.find('option[value="' + tag.attr('data-pk') + '"]').attr('data-color', tag.attr('data-color'));
        })

        select.select2({
            dropdownAutoWidth: true,
            templateResult: function formatSelect(tag){
                var selected = select.find('option[value="' + tag.id + '"]')
                var color = selected.attr('data-color');
                if (color){
                    return $('<span class="tag-bulleted"></span>').text(tag.text).prepend($('<span></span>').css('background-color', color));
                }

                var image = selected.attr('data-image');
                if (image){
                    return $('<span class="tag-image"></span>').text(tag.text).prepend($('<div class="profile-circle"><img src="'+image+'"></div>').css('background-color', color));
                }
            },
            templateSelection: function formatTag(tag){
                var color = select.find('option[value="' + tag.id + '"]').attr('data-color');
                if (color)
                    return $('<span class="tag-selected"></span>').text(tag.text).css('background-color', color);
                else return tag.text;
            }
        }).css('width', '100%;');
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

	$(".image-field").each(function(){
        var field = $(this);
        var target = field.attr('data-ref');
        var type = field.attr('data-ref-type');
        field.find('input').on('change', function(){
            var input = this;
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    if (type == 'image'){
                        $(target).attr('src', e.target.result);
                    }
                    else{
                        $(target).css('background-image', 'url(' + e.target.result + ')');
                    }
                }
                reader.readAsDataURL(input.files[0]);
            }
        });
    });

    var toastCounter = 1;
    $($('.toast-messages .toast').get().reverse()).each(function(){
        var message = $(this);
        setTimeout(function(){ message.fadeOut(); }, TOAST_DELAY * toastCounter);
        toastCounter++;
    });

});
