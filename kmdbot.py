from telebot import TeleBot, types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telebot.custom_filters import TextFilter, TextMatchFilter

import angles, lists, channels, ibeams, tubes

TOKEN = "5357115674:AAGaykTtMo1FXR9WHp7Q_TDjg7S3YdiNlY8"

bot = TeleBot(TOKEN, parse_mode='Markdown')
bot.remove_webhook()

# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.send_message(
        message.chat.id, "Привiт! Я _KMDist_ - бот-помiчник для тих, хто займаєтся проектуванням металоконстркцiй")
    markup = types.ReplyKeyboardMarkup(row_width=6, resize_keyboard=True)
    itembtn = []
    itembtn.append(types.KeyboardButton('Кутик'))
    itembtn.append(types.KeyboardButton('Швелер'))
    itembtn.append(types.KeyboardButton('Двотавр'))
    itembtn.append(types.KeyboardButton('Лист'))
    itembtn.append(types.KeyboardButton('Рифл'))
    itembtn.append(types.KeyboardButton('ПВЛ'))
    itembtn.append(types.KeyboardButton('Труба'))
    itembtn.append(types.KeyboardButton('Тр.кв.'))
    itembtn.append(types.KeyboardButton('Тр.пр.'))
    itembtn.append(types.KeyboardButton('HSS'))
    itembtn.append(types.KeyboardButton('RHS'))
    markup.add(*itembtn)
    msg = bot.send_message(
        message.chat.id, "Почнiть з меню:", reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
    msg = bot.send_message(
        message.chat.id,
        "Я намагаюся бути максимально простим у спiлкуваннi i розумiю такi команди \
            \n*кутик* \
            \n_або_ \
            \n*кутик (хрест|тавр|короб) 50х5* \
            \n_або_ \
            \n*кутик 50х5 10м* \
            \n_або_ \
            \n*кутик 50х5 0.6кг* \
            \nДля нагадування доступних опцiй наберить знак питання (?) пiсля найменування проката \
            \n_наприклад_ *кутик ?* або *швелер ?*")


##@bot.message_handler(text=TextFilter(starts_with=['кутик', 'угол'], ignore_case=True))
##def angle_filter(message):
##    kbd = InlineKeyboardMarkup()
##    kbd.add(
##        InlineKeyboardButton(text='хрест', callback_data=message.text+' хрест'),
##        InlineKeyboardButton(text='тавр', callback_data=message.text+' тавр'),
##        InlineKeyboardButton(text='короб', callback_data=message.text+' короб')
##    )
##    bot.send_message(message.chat.id, angles.reply_to_message(message.text), parse_mode='HTML') #reply_markup=kbd

@bot.callback_query_handler(func=lambda call: call.data.endswith('png'))
def callback_query(call):
    bot.send_photo(call.message.chat.id, photo=open(call.data, 'rb'))

@bot.callback_query_handler(func=lambda call: call.data.startswith('HLP'))
def callback_query(call):
    if call.data == "HLPangle":
        s = angles.HELPSTRING[3:]
    elif call.data == "HLPchannel":
        s = channels.HELPSTRING[3:]
    elif call.data == "HLPibeam":
        s = ibeams.HELPSTRING[3:]
    elif call.data == "HLPtube":
        s = tubes.HELPSTRING_TUBE[3:]
    elif call.data == "HLPsqtube":
        s = tubes.HELPSTRING_SQTUBE[3:]
    elif call.data == "HLPprtube":
        s = tubes.HELPSTRING_PRTUBE[3:]
    elif call.data == "HLPhss":
        s = tubes.HELPSTRING_HSS[3:]
    elif call.data == "HLPrhs":
        s = tubes.HELPSTRING_RHS[3:]
    elif call.data == "HLPlist":
        s = lists.HELPSTRINGLIST[3:]
    elif call.data == "HLPrif":
        s = lists.HELPSTRINGRIF[3:]
    elif call.data == "HLPpvl":
        s = lists.HELPSTRINGPVL[3:]
    else:
        s = None
    bot.send_message(call.message.chat.id, s, parse_mode='HTML')

@bot.message_handler(text=TextFilter(starts_with=['кутик', 'угол'], ignore_case=True))
def angle_filter(message):
    txt, pic =  angles.reply_to_message(message.text)
    kbd = InlineKeyboardMarkup()
    row = [(InlineKeyboardButton(text='Малюнок', callback_data=pic)),
           (InlineKeyboardButton(text='Довiдка', callback_data= "HLPangle" ))]
    kbd.add(*row)
    bot.send_message(message.chat.id, txt, reply_markup=kbd, parse_mode='HTML')

@bot.message_handler(text=TextFilter(starts_with='лист', ignore_case=True))
def list_filter(message):
    kbd = InlineKeyboardMarkup()
    row = [(InlineKeyboardButton(text='Довiдка', callback_data= "HLPlist" ))]
    kbd.add(*row)
    bot.send_message(message.chat.id, lists.reply_to_message_list(message.text), reply_markup=kbd, parse_mode='HTML')

@bot.message_handler(text=TextFilter(starts_with='риф', ignore_case=True))
def rif_filter(message):
    kbd = InlineKeyboardMarkup()
    row = [(InlineKeyboardButton(text='Довiдка', callback_data= "HLPrif" ))]
    kbd.add(*row)
    bot.send_message(message.chat.id, lists.reply_to_message_rif(message.text), reply_markup=kbd, parse_mode='HTML')

@bot.message_handler(text=TextFilter(starts_with='пвл', ignore_case=True))
def pvl_filter(message):
    kbd = InlineKeyboardMarkup()
    row = [(InlineKeyboardButton(text='Довiдка', callback_data= "HLPpvl" ))]
    kbd.add(*row)
    bot.send_message(message.chat.id, lists.reply_to_message_pvl(message.text), reply_markup=kbd, parse_mode='HTML')

@bot.message_handler(text=TextFilter(starts_with=['швелер', 'швеллер'], ignore_case=True))
def channel_filter(message):
    txt, pic =  channels.reply_to_message(message.text)
    kbd = InlineKeyboardMarkup()
    row = [(InlineKeyboardButton(text='Малюнок', callback_data=pic)),
           (InlineKeyboardButton(text='Довiдка', callback_data= "HLPchannel" ))]
    kbd.add(*row)
    bot.send_message(message.chat.id, txt, reply_markup=kbd, parse_mode='HTML')

@bot.message_handler(text=TextFilter(starts_with=['двотавр', 'двутавр'], ignore_case=True))
def ibeam_filter(message):
    txt, pic =  ibeams.reply_to_message(message.text)
    kbd = InlineKeyboardMarkup()
    row = [(InlineKeyboardButton(text='Малюнок', callback_data=pic)),
           (InlineKeyboardButton(text='Довiдка', callback_data= "HLPibeam" ))]
    kbd.add(*row)
    bot.send_message(message.chat.id, txt, reply_markup=kbd, parse_mode='HTML')

@bot.message_handler(text=TextFilter(starts_with=['кв.тр', 'кв тр', 'тр.кв', 'тр кв'], ignore_case=True))
def sqtube_filter(message):
    txt, pic = tubes.reply_to_message("тр.кв.", message.text)
    kbd = InlineKeyboardMarkup()
    row = [(InlineKeyboardButton(text='Малюнок', callback_data=pic)),
           (InlineKeyboardButton(text='Довiдка', callback_data= "HLPsqtube" ))]
    kbd.add(*row)
    bot.send_message(message.chat.id, txt, reply_markup=kbd, parse_mode='HTML')

@bot.message_handler(text=TextFilter(starts_with=['пр.тр', 'пр тр', 'тр.пр', 'тр пр'], ignore_case=True))
def prtube_filter(message):
    txt, pic = tubes.reply_to_message("тр.пр.", message.text)
    kbd = InlineKeyboardMarkup()
    row = [(InlineKeyboardButton(text='Малюнок', callback_data=pic)),
           (InlineKeyboardButton(text='Довiдка', callback_data= "HLPprtube" ))]
    kbd.add(*row)
    bot.send_message(message.chat.id, txt, reply_markup=kbd, parse_mode='HTML')

@bot.message_handler(text=TextFilter(starts_with='труба', ignore_case=True))
def tube_filter(message):
    txt, pic = tubes.reply_to_message("труба", message.text)
    kbd = InlineKeyboardMarkup()
    row = [(InlineKeyboardButton(text='Малюнок', callback_data=pic)),
           (InlineKeyboardButton(text='Довiдка', callback_data= "HLPtube" ))]
    kbd.add(*row)
    bot.send_message(message.chat.id, txt, reply_markup=kbd, parse_mode='HTML')

@bot.message_handler(text=TextFilter(starts_with='HSS', ignore_case=True))
def hss_filter(message):
    txt, pic = tubes.reply_to_message("HSS", message.text)
    kbd = InlineKeyboardMarkup()
    row = [(InlineKeyboardButton(text='Малюнок', callback_data=pic)),
           (InlineKeyboardButton(text='Довiдка', callback_data= "HLPhss" ))]
    kbd.add(*row)
    bot.send_message(message.chat.id, txt, reply_markup=kbd, parse_mode='HTML')

@bot.message_handler(text=TextFilter(starts_with='RHS', ignore_case=True))
def rhs_filter(message):
    txt, pic = tubes.reply_to_message("RHS", message.text)
    kbd = InlineKeyboardMarkup()
    row = [(InlineKeyboardButton(text='Малюнок', callback_data=pic)),
           (InlineKeyboardButton(text='Довiдка', callback_data= "HLPrhs" ))]
    kbd.add(*row)
    bot.send_message(message.chat.id, txt, reply_markup=kbd, parse_mode='HTML')




bot.add_custom_filter(TextMatchFilter())
bot.infinity_polling()
