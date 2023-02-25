


$('.icon-roll').click(function() {
    var $body = $(this).closest('.module').find('.body');

    if ($body.is(':hidden')) {
        $body.show();
    } else {
        $body.hide();
    }
    });
