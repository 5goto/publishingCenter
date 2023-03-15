


// Панель администрирования
$('.icon-roll-add').click(function() {
    var $body = $(this).closest('.module').find('.body');
    console.log($body);
    if ($body.is(':hidden')) {
        $body.show();
    } else {
        $body.hide();
    }
    });


$('.icon-roll-remove').click(function() {
    var $body = $(this).closest('.module').find('.body');
    console.log($body);
    if ($body.is(':hidden')) {
        $body.show();
    } else {
        $body.hide();
    }
    });

// Выделение строк в таблице
$(document).ready(function(){
	$table_td = $('.table tr')
	$table_td.hover(function(){
		$(this).addClass('hover');
	}, function() {
		$(this).removeClass('hover');
	});

	$table_td.click(function(){
		$('.table tr').removeClass('active');
		$(this).addClass('active');

		const target = $.makeArray(document.querySelectorAll("tr.active td"));

        $("input[name=id]").attr("value", $.trim(target[0].textContent))

        $("input[name=number]").attr("value", $.trim(target[1].textContent))
        $("input[name=reg-date]").attr("value", $.trim(target[2].textContent))
        $("input[name=finish-date]").attr("value", $.trim(target[3].textContent))
        $("input[name=quantity]").attr("value", $.trim(target[4].textContent))
        $("input[name=cust-id]").attr("value", $.trim(target[5].textContent))
        $("input[name=book-id]").attr("value", $.trim(target[6].textContent))

	});
});

// Валидация ссылок по текущему пользователю
$.getJSON("/books?user=true", "", (data) => {
    if(data.user === "representative") {
        $('.representative').removeClass("disabled");
        $('.admin-panel').css("display", "none");
    } else if(data.user === "manager") {
        $('.manager').removeClass("disabled");

    }
    else {
        $('.menu-link').removeClass("disabled");
    }
})

$('input[name=number]').on('input', function (event) {
    if(/^[1-9]{1}[0-9]{4}$/i.test(event.target.value)  && Number(event.target.value) !== 0) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Число [xxxxx]');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=reg-date]').on('input', function (event) {
    if(/^\d{4}-{1}\d{2}-{1}\d{2}$/.test(event.target.value)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Фомрат {YYYY-MM-DD}');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=finish-date]').on('input', function (event) {
    if(/^\d{4}-{1}\d{2}-{1}\d{2}$/.test(event.target.value)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Фомрат {YYYY-MM-DD}');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=quantity]').on('input', function (event) {
    if(/^[0-9]+$/i.test(event.target.value) && Number(event.target.value) >= 50 && Number(event.target.value) <= 10000) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Число [50-10000]');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=cust-id]').on('input', function (event) {
    if(/^[0-9]+$/i.test(event.target.value)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Целое число');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=book-id]').on('input', function (event) {
    if(/^[0-9]+$/i.test(event.target.value)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Целое число');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

