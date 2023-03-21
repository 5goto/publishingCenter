
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

$('#in_button').on('click', function (event) {
    event.preventDefault();
    console.log("Prevent submit")

    const start = document.querySelector('#start_id').value
    const end = document.querySelector('#end_id').value
    if (!start || !end) {
        return
    }
    const data_to_send = JSON.stringify({
        start,
        end
    })
    "/year_result?operation=result"

    fetch("/year_result?operation=result", {
        method: 'POST',
        body: data_to_send
    })
        .then(res => res.json())
        .then(data => {
            $placeForData = $('#result');
            $placeForData.empty()

            objWithData = data['data']

            if(objWithData.length !== 0) {

                let content = "<table class=\"table\">"
                content += '<tr><th>Название книги</th><th>Себестоимость</th><th>Цена продажи</th><th>Количество экземпляров</th><th>Прибыль от продажи</th></tr>'
                let full_sum = 0;
                for (const item of objWithData) {
                    for (const arrName in item) {
                        content += '<tr><td colspan="5">' + `Заказчик: ${arrName}` + '</td></tr>'
                        let sum = 0
                        for (const row of item[arrName]) {
                            content += '<tr>';
                            for (const index of row) {
                                content += '<td>' + `${index}` + '</td>'
                            }
                            sum += Number(row[4])
                            content += '</tr>';
                        }
                        full_sum += sum;
                        content += '<tr><td colspan="4">' + `Суммарная прибыль от заказчика:` + '</td><td>' + `${sum}` + '</td></tr>'
                        // console.log(arrName)
                        // console.log(item[arrName])
                    }
                }
                content += '<tr><td colspan="4">' + `Суммарная прибыль за указанный период:` + '</td><td>' + `${full_sum}` + '</td></tr>'
                content += "</table>";
                $placeForData.append(content);
            } else {
                content = '<h1 class="warning_message">' + 'Прибыль за указанный период отсутствует' + '</h1>'
                $placeForData.append(content);
            }
        })

})
