import telegram.ext
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from Tools import slice_lst, get_lst, base_key, send_mail
from stats import new_json_data, plot_data
import random
import logging
import os

logging.basicConfig(filename="log.txt", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = json.load(open("token.json"))["tok"]
devid = json.load(open("token.json"))["chatid"]
reconocimientos = json.load(open("reconicimientos.json"))
updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher
datos = json.load(open("datos.json"))
tyc = json.load(open("typ.json"))

def mel_rit(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
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
    keyboard = base_key("Atras", c[1], two=False)
    k2 = []
    d = {"m": True, "r": False}
    try:
        for i in get_lst(c[0] + "/" + c[1] + "/" + c[2], clear=True, nr=d[c[1]]):
            k2.append(InlineKeyboardButton(str(i), callback_data="o" + str(i)))
            disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="o" + str(i), callback=send_dic_lec))
        keyboard = slice_lst(k2, keyboard, 4)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(text="\U0001f916<strong>" + datos[c[0]][2] + "</strong>",
                                                reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
    except: # FileNotFoundError
        return error_no_file(update, context)



def send_dic_lec(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[3] = update.callback_query["data"][1:]
    logging.info("Sending Dict/Lect -- " + c[0] + "/" + c[1] + "/" + c[2] + "/" + c[3])
    path = c[0] + "/" + c[1] + "/" + c[2] + "/" + c[3]

    if c[0] == "dict":
        update.callback_query.edit_message_text(text="\U0001f916 <strong>Esperá.. te voy a mandar 5 audios\n"
                                                     "Ahí van..!! </strong>",
                                                parse_mode=telegram.ParseMode.HTML)
        if c[1] == "m":
            new_json_data("dm")
            nro = u"\U0001F3BC " + c[2] + " / " + c[3] + u" \U0001F449"
            cp = "captionm"
        elif c[1] == "r":
            new_json_data("dr")
            nro = u"\U0001F941 " + c[2] + " / " + c[3] + u" \U0001F449"
            cp = "captionr"

        for i, j in zip(get_lst(path, clear=False, nr=False), datos[cp]):
            context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_audio")
            with open(path + "/" + i, "rb") as audio_file:
                context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                                       caption=nro + j, timeout=20)

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
        update.callback_query.edit_message_text(text="\U0001f916 <strong>As2d2 working.... </strong>",
                                                parse_mode=telegram.ParseMode.HTML)
        if c[1] == "m":
            new_json_data("lm")
            msg = u'\U0001F440 \U0001F3BC' + " Nro: " + c[3]
        elif c[1] == "r":
            new_json_data("lr")
            msg = u'\U0001F440 \U0001F941' + " Letra: " + c[3]

        with open(path + ".png", "rb") as photo_file:
            context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_audio")
            context.bot.send_photo(chat_id=update.callback_query["message"]["chat"]["id"], photo=photo_file,
                                   caption=msg)
        keyboard = base_key("Volver a lecturas", "lect", two=False)
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                                text="\U0001f916 <strong>Elegí una opción</strong>",
                                reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
    else:
        return error_no_file(update, context)


def send_sol(update, context):
    update.callback_query.answer()
    c = context.user_data
    path = c[1] + "/" + c[2] + "/" + c[3]
    update.callback_query.edit_message_text(text="\U0001f916 <strong>A ver.........</strong>",
                                            parse_mode=telegram.ParseMode.HTML)
    with open("dictimag/" + path + ".png", "rb") as photo_file:
        context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_photo")
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
    keyboard = [[InlineKeyboardButton("volver a dictados", callback_data="dict")],
                [InlineKeyboardButton("Solución", callback_data="sol")]]
    reply_markup = InlineKeyboardMarkup(keyboard, remove_keyboard=True)
    update.callback_query.edit_message_text(text=" \U0001f916 <strong>Está en: " + tyc[c[1]][c[2]][c[3]] +
                                                 "</strong>", reply_markup=reply_markup,
                                            parse_mode=telegram.ParseMode.HTML)


def chapters(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
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
    keyboard = base_key("Atras", c[0], two=False)
    k2 = []
    try:
        for i in get_lst(c[0] + "/" + c[1], clear=True, nr=False):
            k2.append(InlineKeyboardButton(i, callback_data=">" + i))
            disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=(">" + i), callback=send_melo_hind))
        keyboard = slice_lst(k2, keyboard, 3)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(text="\U0001f916 <strong>Puedo ofrecerte estos ejercicios:</strong>",
                                                reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
    except:
        return error_no_file(update, context)


def send_melo_hind(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[2] = update.callback_query["data"][1:]
    logging.info("Sending Melo/Hind -- " + c[0] + "/" + c[1] + "/" + c[2])
    update.callback_query.edit_message_text(text="\U0001f916 <strong>As2d2 procesando...</strong>",
                                            parse_mode=telegram.ParseMode.HTML)
    if c[0] == "melo":
        new_json_data("melo")
        cap = u'\U0001F941' + " Melo Castillo " + c[2]
    elif c[0] == "hind":
        new_json_data("hind")
        cap = u'\U0001F941' + " Hindemith " + c[2]

    with open(c[0] + "/" + c[1] + "/" + c[2] + ".mp3", "rb") as audio_file:
        context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_audio")
        context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                               caption=cap, timeout=20)

    keyboard = base_key("Atras", "<" + c[1], two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Hecho!!, Como seguimos...?</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def books(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
    keyboard = base_key(two=True)
    k2 = []
    for i in get_lst(c[0], clear=True, nr=False):
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
    logging.info("Sending .pdf file -- " + c[1])
    new_json_data("bib")
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Esperame que lo tengo que buscar...\n"
                                                 "Mi casa es un lio de papeles</strong>",
                                            parse_mode=telegram.ParseMode.HTML)
    with open(c[0] + "/" + c[1] + ".pdf", "rb") as pdf_file:
        context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_document")
        context.bot.send_document(chat_id=update.callback_query["message"]["chat"]["id"], document=pdf_file,
                                  caption=u'📖 🤓 ' + c[1], timeout=20)
    keyboard = base_key("Atras", c[0], two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Ahí está!! Que mas....?</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def sequence(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
    keyboard = base_key(two=True)
    k2 = []
    for i in get_lst(c[0] + "/", True, False):
        k2.append(InlineKeyboardButton(i, callback_data="q" + str(i)))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="q" + str(i), callback=seq2))

    keyboard = slice_lst(k2, keyboard, 1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Melódicas o Rítmicas?....</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def seq2(update, context):
    msg = {'M': "\U0001f916 <strong> Elegí una fundamental....... </strong>",
           'R': "\U0001f916 <strong> Pie binario o ternario?....... </strong>"}
    update.callback_query.answer()
    c = context.user_data
    c[1] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", c[0], two=False)
    k2 = []
    for i in get_lst(c[0] + "/" + c[1], True, False):
        k2.append(InlineKeyboardButton(i, callback_data="e" + str(i)))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="e" + str(i), callback=seq3))
    keyboard = slice_lst(k2, keyboard, 7)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        text=msg[c[1][0]], reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def seq3(update, context):
    msg = {'M': "\U0001f916 <strong>Eligí un modo.....</strong>",
           'R': "\U0001f916 <strong> Que nivel de dificultad?....... </strong>"}
    update.callback_query.answer()
    c = context.user_data
    c[2] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", "q" + c[1], two=False)
    k2 = []
    for i in get_lst(c[0] + "/" + c[1] + "/" + c[2], True, False):
        k2.append(InlineKeyboardButton(i, callback_data="s" + str(i)))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="s" + str(i), callback=seq4))
    keyboard = slice_lst(k2, keyboard, 2)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        text=msg[c[1][0]], reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def seq4(update, context):
    msg = {'M': ["\U0001f916 <strong>Cuantas notas te mando?\n3, 4 y 5 son secuencias que comienzan siempre "
                          "en la tónica.\n"
                          "Hard son seis notas y puede empezar por cualquier sonido!!!</strong>", "snd_scl", "x"],
           'R': ["\U0001f916 <strong> Cuantos pulsos?....... </strong>", "snd_pulse", "y"]}
    update.callback_query.answer()
    c = context.user_data
    c[3] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", "e" + c[2], two=False)
    k2 = []
    for i in get_lst(c[0] + "/" + c[1] + "/" + c[2] + "/" + c[3], True, False):
        k2.append(InlineKeyboardButton(i, callback_data="x" + i))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="x" + i, callback=snd_scale_or_pulse))
    keyboard = slice_lst(k2, keyboard, 7)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        text=msg[c[1][0]][0],
        reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def snd_scale_or_pulse(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[4] = update.callback_query["data"][1:]
    if c[1][0] == "M":
        update.callback_query.edit_message_text(text="\U0001f916 <strong>Primero te mando la escala!! </strong>",
                                                parse_mode=telegram.ParseMode.HTML)
        with open("escalas/" + c[3] + "/" + c[2] + ".mp3", "rb") as audio_file:
            context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                                   caption="<strong>" + c[2] + " " + c[3] + ":</strong>" + " " +
                                   str(json.load(open("scale_note_names.json"))[c[3]][c[2]])[2:-2],
                                   parse_mode=telegram.ParseMode.HTML)
        return snd_seq(update, context)
    else:
        update.callback_query.edit_message_text(text="\U0001f916 <strong>Primero te mando el pulso!! </strong>",
                                                parse_mode=telegram.ParseMode.HTML)

        with open("escalas/pulsos/" + c[2] + "/" + c[4] + ".flac", "rb") as audio_file:
            context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_audio")
            context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                                   caption=c[4] + " pulsos", parse_mode=telegram.ParseMode.HTML)
        return snd_seq(update, context)


def snd_seq(update, context):
    update.callback_query.answer()
    c = context.user_data
    logging.info("Enviando secuencia -- " + c[1] + "/" + c[2] + "/" + c[3] + "/" + c[4])
    if c[1] == 'Melódicas':
        new_json_data("sm")
    else:
        new_json_data("sr")
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Elegí estos sonidos para vos....\n"
                                 "Cuando lo tengas pedime la solución </strong>",
                            parse_mode=telegram.ParseMode.HTML)
    file = random.choice(get_lst("secuencias/" + c[1] + "/" + c[2] + "/" + c[3] + "/" + c[4], True, False))
    with open("secuencias/" + c[1] + "/" + c[2] + "/" + c[3] + "/" + c[4] + "/" + file + ".flac", "rb") as audio_file:
        context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_audio")
        context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                               caption="Secuencia, " + c[1] + ", " + c[2] + ", " + c[3], timeout=20)
    keyboard = base_key("Solución", "y" + file, two=False)
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="y" + file, callback=seq_sol))
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Waiting orders .......</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def seq_sol(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[5] = update.callback_query["data"][1:].split(".")[0]
    update.callback_query.edit_message_text(text="\U0001f916 <strong>A ver ????....</strong>",
                                            parse_mode=telegram.ParseMode.HTML)

    with open("secuencias/" + c[1] + "/" + c[2] + "/" + c[3] + "/" + c[4] + "/" + c[5] + ".png", "rb") as png_file:
        context.bot.send_photo(chat_id=update.callback_query["message"]["chat"]["id"], photo=png_file,
                               caption="Secuencia de " + c[4] + " pulsos en " + c[2])

    keyboard = base_key("Otro!!", "ñ", two=False)
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="ñ", callback=snd_seq))
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Como seguimos? .......</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def solf(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
    keyboard = base_key(two=True)
    k2 = []
    for i in get_lst(c[0] + "/", True, False):
        k2.append(InlineKeyboardButton(i, callback_data="s" + str(i)))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="s" + str(i), callback=solf_lst))
    keyboard = slice_lst(k2, keyboard, 1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>De que libro?....</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def solf_lst(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[1] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", "solf", two=False)
    k2 = []
    for i in get_lst(c[0] + "/" + c[1] + "/", True, True):
        k2.append(InlineKeyboardButton(i, callback_data="d" + str(i)))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="d" + str(i), callback=snd_solf))
    keyboard = slice_lst(k2, keyboard, 1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Tengo estas lecciones para ofrecerte:...</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def snd_solf(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[2] = update.callback_query["data"][1:]
    logging.info("Enviando solfeo -- " + c[0] + "/" + c[1] + "/" + c[2])
    new_json_data("sol")
    update.callback_query.edit_message_text(text="\U0001f916 <strong>As2d2 procesando...</strong>",
                                            parse_mode=telegram.ParseMode.HTML)
    cap = u"\U0001F3B6 Solfeo " + c[1] + " " + c[2]
    for i, j in zip(get_lst(c[0] + "/" + c[1] + "/" + c[2] + "/", False, False), datos["solf"]):
        context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_document")
        with open(c[0] + "/" + c[1] + "/" + c[2] + "/" + i, "rb") as audio_file:
            context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                                   caption=cap + j, timeout=30)

    keyboard = base_key("Atras", "s" + c[1], two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Hecho!!, Como seguimos...?</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def recon(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
    keyboard = base_key(two=True)
    k2 = []
    for i in get_lst(c[0] + "/", True, False):
        k2.append(InlineKeyboardButton(i, callback_data="1" + str(i)))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="1" + str(i), callback=recon2))

    keyboard = slice_lst(k2, keyboard, 1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Que tipo de reconocimiento?....</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

def recon2(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[1] = update.callback_query["data"][1:]
    keyboard = base_key(two=True)
    k2 = []
    for i in reconocimientos[c[1]]:
        k2.append(InlineKeyboardButton(i, callback_data="2" + str(i)))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="2" + str(i), callback=snd_recon))

    keyboard = slice_lst(k2, keyboard, 1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>De que año?....</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

def snd_recon(update, context):
    update.callback_query.answer()
    c = context.user_data
    if update.callback_query["data"] != "2":
        c[2] = update.callback_query["data"][1:]
    logging.info("Enviando Reconocimiento -- " + c[1] + "/" + c[2])
    new_json_data("rec")  #revisar stats.py para agregarlo

    try:
        file = random.choice(reconocimientos[c[1]][c[2]])
        with open("rec/" + c[1] + "/" + file + ".mp3", "rb") as audio_file:
            context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                                    text="\U0001f916 <strong>Elegí este ejemplo para vos....\n"
                                         "Cuando lo tengas pedime la solución </strong>",
                                    parse_mode=telegram.ParseMode.HTML)
            context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_audio")
            context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                                   caption="Reconocimiento de " + c[1] + " " + c[2])

        keyboard = base_key("Solución", "3" + file, two=False)
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="3" + file, callback=recon_sol))
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                                text="\U0001f916 <strong>Waiting orders .......</strong>",
                                reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
    except:
        return error_no_file(update, context)

def recon_sol(update, context):
    update.callback_query.answer()
    c = context.user_data
    c[3] = update.callback_query["data"][1:].split(".")[0]
    update.callback_query.edit_message_text(text="\U0001f916 <strong>La respuesta es:\n" + c[3].split("-")[1] +
                                                 "</strong>", parse_mode=telegram.ParseMode.HTML)

    keyboard = base_key("Otro!!", "2", two=False)
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="2", callback=snd_recon))
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Como seguimos? .......</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)




def rep(update, context):
    logging.info("Reporting")
    update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
    keyboard = base_key(two=True)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Escribime un mensaje con tu reporte.</strong>\n"
                                                 "Podes reportar si no estoy funcionando bien, o si encontraste "
                                                 "algun error en los materiales que envío.\nTambién podes escribirme a:"
                                                 "\n astorito.bot@gmail.com",
                                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def start(update, context):
    update.message.reply_text('🤖')
    first_name = update.message.from_user.first_name
    context.user_data[0] = "start"
    msg = u" <strong>Hola {}!! soy Astorito, el droide de Astor.</strong>\U0001FA97\n" \
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


def start_over(update, context):
    update.callback_query.answer()
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"], text="🤖",
                            parse_mode=telegram.ParseMode.HTML)
    context.user_data[0] = "start"
    k = [InlineKeyboardButton(text="Programa", url="https://cmbsas-caba.infd.edu.ar/sitio/nivel-medio/")]
    k2 = []
    for i in json.load(open("datos.json"))["start"]:
        k.append(InlineKeyboardButton(i[0], callback_data=i[1]))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=i[1], callback=eval(i[2])))
    for i in range(0, len(k), 2):
        k2.append(k[i:i + 2])
    reply_markup = InlineKeyboardMarkup(k2)
    context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="<strong>Empecemos otra vez!!</strong>\n"
                                 "Contame que queres hacer.",
                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def end(update, context):
    update.callback_query.answer()
    update.callback_query.edit_message_text(text="\U0001f916 <strong>Nos vemos la próxima</strong> \U0001FA97",
                                            parse_mode=telegram.ParseMode.HTML)
    return ConversationHandler.END


def handle_message(update, context):
    if context.user_data[0] == "rep":
        context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        send_mail(update.message["text"])
        update.message.reply_text("\U0001f916 <strong>Listo!!\nTu reporte fue enviado.\nGracias!!\n"
                                  f"Algo mas? 👉 /start"
                                  f"</strong>", parse_mode=telegram.ParseMode.HTML)
        context.user_data[0] = "-"
    else:
        update.message.reply_text(f"\U0001f916 <strong>Dijiste {update.message.text} y no te entiendo.....</strong>\n"
                                  "Todavia no se conversar pero tengo muchos botones!!\n"
                                  "para inciar apretá 👉 /start", parse_mode=telegram.ParseMode.HTML)


def error_no_file(update, context):
    update.callback_query.answer()
    c = context.user_data
    logging.error("No habia materiales en " + str(c))
    #context.bot.sendMessage(chat_id=devid, text="No habia materiales en " + str(c))
    if c[0] == "start":
        keyboard = base_key("Volver", c[0], two=True)
    else:
        keyboard = base_key("Volver", c[0], two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="\U0001f916 <strong>No tengo materiales en esa categoría....\n"
                                                 "Que hacemos?</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def error(update, context): # Para cuando usan botoneras viejas y se marea el dicc user_data
    logging.error(str(context.error))
    if str(context.error) != "Message is not modified: specified new message content and reply markup are exactly" \
                             " the same as a current content and reply markup of the message":
        context.bot.sendMessage(chat_id=devid, text="Hubo un error " + str(context.error))
        context.bot.sendMessage(chat_id=update.effective_chat.id,
                                text="<strong>🤖 Que papelón!!,\nalgo salió mal..... \n"
                                     f"Seguí por acá 👉 /start </strong>", parse_mode=telegram.ParseMode.HTML)

def stats(update, context):
    update.message.reply_text('🤖')
    first_name = update.message.from_user.first_name
    context.user_data[0] = "start"
    msg = u" <strong>Hola {}!! Aqui están algunos datos del uso del bot.</strong>".format(first_name)
    context.bot.sendMessage(chat_id=devid, text=msg, parse_mode=telegram.ParseMode.HTML)
    plot_data(json.load(open("usage.json")))
    with open("grafico_uso.png", "rb") as photo_file:
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_file)
    os.remove("grafico_uso.png")
    context.bot.sendMessage(chat_id=update.effective_chat.id,
                            text="<strong>🤖 No vayas a tipear esto..... \n"
                                 f"Seguí por acá 👉 /start </strong>", parse_mode=telegram.ParseMode.HTML)

disp.add_handler(telegram.ext.CommandHandler("stats", stats))
disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="home", callback=start_over))
disp.add_error_handler(error)

updater.start_polling(drop_pending_updates=True, timeout=15)
updater.idle()
