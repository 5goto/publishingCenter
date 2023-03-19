

$('#in_button').on('click', function (event) {
    event.preventDefault();
    console.log("Prevent submit")

    const start = document.querySelector('#start_id').value
    const end = document.querySelector('#end_id').value

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
                        content += '<tr><td colspan="4">' + `Суммарная прибыль от заказчика:` + '</td><td>' + `${sum}` + '</td></tr>'
                        // console.log(arrName)
                        // console.log(item[arrName])
                    }
                }
                content += "</table>";
                $placeForData.append(content);
            } else {
                content = '<h1 class="warning_message">' + 'Прибыль за указанный период отсутствует' + '</h1>'
                $placeForData.append(content);
            }
        })

})
