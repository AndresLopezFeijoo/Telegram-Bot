import os
import telegram.ext
from telegram import InlineKeyboardButton

TOKEN = "1965896728:AAFgG4MTLoLy8QnqINF4qLm4_umRJM7DJHo"
updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher


def slice_lst(lst, lst2, step):
    for i in range(0, len(lst), step):
        lst2.append(lst[i:i+step])
    return lst2


def get_lst(path, clear: bool):
    if clear:
        lst = [i.split(".")[0] for i in os.listdir(path) if not i.startswith('.')]
    else:
        lst = [i for i in os.listdir(path) if not i.startswith('.')]

    return sorted(lst)


def base_key(*args, two: bool):
    if two:
        keyboard = [[InlineKeyboardButton("Terminar", callback_data="end"),
                     InlineKeyboardButton("Home", callback_data="home")]]
    else:
        keyboard = [[InlineKeyboardButton(args[0], callback_data=args[1])],
                    [InlineKeyboardButton("Home", callback_data="home"),
                     InlineKeyboardButton("Terminar", callback_data="end")]]
    return keyboard

