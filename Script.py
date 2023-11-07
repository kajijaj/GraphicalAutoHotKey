import ctypes
import csv
from time import sleep
import datetime
from apscheduler.schedulers.background import BackgroundScheduler


HEX_CODES = {'esc': 0x01, 'f1': 0x3B, 'f2': 0x3C, 'f3': 0x3D, 'f4': 0x3E, 'f5': 0x3F, 'f6': 0x40,
             'f7': 0x41, 'f8': 0x42, 'f9': 0x43, 'f10': 0x44, 'f11': 0x57, 'f12': 0x58, 'prtscn': 0xE037,
             'scrlk': 0x46, 'pause': 0xE11D45, 'ё': 0x29, '1': 0x02, '2': 0x03, '3': 0x04, '4': 0x05, '5': 0x06,
             '6': 0x07, '7': 0x08, '8': 0x09, '9': 0x0A, '0': 0x0B, '-': 0x0C, '+': 0x0D, 'backspace': 0x0E,
             'insert': 0xE052, 'home': 0xE047, 'pgup': 0xE049, 'numlock': 0x45, '/': 0x35, '*': 0x37, 'tab': 0x0F,
             'q': 0x10, 'w': 0x11, 'e': 0x12, 'r': 0x13, 't': 0x14, 'y': 0x15, 'u': 0x16, 'i': 0x17, 'o': 0x18,
             'p': 0x19, '{': 0x1A, '}': 0x1B, '|': 0x2B, 'del': 0xE053, 'end': 0xE04F, 'pgdown': 0xE051,
             'capslock': 0x3A, 'a': 0x1E, 's': 0x1F, 'd': 0x20, 'f': 0x21, 'g': 0x22, 'h': 0x23, 'j': 0x24,
             'k': 0x25, 'l': 0x26, ':': 0x27, "'": 0x28, 'enter': 0x1C, 'shift': 0x2A, 'z': 0x2C, 'x': 0x2D,
             'c': 0x2E, 'v': 0x2F, 'b': 0x30, 'n': 0x31, 'm': 0x32, '<': 0x33, '>': 0x34, '?': 0x35, 'up': 0xE048,
             'ctrl': 0x1D, 'windows': 0xDB, 'alt': 0x38, 'space': 0x39, 'left': 0xE04B, 'down': 0xE050, 'right': 0xE04D}

SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def execute(event, action):
    buttons_list = event.split('_')
    if action == 'кликнуть':
        for button in buttons_list:
            PressKey(HEX_CODES[button])
            ReleaseKey(HEX_CODES[button])
    elif 'удерживать' in action:
        hold_time = float(action[action.index('(') + 1: action.index(')')])
        current_timer = 0
        while current_timer <= hold_time:
            for button in buttons_list:
                PressKey(HEX_CODES[button])
                ReleaseKey(HEX_CODES[button])
            current_timer += 0.1
            sleep(0.1)


rows = []
file = open('ScriptFiles/output.csv', encoding='utf8')
reader = csv.DictReader(file, delimiter=';', quotechar='"')
for row in reader:
    rows.append(row)
file.close()


scheduler = BackgroundScheduler()
for row in rows:
    time = list(map(int, row['time'].split(':')))
    date = list(map(int, row['date'].split('-')))
    date_datetime = datetime.datetime(date[0], date[1], date[2], time[0], time[1])
    scheduler.add_job(execute, 'date', run_date=date_datetime, args=(row['event'], row['action']))


scheduler.start()
sleep(86500)






