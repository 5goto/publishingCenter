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

        $("#contract-id-delete").attr("value", $.trim(target[0].textContent))


        $("#add-contract-num").attr("value", $.trim(target[1].textContent));
        $("#add-date_start").attr("value", $.trim(target[2].textContent));
        $("#add-validity").attr("value", $.trim(target[3].textContent));
        // $.trim(target[4].textContent) === 'True' ?
        //     $("#add-contract_resolved").prop('checked', true) :
        //     $("#add-contract_unresolved").prop('checked', true);
        // $("#add-date_of_completion").attr("value", $.trim(target[5].textContent));

        $("#update-contract-id").attr("value", $.trim(target[0].textContent));
        $("#update-contract-num").attr("value", $.trim(target[1].textContent));
        $("#update-date_start").attr("value", $.trim(target[2].textContent));
        $("#update-validity").attr("value", $.trim(target[3].textContent));
        // $.trim(target[4].textContent) === 'True' ?
        //     $("#update-contract_resolved").prop('checked', true) :
        //     $("#update-contract_unresolved").prop('checked', true);
        $("#update-date_of_completion").attr("value", $.trim(target[5].textContent));
	});
});

// Валидация ссылок по текущему пользователю
$.getJSON("/contracts?user=true", "", (data) => {
    if(data.user === "representative") {
        $('.representative').removeClass("disabled");
    } else if(data.user === "manager") {
        $('.manager').removeClass("disabled");

    }
    else {
        $('.menu-link').removeClass("disabled");
    }
})

$('input[name=contract-num]').on('input', function (event) {
    if(/^[1-9]{1}[0-9]{4}$/i.test(event.target.value) && Number(event.target.value) !== 0) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Число [xxxxx]');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=date_start]').on('input', function (event) {
    if(/^\d{4}-{1}\d{2}-{1}\d{2}$/.test(event.target.value)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Фомрат {YYYY-MM-DD}');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=validity]').on('input', function (event) {
    if(/^[1-9]{1}$/i.test(event.target.value) && (Number(event.target.value) <= 5)  && Number(event.target.value) !== 0) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Число 1-5');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=date_of_completion]').on('input', function (event) {
    if(/^\d{4}-{1}\d{2}-{1}\d{2}$/.test(event.target.value)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Фомрат {YYYY-MM-DD}');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=seria]').on('input', function (event) {
    if(/^[1-9]{1}[0-9]{3}$/i.test(event.target.value)  && Number(event.target.value) !== 0) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Число [xxxx]');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=number]').on('input', function (event) {
    if(/^[1-9]{1}[0-9]{5}$/i.test(event.target.value)  && Number(event.target.value) !== 0) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Число [xxxxxx]');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=lastname]').on('input', function (event) {
    if(/^[A-ZА-ЯЁ]+$/i.test(event.target.value) && event.target.value.length <= 64) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Строка (латиница и кириллица) до 64 символов');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=name]').on('input', function (event) {
    if(/^[A-ZА-ЯЁ]+$/i.test(event.target.value) && event.target.value.length <= 64) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Строка (латиница и кириллица) до 64 символов');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=patro]').on('input', function (event) {
    if((/^[A-ZА-ЯЁ]+$/i.test(event.target.value) && event.target.value.length <= 64) || event.target.value.length ===0) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Строка (латиница и кириллица) до 64 символов');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=address]').on('input', function (event) {
    if(event.target.value.length <= 64 && event.target.value.length >= 10) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Строка (латиница и кириллица) от 10 до 64 символов');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=phone]').on('input', function (event) {
    if(/^(\+?7|8)?9\d{9}$/.test(event.target.value)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Номер телефона 7|89[0-9]');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

