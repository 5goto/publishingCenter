
var rendered = false;
// Панель администрирования
$('.icon-roll-add').click(function() {
    var $body = $(this).closest('.module').find('.body');
    console.log($body);
    if ($body.is(':hidden')) {
        $body.show();
        if (!rendered) {
            renderBooksTable();
            renderCustomerTable();
            rendered = true;
        }
    } else {
        $body.hide();
        $("#books").empty();
        rendered = false;
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

        $("input[name=title]").attr("value", $.trim(target[1].textContent))
        $("input[name=lastname]").attr("value", $.trim(target[2].textContent))
        $("input[name=name]").attr("value", $.trim(target[3].textContent))
        $("input[name=patro]").attr("value", $.trim(target[4].textContent))
        $("input[name=address]").attr("value", $.trim(target[5].textContent))
        $("input[name=phone]").attr("value", $.trim(target[6].textContent))
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

function renderBooksTable() {
    $.getJSON("/orders?books=true", "", (data) => {
    const currentData = JSON.parse(data.books)

    let content = "<table class=\"table\">"
        content += '<tr><th>#</th><th>ISBN</th><th>Название</th><th>Количество копий</th><th>Дата публикации</th><th>Себестоимость</th><th>Цена продажи</th><th>Гонорар</th></tr>'
    for(item of currentData){
        content += '<tr>';
        for(row of item) {
            content += '<td>' + `${row}` + '</td>'
        }
        content += '</tr>';
    }
    content += "</table>";
$('#books').append(content);
})
}

$('input[name=title]').on('input', function (event) {
    if(/^[0-9A-ZА-ЯЁ]+$/i.test(event.target.value) && event.target.value.length <= 64) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Строка (латиница и кириллица) до 64 символов');
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
    if((/^[0-9A-ZА-ЯЁ\s]+$/i.test(event.target.value) && event.target.value.length <= 64) || event.target.value.length ===0) {
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

$('input[name=number]').on('input', function (event) {
    if(/^[1-9]{1}[0-9]{4}$/i.test(event.target.value)) {
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


$('input[name=book-id]').on('input', function (event) {
    if(/^[0-9]+$/i.test(event.target.value)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Целое число');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});
