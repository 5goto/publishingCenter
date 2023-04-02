import datetime

import sqlite3


def getAllBooks():
    sqlite_connection = sqlite3.connect("publishing.sqlite")
    try:
        cursor = sqlite_connection.cursor()

        cursor.execute('SELECT * FROM books')
        all_books = cursor.fetchall()

        cursor.close()
        return all_books
    except sqlite3.Error as error:
        print("Some error [getAllBooks]", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def getAllWriters():
    sqlite_connection = sqlite3.connect("publishing.sqlite")
    try:
        cursor = sqlite_connection.cursor()

        cursor.execute('SELECT * FROM writers')
        all_writers = cursor.fetchall()

        cursor.close()
        return all_writers
    except sqlite3.Error as error:
        print("Some error [getAllWriters]", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def getAllContracts():
    sqlite_connection = sqlite3.connect("publishing.sqlite")
    try:
        cursor = sqlite_connection.cursor()

        cursor.execute('SELECT * FROM contracts')
        all_contracts = cursor.fetchall()

        cursor.close()
        return all_contracts
    except sqlite3.Error as error:
        print("Some error [getAllContracts]", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def getAllCustomers():
    sqlite_connection = sqlite3.connect("publishing.sqlite")
    try:
        cursor = sqlite_connection.cursor()

        cursor.execute('SELECT * FROM customers')
        all_customers = cursor.fetchall()

        cursor.close()
        return all_customers
    except sqlite3.Error as error:
        print("Some error [getAllCustomers]", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def getAllOrders():
    sqlite_connection = sqlite3.connect("publishing.sqlite")
    try:
        cursor = sqlite_connection.cursor()

        cursor.execute('SELECT * FROM orders')
        all_orders = cursor.fetchall()

        cursor.close()
        return all_orders
    except sqlite3.Error as error:
        print("Some error [getAllOrders]", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def deleteBookById(id):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    cursor = sqlite_connection.cursor()

    cursor.execute(f"SELECT order_id FROM orders WHERE fk_book_id = {id};")
    ordersWithThatBookId = cursor.fetchall()
    for item in ordersWithThatBookId:
        deleteOrderById(item[0])

    cursor.execute(f"DELETE FROM books WHERE book_id = {id}")
    op_result = cursor.rowcount
    sqlite_connection.commit()

    cursor.close()
    sqlite_connection.close()

    if op_result != 0:
        return [u'success', u'Запись успешно удалена']
    else:
        return [u'error', u'Кандидат на удаление не найден']

def deleteCustomerById(id):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    cursor = sqlite_connection.cursor()
    cursor.execute(f"DELETE FROM orders WHERE fk_customer_id = {id};")
    cursor.execute(f"DELETE FROM customers WHERE customer_id = {id};")

    op_result = cursor.rowcount
    sqlite_connection.commit()

    cursor.close()
    sqlite_connection.close()
    if op_result != 0:
        return [u'success', u'Запись успешно удалена']
    else:
        return [u'error', u'Кандидат на удаление не найден']

def deleteOrderById(id):
    sqlite_connection = sqlite3.connect("publishing.sqlite")
    cursor = sqlite_connection.cursor()

    cursor.execute(f"SELECT fk_customer_id FROM orders WHERE order_id = {id};")
    fk_customer_id = cursor.fetchall()[0][0]

    cursor.execute(f"SELECT COUNT(order_id) FROM orders WHERE fk_customer_id = {fk_customer_id};")
    bindedOrders = cursor.fetchall()[0][0]

    op_result = 0
    if bindedOrders > 1:
        cursor.execute(f"DELETE FROM orders WHERE order_id = {id};")
        op_result = cursor.rowcount
    elif bindedOrders == 1:
        cursor.execute(f"DELETE FROM orders WHERE order_id = {id};")
        op_result = cursor.rowcount
        cursor.execute(f"DELETE FROM customers WHERE customer_id = {fk_customer_id};")
    sqlite_connection.commit()

    cursor.close()
    sqlite_connection.close()
    if op_result != 0:
        return [u'success', u'Запись успешно удалена']
    else:
        return [u'error', u'Кандидат на удаление не найден']


def deleteContractById(id):
    sqlite_connection = sqlite3.connect("publishing.sqlite")
    cursor = sqlite_connection.cursor()

    cursor.execute(f"DELETE FROM writers WHERE fk_contract_number = {id};")
    cursor.execute(f"DELETE FROM contracts WHERE contract_id = {id};")
    op_result = cursor.rowcount
    sqlite_connection.commit()

    cursor.close()
    sqlite_connection.close()
    if op_result != 0:
        return [u'success', u'Запись успешно удалена']
    else:
        return [u'error', u'Кандидат на удаление не найден']


def deleteWriterById(id):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    now = datetime.datetime.now()
    current_date = str(now).split(' ')[0]

    cursor = sqlite_connection.cursor()
    cursor.execute(f"SELECT fk_contract_number FROM writers WHERE writer_id = {id};")
    fk_contract_number = cursor.fetchall()[0][0]
    cursor.execute(f"DELETE FROM writers WHERE writer_id = {id};")
    op_result = cursor.rowcount
    cursor.execute(
        f"UPDATE contracts SET is_the_contract_terminated = true, "
        f"contract_termination_date = '{current_date}' WHERE contract_id = {fk_contract_number};")

    sqlite_connection.commit()

    cursor.close()
    sqlite_connection.close()

    if op_result != 0:
        return [u'success', u'Запись успешно удалена']
    else:
        return [u'error', u'Кандидат на удаление не найден']

######################Add###################################

def addBook(data):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    cursor = sqlite_connection.cursor()

    cursor.execute(f"SELECT COUNT(writer_id) FROM writers WHERE writer_id = {int(data['autor'])};")
    writersWithCurrentId = cursor.fetchall()[0][0]
    cursor.execute(f"SELECT COUNT(book_cipher) FROM books WHERE book_cipher = '{data['book-isbn']}';")
    excist_isbn = cursor.fetchall()[0][0]
    if excist_isbn:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'ISBN книги должен быть уникальным']

    if (writersWithCurrentId):
        fee = (int(data['book-price']) - int(data['book-cost'])) * int(data['book-copy'])
        if int(data['book-fee']) - fee > 0:
            return [u'error', u'Гонорар писателей не должен превышать суммарную прибыль от производства']

        try:
            cursor.execute(f'''INSERT INTO books (book_cipher, book_name, circulation, date_of_publication, cost_price, selling_price, fee)
             VALUES
              (%s, %s, %s, %s, %s, %s, %s)''', (
            data['book-isbn'], data['book-title'], int(data['book-copy']), data['book-date_pub'], int(data['book-cost']),
            int(data['book-price']), data['book-fee']))
        except sqlite3.Error:
            return [u'error', u'Указан неверный формат времени']

        cipher = data['book-isbn']
        cursor.execute(f"SELECT book_id FROM books WHERE book_cipher = '{cipher}';")
        id = cursor.fetchall()[0][0]

        cursor.execute(f"INSERT INTO wr_id_book_id (writer_id, book_id) VALUES (%s, %s)", (int(data['autor']), int(id)))
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        return [u'success', u'Запись успешно добавлена']
    else:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Писателя с указанным ID не существует']


def addWriter(data):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    cursor = sqlite_connection.cursor()

    cursor.execute(f"SELECT COUNT(passport_number) FROM writers WHERE passport_number = '{int(data['number'])}';")
    excist_number = cursor.fetchall()[0][0]
    cursor.execute(f"SELECT COUNT(phone_number) FROM writers WHERE phone_number = '{data['phone']}';")
    excist_phone = cursor.fetchall()[0][0]
    if excist_number:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Номер пасспорта должен быть уникальным']
    if excist_phone:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Номер телефона должен быть уникальным']
    cursor.execute(
        f"SELECT COUNT(contract_number) FROM contracts WHERE contract_number = '{int(data['contract-num'])}';")
    excist_contract = cursor.fetchall()[0][0]
    if excist_contract:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Контракт с такими номером уже существует']
    else:
        now = datetime.datetime.now()
        current_date = str(now).split(' ')[0]
        date_of_finish = now + datetime.timedelta(days=(365 * int(data['validity'])))

        cursor.execute(f'''INSERT INTO contracts (contract_number, date_of_conclusion, term_of_imprisonment, is_the_contract_terminated, contract_termination_date)
         VALUES
          (%s, %s, %s, %s, %s)''',
                       (int(data['contract-num']), current_date, int(data['validity']), 'false', date_of_finish))
        sqlite_connection.commit()
        patr = None
        if data['patro'] != '':
            patr = data['patro']

        cursor.execute(f"SELECT contract_id FROM contracts WHERE contract_number  = '{int(data['contract-num'])}';")
        id = cursor.fetchall()[0][0]

        cursor.execute(f'''INSERT INTO writers (passport_series, passport_number, last_name, first_name, surname, address, phone_number, fk_contract_number)
                 VALUES
                  (%s, %s, %s, %s, %s, %s, %s, %s)''',
                       (data['seria'], data['number'], data['lastname'], data['name'], patr, data['address'],
                        data['phone'], id))
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        return [u'success', u'Запись успешно добавлена']


def addСontract(data):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    cursor = sqlite_connection.cursor()

    cursor.execute(f"SELECT COUNT(passport_number) FROM writers WHERE passport_number = '{int(data['number'])}';")
    excist_number = cursor.fetchall()[0][0]
    cursor.execute(f"SELECT COUNT(phone_number) FROM writers WHERE phone_number = '{data['phone']}';")
    excist_phone = cursor.fetchall()[0][0]
    if excist_number:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Номер пасспорта должен быть уникальным']
    if excist_phone:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Номер телефона должен быть уникальным']
    cursor.execute(
        f"SELECT COUNT(contract_number) FROM contracts WHERE contract_number = '{int(data['contract-num'])}';")
    excist_contract = cursor.fetchall()[0][0]
    if excist_contract:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Контракт с такими номером уже существует']
    else:
        now = datetime.datetime.now()
        current_date = str(now).split(' ')[0]
        date_of_finish = now + datetime.timedelta(days=(365 * int(data['validity'])))

        cursor.execute(f'''INSERT INTO contracts (contract_number, date_of_conclusion, term_of_imprisonment, is_the_contract_terminated, contract_termination_date)
         VALUES
          (%s, %s, %s, %s, %s)''',
                       (int(data['contract-num']), current_date, int(data['validity']), 'false', date_of_finish))
        sqlite_connection.commit()
        patr = None
        if data['patro'] != '':
            patr = data['patro']

        cursor.execute(f"SELECT contract_id FROM contracts WHERE contract_number  = '{int(data['contract-num'])}';")
        id = cursor.fetchall()[0][0]

        cursor.execute(f'''INSERT INTO writers (passport_series, passport_number, last_name, first_name, surname, address, phone_number, fk_contract_number)
                 VALUES
                  (%s, %s, %s, %s, %s, %s, %s, %s)''',
                       (data['seria'], data['number'], data['lastname'], data['name'], patr, data['address'],
                        data['phone'], id))
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        return [u'success', u'Запись успешно добавлена']


def addСustomer(data):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    cursor = sqlite_connection.cursor()

    cursor.execute(f"SELECT COUNT(order_number) FROM orders WHERE order_number = '{int(data['number'])}';")
    excist_number = cursor.fetchall()[0][0]
    cursor.execute(f"SELECT COUNT(phone_number) FROM customers WHERE phone_number = '{data['phone']}';")
    excist_phone = cursor.fetchall()[0][0]
    cursor.execute(f"SELECT COUNT(book_id) FROM books WHERE book_id = '{int(data['book-id'])}';")
    excist_book = cursor.fetchall()[0][0]
    if excist_number:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Заказ с таким номером уже существует']
    if excist_phone:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Номер телефона должен быть уникальным']
    if not excist_book:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Книги с указанным ID не существует']
    cursor.execute(f"SELECT COUNT(legal_name) FROM customers WHERE legal_name = '{data['title']}';")
    excist_legal_name = cursor.fetchall()[0][0]
    if excist_legal_name:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Заказчик с указанным названием уже существует']
    else:
        now = datetime.datetime.now()
        current_date = str(now).split(' ')[0]
        if checkDate(current_date, data['finish-date']):
            cursor.close()
            sqlite_connection.close()
            return [u'error', u'Дата выполнения не должна предшествовать текущей дате']

        patr = None
        if data['patro'] != '':
            patr = data['patro']

        cursor.execute(f'''INSERT INTO customers (legal_name, last_name, first_name, surname, address, phone_number)
         VALUES
          (%s, %s, %s, %s, %s, %s)''',
                       (data['title'], data['lastname'], data['name'], patr, data['address'], data['phone']))
        sqlite_connection.commit()

        cursor.execute(f"SELECT customer_id FROM customers WHERE phone_number = '{data['phone']}';")
        id = cursor.fetchall()[0][0]

        cursor.execute(f'''INSERT INTO orders (order_number, registration_date, date_of_completion, number_of_copies, fk_customer_id, fk_book_id)
            VALUES
                  (%s, %s, %s, %s, %s, %s)''', (
        int(data['number']), current_date, data['finish-date'], int(data['quantity']), id, int(data['book-id'])))
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        return [u'success', u'Запись успешно добавлена']

def addOrder(data):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    cursor = sqlite_connection.cursor()

    cursor.execute(f"SELECT COUNT(order_number) FROM orders WHERE order_number = '{int(data['number'])}';")
    excist_number = cursor.fetchall()[0][0]
    cursor.execute(f"SELECT COUNT(book_id) FROM books WHERE book_id = '{int(data['book-id'])}';")
    excist_book = cursor.fetchall()[0][0]
    cursor.execute(f"SELECT COUNT(customer_id) FROM customers WHERE customer_id = '{int(data['cust-id'])}';")
    excist_cust = cursor.fetchall()[0][0]
    if excist_number:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Заказ с таким номером уже существует']
    if not excist_cust:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Заказчика с указанным ID не существует']
    if not excist_book:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Книги с указанным ID не существует']
    else:
        now = datetime.datetime.now()
        current_date = str(now).split(' ')[0]
        if checkDate(current_date, data['finish-date']):
            cursor.close()
            sqlite_connection.close()
            return [u'error', u'Дата выполнения не должна предшествовать текущей дате']

        cursor.execute(f'''INSERT INTO orders (order_number, registration_date, date_of_completion, number_of_copies, fk_customer_id, fk_book_id)
            VALUES
                  (%s, %s, %s, %s, %s, %s)''', (
        int(data['number']), current_date, data['finish-date'], int(data['quantity']), int(data['cust-id']),
        int(data['book-id'])))
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        return [u'success', u'Запись успешно добавлена']


###################Change##########################

def changeBook(data):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    cursor = sqlite_connection.cursor()

    cursor.execute(
        f"SELECT COUNT(book_cipher) FROM books WHERE book_cipher = '{data['book-isbn']}' AND book_id != '{data['book-id']}';")
    isbn = cursor.fetchall()[0][0]
    if isbn:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Указанные ISBN книги уже существует']
    else:
        fee = (int(data['book-price']) - int(data['book-cost'])) * int(data['book-copy'])
        if int(data['book-fee']) - fee > 0:
            return [u'error', u'Гонорар писателей не должен превышать суммарную прибыль от производства']

        cursor.execute(
            f'''UPDATE books SET book_cipher = %s, book_name = %s, circulation = %s, date_of_publication = %s, cost_price = %s, selling_price = %s, fee = %s WHERE book_id = {int(data['book-id'])}''',
            (data['book-isbn'], data['book-title'], int(data['book-copy']), data['book-date_pub'],
             int(data['book-cost']), int(data['book-price']), data['book-fee']))
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        return [u'success', u'Запись успешно изменена']


def changeWriter(data):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    cursor = sqlite_connection.cursor()

    cursor.execute(
        f"SELECT COUNT(phone_number) FROM writers WHERE phone_number = '{data['phone']}' AND writer_id != '{data['id']}';")
    phone = cursor.fetchall()[0][0]
    if phone:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Указанный номер телефона уже существует']
    cursor.execute(
        f"SELECT COUNT(passport_number) FROM writers WHERE passport_number = '{data['number']}' AND writer_id != '{data['id']}';")
    pass_number = cursor.fetchall()[0][0]
    if pass_number:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Указанный номер паспорта уже существует']
    else:
        patr = None
        if data['patro'] != '':
            patr = data['patro']
        cursor.execute(
            f'''UPDATE writers SET passport_series = %s, passport_number = %s, last_name = %s, first_name = %s,
             surname = %s, address = %s, phone_number = %s WHERE writer_id = {int(data['id'])}''',
            (data['seria'], data['number'], data['lastname'], data['name'], patr, data['address'], data['phone']))
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        return [u'success', u'Запись успешно изменена']


def changeContract(data):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    cursor = sqlite_connection.cursor()

    cursor.execute(
        f"SELECT COUNT(contract_number) FROM contracts WHERE contract_number = '{data['contract-num']}' AND contract_id != '{data['title']}';")
    contract_num = cursor.fetchall()[0][0]
    if contract_num:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Указанный номер контракта уже существует']
    else:

        current_date = data['date_start'].split('-')
        current_date = datetime.date(int(current_date[0]), int(current_date[1]), int(current_date[2]))
        date_of_finish = current_date + datetime.timedelta(days=(365 * int(data['validity'])))

        cursor.execute(
            f'''UPDATE contracts SET contract_number = %s, date_of_conclusion = %s, term_of_imprisonment = %s,
             contract_termination_date = %s WHERE contract_id = {int(data['title'])}''',
            (data['contract-num'], data['date_start'], int(data['validity']), date_of_finish))
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        return [u'success', u'Запись успешно изменена']


def changeCustomer(data):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    cursor = sqlite_connection.cursor()

    cursor.execute(
        f"SELECT COUNT(legal_name) FROM customers WHERE legal_name = '{data['title']}' AND customer_id != '{data['id']}';")
    legal_name = cursor.fetchall()[0][0]
    if legal_name:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Организация с указанным именем уже существует']
    cursor.execute(
        f"SELECT COUNT(phone_number) FROM customers WHERE phone_number = '{data['phone']}' AND customer_id != '{data['id']}';")
    phone = cursor.fetchall()[0][0]
    if phone:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Указанный номер телефона уже существует']
    else:
        patr = None
        if data['patro'] != '':
            patr = data['patro']
        cursor.execute(
            f'''UPDATE customers SET legal_name = %s, last_name = %s, first_name = %s, surname = %s,
             address = %s, phone_number = %s WHERE customer_id = {int(data['id'])}''',
            (data['title'], data['lastname'], data['name'], patr, data['address'], data['phone']))
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        return [u'success', u'Запись успешно изменена']


def changeOrder(data):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    cursor = sqlite_connection.cursor()

    cursor.execute(
        f"SELECT COUNT(order_number) FROM orders WHERE order_number = '{data['number']}' AND order_id != '{data['id']}';")
    order_num = cursor.fetchall()[0][0]
    if order_num:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Заказ с указанным номером уже существует']
    cursor.execute(f"SELECT registration_date FROM orders WHERE order_id = '{data['id']}';")
    reg_date = cursor.fetchall()[0][0]
    if checkDate(str(reg_date), data['finish-date']):
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Дата завершения заказа не может быть меньше даты регистрации']
    else:
        cursor.execute(
            f'''UPDATE orders SET order_number = %s, date_of_completion = %s, number_of_copies = %s WHERE order_id = {int(data['id'])}''',
            (data['number'], data['finish-date'], data['quantity']))
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        return [u'success', u'Запись успешно изменена']


def addBookToAutor(data):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    cursor = sqlite_connection.cursor()

    cursor.execute(f"SELECT COUNT(writer_id) FROM writers WHERE writer_id = {int(data['autor_id'])};")
    writersWithCurrentId = cursor.fetchall()[0][0]

    if (writersWithCurrentId):

        cursor.execute(f'''INSERT INTO wr_id_book_id (writer_id, book_id)
         VALUES
          (%s, %s)''', (data['autor_id'], data['book_id']))

        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        return [u'success', u'Добавление автора успешно']
    else:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Писателя с указанным ID не существует']


def removeAutorToBook(data):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    cursor = sqlite_connection.cursor()

    cursor.execute(f"SELECT COUNT(writer_id) FROM writers WHERE writer_id = {int(data['autor_id'])};")
    writersWithCurrentId = cursor.fetchall()[0][0]

    if writersWithCurrentId:
        cursor.execute(
            f"SELECT COUNT(writer_id) FROM wr_id_book_id WHERE writer_id = {int(data['autor_id'])} AND book_id = {int(data['book_id'])} ;")
        writersToBook = cursor.fetchall()[0][0]

        if not writersToBook:
            cursor.close()
            sqlite_connection.close()
            return [u'error', u'Указанный писатель не ялвяется автором данной книги']

        cursor.execute(
            f"DELETE FROM wr_id_book_id WHERE writer_id = {data['autor_id']} AND book_id = {data['book_id']} ;")

        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        return [u'success', u'Связь книга - автор удалена']
    else:
        cursor.close()
        sqlite_connection.close()
        return [u'error', u'Писателя с указанным ID не существует']

#########################################################

def getUserByLogin(login):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    cursor = sqlite_connection.cursor()
    cursor.execute(f"SELECT * FROM users WHERE login='{login}'")
    user = cursor.fetchall()

    cursor.close()
    sqlite_connection.close()
    return user

def getUserByID(id):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    cursor = sqlite_connection.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_id='{id}'")
    user = cursor.fetchall()

    cursor.close()
    sqlite_connection.close()
    return user

def checkDate(current, next):
    splitted_curr = current.split('-')
    splitted_next = next.split('-')
    if datetime.date(int(splitted_curr[0]), int(splitted_curr[1]), int(splitted_curr[2])) < datetime.date(
            int(splitted_next[0]), int(splitted_next[1]), int(splitted_next[2])):
        return False
    else:
        return True

def getYearResult(date_dictionary):
    sqlite_connection = sqlite3.connect("publishing.sqlite")

    if checkDate(date_dictionary['start'], date_dictionary['end']):
        return False

    cursor = sqlite_connection.cursor()
    cursor.execute('SELECT * FROM orders')
    all_orders = cursor.fetchall()

    start_date = splitAndReturnDate(date_dictionary['start'])
    end_date = splitAndReturnDate(date_dictionary['end'])
    flitred_orders = filterByDate(all_orders, start_date, end_date)

    result_list = []
    for order in flitred_orders:
        row = {}

        cursor.execute(f'SELECT legal_name FROM customers WHERE customer_id = {order[5]} LIMIT 1')
        customer_name = cursor.fetchall()[0][0]

        number_of_book_copies = order[4]

        cursor.execute(f'SELECT book_name, cost_price, selling_price FROM books WHERE book_id = {order[6]}')
        book = cursor.fetchall()
        book_name = book[0][0]
        cost = book[0][1].replace('\xa0', '').split(',')[0]
        price = book[0][2].replace('\xa0', '').split(',')[0]

        final_money = (int(price) - int(cost)) * int(number_of_book_copies)

        for item in result_list:
            if customer_name in item.keys():
                item[customer_name].append([book_name, cost, price, number_of_book_copies, str(final_money)])
                break
        else:
            row[customer_name] = [[book_name, cost, price, number_of_book_copies, str(final_money)]]
            result_list.append(row)

    cursor.close()
    sqlite_connection.close()
    return result_list


def filterByDate(orders_list: list, start_date, end_date):
    return filter(lambda x: start_date <= x[3] <= end_date, orders_list)

def splitAndReturnDate(date_str: str):
    splitted_curr = date_str.split('-')
    return datetime.date(int(splitted_curr[0]), int(splitted_curr[1]), int(splitted_curr[2]))

def makeStringifyObject(inputList: list):
    pass


# if __name__ == '__main__':
#     print(getAllWriters())
#     print(getAllOrders())
#     print(getAllCustomers())
#     print(getAllContracts())
#     print(getAllBooks())
