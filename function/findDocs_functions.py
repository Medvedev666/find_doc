import docx
import os
import tkinter as tk
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import tkinter.messagebox as mb

from tkinter import filedialog as fd

from PyPDF2 import PdfReader
import pyexcel_xls
import pyexcel

import threading
import chardet

from .config import logger


def callback():
    return fd.askdirectory()


def find_all(chose_dir):

    paths = []
    paths_pdf = []
    paths_xls = [] 

    for root, dirs, files in chose_dir:

        for file in files:
            if file.endswith(('docx')) and not file.startswith('~'):
                paths.append(os.path.join(root, file))
            if file.endswith('pdf') and not file.startswith('~'):
                paths_pdf.append(os.path.join(root, file))
            if file.endswith(('xls', 'xlsx')) and not file.startswith('~'):
                paths_xls.append(os.path.join(root, file))
    
    return paths, paths_pdf, paths_xls



# def find_only_dir(chosen_dir):
    
#     paths = []
#     paths_pdf = []
#     paths_xls = []

#     # Обходим все файлы в выбранной директории, но не во вложенных папках
#     for root, dirs, files in chosen_dir:

#         for file in files:
#             if file.endswith('docx') and not file.startswith('~'):
#                 paths.append(os.path.join(root, file))
#             if file.endswith('pdf') and not file.startswith('~'):
#                 paths_pdf.append(os.path.join(root, file))
#             if file.endswith(('xls', 'xlsx')) and not file.startswith('~'):
#                 paths_xls.append(os.path.join(root, file))
#         break
    
#     return paths, paths_pdf, paths_xls



def findDocs_process(chose_dir, find, txt1, search_mode):

    flag_xls = 0
    flag = 0
    not_found = 1
    
    # if search_mode.get():
    logger.info(f'Find_all_function_without_xlsx')
    paths, paths_pdf, paths_xls = find_all(chose_dir)
    # else:
    #     logger.info(f'Find_one_function')
    #     paths, paths_pdf, paths_xls = find_only_dir(chose_dir)

    logger.info(f'{paths=}\n\n{paths_pdf=}\n\n{paths_xls=}')
    # поиск по docx
    for path in paths:
        logger.info('Check .docx')
        try:
            doc = docx.Document(path)
            for paragraph in doc.paragraphs:

                try:
                    # Преобразование текста для проверки корректности кодировки
                    logger.info(f'Begin')
                    result = chardet.detect(paragraph.text.encode('utf-8'))
                    logger.info(f'{result=}')
                    logger.info(f'{paragraph.text.encode('utf-8').decode('utf-8')=}')
                    # print(f'{cell.text.encode('utf-8').decode('utf-8')=}')
                except UnicodeDecodeError:
                    logger.error(f"File '{path}' contains non-UTF-8 characters.")
                    logger.error(f'{paragraph.text[:100]=}')

                if find in paragraph.text.lower():

                    not_found = 0
                    flag = 1
                    path, filename = os.path.split(path)
                    update_result_text(filename, path, txt1)
                    break

            if flag == 0:  # если не нашли в параграфах, ищем в таблицах
                for table in doc.tables:
                    for row in table.rows:
                        for cell in row.cells:

                            try:
                                result = chardet.detect(cell.text.encode('utf-8'))
                                logger.info(f'{result=}')
                                # Преобразование текста для проверки корректности кодировки
                                logger.info(f'{cell.text.encode('utf-8').decode('utf-8')=}')
                                # print(f'{cell.text.encode('utf-8').decode('utf-8')=}')
                            except UnicodeDecodeError:
                                logger.error(f"File '{path}' contains non-UTF-8 characters.")
                                logger.error(f'{cell.text[:100]=}')

                            if find in cell.text.lower():
                                not_found = 0
                                path, filename = os.path.split(path)
                                update_result_text(filename, path, txt1)
                                break
                        if not_found == 0:
                            break
                    if not_found == 0:
                        break
        except Exception as e:
            logger.error(f'Error docx: {e}')

    # поиск по pdf
    for path in paths_pdf:
        logger.info('Check .pdf')
        try:
            reader = PdfReader(path)
            for page in reader.pages:
                clear_page = page.extract_text().replace('\n', '')

                try:
                    result = chardet.detect(clear_page.encode('utf-8'))
                    logger.info(f'{result=}')
                    # Преобразование текста для проверки корректности кодировки
                    logger.info(f'{clear_page.encode('utf-8').decode('utf-8')=}')
                    # print(f'{clear_page.encode('utf-8').decode('utf-8')=}')
                except UnicodeDecodeError:
                    logger.error(f"File '{path}' contains non-UTF-8 characters.")
                    logger.error(f'{clear_page[:100]=}')

                if find in clear_page.lower():
                    not_found = 0
                    path, filename = os.path.split(path)
                    update_result_text(filename, path, txt1)
                    break
        except Exception as e:
            logger.error(f'Error pdf: {e}')

    # поиск по xls
    # for path in paths_xls:
    #     logger.info('Check .xls and .xlsx')
    #     try:
    #         excel_file = pyexcel.get_array(file_name=path)
    #         for elem in excel_file:
    #             for cell in elem:

    #                 try:
    #                     result = chardet.detect(str(cell).encode('utf-8'))
    #                     logger.info(f'{result=}')
    #                     # Преобразование текста для проверки корректности кодировки
    #                     logger.info(f'{str(cell).encode('utf-8').decode('utf-8')=}')
    #                     # print(f'{str(cell).encode('utf-8').decode('utf-8')=}')
    #                 except UnicodeDecodeError:
    #                     logger.error(f"File '{path}' contains non-UTF-8 characters.")
    #                     logger.error(f'{str(cell)[:100]=}')

    #                 if find in str(cell).lower():
    #                     not_found = 0
    #                     path, filename = os.path.split(path)
    #                     update_result_text(filename, path, txt1)
    #                     flag_xls = 1
    #                     break
    #             if flag_xls == 1:
    #                 break
    #     except Exception as e:
    #         logger.error(f'Error xls: {e}')

    if not_found == 1:
        mb.showwarning('Ошибка!', 'Не найдено документов, содержащих данное слово/предложение!')
    
    progress_bar.stop()
    progress_bar.pack_forget()

def update_result_text(filename, path, txt1):
    txt1.config(state="normal")
    txt1.insert(tk.END, '\n' + filename + '\n' + path + '\n')
    txt1.config(state="disabled")

def start_search(chose_dir, find, txt1, left_frame1, search_mode):

    global progress_bar
    progress_bar = ttk.Progressbar(left_frame1, bootstyle="success-striped")
    progress_bar.pack(side=TOP, fill=BOTH, padx=10, pady=10)
    progress_bar.start()

    thread = threading.Thread(target=lambda: findDocs_process(chose_dir, find, txt1, search_mode))
    thread.start()

def findDocs(find_entry, txt1, left_frame1, search_mode):

    find = find_entry.get("1.0", tk.END).strip().lower()
    
    if find != '':
        logger.info(f'Start funding: {find=}')
        chose_dir = os.walk(callback())
        start_search(chose_dir, find, txt1, left_frame1, search_mode)
    else:
        mb.showwarning('Ошибка!', 'Вы ввели пустое значение!')