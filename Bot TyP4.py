import telegram.ext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

TOKEN = ""
updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher

tyc = {"1": "Do Mayor y en 3/4", "2": "Do Mayor y en 3/4", "51": "Do Mayor y en 3/4", "52": "Do Mayor y en 3/4",
       "110": "Do Mayor y en 3/4", "163": "Do Mayor y en 3/4", "203": "3/4", "254": "2/4",
       "306": "7/8", "378": "6/4"}

dicts = {"1": ["1.1.mp3", "1.2.mp3", "1.3.mp3", "1.4.mp3", "1.5.mp3", "Do Mayor, 3/4", "1.png"],
         "2": ["2.1.mp3", "2.2.mp3", "2.3.mp3", "2.4.mp3", "2.5.mp3"],
         "51": ["51.1.mp3", "51.2.mp3", "51.3.mp3", "51.4.mp3", "51.5.mp3"],
         "52": ["52.1.mp3", "52.2.mp3", "52.3.mp3", "52.4.mp3", "52.5.mp3"],
         "110": ["110.1.mp3", "110.2.mp3", "110.3.mp3", "110.4.mp3", "110.5.mp3"],
         "163": ["163.1.mp3", "163.2.mp3", "163.3.mp3", "163.4.mp3", "163.5.mp3"],
         "203": ["203.1.mp3", "203.2.mp3", "203.3.mp3", "203.4.mp3", "203.5.mp3"],
         "254": ["254.1.mp3", "254.2.mp3", "254.3.mp3", "254.4.mp3", "254.5.mp3"],
         "306": ["306.1.mp3", "306.2.mp3", "306.3.mp3", "306.4.mp3", "306.5.mp3"],
         "378": ["378.1.mp3", "378.2.mp3", "378.3.mp3", "378.4.mp3", "378.5.mp3"]}

hind = {"III": {},
        "IV": {},
        "V": {},
        "VI": {},
        "VII": {"78a", "78b", "79b", "79c", "79d", "80a", "80e", "80f", "81b", "81c", "81d", "82e"},
        "VIII": {"102a", "103c", "103d"},
        "IX": {"122c", "124d", "124e", },
        "X": {"141a", "142c", "142d"}}

melo = {"mIII": {"74", "75", "76"},
        "mV": {},
        "mVI": {},
        "mVII": {},
        "mVIII": {"245", "252", "256", "257", "258"},
        "mIX": {"278", "280", "282", "289", "291", "293"},
        "mX": {"315", "319", "323", "325"},
        "mXI": {"346", "348", "361", "364", "365", "366", "367"}}

lect = {"lmI": {"1", "2", "3"},
        "lmII": {"1", "2", "3"},
        "lmIII": {},
        "lmIV": {},
        "lrI": {},
        "lrII": {},
        "lrIII": {},
        "lrIV": {}}


def lista_dictados(update, context):
    update.callback_query.answer()
    msg = "Estos son los dictados que te puedo ofrecer:"

    if update.callback_query["data"] == "mI":
        keyboard = [[InlineKeyboardButton("volver a Dictados", callback_data="dict"),]]
        for i in dicts:
            if int(i) < 51:
                keyboard.append([InlineKeyboardButton(str(i), callback_data=str(i))])
                disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=str(i), callback=send_dict))
                reply_markup = InlineKeyboardMarkup(keyboard) #Creo que esto deberia estar afuera del if. funciona igual...
                update.callback_query.edit_message_text(text=msg, reply_markup=reply_markup) #Idem arriba
    elif update.callback_query["data"] == "mII":
        keyboard = [[InlineKeyboardButton("volver a Dictados", callback_data="dict"), ]]
        for i in dicts:
            if 50 < int(i) < 101:
                keyboard.append([InlineKeyboardButton(str(int(i)-50), callback_data=str(i))])
                disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=str(i), callback=send_dict))
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.callback_query.edit_message_text(text=msg, reply_markup=reply_markup)
    elif update.callback_query["data"] == "mIII":
        keyboard = [[InlineKeyboardButton("volver a Dictados", callback_data="dict"), ]]
        for i in dicts:
            if 100 < int(i) < 151:
                keyboard.append([InlineKeyboardButton(str(int(i) - 100), callback_data=str(i))])
                disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=str(i), callback=send_dict))
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.callback_query.edit_message_text(text=msg, reply_markup=reply_markup)
    elif update.callback_query["data"] == "mIV":
        keyboard = [[InlineKeyboardButton("volver a Dictados", callback_data="dict"), ]]
        for i in dicts:
            if 150 < int(i) < 201:
                keyboard.append([InlineKeyboardButton(str(int(i) - 150), callback_data=str(i))])
                disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=str(i), callback=send_dict))
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.callback_query.edit_message_text(text=msg, reply_markup=reply_markup)
    elif update.callback_query["data"] == "rI":
        keyboard = [[InlineKeyboardButton("volver a Dictados", callback_data="dict"), ]]
        for i in dicts:
            if 200 < int(i) < 251:
                keyboard.append([InlineKeyboardButton(str(int(i) - 200), callback_data=str(i))])
                disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=str(i), callback=send_dict))
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.callback_query.edit_message_text(text=msg, reply_markup=reply_markup)
    elif update.callback_query["data"] == "rII":
        keyboard = [[InlineKeyboardButton("volver a Dictados", callback_data="dict"), ]]
        for i in dicts:
            if 250 < int(i) < 301:
                keyboard.append([InlineKeyboardButton(str(int(i) - 250), callback_data=str(i))])
                disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=str(i), callback=send_dict))
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.callback_query.edit_message_text(text=msg, reply_markup=reply_markup)
    elif update.callback_query["data"] == "rIII":
        keyboard = [[InlineKeyboardButton("volver a Dictados", callback_data="dict"), ]]
        for i in dicts:
            if 300 < int(i) < 351:
                keyboard.append([InlineKeyboardButton(str(int(i) - 300), callback_data=str(i))])
                disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=str(i), callback=send_dict))
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.callback_query.edit_message_text(text=msg, reply_markup=reply_markup)
    elif update.callback_query["data"] == "rIV":
        keyboard = [[InlineKeyboardButton("volver a Dictados", callback_data="dict"), ]]
        for i in dicts:
            if 350 < int(i) < 401:
                keyboard.append([InlineKeyboardButton(str(int(i) - 350), callback_data=str(i))])
                disp.add_handler(telegram.ext.CallbackQueryHandler(pattern='^' + str(i) + '$', callback=send_dict))
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.callback_query.edit_message_text(text=msg, reply_markup=reply_markup)


def send_dict(update, context):
    update.callback_query.answer()
    caption = [" completo", " Comapases 1, 2 y primer sonido del 3", " Compases 3, 4 y primer sonido del 5",
               " Compases 5, 6 y primer sonido del 7", " Compases 7 y 8"]
    if int(update.callback_query["data"]) < 201:
        if int((update.callback_query["data"])) < 50:
            nro = u'\U0001F3BC I/' + str(int(update.callback_query["data"])) + u'\U0001F449 '
        elif int((update.callback_query["data"])) < 100:
            nro = u'\U0001F3BC II/' + str(int(update.callback_query["data"]) - 50) + u' \U0001F449'
        elif int((update.callback_query["data"])) < 150:
            nro = u'\U0001F3BC III/' + str(int(update.callback_query["data"]) - 100) + u' \U0001F449'
        else:
            nro = u'\U0001F3BC IV/' + str(int(update.callback_query["data"]) - 150) + u' \U0001F449'
    elif int(update.callback_query["data"]) > 200:
        if int((update.callback_query["data"])) < 250:
            nro = u'\U0001F941 I/' + str(int(update.callback_query["data"]) - 200) + u'\U0001F449 '
        elif int((update.callback_query["data"])) < 300:
            nro = u'\U0001F941 II/' + str(int(update.callback_query["data"]) - 250) + u' \U0001F449'
        elif int((update.callback_query["data"])) < 350:
            nro = u'\U0001F941 III/' + str(int(update.callback_query["data"]) - 300) + u' \U0001F449'
        else:
            nro = u'\U0001F941 IV/' + str(int(update.callback_query["data"]) - 350) + u' \U0001F449'

    for i, j in zip(dicts[update.callback_query["data"]], caption):
        with open("dictaudios/" + i, "rb") as audio_file:
            context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                                       caption=nro + j)

    keyboard = [[InlineKeyboardButton("volver a dictados", callback_data="dict")],
                [InlineKeyboardButton("Tonalidad y/o compás", callback_data=str(int(update.callback_query["data"]) + 400))],
                [InlineKeyboardButton("Solución", callback_data=str(int(update.callback_query["data"]) + 800))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="Elegí una opción", reply_markup=reply_markup)
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=str(int(update.callback_query["data"]) + 400),
                                                       callback=send_tyc))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=str(int(update.callback_query["data"]) + 800),
                                                       callback=send_sol))


def años(update, context):
    update.callback_query.answer()
    if update.callback_query["data"] == "mel":
        keyboard = [[InlineKeyboardButton("I", callback_data="mI"),
                     InlineKeyboardButton("II", callback_data="mII"),
                     InlineKeyboardButton("III", callback_data="mIII"),
                     InlineKeyboardButton("IV", callback_data="mIV")],
                    [InlineKeyboardButton("Home", callback_data="home")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(text="De que año?", reply_markup=reply_markup)

    elif update.callback_query["data"] == "rit":
        keyboard = [[InlineKeyboardButton("I", callback_data="rI"),
                     InlineKeyboardButton("II", callback_data="rII"),
                     InlineKeyboardButton("III", callback_data="rIII"),
                     InlineKeyboardButton("IV", callback_data="rIV")],
                    [InlineKeyboardButton("Home", callback_data="home")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(text="De que año?", reply_markup=reply_markup)

    elif update.callback_query["data"] == "lmel":
        keyboard = [[InlineKeyboardButton("I", callback_data="lmI"),
                     InlineKeyboardButton("II", callback_data="lmII"),
                     InlineKeyboardButton("III", callback_data="lmIII"),
                     InlineKeyboardButton("IV", callback_data="lmIV")],
                    [InlineKeyboardButton("Home", callback_data="home")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(text="De que año?", reply_markup=reply_markup)

    elif update.callback_query["data"] == "lrit":
        keyboard = [[InlineKeyboardButton("I", callback_data="lrI"),
                     InlineKeyboardButton("II", callback_data="lrII"),
                     InlineKeyboardButton("III", callback_data="lrIII"),
                     InlineKeyboardButton("IV", callback_data="lrIV")],
                    [InlineKeyboardButton("Home", callback_data="home")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(text="De que año?", reply_markup=reply_markup)

    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="mI", callback=lista_dictados))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="mII", callback=lista_dictados))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="mIII", callback=lista_dictados))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="mIV", callback=lista_dictados))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="rI", callback=lista_dictados))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="rII", callback=lista_dictados))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="rIII", callback=lista_dictados))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="rIV", callback=lista_dictados))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="lmI", callback=lista_lect))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="lmII", callback=lista_lect))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="lmIII", callback=lista_lect))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="lmIV", callback=lista_lect))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="lrI", callback=lista_lect))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="lrII", callback=lista_lect))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="lrIII", callback=lista_lect))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="lrIV", callback=lista_lect))


def dictados(update, context):
    update.callback_query.answer()
    keyboard = [[InlineKeyboardButton("Melódicos", callback_data="mel"),
                 InlineKeyboardButton("Rítmicos", callback_data="rit")],
                [InlineKeyboardButton("Home", callback_data="home")]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="Melodicos o Ritmicos?", reply_markup=reply_markup)
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="mel", callback=años))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="rit", callback=años))



def send_sol(update, context):
    update.callback_query.answer()
    with open("dictimag/" + str(int(update.callback_query["data"]) - 800) + ".png", "rb") as photo_file:
        context.bot.send_photo(chat_id=update.callback_query["message"]["chat"]["id"], photo=photo_file,
                               caption=u'\U0001F648'u'\U0001F648'u'\U0001F648'u'\U0001F602'u'\U0001F602'u'\U0001F602')

    keyboard = [[InlineKeyboardButton("Home", callback_data="home")],
                [InlineKeyboardButton("Terminar", callback_data="end")],
                [InlineKeyboardButton("volver a dictados", callback_data="dict")]]  # Inventar un boton par aterminar el bot
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="Hacemos algo mas?", reply_markup=reply_markup)


def send_tyc(update, context):
    update.callback_query.answer()
    keyboard = [[InlineKeyboardButton("volver a dictados", callback_data="dict")],
                [InlineKeyboardButton("Solución", callback_data=str(int(update.callback_query["data"]) + 400))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="Está en: " + tyc[str(int(update.callback_query["data"]) - 400)],
                                            reply_markup=reply_markup)


def chapters(update, context):
    update.callback_query.answer()
    if update.callback_query["data"] == "hindemith":
        keyboard = [[InlineKeyboardButton("Cap III ", callback_data="III"),
                    InlineKeyboardButton("Cap IV ", callback_data="IV"),
                    InlineKeyboardButton("Cap V ", callback_data="V")],
                    [InlineKeyboardButton("Cap VI ", callback_data="VI"),
                    InlineKeyboardButton("Cap VII ", callback_data="VII"),
                    InlineKeyboardButton("Cap VIII ", callback_data="VIII")],
                    [InlineKeyboardButton("Cap IX ", callback_data="IX"),
                    InlineKeyboardButton("Cap X ", callback_data="X"),
                    InlineKeyboardButton("Home", callback_data="home")],
                    [InlineKeyboardButton("Terminar", callback_data="end"),
                    InlineKeyboardButton("Home", callback_data="home")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(text="Elegí un capítulo", reply_markup=reply_markup)
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="III", callback=hind_list))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="IV", callback=hind_list))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="v", callback=hind_list))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="VI", callback=hind_list))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="VII", callback=hind_list))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="VIII", callback=hind_list))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="IX", callback=hind_list))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="X", callback=hind_list))

    elif update.callback_query["data"] == "melo":
        keyboard = [[InlineKeyboardButton("Cap III ", callback_data="mIII"),
                     InlineKeyboardButton("Cap V ", callback_data="mV"),
                     InlineKeyboardButton("Cap VI ", callback_data="mVI")],
                    [InlineKeyboardButton("Cap VII ", callback_data="mVII"),
                     InlineKeyboardButton("Cap VIII ", callback_data="mVIII"),
                     InlineKeyboardButton("Cap IX ", callback_data="mIX")],
                    [InlineKeyboardButton("Cap X ", callback_data="mX"),
                     InlineKeyboardButton("Cap XI ", callback_data="mXI"),
                     InlineKeyboardButton("Home", callback_data="home")],
                    [InlineKeyboardButton("Terminar", callback_data="end"),
                     InlineKeyboardButton("Home", callback_data="home")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(text="Elegí un capítulo", reply_markup=reply_markup)
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="mIII", callback=melo_list))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="mV", callback=melo_list))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="mvI", callback=melo_list))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="mVII", callback=melo_list))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="mVIII", callback=melo_list))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="mIX", callback=melo_list))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="mX", callback=melo_list))
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="mXI", callback=melo_list))


def melo_list(update, context):
    update.callback_query.answer()
    keyboard = [[InlineKeyboardButton("Atras", callback_data="melo"),
                 InlineKeyboardButton("Home", callback_data="home"), ]]
    for i in melo[update.callback_query["data"]]:
        keyboard.append([InlineKeyboardButton(i, callback_data="mc" + str(int(i) + 1600))])
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="mc" + str(int(i) + 1600), callback=send_melo))
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="Puedo ofrecerte estos ejercicios:", reply_markup=reply_markup)

def send_melo(update, context):
    update.callback_query.answer()
    keyboard = [[InlineKeyboardButton("Volver a Melo Castillo", callback_data="melo")],
                [InlineKeyboardButton("Home", callback_data="home"),
                 InlineKeyboardButton("Terminar", callback_data="end")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="Elegí una opción:", reply_markup=reply_markup)

    with open("melo/" + str(int(update.callback_query["data"][2::]) - 1600) + ".mp3", "rb") as audio_file:
        context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file)



def lista_lect(update, context):
    update.callback_query.answer()
    keyboard = [[InlineKeyboardButton("Atras", callback_data="lecturas"),
                 InlineKeyboardButton("Home", callback_data="home"),]]
    for i in lect[update.callback_query["data"]]:
        keyboard.append([InlineKeyboardButton(i, callback_data="l" + str(int(i) + 1200))])
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="l" + str(int(i) + 1200), callback=send_lect))


    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="Puedo ofrecerte las siguientes lecturas :",
                                            reply_markup=reply_markup)

def send_lect(update, context):
    update.callback_query.answer()
    keyboard = [[InlineKeyboardButton("Volver a lecturas", callback_data="lecturas")],
                [InlineKeyboardButton("Home", callback_data="home"),
                 InlineKeyboardButton("Terminar", callback_data="end")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="Elegi una opción:", reply_markup=reply_markup)

    with open("lecturas/" + str(int(update.callback_query["data"][1::]) - 1200) + ".png", "rb") as photo_file:
        context.bot.send_photo(chat_id=update.callback_query["message"]["chat"]["id"], photo=photo_file)


def hind_list(update, context):
    update.callback_query.answer()
    keyboard = [[InlineKeyboardButton("Atras", callback_data="hindemith"),
                 InlineKeyboardButton("Home", callback_data="home")]]
    for i in hind[update.callback_query["data"]]:
        keyboard.append([InlineKeyboardButton(i, callback_data=i[::-1])])
        disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=i[::-1], callback=send_hind))

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="Puedo ofrecerte los siguientes ejercicios:", reply_markup=reply_markup)


def send_hind(update, context):
    update.callback_query.answer()
    keyboard = [[InlineKeyboardButton("Volver a hindemith", callback_data="hindemith")],
                [InlineKeyboardButton("Home", callback_data="home"),
                 InlineKeyboardButton("Terminar", callback_data="end")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="Elegí una opción:", reply_markup=reply_markup)

    with open("hindemith/" + update.callback_query["data"][::-1] + ".mp3", "rb") as audio_file:
        context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file)


def lecturas(update, context):
    update.callback_query.answer()
    keyboard = [[InlineKeyboardButton("Melódicas", callback_data="lmel"),
                 InlineKeyboardButton("Rítmicas", callback_data="lrit")],
                [InlineKeyboardButton("Home", callback_data="home")]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="Melodicas o Ritmicas?", reply_markup=reply_markup)
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="lmel", callback=años))
    disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="lrit", callback=años))


def working(update, context):
    update.callback_query.answer()
    keyboard = [[InlineKeyboardButton("Home", callback_data="home")],
                [InlineKeyboardButton("Terminar", callback_data="end")]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text=u'\U0001F4BB\U0001F9F0 Estamos codeando para usted',
                                            reply_markup=reply_markup)


def start_over(update, context):
    """Para volver a empezar pero no ingresando un mensaje"""
    update.callback_query.answer()
    keyboard = [[
        InlineKeyboardButton(text="Programa", url="https://cmbsas-caba.infd.edu.ar/sitio/nivel-medio/"),
        InlineKeyboardButton(text="Dicatdos", callback_data="dict")],
        [InlineKeyboardButton(text="hindemith", callback_data="hindemith"),
         InlineKeyboardButton(text="Melo Castillo", callback_data="melo")],
        [InlineKeyboardButton(text="Lecturas", callback_data="lecturas"),
         InlineKeyboardButton(text="Solfeos", callback_data="solfeos")],
         [InlineKeyboardButton(text="Teoria", callback_data="teoria"),
          InlineKeyboardButton(text="Terminar", callback_data="end")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="Empecemos otra vez!!\nContame que queres hacer.",
                                            reply_markup=reply_markup)


def end(update, context):
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=u'\U0001F609'" Nos vemos la próxima")
    return ConversationHandler.END


def start(update, context):
    first_name = update.message.from_user.first_name
    msg = "Hola {} bienvenido al bot de TyP de la música!!\nElegí con que empezamos, mucha suerte!!".format(first_name)
    keyboard = [[
        InlineKeyboardButton(text="Programa", url="https://cmbsas-caba.infd.edu.ar/sitio/nivel-medio/"),
        InlineKeyboardButton(text="Dicatdos", callback_data="dict")],
        [InlineKeyboardButton(text="hindemith", callback_data="hindemith"),
         InlineKeyboardButton(text="Melo Castillo", callback_data="melo")],
        [InlineKeyboardButton(text="Lecturas", callback_data="lecturas"),
         InlineKeyboardButton(text="Solfeos", callback_data="solfeos")],
        [InlineKeyboardButton(text="Teoria", callback_data="teoria"),
         InlineKeyboardButton(text="Terminar", callback_data="end")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendMessage(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup)


disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="home", callback=start_over))
disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="dict", callback=dictados))
disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="hindemith", callback=chapters))
disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="lecturas", callback=lecturas))
disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="melo", callback=chapters))
disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="solfeos", callback=working))
disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="teoria", callback=working))
disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="end", callback=end))


def handle_message(update, context):
    print(update.message)
    update.message.reply_text(f"Dijiste: {update.message.text}, no entiendo, \n"
                              "para inciar escribí /start")


disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))


updater.start_polling()
updater.idle()
