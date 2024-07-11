import os
import time

import tkinter as tk
from tkinter import Tk, Toplevel, Entry

import pyautogui
import pyperclip
import pygetwindow as gw

from .config import USER, PASSWORD, logger

def close_window(root: Tk):
    root.destroy()


def center_window(w, h, root: Tk):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    return "{}x{}+{}+{}".format(w, h, int(x), int(y))



def login(username_entry: Entry, password_entry: Entry, root: Tk, top: Toplevel):
    if username_entry.get() == USER and password_entry.get() == PASSWORD: 
        root.deiconify()
        top.destroy()


def paste(text: str):
    buffer = pyperclip.paste()
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")


def ensure_window_is_active(path):
    # Получить имя файла из пути
    filename = os.path.basename(path)

    # Получить список всех открытых окон
    windows = gw.getAllTitles()

    # Найти окно, которое содержит имя файла
    target_window = None
    for window_title in windows:
        if filename in window_title:
            target_window = gw.getWindowsWithTitle(window_title)[0]
            break

    if target_window:
        target_window.activate()
        # Дополнительная задержка для гарантии активации окна
        time.sleep(1)

def clear_text(find_entry, txt1):
    find_entry.delete("1.0", tk.END)
    txt1.configure(state='normal')
    txt1.delete("1.0", tk.END)
    txt1.configure(state='disabled')

def open_file(txt1, root, find_entry, event=None, index=None):
    if index:
        start = txt1.search(r"\n\n", f"{index} linestart", "1.0", backwards=True, regexp=True)
        if not start:
            start = "1.0"
        end = txt1.index("end")
        selected_text = txt1.get(start, end).strip()
        root.clipboard_clear()
        root.clipboard_append(selected_text)

        # Разделить текст для получения пути к файлу
        lines = selected_text.split('\n')
        path = lines[1] + '/' + lines[0] if len(lines) > 1 else ''

        # Открыть файл по пути
        if path:
            os.startfile(path, 'open')

        # Ожидание для обеспечения выполнения открытия файла
        time.sleep(2)

        # Проверка и ожидание активации окна
        ensure_window_is_active(path)

        # Симуляция нажатия Ctrl+F для поиска
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        # Вставка текста из поля ввода для поиска
        search_text = find_entry.get("1.0", tk.END)
        paste(search_text)


def handle_left_click(event, txt1, root, find_entry):
    if find_entry.get("1.0", tk.END) != '':
        index = txt1.index("@%d,%d" % (event.x, event.y))
        open_file(txt1, root, find_entry, index=index)

