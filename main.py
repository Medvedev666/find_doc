from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import scrolledtext
from tkinter.ttk import Notebook

from function.main_function import (
    login, close_window, center_window, 
    handle_left_click, clear_text
)
from function.findDocs_functions import findDocs




root = ttk.Window(themename="newtheme")

top = Toplevel(root)
top.resizable(False, False)
top.title('Окно авторизации')
top.geometry('420x220')


# Настройка стилей ttkbootstrap
style = ttk.Style()
style.configure('CustomSize.TButton', font=('Arial', 10), width=17, height=10)
style.configure('Custom.TCheckbutton', background='#d0e3f7')


username_label = ttk.Label(top, text='Имя пользователя')
username_label.pack()


username_entry = ttk.Entry(top)
username_entry.pack()


password_label = ttk.Label(top, text='Пароль')
password_label.pack()


password_entry = ttk.Entry(top)
password_entry.pack()


send_btn = ttk.Button(top, text='Войти', command=lambda: login(username_entry, password_entry, root, top), style='CustomSize.TButton')
send_btn.pack(pady=15)


flag = 0
root['bg'] = '#ffffff'
root.title("Поиск документов")

# обработка комбинаций клавишь
def _onKeyRelease(event):
    ctrl = (event.state & 0x4) != 0
    if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")

    if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")

    if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

root.bind_all("<Key>", _onKeyRelease, "+")
root.geometry('900x500')
root.geometry(center_window(900, 500, root))


main_container = Frame(root)
main_container.config(bg="#fbfbfb")
main_container.pack(fill="both", expand=True)


tab_control = Notebook(main_container)
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Поле ввода")


left_frame1 = ttk.Frame(tab1, bootstyle="light")
left_frame1.pack(side=LEFT, fill=BOTH, expand=True)

right_frame1 = ttk.Frame(tab1, bootstyle="light")
right_frame1.pack(side=LEFT, fill=BOTH, expand=True)


find_label = ttk.Label(
    left_frame1, text='Введите искомое слово или предложение:', 
    font=('Arial Bold', 12), 
    bootstyle="inverse-light"
)
find_label.pack(side=TOP, anchor=W, padx=10, pady=2)

find_entry = scrolledtext.ScrolledText(left_frame1, width=50, height=10, wrap=ttk.WORD)
find_entry.pack(side=TOP, fill=BOTH, anchor=W, padx=10, pady=5)


# Создание булевого переключателя
search_mode = ttk.IntVar()
# checkbutton = ttk.Checkbutton(
#     left_frame1, text="Искать во вложенных директориях", 
#     variable=search_mode, onvalue=1, offvalue=0,
#     bootstyle="success-square-toggle",
# )
# checkbutton.pack(side=TOP, anchor=NW, padx=10, pady=10)


change_button = ttk.Button(
    left_frame1, 
    text="Поиск по документам", cursor='hand2', 
    command=lambda: findDocs(find_entry, txt1, left_frame1, search_mode),
    bootstyle=SUCCESS
)
change_button.pack(side=TOP, anchor=NW, padx=10, pady=10)

delete_button = ttk.Button(
    left_frame1, 
    text='Очистить поля', 
    cursor='hand2', 
    command=lambda: clear_text(find_entry, txt1),
    bootstyle=DANGER
)
delete_button.pack(side=TOP, anchor=NW, padx=10, pady=10)



open_label = ttk.Label(
    right_frame1, text='Нажмите на название файла, чтобы открыть его', 
    font=('Arial Bold', 11), 
    bootstyle="inverse-light"
)
open_label.pack(side=TOP, anchor=W, padx=10, pady=2)
txt1 = scrolledtext.ScrolledText(right_frame1, wrap="word", width=50, height=30, cursor='hand2', state='disabled')
txt1.pack(side=TOP, fill=BOTH, expand=True)
txt1.configure(font=("times new roman", 13))


txt1.bind(
    "<Button-1>", 
    lambda event, txt1=txt1, root=root, find_entry=find_entry: handle_left_click(event, txt1, root, find_entry)
)

tab_control.pack(expand=True, fill="both")
top.protocol('WM_DELETE_WINDOW', lambda: close_window(root))
root.withdraw()
root.mainloop()
