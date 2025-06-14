import telebot
import sqlite3
from telebot import types
from datetime import datetime

bot = telebot.TeleBot("6642115715:AAE4uQUdVYNryZD8e5HijvjlzexHEw1Ipok")

# Подключение к базе данных (или создание новой, если она не существует)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создание таблицы для хранения данных пользователя
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    date_added TEXT
)
''')

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

# Функция для добавления пользователя в базу данных
def add_user_to_db(user_id, username, first_name, last_name):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Добавление пользователя в таблицу
    cursor.execute('''
    INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, date_added)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    conn.commit()
    conn.close()

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Основные документы гражданина Российской Федерации")
    #item2 = types.KeyboardButton(text="Семья в России")
    #item3 = types.KeyboardButton(text="Живу в России")
    #item4 = types.KeyboardButton(text="Быть здоровым")
    #item5 = types.KeyboardButton(text="Дом в России")
    item6 = types.KeyboardButton(text="Работаю в России")
    item7 = types.KeyboardButton(text="Дети и образование")
    item8 = types.KeyboardButton(text="Служу России")
    item9 = types.KeyboardButton(text="Вожу в России")
    #item10 = types.KeyboardButton(text="Молодость в России")
    #item11 = types.KeyboardButton(text="Поддержка агропромышленного комплекса")
    #item12 = types.KeyboardButton(text="Порядок обращения в правоохранительные органы")
    #item13 = types.KeyboardButton(text="Полезные контакты")
    
    keyboard.add(item1, item6, item7, item8, item9,)

    # Добавление пользователя в базу данных
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    add_user_to_db(user_id, username, first_name, last_name)
    
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! Я бот, который поможет тебе. Что ты хочешь узнать?\n"
        "Здесь можно найти информацию по темам:\n"
        "- Основные документы гражданина Российской Федерации\n"
        "- Работаю в России (пособие по безработице, оформление банковских карт)\n"
        "- Дети и образование (детский садик, школы и вузы)\n"
        "- Служу России (все о долге Родине, военной службе и военном образовании)\n"
        "- Вожу в России (регистрации автомобиля, парковка для инвалидов)\n",
        reply_markup=keyboard,
    )

# Обработчик для основных документов
@bot.message_handler(func=lambda message: message.text == "Основные документы гражданина Российской Федерации")
def handle_main_documents(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    item1 = types.KeyboardButton(text="Паспорт РФ")
    item2 = types.KeyboardButton(text="Регистрация")
    item3 = types.KeyboardButton(text="Загранпаспорт")
    item4 = types.KeyboardButton(text="ИНН")
    item5 = types.KeyboardButton(text="Полис ОМС")
    item6 = types.KeyboardButton(text="СНИЛС")
    item7 = types.KeyboardButton(text="Водительское удостоверение")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, item2, item3, item4, item5, item6, item7, back_button)
    
    bot.send_message(
        message.chat.id,
        "Выберите интересующий вас тип документа:",
        reply_markup=markup,
    )

# Обработчики для каждого типа документа

@bot.message_handler(func=lambda message: message.text == "Паспорт РФ")
def handle_passport_rf(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Кто может получить Паспорт?")
    item2 = types.KeyboardButton(text="Порядок получения")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, item2, back_button)
    
    bot.send_message(
        message.chat.id,
        "Паспорт гражданина РФ - это основной документ, удостоверяющий личность гражданина России на ее территории, паспорт должны иметь все граждане РФ достигшие 14 лет",
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Регистрация")
def handle_registration(message):
    bot.send_message(
        message.chat.id,
        "Регистрация: по месту жительства - постоянная регистрация, не имеющая срока; по месту пребывания - временная регистрация на определенный срок",
    )

@bot.message_handler(func=lambda message: message.text == "Загранпаспорт")
def handle_foreign_passport(message):
    bot.send_message(
        message.chat.id,
        "Заграничный паспорт удостоверяет личность гражданина России в других странах, его можно получить в своем регионе",
    )

@bot.message_handler(func=lambda message: message.text == "ИНН")
def handle_inn(message):
    bot.send_message(
        message.chat.id,
        "ИНН - индивидуальный номер налогоплательщика. Необходим для оплаты налогов, после получения паспорта РФ запрос на ИНН отправляется в налоговый орган автоматически",
    )

@bot.message_handler(func=lambda message: message.text == "Полис ОМС")
def handle_oms_policy(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Кто может получить Полис ОМС?")
    item2 = types.KeyboardButton(text="Что оформить до получения?")
    item3 = types.KeyboardButton(text="Порядок получения Полиса ОМС")
    item4 = types.KeyboardButton(text="С полисом можно")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, item2, item3, item4, back_button)
    
    bot.send_message(
        message.chat.id,
        "Полис обязательного медицинского страхования (ОМС) — документ, подтверждающий право на бесплатную медицинскую помощь.",
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text in {"Кто может получить Полис ОМС?", "Что оформить до получения?", "Порядок получения Полиса ОМС", "С полисом можно"})
def handle_oms_policy1(message):
    if message.text == "Кто может получить Полис ОМС?":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton(text="Что оформить до получения?")
        back_button = types.KeyboardButton(text="Назад")
        markup.add(item1, back_button)
        bot.send_message(
            message.chat.id,
            "• Граждане РФ\n"
            "• Иностранцы, постоянно проживающие на территории РФ\n"
            "• Лица без гражданства\n"
            "• Работающие в России граждане стран ЕАЭС.",
            reply_markup=markup,
        )
    elif message.text == "Что оформить до получения?":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("Паспорт")
        item2 = types.KeyboardButton("Свидетельство о рождении")
        item3 = types.KeyboardButton("СНИЛС")
        back_button = types.KeyboardButton(text="Назад")
        markup.add(item1, item2, item3, back_button)
        bot.send_message(
            message.chat.id,
            "• Паспорт РФ — для граждан от 14 лет\n"
            "• Свидетельство о рождении — для детей до 14 лет\n"
            "• Документ, подтверждающий права законного представителя — для законного представителя ребёнка\n"
            "• СНИЛС — для граждан РФ старше 14 лет\n"
            "• Доверенность на получение полиса ОМС в выбранной страховой медицинской организации — для представителя гражданина",
            reply_markup=markup,
        )
    elif message.text == "С полисом можно":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("Кто может получить Полис ОМС?")
        back_button = types.KeyboardButton(text="Назад")
        markup.add(item1, back_button)
        bot.send_message(
            message.chat.id, 
            "Записываться на приём к врачу, бесплатно проходить обследования, делать операции, лечиться в стационаре, вызывать врача на дом на всей территории РФ выбрать любую медицинскую организацию, принимающую с полисом получить информацию о видах, качестве и условиях медицинских услуг лечиться в частных клиниках, если они участвуют в программе ОМС",
            reply_markup=markup,
        )



@bot.message_handler(func=lambda message: message.text == "СНИЛС")
def handle_snils(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Кто может получить СНИЛС?")
    item2 = types.KeyboardButton(text="Зачем нужен СНИЛС?")
    item3 = types.KeyboardButton(text="Порядок получения СНИЛС")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, item2, item3, back_button)
    bot.send_message(
        message.chat.id,
        "СНИЛС - страховой номер индивидуального лицевого счета, необходим для оценки пенсионных прав, оформления соцвыплат, регистрации на госуслугах и получения госуслуг.",
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text in {"Кто может получить СНИЛС?", "Зачем нужен СНИЛС?", "Порядок получения СНИЛС"})
def handle_snils_info(message):
    if message.text == "Кто может получить СНИЛС?":
        bot.send_message(
            message.chat.id,
            "• Гражданин РФ \n"
            "• Иностранец или лицо без гражданства \n"
            "• Представитель по доверенности",
        )
    elif message.text == "Зачем нужен СНИЛС?":
        bot.send_message(
            message.chat.id,
            "СНИЛС нужен при трудоустройстве для пенсионных отчислений, оформления социальных выплат и пособий, а также регистрации на Госуслугах и сайтах ведомств.",
        )
    elif message.text == "Порядок получения СНИЛС":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton(text="Что оформить заранее?")
        back_button = types.KeyboardButton(text="Назад")
        markup.add(item1, back_button)
        bot.send_message(
            message.chat.id, 
            "Для получения СНИЛС требуется обратиться в уполномоченный орган с документами, подтверждающими личность.",
            reply_markup=markup,
        )

@bot.message_handler(func=lambda message: message.text == "Что оформить заранее?")
def handle_snils_info1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Получение")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, back_button)
    bot.send_message(
        message.chat.id,
        "Для получения СНИЛС потребуется один из документов, удостоверяющих личность (ДУЛ): паспорт РФ паспорт ДНР, ЛНР паспорт Украины вид на жительство паспорт иностранного гражданина свидетельство о рождении ребёнка — если оформляете СНИЛС для детей до 14 лет. Дополнительные документы для представителей: Доверенность; ДУЛ человека, интересы которого он представляет, если доверенность не заверена нотариально",
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Получение")
def handle_snils_info2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Проверьте наличие СНИЛСа")
    item2 = types.KeyboardButton(text="Подайте заявление")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, item2, back_button)
    bot.send_message(
        message.chat.id,
        "Переводить документы с украинского языка на русский не нужно Принимаются документы, выданные уполномоченными органами: Украины — до 30 сентября 2022 г. ДНР и ЛНР — с 11 мая 2014 г. по 28 февраля 2023 г. Запорожской и Херсонской областей — с 30 сентября 2022 г. по 28 февраля 2023 гг",
    reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text in {"Проверьте наличие СНИЛСа", "Подайте заявление"})
def handle_snils_info3(message):
    if message.text=="Проверьте наличие СНИЛСа":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton(text="Подайте заявление")
        back_button = types.KeyboardButton(text="Назад")
        markup.add(item1, back_button)
        bot.send_message(
            message.chat.id,
            "Узнайте, есть ли у вас СНИЛС На Госуслугах в разделе «Личные документы» — если у вас есть подтверждённая учётная запись В отделении СФР или ближайшем МФЦ. В некоторых из них нужна предварительная запись — уточните это перед обращением. Возьмите с собой паспорт. Если у вас уже есть СНИЛС, вам распечатают уведомление с его данными — форму АДИ‐РЕГ. Если СНИЛС нет, вы сможете подать заявление на оформление У работодателя — в отделе кадров или у руководителя",
        reply_markup=markup,
    )
    elif message.text=="Подайте заявление":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton(text="При посещении СФР и МФЦ")
        item2 = types.KeyboardButton(text="Через работодателя")
        back_button = types.KeyboardButton(text="Назад")
        markup.add(item1, item2, back_button)
        bot.send_message(
            message.chat.id,
            "Выберите подходящий вам вариант ниже.",
        reply_markup=markup,
        )

@bot.message_handler(func=lambda message: message.text in {"При посещении СФР и МФЦ", "Через работодателя"})
def handle_snils_info4(message):
    if message.text=="При посещении СФР и МФЦ":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        back_button = types.KeyboardButton(text="Назад")
        markup.add(back_button)
        bot.send_message(
            message.chat.id,
            "Выберите СФР или МФЦ Возьмите необходимые документы Заполните заявление на приёме ИЛС откроют и сразу распечатают форму АДИ‐РЕГ с данными СНИЛС. Либо назначат дату, когда вы сможете прийти, чтобы его узнать, но не позднее 5 рабочих дней со дня визита",
        reply_markup=markup,
        )
    elif message.text=="Через работодателя":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        back_button = types.KeyboardButton(text="Назад")
        markup.add(back_button)
        bot.send_message(
            message.chat.id,
            "Обратитесь с просьбой оформить СНИЛС Работодатель подготовит и направит пакет документов в отделение СФР В течение 5 рабочих дней СФР уведомит работодателя о регистрации в системе индивидуального учёта и присвоении СНИЛС Работодатель сообщит вам СНИЛС и прикрепит его к личному делу",
        reply_markup=markup,
        )

@bot.message_handler(func=lambda message: message.text == "Водительское удостоверение")
def handle_driver_license(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Порядок получения")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, back_button)
    bot.send_message(
        message.chat.id,
        "Иностранное водительское удостоверение на территории РФ можно использовать в пределах срока, на который оно выдано Чтобы использовать авто для трудовой, предпринимательской или другой деятельности, связанной с получением дохода, потребуется российское водительское удостоверение Подать заявление на обмен водительского удостоверения можно в упрощённом порядке до 1 января 2026 г. или на общих основаниях Услугу не могут получить люди, которые ранее никогда не имели водительского удостоверения, выданного на Украине",
    reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Порядок получения")
def handle_driver_license1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Гражданам Украины и людям без гражданства")
    item2 = types.KeyboardButton(text="Жителям Херсонской области")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, item2, back_button)
    bot.send_message(
        message.chat.id,
        "Выберите подходящий вам вариант ниже.",
    reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text in {"Гражданам Украины и людям без гражданства", "Жителям Херсонской области"})
def handle_driver_license2(message):
    if message.text=="Гражданам Украины и людям без гражданства":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("Если потеряли водительское удостоверение")
        back_button = types.KeyboardButton(text="Назад")
        markup.add(item1, back_button)
        bot.send_message(
            message.chat.id,
            "1.Подготовьте документы.  Любой из документов:  • разрешение на временное проживание в РФ • вид на жительство РФ  • удостоверение беженца  • свидетельство о предоставлении временного убежища на территории РФ  • свидетельство участника Госпрограммы переселения соотечественников в РФ, постоянно проживающих на территории Украины  • Водительское удостоверение Украины, ДНР или ЛНР  • Справку о прохождении медосмотра образца 003-В/у  2.Приходите на приём в ГИБДД  Подать заявление можно лично в любом подразделении ГИБДД. С собой возьмите все документы, необходимые для получения услуги На приёме сотрудники ведомства примут оригиналы документов, сфотографируют вас и выдадут российское водительское удостоверение",
        reply_markup=markup,
        )
    elif message.text=="Жителям Херсонской области":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("Если потеряли водительское удостоверение")
        back_button = types.KeyboardButton(text="Назад")
        markup.add(item1, back_button)
        bot.send_message(
            message.chat.id,
            "1.Подготовьте документы.  • Паспорт РФ или вид на жительство в РФ  • Документы, подтверждающие постоянное проживание на территории Херсонской области  • Водительское удостоверение Украины, ДНР или ЛНР  2.Приходите на приём в ГИБДД  Подать заявление можно лично в любом подразделении ГИБДД. С собой возьмите все документы, необходимые для получения услуги На приёме сотрудники ведомства примут оригиналы документов, сфотографируют вас и выдадут российское водительское удостоверение",
        reply_markup=markup,
        )
    
@bot.message_handler(func=lambda message: message.text == "Если потеряли водительское удостоверение")
def handle_driver_license3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)
    bot.send_message(
        message.chat.id, 
        "Если потеряли водительское удостоверение Нужно предоставить любые документы, подтверждающие его выдачу. Например, водительскую карточку или свидетельство об обучении по программе подготовки водителей, где указан номер ранее выданного удостоверения. Если таких документов нет, уточнить порядок получения можно лично в ГИБДД",
    reply_markup=markup,
    )





#Блок Вожу в России

# Обработчик для кнопки "Вожу в России"
@bot.message_handler(func=lambda message: message.text == "Вожу в России")
def handle_driving_in_russia(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Перерегистрировать автомобиль")
    item2 = types.KeyboardButton(text="Получение водительского удостоверения впервые")
    item3 = types.KeyboardButton(text="Водительские права категории А и А1")
    item4 = types.KeyboardButton(text="Обмен иностранного водительского удостоверения")
    item5 = types.KeyboardButton(text="Компенсация стоимости полиса ОСАГО инвалидам")
    item6 = types.KeyboardButton(text="Предоставление парковки на местах для инвалидов")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, item2, item3, item4, item5, item6, back_button)
    bot.send_message(
        message.chat.id,
        "Выберите подходящий вам вариант ниже.",
        reply_markup=markup,
    )

# Обработчик для кнопки "Перерегистрировать автомобиль"
@bot.message_handler(func=lambda message: message.text == "Перерегистрировать автомобиль")
def handle_vehicle_re_registration(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Что нужно оформить до получения?")
    item2 = types.KeyboardButton(text="Кто может получить услугу?")
    item3 = types.KeyboardButton(text="Порядок действий")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, item2, item3, back_button)
    
    text_message = """
    Жителям Херсонской области нужно перерегистрировать личный транспорт — заменить документы на автомобиль и госномера, выданные до 14 декабря 2022 г. Это можно сделать без госпошлины, таможенных документов и техосмотра. Такая опция доступна до 1 января 2026 г. До 1 января 2025 г. полис обязательного страхования автогражданской ответственности (ОСАГО) не нужен при поездках по новым регионам РФ. Но выезжать без полиса ОСАГО в другие субъекты РФ нельзя — вас могут оштрафовать
    """
    
    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

# Обработчик для кнопки "Что нужно оформить до получения?"
@bot.message_handler(func=lambda message: message.text == "Что нужно оформить до получения?")
def handle_what_to_prepare(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)
    
    text_message = """
    До получения нужно оформить:
    - гражданам — паспорт РФ или вид на жительство в России
    - организациям — встать на учёт в налоговом органе: для перерегистрации понадобятся сведения из ЕГРЮЛ о местонахождении на территории Херсонской области
    """
    
    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

# Обработчик для кнопки "Кто может получить услугу?"
@bot.message_handler(func=lambda message: message.text == "Кто может получить услугу?")
def handle_who_can_get_service(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)
    
    text_message = """
    Получить услугу могут:
    - граждане РФ, иностранцы и лица без гражданства, которые ранее постоянно проживали в Херсонской области на день ее принятия в состав России. жители, кто ранее постоянно проживал в херсонской области, но выехал на другую территорию России;
    - организации, зарегистрированные на указанных территориях на день их принятия в состав России.
    """
    
    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

# Обработчик для кнопки "Порядок действий"
@bot.message_handler(func=lambda message: message.text == "Порядок действий")
def handle_procedure(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)
    
    text_message = """
    Порядок действий:
    1. Подготовьте документы:
       - паспорт РФ или вид на жительство в России;
       - организациям — выписку из ЕГРЮЛ с указанием местонахождения;
       - документы, подтверждающие постоянное проживание на территории Херсонской области, например: паспорт РФ с отметкой о регистрации по месту жительства;
       - выписку из реестра по месту пребывания;
       - регистрационные документы и госномера, выданные до 14 декабря 2022 г. компетентными органами Украины, при их отсутствии — другие документы, которые подтвердят ранее оформленную регистрацию автомобиля;
       - при необходимости — документы, подтверждающие полномочия заявителя на владение автомобилем или представление интересов собственника. Например, это могут быть договор лизинга или доверенность. Эти документы также должны быть оформлены до 14 декабря 2022 г. в соответствии с действовавшим законодательством Украины и Херсонской областей. Постановление Правительства от 02.12.2022 n 2216, п. 1, подп. А, Б.
    2. Подайте заявление:
       - в удобном подразделении Госавтоинспекции Херсонской области. С собой возьмите все документы, необходимые для получения услуги. Можно подойти в порядке живой очереди или заранее записаться по телефону — такая запись возможна только для жителей новых субъектов РФ;
       - в столице другого региона РФ. Таблица с адресами, где такое заявление примут, есть на сайте ГИБДД.
    3. Предъявите автомобиль к осмотру. Инспектор осмотрит ваш автомобиль в день обращения на площадке у ГИБДД.
    4. Получите документы о перерегистрации:
       - в день обращения вы получите новые регистрационные документы. Вся процедура занимает около часа;
       - номерные знаки — таблички с госномером, которые нужно установить на транспортном средстве, — выдадут сразу, если обращаетесь в отделение по месту постоянного проживания;
       - при обращении в другом регионе — выдадут СТС, инспектор присвоит госномер, но таблички не выдаст. За ними придётся обратиться к изготовителю номерных знаков. При его посещении возьмите СТС с присвоенным госномером.
    """
    
    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

# Обработчик для кнопки "Получение водительского удостоверения впервые"
@bot.message_handler(func=lambda message: message.text == "Получение водительского удостоверения впервые")
def getting_a_drivers_license_for_the_first_time(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Что подготовить?")
    item2 = types.KeyboardButton(text="Право на управление транспортным средством")
    item3 = types.KeyboardButton(text="Порядок действий")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, item2, item3, back_button)

    text_message = """
    Получить водительские права в России может любой человек старше 16 лет. Для разных категорий транспортных средств разные требования Чтобы получить права, нужно отучиться в автошколе и сдать экзамен в ГИБДД. Для открытия новой категории придётся сдавать экзамен ещё раз
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Что подготовить?")
def getting_a_drivers_license_for_the_first_time1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    - Паспорт РФ. Также подготовьте загранпаспорт, если для вас важно, чтобы в российских правах была такая же транслитерация, как в нём. 
    - Медицинская справка по форме 003-В/у. 
    - Документ о прохождении обучения в автошколе. 
    - Письменное согласие законных представителей — для несовершеннолетних.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Право на управление транспортным средством")
def getting_a_drivers_license_for_the_first_time2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    - С 16 лет на управление лёгкими мотоциклами (А1) и мопедами (М). 
    - С 18 лет на мотоциклы (А), легковые (В) и грузовые (С) автомобили. 
    - С 21 года на автобусы (D) . 
    - Получить права на управление автобусами и автомобилями с тяжёлыми прицепами (ВЕ, СЕ и DE) можно только после года водительского стажа с соответствующей категорией без прицепа.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Порядок действий")
def getting_a_drivers_license_for_the_first_time3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    Порядок действий: 
    1. Медицинский осмотр. 
    Для подачи документов в автошколу и в ГИБДД понадобится медицинская справка. Врачи должны проверить, может ли человек водить машину, есть ли какие-то ограничения. Например, в справке могут написать, что разрешается вождение только в очках. Справку оформляют по форме 003-В/у. 
    2. Обучение в автошколе. 
    Перед тем как записываться на экзамен в ГИБДД, нужно пройти обучение в автошколе, сдать теоретический и практический экзамены. По итогам обучения выдадут свидетельство о профессии водителя. Автошкола должна иметь лицензию на образовательную деятельность и аккредитацию от ГИБДД. 
    3. Запись в гибдд. 
    По окончании обучения в автошколе вы должны сдать экзамен в ГИБДД. Записаться на подачу документов можно через Госуслуги — выбрать подходящее подразделение ГИБДД, дату и время посещения. Сотрудник ГИБДД примет документы и назначит дату и время сдачи экзамена. 
    4. Получите водительское удостоверение. 
    После успешной сдачи экзамена сотрудник ГИБДД запишет вас на фотографирование и выдачу прав. Водительские права действуют 10 лет. Для продления сдавать экзамен заново не придётся, но надо будет получить медицинскую справку
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )


@bot.message_handler(func=lambda message: message.text == "Водительские права категории А и А1")
def driving_license_categories_a_and_a1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Условия допуска к экзаменам")
    item2 = types.KeyboardButton(text="Порядок действий")
    item3 = types.KeyboardButton(text="Как получить права на мотоцикл?")
    item4 = types.KeyboardButton(text="Что необходимо для получения категории А?")
    item5 = types.KeyboardButton(text="Оформление документов")
    item6 = types.KeyboardButton(text="Кто может получить?")
    item7 = types.KeyboardButton(text="Государственная пошлина")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, item2, item3, item4, item5, item6, item7, back_button)

    text_message = """
    Права категории А дают возможность управлять мотоциклами, мопедами, трициклами, квадрициклами. Для этого следует пройти обучение в автошколе. Даже если водитель уже открыл категории В и С, то для получения категории А все равно придется посещать курсы.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Условия допуска к экзаменам")
def driving_license_categories_a_and_a1_1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    Прежде чем подавать заявку в ГИБДД на сдачу экзамена, нужно сдать его в автошколе и получить свидетельство о прохождении обучения. Также следует предоставить медсправку и пройти верификацию свидетельства, в том случае, если испытуемый обучался в другом городе.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Порядок действий")
def driving_license_categories_a_and_a1_2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    1. Подать пакет документов в ГИБДД; 
    2.Сдать экзамен; 
    После сдачи практической части экзамена водительское удостоверение выдают в течение месяца. 
    3. Получить водительское удостоверение.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Как получить права на мотоцикл?")
def driving_license_categories_a_and_a1_3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    В 2024 году требуется проходить обучение в автошколе, сдавать теоретическую и практическую часть экзамена.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Что необходимо для получения категории А?")
def driving_license_categories_a_and_a1_4(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Список врачей")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, back_button)

    text_message = """
    Пройти медобследование. 
    Медобследование можно пройти в любой клинике ― частной или муниципальной. Однако если обращаться в платную, то следует уточнить, есть ли у них лицензия на оформление справок для получения водительских прав. Медучреждения, расположенные на территории ГИБДД, автоматически имеют право на оформление подобных справок. Если у обучающегося уже есть права, например, категории В, то ему все равно нужно заново пройти обследование.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Список врачей")
def driving_license_categories_a_and_a1_5(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    -офтальмолога;  
    - терапевта;  
    - нарколога;  
    - психиатра. 
    В результате выдают три справки: 
    общая от офтальмолога и терапевта, по одной от нарколога и психиатра.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )


@bot.message_handler(func=lambda message: message.text == "Оформление документов")
def driving_license_categories_a_and_a1_5(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    Для получения водительского удостоверения необходимо подготовить документы: 
    паспорт; 
    медицинская справка формы n 003-В/у; 
    заявление на получение прав; свидетельство об обучении в автошколе; 
    документ, предоставляющий право на льготу для оплаты госпошлины (если есть); 
    квитанция об оплате госпошлины; 
    действующее водительское удостоверение (если такое есть); 
    если обращается несовершеннолетний ― письменное согласие законных представителей (родители, опекуны).
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )


@bot.message_handler(func=lambda message: message.text == "Кто может получить?")
def driving_license_categories_a_and_a1_5(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    Пройти обучение разрешается уже с 16 лет, а получить права и управлять мотоциклом — с 18 лет.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )


@bot.message_handler(func=lambda message: message.text == "Государственная пошлина")
def driving_license_categories_a_and_a1_5(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    Госпошлину могут не платить: граждане Украины, въехавшие на территорию РФ после 21.02.2022, которые имеют документы, дающие право на проживание в РФ, и желают обменять национальные ВУ на права российского образца;
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )


#Обработчик для кнопки Обмен иностранного водительского удостоверения
@bot.message_handler(func=lambda message: message.text == "Обмен иностранного водительского удостоверения")
def exchange_of_a_foreign_drivers_license(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Жителям Херсонской области")
    item2 = types.KeyboardButton(text="Если потеряли водительское удостоверение")
    item3 = types.KeyboardButton(text="Людям без гражданства")
    item4 = types.KeyboardButton(text="Гражданам России")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, item2, item3, item4, back_button)

    text_message = """
    Иностранное водительское удостоверение на территории РФ можно использовать в пределах срока, на который оно выдано Чтобы использовать авто для трудовой, предпринимательской или другой деятельности, связанной с получением дохода, потребуется российское водительское удостоверение Подать заявление на обмен водительского удостоверения можно в упрощённом порядке до 1 января 2026 г. или на общих основаниях Услугу не могут получить люди, которые ранее никогда не имели водительского удостоверения, выданного на Украине, в ДНР или ЛНР
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Жителям Херсонской области")
def exchange_of_a_foreign_drivers_license2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Что нужно оформить до получения?")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, back_button)

    text_message = """
    Услугу можно получить упрощённо, если вы постоянно жили на этих территориях на день их принятия в РФ или раньше, но выехали в РФ
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Что нужно оформить до получения?")
def exchange_of_a_foreign_drivers_license3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    1. Подготовьте документы. 
    Паспорт РФ или вид на жительство в РФ Документы, подтверждающие постоянное проживание на территории Херсонской области Водительское удостоверение Украины; 
    2. Приходите на приём в ГИБДД. 
    Подать заявление можно лично в любом подразделении ГИБДД. С собой возьмите все документы, необходимые для получения услуги На приёме сотрудники ведомства примут оригиналы документов, сфотографируют вас и выдадут российское водительское удостоверение.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Если потеряли водительское удостоверение")
def exchange_of_a_foreign_drivers_license4(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    Нужно предоставить любые документы, подтверждающие его выдачу. Например, водительскую карточку или свидетельство об обучении по программе подготовки водителей, где указан номер ранее выданного удостоверения. Если таких документов нет, уточнить порядок получения можно лично в ГИБДД.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Людям без гражданства")
def exchange_of_a_foreign_drivers_license4(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    Приходите на приём в ГИБДД Подать заявление можно лично в любом подразделении ГИБДД. 
    С собой возьмите все документы, необходимые для получения услуги На приёме сотрудники ведомства примут оригиналы документов, сфотографируют вас и выдадут российское водительское удостоверение 
    Подготовьте документы любой из документов:  
    - разрешение на временное проживание в РФ; 
    - вид на жительство РФ; 
    - удостоверение беженца; 
    - свидетельство о предоставлении временного убежища на территории РФ; 
    - свидетельство участника Госпрограммы переселения соотечественников в РФ, постоянно проживающих на территории Украины; 
    - водительское удостоверение Украины;
    - справку о прохождении медосмотра образца 003-В/у.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Гражданам России")
def exchange_of_a_foreign_drivers_license5(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    Услугу можно получить упрощённо, если вы приобрели гражданство РФ как гражданин Украины или человек без гражданства, постоянно проживавший на территории Украины, и имеете паспорт РФ 
    1. Подготовьте документы 
    - Паспорт РФ 
    - Водительское удостоверение Украины, ДНР или ЛНР 
    - Справку о прохождении медосмотра образца 003-В/у 
    2. Приходите на приём в ГИБДД 
    Подать заявление можно лично в любом подразделении ГИБДД. С собой возьмите все документы, необходимые для получения услуги. На приёме сотрудники ведомства примут оригиналы документов, сфотографируют вас и выдадут российское водительское удостоверение.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

#Обработчик для кнопки Компенсация стоимости полиса ОСАГО инвалидам
@bot.message_handler(func=lambda message: message.text == "Компенсация стоимости полиса ОСАГО инвалидам")
def exchange_of_a_foreign_drivers_license(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Кто может оформить?")
    item2 = types.KeyboardButton(text="Условия назначения")
    item3 = types.KeyboardButton(text="Порядок действий")
    item4 = types.KeyboardButton(text="Что нужно оформить заранее")
    item5 = types.KeyboardButton(text="Кто не может оформить?")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, item2, item3, item4, item5, back_button)

    text_message = """
    Инвалиды, имеющие транспортные средства в соответствии с медицинскими показаниями, или их законные представители могут оформить компенсацию — 50% от стоимости полиса обязательного страхования автогражданской ответственности (ОСАГО). Выплату можно получить раз в год
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Кто может оформить?")
def exchange_of_a_foreign_drivers_license1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    - Инвалид самостоятельно. 
    - Законный представитель инвалида или ребёнка‐инвалида.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Условия назначения")
def exchange_of_a_foreign_drivers_license2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    - В полисе ОСАГО указано не более двух водителей, помимо инвалида или его законного представителя. 
    - Полис должен быть действителен на момент подачи заявления.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Порядок действий")
def exchange_of_a_foreign_drivers_license3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    Порядок действий: 
    1. Подготовьте документы. 
    - Паспорт РФ 
    - СНИЛС 
    - ИПРА 
    - Действующий полис ОСАГО 
    - Реквизиты банка и номер банковского счёта для перечисления — если хотите получить на него компенсацию 
    Если заявление подаёт представитель инвалида, дополнительно потребуются: 
    - паспорт РФ представителя 
    - документ, подтверждающий полномочия представителя 
    2. Подайте заявление. 
    Без заявления компенсацию назначают, если при заключении договора ОСАГО был указан СНИЛС страхователя или собственника транспортного средства (ТС), а в Социальном фонде (СФР) есть сведения: 
    - о банковском счёте гражданина в кредитной организации 
    - об инвалидности и наличии в ИПРА медицинских показаний для приобретения ТС 
    - о законном представителе, если он выступает страхователем 
    Подать заявление можно любым способом: 
    - на Госуслугах — потребуется подтверждённая учётная запись 
    - в СФР 
    - в МФЦ 
    3. Дождитесь проверки документов. 
    4. Получите компенсацию. 
    Заявление рассмотрят в течение 5 рабочих дней со дня приёма всех документов. Если подавали заявление на Госуслугах, информация о назначении появится в личном кабинете. Выплата в размере 50% от стоимости ОСАГО придёт на указанный в заявлении счёт. В других случаях вас уведомят по телефону или по почте. Компенсацию перечислят в течение 5 рабочих дней с момента принятия решения  
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Что нужно оформить заранее")
def exchange_of_a_foreign_drivers_license4(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    1. ИПРА. Для этого нужно пройти медико‐социальную экспертизу (МСЭ). Её проводит специализированное учреждение по направлению из медицинской организации. 
    2. Полис ОСАГО. Его можно оформить в страховой компании или на её сайте. 
    3. Банковский счёт — если хотите получить на него компенсацию. Счёт должен быть открыт на имя человека с инвалидностью или его законного представителя.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Кто не может оформить?")
def exchange_of_a_foreign_drivers_license5(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    - Граждане, у которых нет установленной инвалидности 
    - Инвалиды, у которых в индивидуальной программе реабилитации и абилитации (ИПРА) отсутствуют медицинские показания для приобретения транспорта
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

#Обработчик для кнопки Предоставление парковки на местах для инвалидов
@bot.message_handler(func=lambda message: message.text == "Предоставление парковки на местах для инвалидов")
def providing_parking_in_spaces_for_disabled_people(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(text="Что нужно оформить заранее?")
    item2 = types.KeyboardButton(text="Кто имеет право на бесплатную парковку?")
    item3 = types.KeyboardButton(text="Порядок действий")
    back_button = types.KeyboardButton(text="Назад")
    markup.add(item1, item2, item3, back_button)

    text_message = """
    Бесплатная парковка на специальных местах доступна для автомобилей, на которых передвигаются люди с инвалидностью — самостоятельно или с другим водителем
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Что нужно оформить заранее?")
def providing_parking_in_spaces_for_disabled_people1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    Нужно оформить инвалидность. 
    Решение о признании человека инвалидом принимается по результатам медико- социальной экспертизы (МСЭ). Сведения о присвоенной группе инвалидности будут добавлены в Федеральную государственную информационную систему «Федеральный реестр инвалидов» (ФГИС ФРИ)
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Кто имеет право на бесплатную парковку?")
def providing_parking_in_spaces_for_disabled_people2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    -Инвалиды I и II группы 
    - Инвалиды III группы с ограничением способности к самостоятельному передвижению любой степени — это подтверждается записью в индивидуальной программе реабилитации и абилитации (ИПРА) 
    - Дети-инвалиды 
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Порядок действий")
def providing_parking_in_spaces_for_disabled_people3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = types.KeyboardButton(text="Назад")
    markup.add(back_button)

    text_message = """
    1. Подготовьте документы: 
    - Паспорт РФ человека с инвалидностью. Для ребёнка — свидетельство о рождении; 
    - СНИЛС человека с инвалидностью — достаточно знать его номер; 
    - Паспорт представителя и документ, подтверждающий его полномочия, — если заявление подаёт представитель; 
    - Сведения о транспортном средстве: марка, модель, госномер. 
    2. Подайте заявление - Онлайн — на Госуслугах. Потребуется подтверждённая учётная запись; 
    - Лично — в МФЦ. Законные представители детей-инвалидов и недееспособных могут подать заявление только в МФЦ. В заявлении укажите данные автомобиля и период, когда планируете пользоваться бесплатной парковкой, — он не должен превышать срок, на который установлена инвалидность. Вы можете оформить парковку бессрочно или для разовых поездок. Минимум — на сутки. Если нужно изменить срок, подайте новое заявление — предыдущее аннулируется автоматически. 
    3. Получите подтверждение о внесении данных в Федеральный реестр инвалидов. 
    Это займёт не больше 15 минут Если подали заявление через Госуслуги, в личный кабинет придут электронное уведомление и файл для печати со знаком «Инвалид» Если подали заявление в МФЦ, сотрудники выдадут заверенное печатью уведомление о внесении автомобиля в реестр Пользоваться бесплатной парковкой можно в течение срока, указанного в заявлении, или до подачи нового заявления. При снятии инвалидности право на бесплатную парковку прекращается.
    """

    bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )



















#Раздел "Учусь в России"
@bot.message_handler(func=lambda message: message.text == "Дети и образование")
def education_russia(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    items = [
        "🏫 Запись в детский сад",
        "📚 Запись в школу",
        "🏢 Поступление в колледж",
        "🏛 Поступление в университет",
        "Назад"
    ]

    for item in items:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(
        message.chat.id,
        "Выберите интересующий раздел:",
        reply_markup=keyboard,
    )

#Запись в детский сад
@bot.message_handler(func=lambda message: message.text == "🏫 Запись в детский сад")
def kindergarten_registration(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    items = [
        "📞 Линия поддержки (детсад)",
        "📌 Порядок действий",
        "📄 Необходимые документы",
        "👨‍👩‍👦 Кто может подать?",
        "📋 Прочие условия",
        "🔙 Назад"
    ]

    for item in items:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(
        message.chat.id,
        "Выберите интересующий раздел:",
        reply_markup=keyboard,
    )

#Линия поддержки (детский сад)
@bot.message_handler(func=lambda message: message.text == "📞 Линия поддержки (детсад)")
def kindergarten_support_line(message):
    bot.send_message(message.chat.id, "📞 Линия поддержки: 8 (990) 091-82-57")


# Порядок действий (детский сад)
@bot.message_handler(func=lambda message: message.text == "📌 Порядок действий")
def kindergarten_steps(message):
    bot.send_message(
        message.chat.id,
        """📌 Порядок действий для записи в детский сад  
            1️⃣ Выберите детский сад  
            🔗 [Список садов на Госуслугах](https://novorossiya.gosuslugi.ru/map/ds)  

            2️⃣ Подготовьте документы  
            📋 Паспорт родителя или опекуна  
            📋 Свидетельство о рождении ребёнка  
            📋 Свидетельство о регистрации ребёнка  

            📌 Дополнительно (при необходимости):  
            - Документ об опеке  
            - Заключение ПМПК  
            - Договор о целевом обучении  
            - Документ о праве на льготы  

            3️⃣ Лично посетите местный орган управления образованием  
            ✅ Подайте заявление и документы  

            4️⃣ Заполните заявление  
            📌 Укажите ФИО ребёнка, дату рождения, адрес проживания и др.  

            5️⃣ Получите направление в детский сад  
            ✅ Если есть места, с вами свяжутся в течение 7 рабочих дней."""
            ,parse_mode="Markdown")


# Необходимые документы (детсад)
@bot.message_handler(func=lambda message: message.text == "📄 Необходимые документы")
def kindergarten_documents(message):
    bot.send_message(
        message.chat.id,
        """📄 Документы для подачи заявления в детский сад  

✅ Паспорт родителя или законного представителя  
✅ Свидетельство о рождении ребёнка  
✅ Свидетельство о регистрации ребёнка  

📌 Если документ на иностранном языке – нужен нотариально заверенный перевод."""
    )

# Кто может подать (детсад)
@bot.message_handler(func=lambda message: message.text == "👨‍👩‍👦 Кто может подать?")
def kindergarten_who_can_apply(message):
    bot.send_message(
        message.chat.id,
        """👨‍👩‍👦 Кто может подать заявление в детсад?  

✅ Родитель или законный представитель ребёнка с момента рождения.  
✅ Услуга доступна без прописки и для всех граждан независимо от гражданства."""
    )

# Прочие условия (детсад)
@bot.message_handler(func=lambda message: message.text == "📋 Прочие условия")
def kindergarten_other_conditions(message):
    bot.send_message(
        message.chat.id,
        """📋 Дополнительные условия  

👶 Дети могут посещать детский сад с 2 месяцев до 8 лет.  
👶 Для самых маленьких есть ясельные группы (не во всех детсадах).  
🏫 В заявлении можно указать несколько детских садов."""
    )

# Назад (детсад)
@bot.message_handler(func=lambda message: message.text == "🔙 Назад")
def back_to_education(message):
    education_russia(message)



# Запись в школу
@bot.message_handler(func=lambda message: message.text == "📚 Запись в школу")
def school_registration(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    items = [
        "📞 Линия поддержки (школа)",
        "🎒 Порядок действий",
        "📄 Кто может подать?",
        "🎒 Запись в 1 класс",
        "🎓 Запись в 10 класс",
        "📋 Что оформить заранее?",
        "🔙 Назад"
    ]

    for item in items:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(
        message.chat.id,
        "Выберите интересующий раздел:",
        reply_markup=keyboard,
    )

# Линия поддержки (школа)
@bot.message_handler(func=lambda message: message.text == "📞 Линия поддержки (школа)")
def school_support_line(message):
    bot.send_message(message.chat.id, "📞 Линия поддержки: 8 (990) 091-82-57")

# Порядок действий (школа)
@bot.message_handler(func=lambda message: message.text == "🎒 Порядок действий")
def school_steps(message):
    bot.send_message(
        message.chat.id,
        """📌 Порядок записи в школу  

1️⃣ Выберите школу  
🏫 Уточните, относится ли ваш адрес к школе.  

📆 Сроки подачи заявления:  
✅ 1 апреля – 30 июня – если школа закреплена за вашим адресом  
✅ 6 июля – 5 сентября – если школа не закреплена (при наличии мест)  

2️⃣ Подготовьте документы  
📋 Заявление о приёме на обучение  
📋 Паспорт родителя/опекуна  
📋 Свидетельство о рождении ребёнка  
📋 СНИЛС (если есть)  
📋 Документы о регистрации ребёнка  
📋 Документ о льготах (при наличии)  

3️⃣ Подайте заявление  
✅ Лично в школе  
✅ В приёмные дни  

4️⃣ Узнайте результат  
📆 Приказ о зачислении подписывается в течение 3 рабочих дней после завершения приёмной кампании."""
    )

# Кто может подать заявление в школу?
@bot.message_handler(func=lambda message: message.text == "📄 Кто может подать?")
def school_who_can_apply(message):
    bot.send_message(
        message.chat.id,
        """📄 Кто может подать заявление?  

✅ В 1 класс – родитель или опекун ребёнка  
✅ В 10 класс – заявление подаёт сам ученик"""
    )

# Запись в 1 класс
@bot.message_handler(func=lambda message: message.text == "🎒 Запись в 1 класс")
def first_grade_registration(message):
    bot.send_message(
        message.chat.id,
        """🎒 Запись в 1 класс  

✅ Возраст: от 6,5 до 8 лет (исключения возможны с разрешения ПМПК)  

📆 Сроки подачи заявления:  
- 1 апреля – 30 июня – если школа закреплена за адресом  
- 6 июля – 5 сентября – если школа не закреплена и есть места"""
    )

# Запись в 10 класс
@bot.message_handler(func=lambda message: message.text == "🎓 Запись в 10 класс")
def tenth_grade_registration(message):
    bot.send_message(
        message.chat.id,
        """🎓 Запись в 10 класс  

✅ Ученик подаёт заявление самостоятельно  
✅ Запись возможна только после успешной сдачи ОГЭ"""
    )

# Что оформить заранее (школа)
@bot.message_handler(func=lambda message: message.text == "📋 Что оформить заранее?")
def school_what_to_prepare(message):
    bot.send_message(
        message.chat.id,
        """📋 Что оформить заранее?  

✅ Льготы: Если ребёнок относится к льготной категории (например, один из родителей – военный), необходимо заранее взять справку с работы  
✅ Для иностранных граждан:  
📋 Документы, подтверждающие родство  
📋 Разрешение на пребывание в РФ  
📋 Нотариально заверенный перевод, если документы на иностранном языке"""
    )

# Назад (школа)
@bot.message_handler(func=lambda message: message.text == "🔙 Назад")
def back_to_education(message):
    education_russia(message)


# Поступление в колледж
@bot.message_handler(func=lambda message: message.text == "🏢 Поступление в колледж")
def college_registration(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    items = [
        "📞 Линия поддержки (колледж)",
        "🏢 Порядок действий",
        "🏢 Кто может подать?",
        "🎓 Льготные категории",
        "🏢 Что оформить заранее?",
        "🔙 Назад"
    ]

    for item in items:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(
        message.chat.id,
        "Выберите интересующий раздел:",
        reply_markup=keyboard,
    )

# Линия поддержки (колледж)
@bot.message_handler(func=lambda message: message.text == "📞 Линия поддержки (колледж)")
def college_support_line(message):
    bot.send_message(message.chat.id, "📞 Линия поддержки: 8 (990) 091-82-57")

# Порядок действий (колледж)
@bot.message_handler(func=lambda message: message.text == "🏢 Порядок действий")
def college_steps(message):
    bot.send_message(
        message.chat.id,
        """📌 Порядок поступления в колледж  

1️⃣ Выберите колледж  
🔎 Найдите нужный колледж на его официальном сайте  

2️⃣ Подготовьте документы  
📋 Паспорт  
📋 Аттестат за 9 или 11 класс  
📋 4 фото 3×4 см  

📌 Дополнительно (при необходимости):  
- Диплом колледжа/вуза  
- Договор о целевом обучении  
- Медицинская справка (форма 086У)  
- Документы, подтверждающие право на льготы  

3️⃣ Подайте заявление  
✅ Онлайн или лично в приёмной комиссии  

📆 Сроки подачи документов:  
✅ До 15 августа – на очное обучение  
✅ До 25 ноября – при наличии свободных мест  

4️⃣ Пройдите вступительные экзамены (если требуются)  

5️⃣ Узнайте результаты  
📅 15 августа – опубликование приказа о зачислении."""
    )

# Кто может подать заявление в колледж?
@bot.message_handler(func=lambda message: message.text == "🏢 Кто может подать?")
def college_who_can_apply(message):
    bot.send_message(
        message.chat.id,
        """📄 Кто может подать заявление?  

✅ Любой гражданин РФ, окончивший 9 или 11 класс  
✅ Выпускники колледжей и вузов (если поступают на новую специальность)  
✅ Ограничений по возрасту нет"""
    )

# Льготные категории (колледж)
@bot.message_handler(func=lambda message: message.text == "🎓 Льготные категории")
def college_privileged_categories(message):
    bot.send_message(
        message.chat.id,
        """🎓 Кто имеет право на льготы при поступлении в колледж?  

✅ Поступление вне конкурса (если успешно сданы экзамены):  
- Участники боевых действий и их дети  
- Дети медиков, погибших от COVID-19  
- Дети погибших военнослужащих  

✅ Преимущественное право на зачисление:  
- Дети-сироты  
- Люди с инвалидностью  
- Ветераны боевых действий  
- Дети военнослужащих  

📌 Подробнее о льготах:  
🔗 [Госуслуги – Льготы при поступлении](https://www.gosuslugi.ru/help/faq/college/102827)"""
    )

# Что оформить заранее (колледж)
@bot.message_handler(func=lambda message: message.text == "🏢 Что оформить заранее?")
def college_what_to_prepare(message):
    bot.send_message(
        message.chat.id,
        """📋 Что оформить заранее?  

✅ Документы, если вы иностранец:  
📋 Паспорт и документ об образовании – с нотариально заверенным переводом  

✅ Льготы:  
📋 Если у вас есть право на льготу – заранее возьмите справку с работы родителя или иные подтверждающие документы"""
    )

# Назад (колледж)
@bot.message_handler(func=lambda message: message.text == "🔙 Назад")
def back_to_education(message):
    education_russia(message)



# Поступление в университет
@bot.message_handler(func=lambda message: message.text == "🏛 Поступление в университет")
def university_registration(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    items = [
        "📞 Линия поддержки (университет)",
        "🏛 Порядок действий",
        "🏛 Кто может подать?",
        "📋 Способы поступления",
        "📆 Сроки подачи документов",
        "🏛 Что оформить заранее?",
        "🔙 Назад"
    ]

    for item in items:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(
        message.chat.id,
        "Выберите интересующий раздел:",
        reply_markup=keyboard,
    )

# Линия поддержки (университет)
@bot.message_handler(func=lambda message: message.text == "📞 Линия поддержки (университет)")
def university_support_line(message):
    bot.send_message(message.chat.id, "📞 Линия поддержки: 8 (990) 091-82-57")

# Порядок действий (университет)
@bot.message_handler(func=lambda message: message.text == "🏛 Порядок действий")
def university_steps(message):
    bot.send_message(
        message.chat.id,
        """📌 Порядок поступления в университет  

1️⃣ Выберите университет  
🔎 Найдите нужный вуз и ознакомьтесь с его требованиями  

2️⃣ Подготовьте документы  
📋 Паспорт  
📋 Аттестат (или диплом колледжа/вуза)  
📋 4 фото 3×4 см  

📌 Дополнительно (при необходимости):  
- Договор о целевом обучении  
- Медицинская справка (форма 086У)  
- Документы, подтверждающие право на льготы  
- Дипломы олимпиад и индивидуальные достижения  

3️⃣ Подайте заявление  
✅ Онлайн или лично в приёмной комиссии  

📆 Сроки подачи документов:  
✅ До 20 июля – если есть вступительные экзамены  
✅ До 25 июля – если поступление без экзаменов  
✅ 3 августа – последний день подачи оригиналов документов  

4️⃣ Пройдите вступительные испытания (если требуются)  

5️⃣ Узнайте результаты  
📅 9 августа – публикация приказов о зачислении"""
    )

# Кто может подать заявление в университет?
@bot.message_handler(func=lambda message: message.text == "🏛 Кто может подать?")
def university_who_can_apply(message):
    bot.send_message(
        message.chat.id,
        """📄 Кто может подать заявление?  

✅ Любой гражданин РФ, окончивший 11 классов  
✅ Выпускники колледжей и вузов (если поступают на новую специальность)  
✅ Ограничений по возрасту нет"""
    )

# Способы поступления
@bot.message_handler(func=lambda message: message.text == "📋 Способы поступления")
def university_admission_methods(message):
    bot.send_message(
        message.chat.id,
        """📋 Способы поступления в университет  

✅ По результатам ЕГЭ  
✅ По результатам вступительных экзаменов вуза  
✅ По собеседованию (если предусмотрено вузом)  

📌 Все результаты оцениваются по 100-балльной шкале  
📌 Количество поданных заявлений ограничено – максимум 5 вузов"""
    )

#Сроки подачи документов
@bot.message_handler(func=lambda message: message.text == "📆 Сроки подачи документов")
def university_deadlines(message):
    bot.send_message(
        message.chat.id,
        """📆 Сроки подачи документов  

✅ До 20 июля – если предусмотрены вступительные экзамены  
✅ До 25 июля – если поступление без экзаменов  
✅ 3 августа – последний день подачи оригиналов документов  
✅ 9 августа – публикация приказов о зачислении"""
    )

# Что оформить заранее (университет)
@bot.message_handler(func=lambda message: message.text == "🏛 Что оформить заранее?")
def university_what_to_prepare(message):
    bot.send_message(
        message.chat.id,
        """🎓 Что оформить заранее?  

✅ Документы, если вы иностранец:  
📋 Паспорт и документ об образовании – с нотариально заверенным переводом  

✅ Льготы:  
📋 Если у вас есть право на льготу – заранее возьмите справку с работы родителя или иные подтверждающие документы"""
    )

# Назад (университет)
@bot.message_handler(func=lambda message: message.text == "🔙 Назад")
def back_to_education(message):
    education_russia(message)




# Раздел "Служу России"
@bot.message_handler(func=lambda message: message.text == "Служу России")
def military_duty(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    items = [
        "🎗 Служба по призыву",
        "📜 Служба по контракту",
        "🎓 Военное образование",
        "🏫 Военный учебный центр",
        "Назад"
    ]
    
    for item in items:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(
        message.chat.id,
        "Выберите интересующий раздел:",
        reply_markup=keyboard,
    )

# Служба по призыву
@bot.message_handler(func=lambda message: message.text == "🎗 Служба по призыву")
def conscription_service(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    items = [
        "ℹ️ Что такое служба по призыву?",
        "🏥 Категории годности",
        "📜 Военный билет",
        "⚖ Закон о защите Отечества",
        "📄 Альтернативная гражданская служба",
        "📋 Список болезней для освобождения",
        "Назад"
    ]
    
    for item in items:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(
        message.chat.id,
        "Выберите подраздел:",
        reply_markup=keyboard,
    )

# Что такое служба по призыву?
@bot.message_handler(func=lambda message: message.text == "ℹ️ Что такое служба по призыву?")
def about_conscription(message):
    bot.send_message(
        message.chat.id,
            """🎗 Военная служба по призыву  
            📌 Что это?  
            Военная служба по призыву (срочная служба) — это исполнение воинского долга гражданами призывного возраста сроком на 12 месяцев.  

            📅 Срок службы — 1 год.  
            📍 Проходит в Вооружённых силах РФ, органах госохраны и других войсках.  
            🗓 Начало — день присвоения звания рядового.  
            🏁 Окончание — день исключения из списков части."""
        )

#Категории годности
@bot.message_handler(func=lambda message: message.text == "🏥 Категории годности")
def fitness_categories(message):
    bot.send_message(
        message.chat.id,
            """🏥 Категории годности к военной службе  
            📌 Присваиваются по результатам медкомиссии:  
            ✅ "А" — годен.  
            ✅ "Б" — годен с ограничениями.  
            ✅ "В" — ограниченно годен.  
            ❌ "Г" — временно не годен.  
            ❌ "Д" — не годен."""
                )

#Военный билет
@bot.message_handler(func=lambda message: message.text == "📜 Военный билет")
def military_id(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    items = [
        "📑 Что такое военный билет?",
        "📋 Информация в военном билете",
        "Назад"
    ]
    
    for item in items:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(
        message.chat.id,
        "Выберите интересующий вопрос:",
        reply_markup=keyboard,
    )

@bot.message_handler(func=lambda message: message.text == "📑 Что такое военный билет?")
def what_is_military_id(message):
    bot.send_message(
        message.chat.id,
            """📑 Военный билет  
            📌 Основной документ воинского учёта.  
            ✅ Подтверждает личность военнослужащего.  
            ✅ Определяет отношение гражданина к воинской обязанности.  
            ✅ Обязательно выдается в запасе или после прохождения службы."""
            )

@bot.message_handler(func=lambda message: message.text == "📋 Информация в военном билете")
def military_id_info(message):
    bot.send_message(
        message.chat.id,
        """📋 Что содержит военный билет?  
        - Решение призывной комиссии  
        - Воинское звание, должность, спецподготовка  
        - Отметки о службе или альтернативной гражданской службе  
        - Награды, ранения, контузии  
        - Информация о прохождении сборов  
        - Антропометрические данные (рост, размер обуви, форма одежды)"""
        )

#Альтернативная гражданская служба
@bot.message_handler(func=lambda message: message.text == "📄 Альтернативная гражданская служба")
def alternative_service(message):
    bot.send_message(
        message.chat.id,
        """📄 Альтернативная гражданская служба  

📌 Вид трудовой деятельности вместо военной службы.  
✅ Доступна гражданам, чьи убеждения или вероисповедание противоречат несению военной службы.  
📍 Проходит в интересах общества и государства."""
    )

#Закон о защите Отечества
@bot.message_handler(func=lambda message: message.text == "⚖ Закон о защите Отечества")
def law_on_defense(message):
    bot.send_message(
        message.chat.id,
        """⚖ Статья 59 Конституции РФ  

📌 Каждый гражданин обязан защищать Отечество.  
✅ Военная служба регламентируется федеральным законом.  
✅ Граждане с определёнными убеждениями могут заменить службу на альтернативную."""
    )

#Список болезней для освобождения
@bot.message_handler(func=lambda message: message.text == "📋 Список болезней для освобождения")
def medical_exemptions(message):
    bot.send_message(
        message.chat.id,
        """📋 Список болезней, с которыми не берут в армию  

🔗 [Смотреть полный перечень](http://pravo.gov.ru/proxy/ips/?docbody=&nd=102166645)"""
    ,parse_mode="Markdown")


#Служба по контракту
@bot.message_handler(func=lambda message: message.text == "📜 Служба по контракту")
def contract_service(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    items = [
        "📑 Организация отбора",
        "📆 Срок контракта",
        "💰 Преимущества службы",
        "🎖 Социальные гарантии",
        "📜 Требования к кандидатам",
        "🎖 Необходимые документы",
        "Назад"
    ]
    
    for item in items:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(
        message.chat.id,
        "Выберите подраздел:",
        reply_markup=keyboard,
    )

#Организация отбора
@bot.message_handler(func=lambda message: message.text == "📑 Организация отбора")
def recruitment_process(message):
    bot.send_message(
        message.chat.id,
        """📑 Как проходит отбор?  

📌 Отбор граждан на службу по контракту организует Главное управление кадров Минобороны РФ.  
✅ Определяется соответствие кандидата требованиям.  
✅ Подбирается воинская часть и должность.  
🔗 [Пункты отбора](https://службапоконтракту.рф/?ysclid=lrny4duv4x446697059#start) расположены в большинстве регионов."""
    ,parse_mode="Markdown")

#Срок контракта
@bot.message_handler(func=lambda message: message.text == "📆 Срок контракта")
def contract_duration(message):
    bot.send_message(
        message.chat.id,
        """📆 На какой срок заключается контракт?  

✅ 1 год  
✅ 3 года  
✅ 5 лет"""
    )

#Преимущества службы
@bot.message_handler(func=lambda message: message.text == "💰 Преимущества службы")
def contract_benefits(message):
    bot.send_message(
        message.chat.id,
        """💰 Денежные выплаты  

📌 При подписании контракта:  
✅ Единовременная выплата 195 000 ₽.  
📌 Во время службы:  
✅ От 210 000 ₽ в месяц при участии в СВО (в зависимости от звания и стажа)."""
    )

#Социальные гарантии
@bot.message_handler(func=lambda message: message.text == "🎖 Социальные гарантии")
def social_guarantees(message):
    bot.send_message(
        message.chat.id,
        """🎖 Социальные льготы  

🏠 Жильё  
✅ Ипотека от Минобороны.  
✅ Служебное жильё или компенсация за аренду.  

🏥 Медицина  
✅ Бесплатное лечение в военных госпиталях.  

👴 Пенсия  
✅ Льготная военная пенсия после 20 лет службы.  

🎓 Дополнительные льготы  
✅ Льготное поступление детей в вузы.  
✅ Бесплатные путёвки в детские лагеря."""
    )

#Требования к кандидатам
@bot.message_handler(func=lambda message: message.text == "📜 Требования к кандидатам")
def contract_requirements(message):
    bot.send_message(
        message.chat.id,
        """📜 Требования для поступления на контрактную службу  

✅ Возраст: от 18 лет.  
✅ Годность по здоровью (категории "А" или "Б")."""
    )

#Необходимые документы
@bot.message_handler(func=lambda message: message.text == "🎖 Необходимые документы")
def required_documents(message):
    bot.send_message(
        message.chat.id,
        """📄 Что нужно для службы по контракту?  

1️⃣ Автобиография и анкета (форма на сайте Минобороны).  
2️⃣ Паспорт.  
3️⃣ Военный билет (если есть).  
4️⃣ Свидетельство о браке и детях (если есть).  
5️⃣ Документы об образовании.  

🔗 Оставить заявку можно на сайте Минобороны или через Госуслуги."""
    )


#Военное образование
@bot.message_handler(func=lambda message: message.text == "🎓 Военное образование")
def military_education(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    items = [
        "📌 Кто может поступить?",
        "🏛 Список военных ВУЗов",
        "📜 Правила приёма",
        "🎓 Как поступить?",
        "⚖ Кто принимает решение?",
        "Назад"
    ]
    
    for item in items:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(
        message.chat.id,
        "Выберите подраздел:",
        reply_markup=keyboard,
    )

#Кто может поступить?
@bot.message_handler(func=lambda message: message.text == "📌 Кто может поступить?")
def who_can_apply(message):
    bot.send_message(
        message.chat.id,
        """📌 Кто может поступить в военный ВУЗ?  

✅ Граждане РФ со средним образованием.  
✅ Те, кто не проходил службу, а также военнослужащие.  
✅ Кандидаты проходят предварительный отбор.  

🔗 [Требования к поступающим](https://www.gosuslugi.ru/help/faq/military_universities/127783)"""
,parse_mode="Markdown")

#Список военных ВУЗов
@bot.message_handler(func=lambda message: message.text == "🏛 Список военных ВУЗов")
def list_military_universities(message):
    bot.send_message(
        message.chat.id,
        """🏛 Военные ВУЗы России  

🔗 [Смотреть список](https://vuz.mil.ru/Vysshie-uchebnye-zavedeniya?ysclid=lro141d3br8812856)"""
,parse_mode="Markdown")

#Правила приёма
@bot.message_handler(func=lambda message: message.text == "📜 Правила приёма")
def admission_rules(message):
    bot.send_message(
        message.chat.id,
        """📜 Правила приёма в военные ВУЗы  

📆 Приём заявлений: с 1 сентября года, предшествующего году поступления.  
📌 Подробнее — в военкомате или на сайте Минобороны.  

🔗 [Справочник абитуриента](https://ens.mil.ru/education/guide.htm)"""
,parse_mode="Markdown")


#Военный учебный центр
@bot.message_handler(func=lambda message: message.text == "🏫 Военный учебный центр")
def military_training_center(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    items = [
        "📚 Что такое ВУЦ?",
        "📅 Сроки обучения",
        "🏛 Список ВУЗов с ВУЦ",
        "🎓 Как поступить?",
        "👩‍🎓 Могут ли девушки поступить?",
        "📜 Требования к кандидатам",
        "Назад"
    ]
    
    for item in items:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(
        message.chat.id,
        "Выберите подраздел:",
        reply_markup=keyboard,
    )

#Что такое ВУЦ?
@bot.message_handler(func=lambda message: message.text == "📚 Что такое ВУЦ?")
def what_is_vuc(message):
    bot.send_message(
        message.chat.id,
        """📚 Военный учебный центр (ВУЦ)  

✅ Подразделение при гражданском ВУЗе.  
✅ Готовит офицеров и солдат запаса.  
✅ Позволяет получить военное образование без срочной службы."""
    )


#Раздел "Поиск работы"
@bot.message_handler(func=lambda message: message.text == "Работаю в России")
def job_search(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    items = [
        "🏢 Центр занятости населения",
        "💰 Пособие по безработице",
        "✅ Кто может получить статус безработного?",
        "📋 Как стать на учёт в ЦЗН?",
        "🔄 Перерегистрация безработного",
        "❌ Кто не может получить пособие?",
        "📌 Трудоустройство без прописки",
        "Назад"
    ]
    
    for item in items:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(
        message.chat.id,
        "Выберите интересующий раздел:",
        reply_markup=keyboard,
    )

#Что такое центр занятости населения?
@bot.message_handler(func=lambda message: message.text == "🏢 Центр занятости населения")
def employment_center(message):
    bot.send_message(
        message.chat.id,
        """🏢 Центр занятости населения (ЦЗН)  

📌 Помогает найти работу.  
✅ Подбирает подходящие вакансии.  
✅ Направляет на собеседования.""")

#Что такое пособие по безработице?
@bot.message_handler(func=lambda message: message.text == "💰 Пособие по безработице")
def unemployment_benefits(message):
    bot.send_message(
        message.chat.id,
        """💰 Пособие по безработице  

📌 Финансовая поддержка от государства.  
✅ Для тех, кто не может найти работу.  
✅ Выплачивается только тем, кто стоит на учёте в ЦЗН.""")

#Кто может получить статус безработного?
@bot.message_handler(func=lambda message: message.text == "✅ Кто может получить статус безработного?")
def who_can_be_unemployed(message):
    bot.send_message(
        message.chat.id,
        """✅ Кто может получить статус безработного?  

🚫 НЕ могут быть признаны безработными:  
- Студенты очных отделений.  
- Военнослужащие и сотрудники МВД.  
- Пенсионеры.  
- Штатные сотрудники (имеющие работу).  
- Самозанятые и ИП.  
- Заключённые и лица на исправительных работах.""")

#Как стать на учёт в центре занятости?
@bot.message_handler(func=lambda message: message.text == "📋 Как стать на учёт в ЦЗН?")
def register_at_czn(message):
    bot.send_message(
        message.chat.id,
        """📋 Как встать на учёт в ЦЗН?  

📌 Порядок действий:  
1️⃣ Соберите документы  
- Паспорт  
- ИНН  
- СНИЛС  
- Трудовая книжка  
- Диплом или другой документ об образовании  

2️⃣ Подайте заявление  
🔗 [Выбрать центр занятости](https://novorossiya.gosuslugi.ru/unauthorized?redirectTo=map%2Fjob)  

3️⃣ Посетите ЦЗН лично  
✅ Заполните заявление.  
✅ Укажите, претендуете ли на пособие.  

4️⃣ Пройдите собеседование  
📌 Получите направление в ЦЗН.  
📌 Пройдите два собеседования.  
📌 Если откажетесь от 2 вакансий, вас не признают безработным.  

5️⃣ Получите статус безработного  
📌 Присваивается через 11 дней.  

6️⃣ Начисление пособия  
📌 Если вас признали безработным, пособие начисляют со дня подачи заявления.  

7️⃣ Перерегистрация  
📌 Обязательна, если хотите сохранить статус и получать пособие."""
,parse_mode="Markdown")

#Перерегистрация безработного
@bot.message_handler(func=lambda message: message.text == "🔄 Перерегистрация безработного")
def re_register_unemployed(message):
    bot.send_message(
        message.chat.id,
        """🔄 Перерегистрация безработного  

📌 Ежемесячное подтверждение отсутствия работы.  
✅ Обязательно для получения пособия.  
✅ Позволяет получать новые вакансии и проходить обучение.""")

#Кто не может получать пособие?
@bot.message_handler(func=lambda message: message.text == "❌ Кто не может получить пособие?")
def who_cannot_get_benefits(message):
    bot.send_message(
        message.chat.id,
        """❌ Кому не положено пособие?🚫 
        НЕ могут получать пособие:  
        - Студенты-очники  
        - Военнослужащие, МВД, ФСИН, ФСО  
        - Пенсионеры  
        - Работающие граждане  
        - Самозанятые, ИП, адвокаты, нотариусы  
        - Осуждённые, лица на исправительных работах.""")

#Трудоустройство при отсутствии регистрации
@bot.message_handler(func=lambda message: message.text == "📌 Трудоустройство без прописки")
def employment_without_registration(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    items = [
        "⚖ Защита прав работников",
        "📄 Документы для трудоустройства",
        "🚫 Отказ в трудоустройстве",
        "Назад"
    ]
    
    for item in items:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(
        message.chat.id,
        "Выберите интересующий вопрос:",
        reply_markup=keyboard,
    )

#Защита прав работников
@bot.message_handler(func=lambda message: message.text == "⚖ Защита прав работников")
def workers_rights(message):
    bot.send_message(
        message.chat.id,
        """⚖ Защита прав работников  

📌 Работодатель обязан заключить трудовой договор, если работник соответствует требованиям.  

🔗 [Официальный сайт Роструда](https://rostrud.gov.ru/)""")

#Необходимые документы для трудоустройства
@bot.message_handler(func=lambda message: message.text == "📄 Документы для трудоустройства")
def required_documents_for_employment(message):
    bot.send_message(
        message.chat.id,
        """📄 Документы для трудоустройства  

✅ Паспорт  
✅ Трудовая книжка  
✅ СНИЛС  
✅ Диплом (если требуется)  
✅ Военный билет (для военнообязанных)  
✅ Медицинская книжка (для отдельных профессий)  

📌 Регистрация по месту жительства НЕ обязательна!  
📌 Работодатель не имеет права отказывать в приёме на работу из-за отсутствия прописки.""")

# 📌 Отказ в трудоустройстве
@bot.message_handler(func=lambda message: message.text == "🚫 Отказ в трудоустройстве")
def job_rejection(message):
    bot.send_message(
        message.chat.id,
        """🚫 Если вам отказали в работе из-за отсутствия регистрации  

📌 Вы можете подать жалобу:  
📞 Горячая линия Роструда: 8 (800) 707-88-41.""")


























# Обработчик кнопки "Назад"
@bot.message_handler(func=lambda message: message.text == "Назад")
def handle_back(message):
    start(message)  # Возвращаем пользователя к основному меню

# Обработчик для любых других сообщений, которые не совпадают ни с одним обработчиком
@bot.message_handler(func=lambda message: True)
def handle_other(message):
    bot.send_message(
        message.chat.id,
        "Извините, я не понимаю ваш запрос. Выберите пункт меню или воспользуйтесь клавиатурой.",
    )




# Запуск бота
bot.polling()

