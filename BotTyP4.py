import telegram.ext
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from Tools import slice_lst, get_lst, base_key
from SeqClass import Sequence, nice_name
import os


TOKEN = json.load(open("token.json"))["tok"]
updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher
datos = json.load(open("datos.json"))
tyc = json.load(open("typ.json"))


def mel_rit(update, context):
    update.callback_query.answer()
    ucq = update.callback_query["data"]
    keyboard = base_key(two=True)
    k2 = []
    for i, j in zip(datos[ucq][0], datos[ucq][1]):
        k2.append(InlineKeyboardButton(i, callback_data=(ucq + "/" + j)[::-1]))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=(ucq + "/" + j)[::-1], callback=años))

    keyboard.append(k2)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>" + datos[ucq][0][0] + " o " + datos[ucq][0][1] + "?</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def años(update, context):
    update.callback_query.answer()
    ucq = update.callback_query["data"][::-1]
    keyboard = base_key("Atras", ucq.split("/")[0], two=False)
    k2 = []
    for i in datos["years"]:
        k2.append(InlineKeyboardButton(i, callback_data=">" + ucq + "/" + i))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=">" + ucq + "/" + i, callback=mel_rit_lst))
    keyboard = slice_lst(k2, keyboard, 4)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>De que año?</strong>", reply_markup=reply_markup,
                                            parse_mode=telegram.ParseMode.HTML)


def mel_rit_lst(update, context):
    update.callback_query.answer()
    ucq = update.callback_query["data"][1:]
    ucq_spl = ucq.split("/")
    keyboard = base_key("Atras", (ucq_spl[0] + "/" + ucq_spl[1])[::-1], two=False)
    k2 = []
    for i in get_lst(ucq, clear=True):
        k2.append(InlineKeyboardButton(i, callback_data="." + ucq + "/" + i))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="." + ucq + "/" + i,
                                                           callback=eval(datos[ucq_spl[0]][3])))
    keyboard = slice_lst(k2, keyboard, 4)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916<strong>" + datos[ucq_spl[0]][2] + "</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def send_dict(update, context):
    update.callback_query.answer()
    ucq = update.callback_query["data"][1:]
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Ahí va!! </strong>",
                                            parse_mode=telegram.ParseMode.HTML)
    if ucq.split("/")[1] == "dm":
        nro = u'\U0001F3BC ' + ucq.split("/")[2] + " / " + ucq.split("/")[3] + u' \U0001F449'
        c = "captionm"
    elif ucq.split("/")[1] == "dr":
        nro = u'\U0001F941 ' + ucq.split("/")[2] + " / " + ucq.split("/")[3] + u' \U0001F449'
        c = "captionr"

    for i, j in zip(get_lst(ucq, clear=False), json.load(open("datos.json"))[c]):
        with open(ucq + "/" + i, "rb") as audio_file:
            context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                                   caption=nro + j)

    keyboard = [[InlineKeyboardButton("volver a dictados", callback_data="dict")],
                [InlineKeyboardButton("Tonalidad y/o compás", callback_data="tyc" + ucq)],
                [InlineKeyboardButton("Solución", callback_data="sol" + ucq)]]
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="tyc" + ucq, callback=send_tyc))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="sol" + ucq, callback=send_sol))
    reply_markup = InlineKeyboardMarkup(keyboard, one_time_Keyboard=True)

    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Elegí una opción</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def send_sol(update, context):
    update.callback_query.answer()
    ucq = update.callback_query["data"][7:]
    update.callback_query.edit_message_text(text="\U0001f916 <strong>A ver.........</strong>",
                                            parse_mode=telegram.ParseMode.HTML)
    with open("dictimag/" + ucq + ".png", "rb") as photo_file:
        context.bot.send_photo(chat_id=update.callback_query["message"]["chat"]["id"], photo=photo_file,
                               caption=u'\U0001F648 \U0001F91E \U0001F91E \U0001F91E')
    keyboard = base_key("Volver a dictados", "dict", two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Elegí una opción</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def send_tyc(update, context):
    update.callback_query.answer()
    ucq = update.callback_query["data"]
    us = ucq.split("/")
    keyboard = [[InlineKeyboardButton("volver a dictados", callback_data="dict")],
                [InlineKeyboardButton("Solución", callback_data="sol" + ucq[3:])]]
    reply_markup = InlineKeyboardMarkup(keyboard, remove_keyboard=True)
    update.callback_query.edit_message_text(text=" \U0001f916 <strong>Está en: " + tyc[us[1]][us[2]][us[3]] +
                                            "</strong>", reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

def send_lect(update, context):
    update.callback_query.answer()
    ucq = update.callback_query["data"][1:]
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Ahí va!!</strong>",
                                            parse_mode=telegram.ParseMode.HTML)
    if ucq.split("/")[1] == "lm":
        msg = u'\U0001F440 \U0001F3BC' + " Nro: " + ucq.split("/")[3]
    elif ucq.split("/")[1] == "lr":
        msg = u'\U0001F440 \U0001F941' + " Nro: " + ucq.split("/")[3]

    with open(ucq + ".png", "rb") as photo_file:
        context.bot.send_photo(chat_id=update.callback_query["message"]["chat"]["id"], photo=photo_file, caption=msg)
    keyboard = base_key("Volver a lecturas", "lect", two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Elegí una opción</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

def chapters(update, context):
    update.callback_query.answer()
    ucq = update.callback_query["data"]
    keyboard = base_key(two=True)
    k2 = []
    for i in datos[ucq]:
        k2.append(InlineKeyboardButton("Cap" + i, callback_data="<" + ucq + "/" + i))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="<" + ucq + "/" + i, callback=melo_hind_list))
    keyboard = slice_lst(k2, keyboard, 4)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Elegí un capítulo</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def melo_hind_list(update, context):
    update.callback_query.answer()
    ucq = update.callback_query["data"][1:]
    keyboard = base_key("Atras", ucq.split("/")[0], two=False)
    k2 = []
    for i in get_lst(ucq, clear=True):
        k2.append(InlineKeyboardButton(i, callback_data=(ucq + "/" + i)[::-1]))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=(ucq + "/" + i)[::-1], callback=send_melo_hind))
    keyboard = slice_lst(k2, keyboard, 3)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Puedo ofrecerte estos ejercicios:</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def send_melo_hind(update, context):
    update.callback_query.answer()
    ucq = update.callback_query["data"][::-1]
    update.callback_query.edit_message_text(text="\U0001f916 <strong>As2D2 procesando...</strong>",
                                            parse_mode=telegram.ParseMode.HTML)
    if ucq.split("/")[0] == "melo":
        cap = u'\U0001F941' + " Melo Castillo " + ucq.split("/")[2]
    elif ucq.split("/")[0] == "hind":
        cap = u'\U0001F941' + " Hindemith " + ucq.split("/")[2]

    with open(ucq + ".mp3", "rb") as audio_file:
        context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                               caption=cap)

    keyboard = base_key("Atras", "<" + ucq.split("/")[0] + "/" + ucq.split("/")[1], two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                                      text="\U0001f916 <strong>Hecho!!, Como seguimos...?</strong>",
                                      reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def books(update, context):
    update.callback_query.answer()
    keyboard = base_key(two=True)
    ucq = update.callback_query["data"]
    k2 = []
    for i in get_lst("bib", clear=True):
        k2.append(InlineKeyboardButton(i, callback_data=(ucq + "/" + i)[::-1]))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=(ucq + "/" + i)[::-1], callback=send_pdf))

    keyboard = slice_lst(k2, keyboard, 2)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Tengo estos libros:</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def send_pdf(update, context):
    update.callback_query.answer()
    ucq = update.callback_query["data"][::-1]
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Esperame que lo tengo que buscar...</strong>",
                                            parse_mode=telegram.ParseMode.HTML)
    with open(ucq + ".pdf", "rb") as pdf_file:
        context.bot.send_document(chat_id=update.callback_query["message"]["chat"]["id"], document=pdf_file,
                                  caption=u'📖 🤓 ' + ucq.split("/")[1])
    keyboard = base_key("Atras", "<" + ucq.split("/")[0] + "/" + ucq.split("/")[1], two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                                      text="\U0001f916 <strong>Ahí está!! Que mas....?</strong>",
                                      reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def working(update, context):
    update.callback_query.answer()
    keyboard = [[InlineKeyboardButton("Home", callback_data="home")],
                [InlineKeyboardButton("Terminar", callback_data="end")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.edit_message_text(text=u'\U0001F4BB\U0001F9F0 Estamos codeando para usted',
                                            reply_markup=reply_markup)


def start(update, context):
    first_name = update.message.from_user.first_name
    msg = u"\U0001f916 <strong>Hola {}!! soy Astorito, el droide de Astor.</strong>\U0001FA97\n"\
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
    for i in range(7):
        if i > 0:
            k2.append(InlineKeyboardButton(i, callback_data="t" + str(i)))
            disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="t" + str(i), callback=fundamental))

    keyboard.append(k2)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        text="\U0001f916 <strong>Cuantas notas querés que te mande?</strong>",
        reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def fundamental(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[3] = update.callback_query["data"][1:]
    print(c)
    keyboard = base_key("Atras", "s" + c[2], two=False)
    k2 = [(InlineKeyboardButton("Si", callback_data="True")), (InlineKeyboardButton("No", callback_data="False"))]
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="True", callback=snd_scl))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="False", callback=snd_scl))
    keyboard.append(k2)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        text="\U0001f916 <strong>Querés que la secuencia empiece siempre con la fundamental?</strong>",
        reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def snd_scl(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[4] = update.callback_query["data"]
    print(c)
    seq = Sequence(c[1], c[2], int(c[3]), c[4])
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Primero te mando la escala!! </strong>",
                                            parse_mode=telegram.ParseMode.HTML)
    #seq.get_scale_audio()
    with open("escalas/" + c[2] + "/" + c[1] + ".mp3", "rb") as audio_file:
        context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                               caption="<strong>" + c[1] + " " + c[2] + ":</strong>" + " " +
                                       nice_name(seq.scale_pitches), parse_mode=telegram.ParseMode.HTML)
        #os.remove("escala.wav")
    return snd_seq(update, context)

def snd_seq(update, context):
    update.callback_query.answer()
    c = context.user_data
    seq = Sequence(c[1], c[2], int(c[3]), c[4])
    c[5] = nice_name(seq.seq_pitches)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Paciencia, estoy eligiendo sonidos para vos...."
                            "Que notas son? </strong>", parse_mode=telegram.ParseMode.HTML)
    seq.get_seq_audio()
    with open("seq.flac", "rb") as audio_file:
        context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                               caption="Secuencia de notas en " + c[1] + " " + c[2])
        os.remove("seq.flac")
    keyboard = base_key("Solución", "y", two=False)
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="y", callback=notes))
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Waiting orders .......</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def notes(update, context):
    update.callback_query.answer()
    c = context.user_data
    keyboard = base_key("Otro!!", "j", two=False)
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="j", callback=snd_seq))
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>" + c[5] + "</strong>",
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


updater.start_polling()#drop_pending_updates=True
updater.idle()
