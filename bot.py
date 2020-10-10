import telebot
import config
import random

from telebot import types
from model.model import oli_price_calc
bot = telebot.TeleBot(config.TOKEN)

models_number_list = [1, 2, 3]
models_pic_dict = {1:"3d", 2:"90d",3:"360d", 4:"model_4.jpg", 5:"model_5.jpg"}
models_discription_dict = {1:"Краткосрочная модель", 2:"Среднесрочная",3:"Доглосрочная", 4:"мя модели #4", 5:"мя модели #5"}

terms_list = ["6m", "12m", "1.5y", "2y"]
terms_discription_dict = {1:"6 месяцев", 2:"12 месяцев", 3:"1,5 года", 4:"2 года"}
oil_price_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

current_model_n = 1
current_term_n = 1
current_oil_price_n = 1

def model_description():
    global current_model_n
    global current_term_n
    global current_oil_price_n
    return f"Расчёт будет проведен на основе следующих параметров: \n" \
                          f"<b>Модель</b>: {models_discription_dict[current_model_n]} \n" \
                          f"<b>Период</b>: {terms_discription_dict[current_term_n]} \n" \
                          f"<b>Цена нефти</b>: {oil_price_list[current_oil_price_n - 1]}$\n\n" \
           f"Настройте параметры модели или сделайте расчёт" \

current_discription = model_description()

def markup_builder(model_n, term_n, price_n):
    markup = types.InlineKeyboardMarkup(row_width=3)
    btn1 = types.InlineKeyboardButton("◄◄", callback_data='model_down')
    btn2 = types.InlineKeyboardButton(f"Модель {models_number_list[model_n-1]} ({model_n}/{len(models_number_list)})",
                                      callback_data='model_up')
    btn3 = types.InlineKeyboardButton("►►", callback_data='model_up')
    markup.row(btn1, btn2, btn3)

    '''btn4 = types.InlineKeyboardButton("◄◄", callback_data='term_down')
    btn5 = types.InlineKeyboardButton(f"Период {terms_list[term_n-1]}", callback_data='term_mid')
    btn6 = types.InlineKeyboardButton("►►", callback_data='term_up')
    markup.row(btn4, btn5, btn6)'''

    btn7 = types.InlineKeyboardButton("◄◄", callback_data='oil_price_down')
    btn8 = types.InlineKeyboardButton(f"Oil_WTI {oil_price_list[price_n-1]} $", callback_data='oil_price_up')
    btn9 = types.InlineKeyboardButton("►►", callback_data='oil_price_up')
    markup.row(btn7, btn8, btn9)
    btn10 = types.InlineKeyboardButton("Сделать расчёт", callback_data='calculate')
    markup.row(btn10)

    # markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9)
    return markup


@bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандомное число")
    item2 = types.KeyboardButton("Предсказание курса RUB")

    markup.add(item2)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':

        if message.text == '🎲 Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == 'Предсказание курса RUB':
            #https://github.com/eternnoir/pyTelegramBotAPI/blob/master/tests/test_telebot.py
            #photo = open('./pic/model_1.jpg', 'rb')


            global current_model_n
            global photo_obj
            #photo = open(f'./pic/{models_pic_dict[current_model_n]}', 'rb')
            photo = open(f'./pic/ds.jpg', 'rb')

            photo_obj = bot.send_photo(message.chat.id, photo)
            print(photo_obj.photo[0])
            markup = markup_builder(current_model_n, current_term_n, current_oil_price_n)

            current_discription = model_description()
            bot.send_message(message.chat.id, current_discription, parse_mode='html', reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item2 = types.KeyboardButton("Предсказание курса RUB")
            markup.add(item2)
            bot.send_message(message.chat.id,
                             "Привет, нажми на кнопку внизу",
                             parse_mode='html', reply_markup=markup)
        '''else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить )'''


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        global current_model_n
        global current_term_n
        global current_oil_price_n

        if call.message:
            if call.data == 'model_down':
                current_model_n -= 1
                current_model_n = scrolling(current_model_n, len(models_number_list))
                #change_inline_picture(call)
                change_inline_menu(call)


            elif call.data == 'model_up':
                current_model_n += 1
                current_model_n = scrolling(current_model_n, len(models_number_list))
                #change_inline_picture(call)
                change_inline_menu(call)

                '''photo2 = open(f'./pic/{models_pic_dict[current_model_n]}', 'rb')
                bot.edit_message_media(chat_id=call.message.chat.id, message_id=photo_obj.message_id,
                                       media=types.InputMediaPhoto(photo2))
                markup = markup_builder(current_model_n, current_term_n, current_oil_price_n)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=call.message.text,
                                      reply_markup=markup)'''

            elif call.data == 'term_down':
                current_term_n -= 1
                current_term_n = scrolling(current_term_n, len(terms_list))
                change_inline_menu(call)
            elif call.data == 'term_up':
                current_term_n += 1
                current_term_n = scrolling(current_term_n, len(terms_list))
                change_inline_menu(call)
            elif call.data == 'oil_price_down':
                current_oil_price_n -= 1
                current_oil_price_n = scrolling(current_oil_price_n, len(oil_price_list))
                change_inline_menu(call)
            elif call.data == 'oil_price_up':
                current_oil_price_n += 1
                current_oil_price_n = scrolling(current_oil_price_n, len(oil_price_list))
                change_inline_menu(call)
            elif call.data == 'calculate':
                oli_price_calc(models_pic_dict[current_model_n], oil_price_list[current_oil_price_n - 1])
                change_inline_picture(call)
                #photo = open(f'./foo.png', 'rb')
                #bot.send_photo(call.message.chat.id, photo)
            else:
                oli_price_calc(models_pic_dict[current_model_n], oil_price_list[current_oil_price_n - 1])
                change_inline_picture(call)
                #pass
                #bot.send_message(call.message.chat.id, 'Ошибка 😢')


                # show alert
                #bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                #                          text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

    except Exception as e:
        print(repr(e))

def scrolling(varible, num_elem):
    if varible > num_elem:
        varible = 1
    elif varible <= 0:
        varible = num_elem
    return varible

def change_inline_menu(call):
    markup = markup_builder(current_model_n, current_term_n, current_oil_price_n)
    current_discription = model_description()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=current_discription, parse_mode='html',
                          reply_markup=markup)

def change_inline_picture(call):

    #photo2 = open(f'./pic/{models_pic_dict[current_model_n]}', 'rb')
    photo2 = open(f'./foo.png', 'rb')
    #bot.send_photo(call.message.chat.id, 'AgACAgIAAxkDAAIBzV97Xk23sGQOKNiXf6h4pN9lhi4OAAKCsDEbb8fRS4rRMe0-0_1Wc7NFmC4AAwEAAwIAA20AA7FTAQABGwQ')
    bot.edit_message_media(chat_id=call.message.chat.id, message_id=photo_obj.message_id,
                           media=types.InputMediaPhoto(photo2))

# RUN

bot.polling(none_stop=True)
