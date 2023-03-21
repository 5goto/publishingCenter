

// Панель администрирования
$('.icon-roll-add').click(function() {
    var $body = $(this).closest('.module').find('.body');
    if ($body.is(':hidden')) {
        $body.show();
    } else {
        $body.hide();
    }
    });


$('.icon-roll-remove').click(function() {
    var $body = $(this).closest('.module').find('.body');
    if ($body.is(':hidden')) {
        $body.show();
    } else {
        $body.hide();
    }
    });

var rendered = false;

$('.icon-roll-add-dell').click(function() {
    var $body = $(this).closest('.module').find('.body');
    if ($body.is(':hidden')) {
        $body.show();
        if (!rendered) {
            renderAuthorsTable();
            rendered = true;
        }
    } else {
        $body.hide();
        $("#authors").empty();
        rendered = false;
    }
    });

// Выделение строк в таблице

function formatMoneyStr(str) {
    const removeSpaces = (str) => str.replace(/\s+/g, '');
    return removeSpaces(str.slice(0, str.indexOf(',')));
}
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

        $("#book-id").attr("value", $.trim(target[0].textContent))

        $("#add-book-isbn").attr("value", $.trim(target[1].textContent))
        $("#add-book-title").attr("value", $.trim(target[2].textContent))
        $("#add-book-copy").attr("value", $.trim(target[3].textContent))
        $("#add-book-date_pub").attr("value", $.trim(target[4].textContent))
        $("#add-book-cost").attr("value", formatMoneyStr($.trim(target[5].textContent)))
        $("#add-book-price").attr("value", formatMoneyStr($.trim(target[6].textContent)))
        $("#add-book-fee").attr("value", formatMoneyStr($.trim(target[7].textContent)))

        $("#update-book-id").attr("value", $.trim(target[0].textContent))
        $("#update-book-isbn").attr("value", $.trim(target[1].textContent))
        $("#update-book-title").attr("value", $.trim(target[2].textContent))
        $("#update-book-copy").attr("value", $.trim(target[3].textContent))
        $("#update-book-date_pub").attr("value", $.trim(target[4].textContent))
        $("#update-book-cost").attr("value", formatMoneyStr($.trim(target[5].textContent)))
        $("#update-book-price").attr("value", formatMoneyStr($.trim(target[6].textContent)))
        $("#update-book-fee").attr("value", formatMoneyStr($.trim(target[7].textContent)))

        $("#book-id-autor").attr("value", $.trim(target[0].textContent))
        $("#book-id-autor-remove").attr("value", $.trim(target[0].textContent))


	});
});


// Валидация ссылок по текущему пользователю
$.getJSON("/books?user=true", "", (data) => {
    if(data.user === "representative") {
        $('.representative').removeClass("disabled");
    } else if(data.user === "manager") {
        $('.manager').removeClass("disabled");
        $('.admin-panel').css("display", "none")
    }
    else {
        $('.menu-link').removeClass("disabled");
    }
})

function renderAuthorsTable() {
    $.getJSON("/books?authors=true", "", (data) => {
    const currentData = JSON.parse(data.authors)

    let content = "<table class=\"table\">"
        content += '<tr><th>#</th><th>Серия паспорта</th><th>Номер паспорта</th><th>Фамилия</th><th>Имя</th><th>Отчество</th><th>Адрес</th><th>Номер телефона</th> <th>ID контракта</th> </tr>'
    for(item of currentData){
        content += '<tr>';
        for(row of item) {
            content += '<td>' + `${row}` + '</td>'
        }
        content += '</tr>';
    }
    content += "</table>";
        console.log(content);
$('#authors').append(content);
})
}

// Валидация корректности формы

$('#book-id').on('input', function (event) {
    if(/^[0-9]+$/i.test(event.target.value)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Только целые числа');
        $('.remove-books-form input[type=submit]').event.preventDefault();
    }
});

$('#autor-id-remove').on('input', function (event) {
    if(/^[0-9]+$/i.test(event.target.value)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Только целые числа');
        $('.add-autor-form input[type=submit]').event.preventDefault();
    }
});


$('#autor-id').on('input', function (event) {
    if(/^[0-9]+$/i.test(event.target.value)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Только целые числа');
        $('.add-autor-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=book-fee]').on('input', function (event) {
    if(/^[0-9]+$/i.test(event.target.value)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Только целые числа');
        $('.add-autor-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=book-isbn]').on('input', function (event) {
    if(/^\d{3}-{1}\d{1}-{1}\d{2}-{1}\d{6}-{1}\d{1}$/.test(event.target.value)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('xxx-x-xx-xxxxxx-x');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=book-title]').on('input', function (event) {
    if(event.target.value.length <= 500) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Строка - латиница и кириллица');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=book-copy]').on('input', function (event) {
    if((/^[0-9]+$/i.test(event.target.value)) && (Number(event.target.value) >= 100) && (Number(event.target.value) <= 10000)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Число [100;10000]');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=book-date_pub]').on('input', function (event) {
    if(/^\d{4}-{1}\d{2}-{1}\d{2}$/.test(event.target.value)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Фомрат {YYYY-MM-DD}');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=book-cost]').on('input', function (event) {
    if((/^[0-9]+$/i.test(event.target.value)) && (Number(event.target.value) >= 50) && (Number(event.target.value) <= 1000)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Число [50;1000]');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=book-price]').on('input', function (event) {
    if((/^[0-9]+$/i.test(event.target.value)) && (Number(event.target.value) >= 100) && (Number(event.target.value) <= 10000)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Число [100;10000]');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});

$('input[name=autor]').on('input', function (event) {
    if(/^[0-9]+$/i.test(event.target.value)) {
        event.target.setCustomValidity('');
    } else {
        event.target.setCustomValidity('Целое число');
        $('.books-form input[type=submit]').event.preventDefault();
    }
});


