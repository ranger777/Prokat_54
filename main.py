import sqlite3
from configparser import ConfigParser
import datetime
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
import os
from werkzeug.utils import secure_filename
import random
import sys
import time
import webbrowser
import shutil



                                        #для работы с настройками

#проверим есть ли файл настроек
isExist = os.path.exists(f'_internal/settings.ini') #проверим есть ли файл с таким именем в папке картинок
print(isExist)
if isExist == True:
    print('файл есть')
    config = ConfigParser()  # создаём объекта парсера
    config.read("_internal/settings.ini")  # читаем конфиг
    server_port = config["Server"]["server_port"]
    path_db = (f'{config["Database"]["db_path"]}{config["Database"]["db_name"]}')
#если нет - создаем дефолтный
else:
    config_file = open("_internal/settings.ini", "w+")
    config_file.close()
    config = ConfigParser()  # создаём объекта парсера
    config.read("settings.ini")  # читаем конфиг
    config.add_section('Database')#создаем секцию для пути к базе
    config.set('Database', 'db_name', 'prokat_41.db')#заполняем секцию
    config.set('Database', 'db_path', '_internal\\\\')#заполняем секцию
    config.add_section('Server')#создаем секцию с портом сервера
    config.set('Server', 'server_port', '5000')#заполняем секцию
    with open('_internal/settings.ini', 'w') as configfile:#Сохраняем файл
        config.write(configfile)
   # os.startfile('server-restart.bat')


                                          #Бэкап БД
#найдем путь для папки бэкапа
config = ConfigParser()  # создаём объекта парсера
config.read("_internal/settings.ini")  # читаем конфиг
path_db_file = (f'{config["Database"]["db_path"]}{config["Database"]["db_name"]}')
isExist_file = os.path.exists(path_db_file) #проверим есть ли файл бд
path_db_bu = (f'{config["Database"]["db_path"]}Backup')
isExist_bu = os.path.exists(path_db_bu) #проверим есть ли папка с таким именем
if isExist_file == True: #если файл есть:
    print('файл есть')
    if isExist_bu == False:# и если папки нет, то оздадим папку
        print('папки нет, надо создать')
        os.makedirs(f'{config["Database"]["db_path"]}Backup')
    #получить сегодняшнюю дату
    #сравнить есть ли файл с сегодняшней датой
    #если папка есть, то проверим наличие файла с сегодняшней датой в ней
    path_db_file_bu = (f'{config["Database"]["db_path"]}Backup\\{str(datetime.now().date())}-{config["Database"]["db_name"]}')
    #print(path_db_file_bu)
    isExist_path_db_file_bu = os.path.exists(path_db_file_bu)  # проверим есть ли файл бд с сегодняшней датой
    if isExist_path_db_file_bu == False:# и если сегодняшнего файла нет, то создадим
        print(f'файла нет, создаю {path_db_file_bu}')
        shutil.copy(path_db_file, path_db_file_bu)
    print(f'файл бэкапа есть, не создаю')
else:
    print('файла нет')

# механизм удаления лишних файлов больше 10
dir_list = sorted(os.listdir(f'{config["Database"]["db_path"]}Backup'), reverse=True)#получим список содержимого папка бэкап сортированный в обратном порядке
dir_list = [f for f in dir_list if os.path.isfile(f'{config["Database"]["db_path"]}Backup'+'/'+f)]#отсеим папки, оставив только файлы и пересоберем
#print(dir_list)
for i in range(0, len(dir_list)):#пройдем циклом все файлы
    if i <10:
        print(dir_list[i])# если порядковый номер меньше 10, просто выведим название для контроля в консоли
    else: os.remove(f'{config["Database"]["db_path"]}Backup\\{dir_list[i]}')# удалим десятый и последующие

#path_db = "C:\\Users\\Ranger\\YandexDisk\\DB\\prokat_41.db"


app = Flask(__name__, static_folder="_internal")


#сразу запускаем страничку
webbrowser.open(f'http://127.0.0.1:{server_port}/')

#проверяем, доступ на ли бд
try:
    connected = sqlite3.connect(f'file:{path_db}?mode=rw', uri=True)
    cursor = connected.cursor()
    try:
        cursor.execute(f'SELECT COUNT(*) FROM clients')
        connect_bd = True
        if config["Database"]["db_name"]  ==  'prokat_41.db':
            name_db = 'по г. Бердск'
        elif config["Database"]["db_name"]  ==  'prokat_42.db':
            name_db = 'по г. Искитим'
    except:
        connect_bd = False
        name_db = ''
    cursor.close()
except:
    connect_bd = False
    name_db = ''



@app.route('/')
def index():
    try:
        connected = sqlite3.connect(f'file:{path_db}?mode=rw', uri=True)  # подключаемся к базе и делаем запрос. если файла бд не существует то он не пересоздается


        cursor_0 = connected.cursor()
        try:
            cursor_0.execute(f'SELECT COUNT(*) FROM clients')
            total_client = cursor_0.fetchone()
        except:
            total_client = ()
        cursor_0.close()

        cursor_1 = connected.cursor()
        try:
            cursor_1.execute(f'SELECT COUNT(*) FROM tools')
            total_tool = cursor_1.fetchone()
        except:
            total_tool = ()
        cursor_1.close()

        cursor_2 = connected.cursor()
        try:
            cursor_2.execute(f'SELECT location, count (*) FROM tools GROUP BY location')
            total_tool_group = cursor_2.fetchall()
        except:
            total_tool_group = ()
        cursor_2.close()
        connected.close()
    except:

        total_client = ()
        total_tool = ()
        total_tool_group = ()
    print(total_client)
    print(total_tool)
    print(total_tool_group)
    print(connect_bd)
    dir_list_index = sorted(os.listdir(f'{config["Database"]["db_path"]}Backup'), reverse=True)  # получим список содержимого папка бэкап сортированный в обратном порядке
    dir_list_index = [f for f in dir_list_index if os.path.isfile(f'{config["Database"]["db_path"]}Backup' + '/' + f)]  # отсеим папки, оставив только файлы и пересоберем
    return render_template("index.html", connect_bd=connect_bd, name_db=name_db, total_client=total_client, total_tool=total_tool, total_tg=total_tool_group, files_bu=dir_list_index)

 #страница переключения между БД Бердска и искитима
@app.route('/settings', methods=['POST', 'GET'])
def settings():
    if request.method == "POST":
        button = request.form['action']
        if button == '1':
            config = ConfigParser()  # создаём объекта парсера
            config.read("settings.ini")  # читаем конфиг
            config.set('Database', 'db_name', 'prokat_41.db')  # заполняем секцию
            with open('settings.ini', 'w') as configfile:  # Сохраняем файл
                config.write(configfile)
        elif button == '2':
            config = ConfigParser()  # создаём объекта парсера
            config.read("settings.ini")  # читаем конфиг
            config.set('Database', 'db_name', 'prokat_42.db')  # заполняем секцию
            with open('settings.ini', 'w') as configfile:  # Сохраняем файл
                config.write(configfile)
        os.startfile('server-restart.bat')
        #subprocess.call('taskkill /f /im main.exe & start main.exe')
        time.sleep(2)
        #subprocess.call('start "" main.exe')
        #time.sleep(2)
        return redirect(f'/all_clients')
    else:
        return render_template("settings.html", server_port=server_port, path_db=path_db)

#Карточка клиента
@app.route('/client/<int:id>', methods=['POST', 'GET'])
def client(id):
    query_str = (f'SELECT * FROM clients WHERE id={id}')
    connected = sqlite3.connect(path_db)  # подключаемся к базе и делаем запрос
    cursor = connected.cursor()
    try:
        cursor.execute(query_str)
        client = cursor.fetchone()
    except:
        client = ()
    cursor.close()
    cursor_1 = connected.cursor()
    try:
        cursor_1.execute(f"select r.id, t.id, t.type, t.brand, t.model, t.serial_number, r.date_take, r.date_plane_return, r.date_return, r.collateral, r.summ, r.description from rentals AS r JOIN clients AS c ON c.id = r.client_id JOIN tools AS t ON t.id = r.tool_id WHERE c.id={id} AND r.date_return !='' AND r.date_return NOT NULL AND r.date_return !='-' AND r.summ !='' AND r.summ !=0.0 AND r.summ !='-' AND r.summ not NULL")
        rentals_history = cursor_1.fetchall()
    except:
        rentals_history = ()
    cursor_1.close()
    cursor_2 = connected.cursor()
    try:
        cursor_2.execute(f"select r.id, t.id, t.type, t.brand, t.model, t.serial_number, t.rent_day_value, t.rent_hour_value, t.collateral_value, r.date_take, r.date_plane_return, r.date_return, r.collateral, r.summ, r.description from rentals AS r JOIN clients AS c ON c.id = r.client_id JOIN tools AS t ON t.id = r.tool_id WHERE c.id={id} AND ((r.date_return='' or r.date_return=NULL or r.date_return='-') OR (r.summ='' or r.summ='0.0' or r.summ=NULL or r.summ='-'))")
        rentals = cursor_2.fetchall()
    except:
        rentals = ()
    #print(rentals)
    cursor_2.close()
    cursor_3 = connected.cursor()
    try:
        cursor_3.execute(f"SELECT id, type, brand, model, serial_number, description, keywords, rent_day_value, rent_hour_value, collateral_value from tools where location = 0")
        issue_tools = cursor_3.fetchall()
    except:
        issue_tools = ()
    # print(rentals)
    cursor_3.close()
    connected.close()
    for i in range(len(rentals)):
        rental_list = list(rentals[i])
        print(rental_list[9] + '  ' + rental_list[11])
        if rental_list[11] != '' and rental_list[11] !='-' and rental_list[11] != None:
            start_d = datetime.strptime(rental_list[9], "%Y-%m-%dT%H:%M")
            end_d = datetime.strptime(rental_list[11], "%Y-%m-%dT%H:%M")
            difference = end_d - start_d
            seconds = difference.total_seconds()
            days = seconds / (60 * 60 * 24)
            days = int(days)
            hours_all = seconds / (60 * 60)
            hours = int(hours_all) - days * 24
            if hours <= 3:
                hours = 3
            summ = days * rental_list[6] + hours/3 * rental_list[7]
            summ_collateral = summ - rental_list[12]
            rental_list.append(days)
            rental_list.append(hours)
            rental_list.append(summ)
            rental_list.append(summ_collateral)
        else:
            rental_list.append('')
            rental_list.append('')
        rentals[i] = tuple(rental_list)
    print(rentals)
    return render_template("client.html", client=client, rentals_h=rentals_history, rentals=rentals, issue_tools=issue_tools)


#обработчик принятия из проката
@app.route('/client_rent_accept/<int:id>', methods=['POST', 'GET'])
def client_rent_accept(id):
    if request.method == "POST":
        client_id = request.form['client_id']
        tool_id = request.form['tool_id']
        date_return = request.form['date_return']
        description = request.form['description'].strip()
        description = description.lower()

        query_str = ''   #собираем строку для запроса

        if type:
            query_str = (f'date_return = \'{date_return}\'')
        if description == '':
            if query_str != '':
                query_str = query_str + (f', description = \'\'')
            elif query_str == '':
                query_str = query_str + (f'description = \'\'')
        elif description:
            if query_str != '':
                query_str = query_str + (f', description = \'{description}\'')
            elif query_str == '':
                query_str = query_str + (f'description = \'{description}\'')
        query_str = (f'UPDATE rentals SET {query_str} WHERE id={id}')
        query_str_1 = (f'UPDATE tools SET location=0 WHERE id={tool_id}')
        print(query_str)
        connected = sqlite3.connect(path_db)#подключаемся к базе и делаем запрос
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        print("Запись успешно вставлена в таблицу tools ", cursor.rowcount)
        cursor.close()
        cursor_1 = connected.cursor()
        cursor_1.execute(query_str_1)
        connected.commit()
        print("Запись успешно вставлена в таблицу tools ", cursor_1.rowcount)
        cursor_1.close()
        connected.close()
        return redirect(f'/client/{client_id}')
    else:
        return redirect(f'/all_clients')


#обработчик расчета проката
@app.route('/client_rent_calc/<int:id>', methods=['POST', 'GET'])
def client_rent_calc(id):
    if request.method == "POST":
        tool_id = request.form['tool_id']
        day = request.form['day']
        client_id = request.form['client_id']
        summ = request.form['summ']
        description = request.form['description'].strip()
        description = description.lower()

        query_str = ''   #собираем строку для запроса

        if type:
            query_str = (f'summ = \'{summ}\'')
        if description == '':
            if query_str != '':
                query_str = query_str + (f', description = \'\'')
            elif query_str == '':
                query_str = query_str + (f'description = \'\'')
        elif description:
            if query_str != '':
                query_str = query_str + (f', description = \'{description}\'')
            elif query_str == '':
                query_str = query_str + (f'description = \'{description}\'')
        query_str = (f'UPDATE rentals SET {query_str} WHERE id={id}')
        print(query_str)
        connected = sqlite3.connect(path_db)#подключаемся к базе и делаем запрос
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        print("Запись успешно вставлена в таблицу tools ", cursor.rowcount)
        cursor.close()
        cursor_1 = connected.cursor()
        cursor_1.execute(f'select count_day from tools where id={tool_id}')
        tool_count_day = cursor_1.fetchone()
        #cursor_1 = list(cursor_1)
        count_day = tool_count_day[0]
        connected.commit()
        cursor_1.close()
        count_day = count_day + int(day)
        cursor_2 = connected.cursor()
        cursor_2.execute(f'UPDATE tools SET count_day={count_day} WHERE id={tool_id}')
        connected.commit()
        cursor_2.close()
        connected.close()
        return redirect(f'/client/{client_id}')
    else:
        return redirect(f'/all_clients')


#обработчик взятия клиентом в прокат оборудования
@app.route('/client_issue_tool', methods=['POST', 'GET'])
def client_issue_tool():
    if request.method == "POST":
        client_id = request.form['client_id']
        tool_id = request.form['tool_id']
        date_take = request.form['date_take']
        date_plane_return = request.form['date_plane_return']
        collateral = request.form['collateral']
        description = request.form['description'].strip()
        description = description.lower()

        query_str = 'INSERT INTO rentals ('
        query_str_name = ''
        query_str_value = ''
        if client_id:
            query_str_name = query_str_name + 'client_id'
            query_str_value = query_str_value + client_id
        if tool_id:
            if query_str_name != '':
                query_str_name = query_str_name + ', tool_id'
                query_str_value = query_str_value + ', ' + tool_id
            if query_str_name == '':
                query_str_name = query_str_name + 'tool_id'
                query_str_value = query_str_value + tool_id
        if date_take:
            if query_str_name != '':
                query_str_name = query_str_name + ', date_take'
                query_str_value = query_str_value + ', ' + '\'' + date_take + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'date_take'
                query_str_value = query_str_value + '\'' + date_take + '\''
        if date_plane_return:
            if query_str_name != '':
                query_str_name = query_str_name + ', date_plane_return'
                query_str_value = query_str_value + ', ' + '\'' + date_plane_return + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'date_plane_return'
                query_str_value = query_str_value + '\'' + date_plane_return + '\''
        if collateral:
            if query_str_name != '':
                query_str_name = query_str_name + ', collateral'
                query_str_value = query_str_value + ', ' + collateral
            if query_str_name == '':
                query_str_name = query_str_name + 'collateral'
                query_str_value = query_str_value + collateral
        if description:
            if query_str_name != '':
                query_str_name = query_str_name + ', description'
                query_str_value = query_str_value + ', ' + '\'' + description + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'description'
                query_str_value = query_str_value + '\'' + description + '\''

        query_str = query_str + query_str_name + ') VALUES (' + query_str_value + ')'
        query_str_1 = (f'UPDATE tools SET location=1 WHERE id={tool_id}')
        print(query_str)
        connected = sqlite3.connect(path_db)#подключаемся к базе и делаем запрос
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        print("Запись успешно вставлена в таблицу tools ", cursor.rowcount)
        cursor.close()
        cursor_1 = connected.cursor()
        cursor_1.execute(query_str_1)
        connected.commit()
        print("Запись успешно вставлена в таблицу tools ", cursor_1.rowcount)
        cursor_1.close()
        connected.close()
        return redirect(f'/client/{client_id}')
    else:
        return redirect(f'/all_clients')


#страница всех клиентов
@app.route('/all_clients', methods=['POST', 'GET'])
def all_clients():
    if request.method == "POST":
        search_text = request.form['search_text'].strip()
        radios = request.form.get('radios')
        s_t = search_text.lower()
        if search_text == '':
            field = ''
        elif search_text != '' and radios == '1':
            try:
                field = (f'WHERE id = {int(search_text)} OR description LIKE \'%{s_t}%\' OR company LIKE \'%{s_t}%\'')
            except:
                field = (f'WHERE description LIKE \'%{s_t}%\' OR company LIKE \'%{s_t}%\'')
        elif search_text != '' and radios == '2':
            field = (f'WHERE description LIKE \'%{s_t}%\' OR phone LIKE \'%{s_t}%\' OR company LIKE \'%{s_t}%\'')
        elif search_text != '' and radios == '3':
            field = (f'WHERE description LIKE \'%{s_t}%\' OR surname LIKE \'%{s_t}%\' OR name LIKE \'%{s_t}%\' OR middle_name LIKE \'%{s_t}%\' OR company LIKE \'%{s_t}%\'')
        elif search_text != '' and radios == '4':
            field = (f'WHERE description LIKE \'%{s_t}%\' OR gos_n LIKE \'%{s_t}%\' OR company LIKE \'%{s_t}%\'')
        connected = sqlite3.connect(path_db)
        cursor = connected.cursor()
        try:
            cursor.execute(f'select * from clients {field}')
            clients = cursor.fetchall()
        except:
            clients = ()
        connected.close()
        return render_template("all_clients.html", clients=clients, search_text=search_text)
    else:
        connected = sqlite3.connect(path_db)
        cursor = connected.cursor()
        try:
            cursor.execute("select * from clients")
            clients = cursor.fetchall()
        except:
            clients = ()
        #print(clients)
        connected.close()
        #print("вход на страничку")
        return render_template("all_clients.html", clients=clients)


#Страница всего оборудования
@app.route('/tools', methods=['POST', 'GET'])
def tools():
    if request.method == "POST":
        search_text = request.form['search_text'].strip()
        if search_text == '':
            field = ''
        else:
            s_t = search_text.lower()
            try:
                field = (f'WHERE id = {int(search_text)} OR type LIKE \'%{s_t}%\' OR brand LIKE \'%{s_t}%\' OR model LIKE \'%{s_t}%\' OR description LIKE \'%{s_t}%\' OR keywords LIKE \'%{s_t}%\'')
            except:

                #s_t = search_text
                field = (f'WHERE type LIKE \'%{s_t}%\' OR brand LIKE \'%{s_t}%\' OR model LIKE \'%{s_t}%\' OR description LIKE \'%{s_t}%\' OR keywords LIKE \'%{s_t}%\'')
                print(field)

        connected = sqlite3.connect(path_db)
        cursor = connected.cursor()
        try:
            cursor.execute(f'select * from tools {field}')
            tools = cursor.fetchall()
        except:
            tools = ()
        connected.close()
        return render_template("tools.html", tools=tools, search_text=search_text)
    else:
        connected = sqlite3.connect(path_db)
        cursor = connected.cursor()
        try:
            cursor.execute("select * from tools")
            tools = cursor.fetchall()
        except:
            tools = ()
        connected.close()
        search_text = ''
        return render_template("tools.html", tools=tools, search_text=search_text)


#карточка оборудования
@app.route('/tool/<int:id>', methods=['POST', 'GET'])
def tool(id):
    query_str = (f'SELECT * FROM tools WHERE id={id}')
    connected = sqlite3.connect(path_db)  # подключаемся к базе и делаем запрос
    cursor = connected.cursor()
    try:
        cursor.execute(query_str)
        tool = cursor.fetchone()
    except:
        tool = ()
    cursor.close()
    cursor_1 = connected.cursor()
    try:
        cursor_1.execute(f"select r.id, c.id, c.surname, c.name, c.middle_name, r.date_take, r.date_plane_return, r.date_return, r.collateral, r.summ, r.description from rentals AS r JOIN clients AS c ON c.id = r.client_id JOIN tools AS t ON t.id = r.tool_id WHERE t.id={id}")
        rentals_history = cursor_1.fetchall()
    except:
        rentals_history = ()
    cursor_1.close()
    cursor_2 = connected.cursor()
    try:
        cursor_2.execute(f"select rn.id, rn.work_type, rn.date_for_repair, rn.date_from_repair, rn.summ, rn.description from renovations AS rn JOIN tools AS t ON t.id = rn.tool_id WHERE t.id={id}")
        renovations_history = cursor_2.fetchall()
    except:
        renovations_history = ()
    cursor_2.close()
    connected.close()
    date = datetime.strptime(tool[5], "%Y-%m-%d")#парсим дату в объект
    purchase_date = date.strftime('%d.%m.%Y {g}').format(g='г.')#форматируем вывод, именно так, русские буквы только подстановкой, иначе выдает ошибку кодировки
    return render_template("tool.html", tool=tool, purchase_date=purchase_date, rentals_h=rentals_history, renovations_h=renovations_history)


#обработчик редактирования характеристик оборудования
@app.route('/tool_info/<int:id>', methods=['POST', 'GET'])
def tool_info_edit(id):
    if request.method == "POST":
        tool_info = request.form['tool_info'].strip()
        query_str = (f'UPDATE tools set tool_info = \'{tool_info}\' WHERE id={id}')
        connected = sqlite3.connect(path_db)  # подключаемся к базе и делаем запрос
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        cursor.close()
        connected.close()
        return redirect(f'/tool/{id}')


#обработчик изменения локации оборудования
@app.route('/tool_local/<int:id>', methods=['POST', 'GET'])
def tool_local_edit(id):
    if request.method == "POST":
        tool_local = request.form['tool_local']
        query_str = (f'UPDATE tools SET location={tool_local} WHERE id={id}')
        connected = sqlite3.connect(path_db)  # подключаемся к базе и делаем запрос
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        cursor.close()
        connected.close()
        return redirect(f'/tool/{id}')


#Страница всех прокатов
@app.route('/rentals', methods=['POST', 'GET'])
def rentals():
    if request.method == "POST":
        search_text = request.form['search_text'].strip()
        if search_text == '':
            field = ''
        else:
            s_t = search_text.lower()
            try:
                field = (f'WHERE r.id = {int(search_text)} OR c.surname LIKE \'%{s_t}%\' OR c.name LIKE \'%{s_t}%\' OR c.middle_name LIKE \'%{s_t}%\' OR t.type LIKE \'%{s_t}%\' OR t.brand LIKE \'%{s_t}%\' OR t.model LIKE \'%{s_t}%\' OR r.description LIKE \'%{s_t}%\' OR t.serial_number LIKE \'%{s_t}%\' OR r.date_take LIKE \'%{s_t}%\' OR r.date_plane_return LIKE \'%{s_t}%\' OR r.date_return LIKE \'%{s_t}%\' OR r.collateral LIKE \'%{s_t}%\' OR r.summ LIKE \'%{s_t}%\' OR r.summ LIKE \'%{s_t}%\'')
            except:

                #s_t = search_text
                field = (f'WHERE c.surname LIKE \'%{s_t}%\' OR c.name LIKE \'%{s_t}%\' OR c.middle_name LIKE \'%{s_t}%\' OR t.type LIKE \'%{s_t}%\' OR t.brand LIKE \'%{s_t}%\' OR t.model LIKE \'%{s_t}%\' OR r.description LIKE \'%{s_t}%\' OR t.serial_number LIKE \'%{s_t}%\' OR r.date_take LIKE \'%{s_t}%\' OR r.date_plane_return LIKE \'%{s_t}%\' OR r.date_return LIKE \'%{s_t}%\' OR r.collateral LIKE \'%{s_t}%\' OR r.summ LIKE \'%{s_t}%\' OR r.summ LIKE \'%{s_t}%\'')
                print(field)

        connected = sqlite3.connect(path_db)
        cursor = connected.cursor()
        try:
            cursor.execute(f'select r.id, c.id, c.surname, c.name, c.middle_name, t.id, t.type, t.brand, t.model, t.serial_number, r.date_take, r.date_plane_return, r.date_return, r.collateral, r.summ, r.description from rentals AS r JOIN clients AS c ON c.id = r.client_id JOIN tools AS t ON t.id = r.tool_id {field}')
            rentals = cursor.fetchall()
        except:
            rentals = ()
        connected.close()
        return render_template("rentals.html", rentals=rentals, search_text=search_text)
    else:
        connected = sqlite3.connect(path_db)
        cursor = connected.cursor()
        try:
            cursor.execute("select r.id, c.id, c.surname, c.name, c.middle_name, t.id, t.type, t.brand, t.model, t.serial_number, r.date_take, r.date_plane_return, r.date_return, r.collateral, r.summ, r.description from rentals AS r JOIN clients AS c ON c.id = r.client_id JOIN tools AS t ON t.id = r.tool_id")
            rentals = cursor.fetchall()
        except:
            rentals = ()
        connected.close()
        search_text = ''
        return render_template("rentals.html", rentals=rentals, search_text=search_text)
        print(rentals)


#обработчик добавления клиента
@app.route('/clients_add', methods=['POST', 'GET'])
def clients_add():
    if request.method == "POST":
        surname = request.form['surname'].strip()
        surname = surname.lower()
        name = request.form['name'].strip()
        name = name.lower()
        middle_name = request.form['middle_name'].strip()
        middle_name = middle_name.lower()
        phone = request.form['phone']
        gos_n = request.form['gos_n'].strip()
        gos_n = gos_n.lower()
        company = request.form['company'].strip()
        company = company.lower()
        description = request.form['description'].strip()
        description = description.lower()

        query_str = 'INSERT INTO clients ('
        query_str_name = ''
        query_str_value = ''
        if surname:
            query_str_name = query_str_name + 'surname'
            query_str_value = query_str_value + '\'' + surname + '\''
        if name:
            if query_str_name != '':
                query_str_name = query_str_name + ', name'
                query_str_value = query_str_value + ', ' + '\'' + name + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'name'
                query_str_value = query_str_value + '\'' + name + '\''
        if middle_name:
            if query_str_name != '':
                query_str_name = query_str_name + ', middle_name'
                query_str_value = query_str_value + ', ' + '\'' + middle_name + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'middle_name'
                query_str_value = query_str_value + '\'' + middle_name + '\''
        if phone:
            if query_str_name != '':
                query_str_name = query_str_name + ', phone'
                query_str_value = query_str_value + ', ' + '\'' + phone + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'phone'
                query_str_value = query_str_value + '\'' + phone + '\''
        if gos_n:
            if query_str_name != '':
                query_str_name = query_str_name + ', gos_n'
                query_str_value = query_str_value + ', ' + '\'' + gos_n + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'gos_n'
                query_str_value = query_str_value + '\'' + gos_n + '\''
        if company:
            if query_str_name != '':
                query_str_name = query_str_name + ', company'
                query_str_value = query_str_value + ', ' + '\'' + company + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'company'
                query_str_value = query_str_value + '\'' + company + '\''
        if description:
            if query_str_name != '':
                query_str_name = query_str_name + ', description'
                query_str_value = query_str_value + ', ' + '\'' + description + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'description'
                query_str_value = query_str_value + '\'' + description + '\''

        query_str = query_str + query_str_name + ') VALUES (' + query_str_value + ')'
        print(query_str)
        connected = sqlite3.connect(path_db)
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        print("Запись успешно вставлена в таблицу tools ", cursor.rowcount)
        cursor.close()
        connected.close()
        return redirect('/all_clients')
    else:
        return redirect('/all_clients')


#обработчик добавления оборудования
@app.route('/tools_add', methods=['POST', 'GET'])
def tools_add():
    if request.method == "POST":
        photo = request.files['photo'] #получим объект картинки
        if photo:                      #если файл есть
            photo_name = photo.filename    #достанем имя картинки
            print(photo_name)

            photo_name = secure_filename(photo_name)#проверим безопасно ли имя файла
            print(photo_name)
            if os.path.splitext(photo_name)[1] == '':
                photo_name = str(random.randint(1,999999999)) + '.' + os.path.splitext(photo_name)[0]
                print(photo_name)
            isExist = os.path.exists(f'_internal/_internal/images/{photo_name}') #проверим есть ли файл с таким именем в папке картинок
            print(isExist)
            if isExist == True:
                #photo_nane_base = os.path.splitext(photo_nane)[0]  # отделим имя от расширения
                photo_name = os.path.splitext(photo_name)[0] + '_1' + os.path.splitext(photo_name)[1]              #добавим к имени (1)
                #print(photo_nane_base)
                print(photo_name)
            photo.save(os.path.join('_internal/_internal/images/', photo_name))
        else: photo_name = 'default.jpg'

        type = request.form['type'].strip()
        type = type.lower()
        brand = request.form['brand'].strip()
        brand = brand.lower()
        model = request.form['model'].strip()
        model = model.lower()
        serial_number = request.form['serial_number'].strip()
        serial_number = serial_number.lower()
        purchase_value = request.form['purchase_value']
        purchase_date = request.form['purchase_date']
        description = request.form['description'].strip()
        description = description.lower()
        keywords = request.form['keywords'].strip()
        keywords = keywords.lower()
        rent_day_value = request.form['rent_day_value']
        rent_hour_value = request.form['rent_hour_value']
        collateral_value = request.form['collateral_value']

        query_str = 'INSERT INTO tools ('
        query_str_name = ''
        query_str_value = ''
        if type:
            query_str_name = query_str_name + 'type'
            query_str_value = query_str_value + '\'' + type + '\''
        if brand:
            if query_str_name != '':
                query_str_name = query_str_name + ', brand'
                query_str_value = query_str_value + ', ' + '\'' + brand + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'brand'
                query_str_value = query_str_value + '\'' + brand + '\''
        if model:
            if query_str_name != '':
                query_str_name = query_str_name + ', model'
                query_str_value = query_str_value + ', ' + '\'' + model + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'model'
                query_str_value = query_str_value + '\'' + model + '\''
        if serial_number:
            if query_str_name != '':
                query_str_name = query_str_name + ', serial_number'
                query_str_value = query_str_value + ', ' + '\'' + serial_number + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'serial_number'
                query_str_value = query_str_value + '\'' + serial_number + '\''
        if purchase_value:
            if query_str_name != '':
                query_str_name = query_str_name + ', purchase_value'
                query_str_value = query_str_value + ', ' + purchase_value
            if query_str_name == '':
                query_str_name = query_str_name + 'purchase_value'
                query_str_value = query_str_value + purchase_value
        if purchase_date:
            if query_str_name != '':
                query_str_name = query_str_name + ', purchase_date'
                query_str_value = query_str_value + ', ' + '\'' + purchase_date + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'purchase_date'
                query_str_value = query_str_value + '\'' + purchase_date + '\''
        if description:
            if query_str_name != '':
                query_str_name = query_str_name + ', description'
                query_str_value = query_str_value + ', ' + '\'' + description + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'description'
                query_str_value = query_str_value + '\'' + description + '\''
        if keywords:
            if query_str_name != '':
                query_str_name = query_str_name + ', keywords'
                query_str_value = query_str_value + ', ' + '\'' + keywords + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'keywords'
                query_str_value = query_str_value + '\'' + keywords + '\''
        if rent_day_value:
            if query_str_name != '':
                query_str_name = query_str_name + ', rent_day_value'
                query_str_value = query_str_value + ', ' + rent_day_value
            if query_str_name == '':
                query_str_name = query_str_name + 'rent_day_value'
                query_str_value = query_str_value + rent_day_value
        if rent_hour_value:
            if query_str_name != '':
                query_str_name = query_str_name + ', rent_hour_value'
                query_str_value = query_str_value + ', ' + rent_hour_value
            if query_str_name == '':
                query_str_name = query_str_name + 'rent_hour_value'
                query_str_value = query_str_value + rent_hour_value
        if collateral_value:
            if query_str_name != '':
                query_str_name = query_str_name + ', collateral_value'
                query_str_value = query_str_value + ', ' + collateral_value
            if query_str_name == '':
                query_str_name = query_str_name + 'collateral_value'
                query_str_value = query_str_value + collateral_value
        if query_str_name != '':
            query_str_name = query_str_name + ', photo'
            query_str_value = query_str_value + ', ' + '\'' + photo_name + '\''
        if query_str_name == '':
            query_str_name = query_str_name + 'photo'
            query_str_value = query_str_value + '\'' + photo_name + '\''
        query_str = query_str + query_str_name + ') VALUES (' + query_str_value + ')'

        connected = sqlite3.connect(path_db)
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        #tools = cursor.fetchall()
        print("Запись успешно вставлена в таблицу tools ", cursor.rowcount)
        cursor.close()
        connected.close()

        print(query_str)

        return redirect('/tools')
    else:
        return redirect('/tools')


#обработчик редактирования клиента
@app.route('/clients_edit/<int:id>', methods=['POST', 'GET'])
def clients_edit(id):
    if request.method == "POST":
        surname = request.form['surname'].strip()
        surname = surname.lower()
        name = request.form['name'].strip()
        name = name.lower()
        middle_name = request.form['middle_name'].strip()
        middle_name = middle_name.lower()
        phone = request.form['phone']
        gos_n = request.form['gos_n'].strip()
        gos_n = gos_n.lower()
        company = request.form['company'].strip()
        company = company.lower()
        description = request.form['description'].strip()
        description = description.lower()

        query_str = ''   #собираем строку для запроса

        if type:
            query_str = (f'surname = \'{surname}\'')
        if name:
            if query_str != '':
                query_str = query_str + (f', name = \'{name}\'')
            if query_str == '':
                query_str = query_str + (f'name = \'{name}\'')
        if middle_name:
            if query_str != '':
                query_str = query_str + (f', middle_name = \'{middle_name}\'')
            if query_str == '':
                query_str = query_str + (f'middle_name = \'{middle_name}\'')
        if phone == '':
            if query_str != '':
                query_str = query_str + (f', phone = \'8xxxxxxxxxx\'')
            if query_str == '':
                query_str = query_str + (f'phone = \'8xxxxxxxxxx\'')
        elif phone:
            if query_str != '':
                query_str = query_str + (f', phone = \'{phone}\'')
            if query_str == '':
                query_str = query_str + (f'phone = \'{phone}\'')
        if gos_n:
            if query_str != '':
                query_str = query_str + (f', gos_n = \'{gos_n}\'')
            if query_str == '':
                query_str = query_str + (f'gos_n = \'{gos_n}\'')
        if company:
            if query_str != '':
                query_str = query_str + (f', company = \'{company}\'')
            if query_str == '':
                query_str = query_str + (f'company = \'{company}\'')
        if description == '':
            if query_str != '':
                query_str = query_str + (f', description = \'\'')
            elif query_str == '':
                query_str = query_str + (f'description = \'\'')
        elif description:
            if query_str != '':
                query_str = query_str + (f', description = \'{description}\'')
            elif query_str == '':
                query_str = query_str + (f'description = \'{description}\'')
        query_str = (f'UPDATE clients SET {query_str} WHERE id={id}')
        print(query_str)
        connected = sqlite3.connect(path_db)#подключаемся к базе и делаем запрос
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        print("Запись успешно вставлена в таблицу tools ", cursor.rowcount)
        cursor.close()
        connected.close()
        return redirect('/all_clients')
    else:
        return redirect('/all_clients')


#обработчик редактирования проката
@app.route('/rental_edit/<int:id>', methods=['POST', 'GET'])
def rental_edit(id):
    if request.method == "POST":
        client_id = int(request.form['client_id'])
        tool_id = int(request.form['tool_id'])
        date_take = request.form['date_take']
        date_plane_return = request.form['date_plane_return']
        print(date_plane_return)
        date_return = request.form['date_return']
        print(date_return)#вставить условия для локации
        collateral = request.form['collateral']
        summ = request.form['summ']
        description = request.form['description'].strip()
        description = description.lower()

        query_str = ''   #собираем строку для запроса

        if type:
            query_str = (f'client_id = {client_id}')
        if tool_id:
            if query_str != '':
                query_str = query_str + (f', tool_id = {tool_id}')
            if query_str == '':
                query_str = query_str + (f'tool_id = {tool_id}')
        if date_take:
            if query_str != '':
                query_str = query_str + (f', date_take = \'{date_take}\'')
            if query_str == '':
                query_str = query_str + (f'date_take = \'{date_take}\'')
        if date_plane_return:
            if query_str != '':
                query_str = query_str + (f', date_plane_return = \'{date_plane_return}\'')
            if query_str == '':
                query_str = query_str + (f'date_plane_return = \'{date_plane_return}\'')
        if date_return == '':
            query_str_1 = (f'UPDATE tools SET location=1 WHERE id={tool_id}')
            if query_str != '':
                query_str = query_str + (f', date_return = \'-\'')
            if query_str == '':
                query_str = query_str + (f'date_return = \'-\'')
        elif date_return:
            query_str_1 = (f'UPDATE tools SET location=0 WHERE id={tool_id}')
            if query_str != '':
                query_str = query_str + (f', date_return = \'{date_return}\'')
            if query_str == '':
                query_str = query_str + (f'date_return = \'{date_return}\'')
        if collateral == '':
            if query_str != '':
                query_str = query_str + (f', collateral = 0')
            if query_str == '':
                query_str = query_str + (f'collateral = 0')
        if collateral:
            if query_str != '':
                query_str = query_str + (f', collateral = {collateral}')
            if query_str == '':
                query_str = query_str + (f'collateral = {collateral}')
        if summ == '':
            if query_str != '':
                query_str = query_str + (f', summ = 0')
            if query_str == '':
                query_str = query_str + (f'summ = 0')
        elif summ:
            if query_str != '':
                query_str = query_str + (f', summ = {summ}')
            if query_str == '':
                query_str = query_str + (f'summ = {summ}')
        if description == '':
            if query_str != '':
                query_str = query_str + (f', description = \'-\'')
            elif query_str == '':
                query_str = query_str + (f'description = \'-\'')
        elif description:
            if query_str != '':
                query_str = query_str + (f', description = \'{description}\'')
            elif query_str == '':
                query_str = query_str + (f'description = \'{description}\'')
        query_str = (f'UPDATE rentals SET {query_str} WHERE id={id}')
        print(query_str)
        connected = sqlite3.connect(path_db)#подключаемся к базе и делаем запрос
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        print("Запись успешно вставлена в таблицу tools ", cursor.rowcount)
        cursor.close()
        cursor_1 = connected.cursor()
        cursor_1.execute(query_str_1)
        connected.commit()
        print("Запись успешно вставлена в таблицу tools ", cursor_1.rowcount)
        cursor_1.close()
        connected.close()
        return redirect('/rentals')
    else:
        return redirect('/rentals')


#обработчик редактирования оборудования
@app.route('/tools_edit/<int:id>', methods=['POST', 'GET'])
def tools_edit(id):
    if request.method == "POST":
        photo = request.files['photo'] #получим объект картинки
        photo_name_old = request.form['photo_name']
        if photo:                      #если файл есть
            photo_name = photo.filename    #достанем имя картинки
            print(photo_name_old)
            if os.path.isfile(f'_internal/_internal/images/{photo_name_old}' and photo_name_old != 'default.jpg'):#проверка есть ли в папке файл с предыдущим именем  и если название не дефолтное
                os.remove(f'_internal/_internal/images/{photo_name_old}') #удаляем его, чтоб не захламлять папку
            photo_name = secure_filename(photo_name)#проверим безопасно ли имя файла и убираем русские символы
            #print(photo_name)
            if os.path.splitext(photo_name)[1] == '':#если имя получилось пустое
                photo_name = str(random.randint(1,999999999)) + '.' + os.path.splitext(photo_name)[0]#даем ему рандомное из цыфр
                #print(photo_name)
            isExist = os.path.exists(f'_internal/_internal/images/{photo_name}') #проверим есть ли файл с таким именем в папке картинок
            #print(isExist)
            if isExist == True:#если такое имя есть
                photo_name = os.path.splitext(photo_name)[0] + '_1' + os.path.splitext(photo_name)[1]              #добавим к имени (1)
                #print(photo_name)
            photo.save(os.path.join('_internal/_internal/images/', photo_name))#сохраняем в папку
        else: photo_name = request.form['photo_name']#если файл не передан, то берем его старое название

        #print(photo_name)  #проверить

        type = request.form['type'].strip() #получаем данные со всех остальных полей
        type = type.lower()
        brand = request.form['brand'].strip()
        brand = brand.lower()
        model = request.form['model'].strip()
        model = model.lower()
        serial_number = request.form['serial_number'].strip()
        serial_number = serial_number.lower()
        purchase_value = request.form['purchase_value']
        purchase_date = request.form['purchase_date']
        description = request.form['description'].strip()
        description = description.lower()
        keywords = request.form['keywords'].strip()
        keywords = keywords.lower()
        rent_day_value = request.form['rent_day_value']
        rent_hour_value = request.form['rent_hour_value']
        collateral_value = request.form['collateral_value']

        query_str = ''   #собираем строку для запроса

        if type:
            query_str = (f'type = \'{type}\'')
        if brand:
            if query_str != '':
                query_str = query_str + (f', brand = \'{brand}\'')
            if query_str == '':
                query_str = query_str + (f'brand = \'{brand}\'')
        if model:
            if query_str != '':
                query_str = query_str + (f', model = \'{model}\'')
            if query_str == '':
                query_str = query_str + (f'model = \'{model}\'')
        if serial_number == '':
            if query_str != '':
                query_str = query_str + (f', serial_number = \'б/н\'')
            if query_str == '':
                query_str = query_str + (f'serial_number = \'б/н\'')
        elif serial_number:
            if query_str != '':
                query_str = query_str + (f', serial_number = \'{serial_number}\'')
            if query_str == '':
                query_str = query_str + (f'serial_number = \'{serial_number}\'')
        if purchase_value:
            if query_str != '':
                query_str = query_str + (f', purchase_value = {purchase_value}')
            if query_str == '':
                query_str = query_str + (f'purchase_value = {purchase_value}')
        if purchase_date:
            if query_str != '':
                query_str = query_str + (f', purchase_date = \'{purchase_date}\'')
            if query_str == '':
                query_str = query_str + (f'purchase_date = \'{purchase_date}\'')
        if description == '':
            if query_str != '':
                query_str = query_str + (f', description = \'\'')
            elif query_str == '':
                query_str = query_str + (f'description = \'\'')
        elif description:
            if query_str != '':
                query_str = query_str + (f', description = \'{description}\'')
            elif query_str == '':
                query_str = query_str + (f'description = \'{description}\'')
        if keywords == '':
            if query_str != '':
                query_str = query_str + (f', keywords = \'\'')
            if query_str == '':
                query_str = query_str + (f'keywords = \'\'')
        elif keywords:
            if query_str != '':
                query_str = query_str + (f', keywords = \'{keywords}\'')
            if query_str == '':
                query_str = query_str + (f'keywords = \'{keywords}\'')
        if rent_day_value:
            if query_str != '':
                query_str = query_str + (f', rent_day_value = {rent_day_value}')
            if query_str == '':
                query_str = query_str + (f'rent_day_value = {rent_day_value}')
        if rent_hour_value:
            if query_str != '':
                query_str = query_str + (f', rent_hour_value = {rent_hour_value}')
            if query_str == '':
                query_str = query_str + (f'rent_hour_value = {rent_hour_value}')
        if collateral_value:
            if query_str != '':
                query_str = query_str + (f', collateral_value = {collateral_value}')
            if query_str == '':
                query_str = query_str + (f'collateral_value = {collateral_value}')
        if query_str == '':
            query_str = query_str + (f'photo = \'{photo_name}\'')
        else:
            query_str = query_str + (f', photo = \'{photo_name}\'')
        query_str = (f'UPDATE tools SET {query_str} WHERE id={id}')

        connected = sqlite3.connect(path_db)#подключаемся к базе и делаем запрос
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        #tools = cursor.fetchall()
        print("Запись успешно вставлена в таблицу tools ", cursor.rowcount)
        cursor.close()
        connected.close()

        print(query_str)

        return redirect('/tools')
    else:
        return redirect('/tools')


#обработчик отправки на ремонт из списка оборудования
@app.route('/tool_renovation/<int:id>', methods=['POST', 'GET'])
def tool_renovation(id):
    if request.method == "POST":

        work_type = request.form['work_type'].strip()
        work_type = work_type.lower()
        date_for_repair = request.form['date_for_repair']
        description = request.form['description'].strip()
        description = description.lower()

        query_str = 'INSERT INTO renovations ('
        query_str_name = ''
        query_str_value = ''
        if id:
            query_str_name = query_str_name + 'tool_id'
            query_str_value = query_str_value + str(id)
        if work_type:
            if query_str_name != '':
                query_str_name = query_str_name + ', work_type'
                query_str_value = query_str_value + ', ' + '\'' + work_type + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'work_type'
                query_str_value = query_str_value + '\'' + work_type + '\''
        if date_for_repair:
            if query_str_name != '':
                query_str_name = query_str_name + ', date_for_repair'
                query_str_value = query_str_value + ', ' + '\'' + date_for_repair + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'date_for_repair'
                query_str_value = query_str_value + '\'' + date_for_repair + '\''
        if description:
            if query_str_name != '':
                query_str_name = query_str_name + ', description'
                query_str_value = query_str_value + ', ' + '\'' + description + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'description'
                query_str_value = query_str_value + '\'' + description + '\''

        query_str = query_str + query_str_name + ') VALUES (' + query_str_value + ')'
        query_str_1 = (f'UPDATE tools SET location=2 WHERE id={id}')
        connected = sqlite3.connect(path_db)#подключаемся к базе и делаем запрос
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        print("Запись успешно вставлена в таблицу tools ", cursor.rowcount)
        cursor.close()
        cursor_1 = connected.cursor()
        cursor_1.execute(query_str_1)
        connected.commit()
        print("Запись успешно вставлена в таблицу tools ", cursor.rowcount)
        cursor_1.close()
        connected.close()

        print(query_str)

        return redirect('/tools')
    else:
        return redirect('/tools')


#обработчик отправки на ремонт из списка оборудования
@app.route('/tool_rn/<int:id>', methods=['POST', 'GET'])
def tool_rn(id):
    if request.method == "POST":

        work_type = request.form['work_type'].strip()
        work_type = work_type.lower()
        date_for_repair = request.form['date_for_repair']
        date_from_repair = request.form['date_for_repair']
        summ = request.form['summ']
        description = request.form['description'].strip()
        description = description.lower()
        count = request.form.get('count')
        query_str = 'INSERT INTO renovations ('
        query_str_name = ''
        query_str_value = ''
        if id:
            query_str_name = query_str_name + 'tool_id'
            query_str_value = query_str_value + str(id)
        if work_type:
            if query_str_name != '':
                query_str_name = query_str_name + ', work_type'
                query_str_value = query_str_value + ', ' + '\'' + work_type + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'work_type'
                query_str_value = query_str_value + '\'' + work_type + '\''
        if date_for_repair:
            if query_str_name != '':
                query_str_name = query_str_name + ', date_for_repair'
                query_str_value = query_str_value + ', ' + '\'' + date_for_repair + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'date_for_repair'
                query_str_value = query_str_value + '\'' + date_for_repair + '\''
        if date_from_repair:
            if query_str_name != '':
                query_str_name = query_str_name + ', date_from_repair'
                query_str_value = query_str_value + ', ' + '\'' + date_from_repair + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'date_from_repair'
                query_str_value = query_str_value + '\'' + date_from_repair + '\''
        if summ:
            if query_str_name != '':
                query_str_name = query_str_name + ', summ'
                query_str_value = query_str_value + ', ' + summ
            if query_str_name == '':
                query_str_name = query_str_name + 'summ'
                query_str_value = query_str_value + summ
        if description:
            if query_str_name != '':
                query_str_name = query_str_name + ', description'
                query_str_value = query_str_value + ', ' + '\'' + description + '\''
            if query_str_name == '':
                query_str_name = query_str_name + 'description'
                query_str_value = query_str_value + '\'' + description + '\''

        query_str = query_str + query_str_name + ') VALUES (' + query_str_value + ')'
        connected = sqlite3.connect(path_db)#подключаемся к базе и делаем запрос
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        print("Запись успешно вставлена в таблицу tools ", cursor.rowcount)
        cursor.close()
        if count:
            cursor_1 = connected.cursor()
            cursor_1.execute(f'UPDATE tools SET count_day = 0 WHERE id={id}')
            connected.commit()
            print("Запись успешно вставлена в таблицу tools ", cursor.rowcount)
            cursor_1.close()

        connected.close()


        return redirect(f'/tool/{id}')
    else:
        return redirect(f'/tool/{id}')


#обработчик удаления клиента
@app.route('/clients_del/<int:id>', methods=['POST', 'GET'])
def clients_del(id):
    if request.method == "POST":
        query_str = (f'DELETE FROM clients WHERE id={id}')
        connected = sqlite3.connect(path_db)
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        print("Запись успешно удалена из таблицы clients ", cursor.rowcount)
        cursor.close()
        connected.close()

        print(query_str)

        return redirect('/all_clients')
    else:
        return redirect('/all_clients')


#обработчик удаления оборудования
@app.route('/tools_del/<int:id>', methods=['POST', 'GET'])
def tools_del(id):
    if request.method == "POST":
        query_str = (f'DELETE FROM tools WHERE id={id}')
        connected = sqlite3.connect(path_db)
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        # tools = cursor.fetchall()
        print("Запись успешно удалена из таблицы tools ", cursor.rowcount)
        cursor.close()
        connected.close()

        print(query_str)

        return redirect('/tools')
    else:
        return redirect('/tools')


#обработчик удаления проката
@app.route('/rental_del/<int:id>', methods=['POST', 'GET'])
def rental_del(id):
    if request.method == "POST":
        tool_id = request.form['tool_id']
        query_str = (f'DELETE FROM rentals WHERE id={id}')
        query_str_1 = (f'UPDATE tools SET location=0 WHERE id={tool_id}')
        connected = sqlite3.connect(path_db)
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        # tools = cursor.fetchall()
        print("Запись успешно удалена из таблицы tools ", cursor.rowcount)
        cursor.close()
        cursor_1 = connected.cursor()
        cursor_1.execute(query_str_1)
        connected.commit()
        print("Запись успешно вставлена в таблицу tools ", cursor_1.rowcount)
        cursor_1.close()
        connected.close()

        return redirect('/rentals')
    else:
        return redirect('/rentals')



# Страница всех ремонтов
@app.route('/renovations', methods=['POST', 'GET'])
def renovations():
    if request.method == "POST":
        search_text = request.form['search_text'].strip()
        if search_text == '':
            field = ''
        else:
            s_t = search_text.lower()
            try:
                field = (
                    f'WHERE rn.id = {int(search_text)} OR t.type LIKE \'%{s_t}%\' OR t.brand LIKE \'%{s_t}%\' OR t.model LIKE \'%{s_t}%\' OR t.serial_number LIKE \'%{s_t}%\' OR rn.work_type LIKE \'%{s_t}%\' OR rn.description LIKE \'%{s_t}%\' OR rn.summ LIKE \'%{s_t}%\'')
            except:

                # s_t = search_text
                field = (
                    f'WHERE t.type LIKE \'%{s_t}%\' OR t.brand LIKE \'%{s_t}%\' OR t.model LIKE \'%{s_t}%\' OR t.serial_number LIKE \'%{s_t}%\' OR rn.work_type LIKE \'%{s_t}%\' OR rn.description LIKE \'%{s_t}%\' OR rn.summ LIKE \'%{s_t}%\'')
                print(field)

        connected = sqlite3.connect(path_db)
        cursor = connected.cursor()
        try:
            cursor.execute(f'select rn.id, rn.tool_id, t.type, t.brand, t.model, t.serial_number, rn.work_type, rn.date_for_repair, rn.date_from_repair, rn.summ, rn.description from renovations AS rn JOIN tools AS t ON t.id = rn.tool_id {field}')
            renovations = cursor.fetchall()
        except:
            renovations = ()
        connected.close()
        return render_template("renovations.html", renovations=renovations, search_text=search_text)
    else:
        connected = sqlite3.connect(path_db)
        cursor = connected.cursor()
        try:
            cursor.execute(f"select rn.id, rn.tool_id, t.type, t.brand, t.model, t.serial_number, rn.work_type, rn.date_for_repair, rn.date_from_repair, rn.summ, rn.description from renovations AS rn JOIN tools AS t ON t.id = rn.tool_id")
            renovations = cursor.fetchall()
        except:
            renovations = ()
        connected.close()
        search_text = ''
        return render_template("renovations.html", renovations=renovations, search_text=search_text)
        print(rentals)


#обработчик удаления ремонта
@app.route('/renovation_del/<int:id>', methods=['POST', 'GET'])
def renovation_del(id):
    if request.method == "POST":
        query_str = (f'DELETE FROM renovations WHERE id={id}')
        connected = sqlite3.connect(path_db)
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        print("Запись успешно удалена из таблицы renovations ", cursor.rowcount)
        cursor.close()
        connected.close()

        return redirect('/renovations')
    else:
        return redirect('/renovations')


#обработчик редактирования ремонта
@app.route('/renovation_edit/<int:id>', methods=['POST', 'GET'])
def renovation_edit(id):
    if request.method == "POST":
        tool_id = request.form['tool_id']
        work_type = request.form['work_type'].strip()
        work_type = work_type.lower()
        date_for_repair = request.form['date_for_repair']
        date_from_repair = request.form['date_from_repair']
        description = request.form['description'].strip()
        description = description.lower()
        summ = request.form['summ']

        query_str = ''   #собираем строку для запроса

        if work_type:
            query_str = (f'work_type = \'{work_type}\'')
        if date_for_repair:
            if query_str != '':
                query_str = query_str + (f', date_for_repair = \'{date_for_repair}\'')
            if query_str == '':
                query_str = query_str + (f'date_for_repair = \'{date_for_repair}\'')
        if date_from_repair == '':
            if query_str != '':
                query_str = query_str + (f', date_from_repair = \'\'')
            if query_str == '':
                query_str = query_str + (f'date_from_repair = \'\'')
        elif date_from_repair:
            if query_str != '':
                query_str = query_str + (f', date_from_repair = \'{date_from_repair}\'')
            if query_str == '':
                query_str = query_str + (f'date_from_repair = \'{date_from_repair}\'')
        if description == '':
            if query_str != '':
                query_str = query_str + (f', description = \'-\'')
            elif query_str == '':
                query_str = query_str + (f'description = \'-\'')
        elif description:
            if query_str != '':
                query_str = query_str + (f', description = \'{description}\'')
            elif query_str == '':
                query_str = query_str + (f'description = \'{description}\'')
        if summ:
            if query_str != '':
                query_str = query_str + (f', summ = {summ}')
            if query_str == '':
                query_str = query_str + (f'summ = {summ}')
        query_str = (f'UPDATE renovations SET {query_str} WHERE id={id}')
        connected = sqlite3.connect(path_db)#подключаемся к базе и делаем запрос
        cursor = connected.cursor()
        cursor.execute(query_str)
        connected.commit()
        print("Запись успешно вставлена в таблицу tools ", cursor.rowcount)
        cursor.close()
        if date_from_repair == '':
            query_str_1 = (f'UPDATE tools SET location=2 WHERE id={tool_id}')
            cursor_1 = connected.cursor()
            cursor_1.execute(query_str_1)
            connected.commit()
            print("Запись успешно вставлена в таблицу tools ", cursor.rowcount)
            cursor_1.close()
        elif date_from_repair != '':
            query_str_1 = (f'UPDATE tools SET location=0 WHERE id={tool_id}')
            cursor_1 = connected.cursor()
            cursor_1.execute(query_str_1)
            connected.commit()
            print("Запись успешно вставлена в таблицу tools ", cursor.rowcount)
            cursor_1.close()
        connected.close()
        return redirect('/renovations')
    else:
        return redirect('/renovations')


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=server_port)