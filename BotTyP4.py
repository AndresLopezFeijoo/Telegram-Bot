import telegram.ext
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from Tools import slice_lst, get_lst, base_key
from SeqClass import Sequence, nice_name
import os
import random

TOKEN = json.load(open("token.json"))["testtok"]
updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher
datos = json.load(open("datos.json"))
tyc = json.load(open("typ.json"))


def mel_rit(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
    print(c)
    keyboard = base_key(two=True)
    k2 = []
    for i, j in zip(datos[c[0]][0], datos[c[0]][1]):
        k2.append(InlineKeyboardButton(i, callback_data=j))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=j, callback=años))

    keyboard.append(k2)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        text="\U0001f916 <strong>" + datos[c[0]][0][0] + " o " + datos[c[0]][0][1] + "?</strong>",
        reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def años(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[1] = update.callback_query["data"]
    print(c)
    keyboard = base_key("Atras", c[0], two=False)
    k2 = []
    for i in datos["years"]:
        k2.append(InlineKeyboardButton(i, callback_data=">" + i))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=">" + i, callback=dic_lec_lst))
    keyboard = slice_lst(k2, keyboard, 4)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>De que año?</strong>", reply_markup=reply_markup,
                                            parse_mode=telegram.ParseMode.HTML)


def dic_lec_lst(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[2] = update.callback_query["data"][1:]
    print(c)
    a = get_lst(c[0] + "/" + c[1] + "/" + c[2], clear=True)
    b = len(a) > 0
    keyboard = base_key("Atras", c[1], two=False)
    k2 = []
    if b:
        for i in a:
            k2.append(InlineKeyboardButton(i, callback_data="o" + i))
            disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="o" + i, callback=send_dic_lec))
        keyboard = slice_lst(k2, keyboard, 4)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(text="\U0001f916<strong>" + datos[c[0]][2] + "</strong>",
                                                reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
    else:
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(text="\U0001f916<strong>No tengo material en esta categoria....."
                                                "</strong>",
                                                reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)




def send_dic_lec(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[3] = update.callback_query["data"][1:]
    print(c)
    path = c[0] + "/" + c[1] + "/" + c[2] + "/" + c[3]
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Ahí va!! </strong>",
                                            parse_mode=telegram.ParseMode.HTML)
    if c[0] == "dict":
        if c[1] == "m":
            nro = u"\U0001F3BC " + c[2] + " / " + c[3] + u" \U0001F449"
            cp = "captionm"
        elif c[1] == "r":
            nro = u"\U0001F941 " + c[2] + " / " + c[3] + u" \U0001F449"
            cp = "captionr"
        for i, j in zip(get_lst(path, clear=False), datos[cp]):
            with open(path + "/" + i, "rb") as audio_file:
                context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                                       caption=nro + j)

        keyboard = [[InlineKeyboardButton("Volver a dictados", callback_data="dict")],
                    [InlineKeyboardButton("Tonalidad y/o compás", callback_data="tyc")],
                    [InlineKeyboardButton("Solución", callback_data="sol")]]
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="tyc", callback=send_tyc))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="sol", callback=send_sol))
        reply_markup = InlineKeyboardMarkup(keyboard, one_time_Keyboard=True)

        context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                                text="\U0001f916 <strong>Elegí una opción</strong>",
                                reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
    elif c[0] == "lect":
        if c[1] == "m":
            msg = u'\U0001F440 \U0001F3BC' + " Nro: " + c[3]
        elif c[1] == "r":
            msg = u'\U0001F440 \U0001F941' + " Letra: " + c[3]

        with open(path + ".png", "rb") as photo_file:
            context.bot.send_photo(chat_id=update.callback_query["message"]["chat"]["id"], photo=photo_file,
                                   caption=msg)
        keyboard = base_key("Volver a lecturas", "lect", two=False)
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                                text="\U0001f916 <strong>Elegí una opción</strong>",
                                reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def send_sol(update, context):
    update.callback_query.answer()
    c = context.user_data
    print(c)
    path = c[1] + "/" + c[2] + "/" + c[3]
    update.callback_query.edit_message_text(text="\U0001f916 <strong>A ver.........</strong>",
                                            parse_mode=telegram.ParseMode.HTML)
    with open("dictimag/" + path + ".png", "rb") as photo_file:
        context.bot.send_photo(chat_id=update.callback_query["message"]["chat"]["id"], photo=photo_file,
                               caption=u'\U0001F648 \U0001F91E \U0001F91E \U0001F91E')
    keyboard = base_key("Volver a dictados", "dict", two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Elegí una opción</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def send_tyc(update, context):
    update.callback_query.answer()
    c = context.user_data
    print(c)
    keyboard = [[InlineKeyboardButton("volver a dictados", callback_data="dict")],
                [InlineKeyboardButton("Solución", callback_data="sol")]]
    reply_markup = InlineKeyboardMarkup(keyboard, remove_keyboard=True)
    update.callback_query.edit_message_text(text=" \U0001f916 <strong>Está en: " + tyc[c[1]][c[2]][c[3]] +
                                            "</strong>", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def chapters(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
    print(c)
    keyboard = base_key(two=True)
    k2 = []
    for i in datos[c[0]]:
        k2.append(InlineKeyboardButton("Cap" + i, callback_data="<" + i))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="<", callback=melo_hind_list))
    keyboard = slice_lst(k2, keyboard, 4)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Elegí un capítulo</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def melo_hind_list(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[1] = update.callback_query["data"][1:]
    print(c)
    keyboard = base_key("Atras", c[0], two=False)
    k2 = []
    try:
        for i in get_lst(c[0] + "/" + c[1], clear=True):
            k2.append(InlineKeyboardButton(i, callback_data=">" + i))
            disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=(">" + i), callback=send_melo_hind))
        keyboard = slice_lst(k2, keyboard, 3)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(text="\U0001f916 <strong>Puedo ofrecerte estos ejercicios:</strong>",
                                                reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
    except:
        return working(update, context)


def send_melo_hind(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[2] = update.callback_query["data"][1:]
    print(c)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>As2d2 procesando...</strong>",
                                            parse_mode=telegram.ParseMode.HTML)
    if c[0] == "melo":
        cap = u'\U0001F941' + " Melo Castillo " + c[2]
    elif c[0] == "hind":
        cap = u'\U0001F941' + " Hindemith " + c[2]

    with open(c[0] + "/" + c[1] + "/" + c[2] + ".mp3", "rb") as audio_file:
        context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                               caption=cap)

    keyboard = base_key("Atras", "<" + c[1], two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Hecho!!, Como seguimos...?</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def books(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
    print(c)
    keyboard = base_key(two=True)
    k2 = []
    for i in get_lst(c[0], clear=True):
        k2.append(InlineKeyboardButton(i, callback_data="b" + i))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=("b" + i), callback=send_pdf))

    keyboard = slice_lst(k2, keyboard, 1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Tengo estos libros:</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def send_pdf(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[1] = update.callback_query["data"][1:]
    print(c)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Esperame que lo tengo que buscar...\n"
                                                 "Mi casa es un lio de papeles</strong>",
                                            parse_mode=telegram.ParseMode.HTML)
    with open(c[0] + "/" + c[1] + ".pdf", "rb") as pdf_file:
        context.bot.send_document(chat_id=update.callback_query["message"]["chat"]["id"], document=pdf_file,
                                  caption=u'📖 🤓 ' + c[1])
    keyboard = base_key("Atras", c[0], two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Ahí está!! Que mas....?</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def working(update, context):
    update.callback_query.answer()
    file = random.choice(os.listdir("memes/gandalf"))
    with open("memes/gandalf/" + file, "rb") as gif:
        context.bot.send_document(chat_id=update.callback_query["message"]["chat"]["id"], document=gif,
                                  caption=u'\U0001F4BB\U0001F9F0 Ups!... En construcción...')
    keyboard = [[InlineKeyboardButton("Home", callback_data="home")],
                [InlineKeyboardButton("Terminar", callback_data="end")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text=u"\U0001f916 <strong> Que hacemos? </strong>",
                            parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)


def start(update, context):
    first_name = update.message.from_user.first_name
    msg = u"\U0001f916 <strong>Hola {}!! soy Astorito, el droide de Astor.</strong>\U0001FA97\n" \
          "Puedo ofrecerte las siguientes opciones, mucha suerte!!\U0001F3B6".format(first_name)
    k = [InlineKeyboardButton(text="Programa", url="https://cmbsas-caba.infd.edu.ar/sitio/nivel-medio/")]
    k2 = []
    for i in json.load(open("datos.json"))["start"]:
        k.append(InlineKeyboardButton(i[0], callback_data=i[1]))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=i[1], callback=eval(i[2])))
    for i in range(0, len(k), 2):
        k2.append(k[i:i + 2])
    reply_markup = InlineKeyboardMarkup(k2)
    context.bot.sendMessage(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.HTML)


def root(update, context):
    update.callback_query.answer()
    context.user_data[0] = update.callback_query["data"]
    keyboard = base_key(two=True)
    k2 = []
    for i in datos["roots"]:
        k2.append(InlineKeyboardButton(i, callback_data="e" + i))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="e" + i, callback=mode))
    keyboard = slice_lst(k2, keyboard, 7)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        text="\U0001f916 <strong>Eligí una fundamental.....</strong>",
        reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def mode(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[1] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", c[0], two=False)
    k2 = []
    for i in datos["modos"]:
        k2.append(InlineKeyboardButton(i, callback_data="s" + i))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="s" + i, callback=n))

    keyboard = slice_lst(k2, keyboard, 1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        text="\U0001f916 <strong>Eligí una escala .....</strong>",
        reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def n(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[2] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", "e" + c[1], two=False)
    k2 = []
    for i in range(6):
        if i > 2:
            k2.append(InlineKeyboardButton(i, callback_data="f" + str(i)))
            disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="f" + str(i), callback=snd_scl))
    k2.append(InlineKeyboardButton("Hard", callback_data="f6"))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="t6", callback=snd_scl))
    keyboard.append(k2)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        text="\U0001f916 <strong>Cuantas notas te mando?\n3 y 4 y 5 son secuencias que comienzan siempre "
             "en la tónica.\nHard son seis notas y puede empezar por cualquier sonido!!!</strong>",
        reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def snd_scl(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[3] = update.callback_query["data"][1:]
    seq = Sequence(c[1], c[2], int(c[3]), "True")
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Primero te mando la escala!! </strong>",
                                            parse_mode=telegram.ParseMode.HTML)
    with open("escalas/" + c[2] + "/" + c[1] + ".mp3", "rb") as audio_file:
        context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                               caption="<strong>" + c[1] + " " + c[2] + ":</strong>" + " " +
                                       nice_name(seq.scale_pitches), parse_mode=telegram.ParseMode.HTML)
    return snd_seq(update, context)


def snd_seq(update, context):
    update.callback_query.answer()
    c = context.user_data
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Elegí estos sonidos para vos....\n"
                                 "Que notas son? </strong>", parse_mode=telegram.ParseMode.HTML)
    file = random.choice(os.listdir("secuencias/" + c[1] + "/" + c[2] + "/" + c[3]))
    with open("secuencias/" + c[1] + "/" + c[2] + "/" + c[3] + "/" + file, "rb") as audio_file:
        context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                               caption="Secuencia de " + c[3] + " notas en " + c[1] + " " + c[2])
    keyboard = base_key("Solución", "y" + file, two=False)
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="y" + file, callback=notes))
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Waiting orders .......</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def notes(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[4] = update.callback_query["data"][1:]
    path = "secuencias/" + c[1] + "/" + c[2] + "/" + c[3] + "/" + c[4]
    nt = os.path.basename(path).split(".")[0]
    keyboard = base_key("Otro!!", "j", two=False)
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="j", callback=snd_seq))
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>" + nt + "</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def start_over(update, context):
    """Para volver a empezar pero no ingresando un mensaje"""
    update.callback_query.answer()
    k = [InlineKeyboardButton(text="Programa", url="https://cmbsas-caba.infd.edu.ar/sitio/nivel-medio/")]
    k2 = []
    for i in json.load(open("datos.json"))["start"]:
        k.append(InlineKeyboardButton(i[0], callback_data=i[1]))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=i[1], callback=eval(i[2])))
    for i in range(0, len(k), 2):
        k2.append(k[i:i + 2])
    reply_markup = InlineKeyboardMarkup(k2)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Empecemos otra vez!!</strong>\n"
                                                 "Contame que queres hacer.",
                                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def end(update, context):
    update.callback_query.answer()
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Nos vemos la próxima</strong> \U0001FA97",
                                            parse_mode=telegram.ParseMode.HTML)
    return ConversationHandler.END


def handle_message(update, context):
    update.message.reply_text(f"\U0001f916 <strong>Dijiste {update.message.text} y no te entiendo.....</strong>\n"
                              "Todavia no se conversar pero tengo muchos botones!!\n"
                              "para inciar escribí /start", parse_mode=telegram.ParseMode.HTML)


disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="home", callback=start_over))

updater.start_polling()  # drop_pending_updates=True
updater.idle()
