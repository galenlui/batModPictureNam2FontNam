'''
批量修改图片名为字体名
(C)2023 Galen Studio(R)
QQ: 284121506
VX: galenlui
Caution: 免费开源给大伙使用，请务贩卖。
version: 1.1
'''

import os
import shutil
from tkinter import *
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import tkinter.messagebox as messagebox

class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_label_frame_selectPathTips = self.__tk_label_frame_selectPathTips(self)
        self.tk_input_selectPath = self.__tk_input_selectPath(self.tk_label_frame_selectPathTips)
        self.tk_button_start = self.__tk_button_start(self.tk_label_frame_selectPathTips)
        self.tk_button_browse = self.__tk_button_browse(self.tk_label_frame_selectPathTips)
        self.tk_label_functionalDescription = self.__tk_label_functionalDescription(self)

    def __win(self):
        self.title("批量修改图片名为字体名")
        width = 600
        height = 200
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)

    def __tk_label_frame_selectPathTips(self, parent):
        frame = LabelFrame(parent, text="请选择要输入的路径", )
        frame.place(x=20, y=83, width=560, height=101)
        return frame

    def __tk_input_selectPath(self, parent):
        self.path_var = StringVar()
        ipt = Entry(parent, textvariable=self.path_var)
        ipt.place(x=10, y=21, width=368, height=30)
        return ipt

    def __tk_button_start(self, parent):
        btn = Button(parent, text="开始", takefocus=False, command=self.start_processing)
        btn.place(x=455, y=21, width=90, height=30)
        return btn

    def __tk_button_browse(self, parent):
        btn = Button(parent, text="浏览", takefocus=False, command=self.browse_path)
        btn.place(x=388, y=21, width=50, height=30)
        return btn

    def __tk_label_functionalDescription(self, parent):
        label = Label(parent, text="程序说明：本程序可以遍历用户提供路径下所有子目录的字体文件，并提取名字；"
                                   "\n         如果目录下有图片文件就把该目录下的图片名字改成字体的名字。"
                                   "\n         （请谨慎使用本程序，文件名是直接修改的，不好撤销，请确定需要本操作）",
                      anchor="center", )
        label.place(x=20, y=15, width=560, height=50)
        return label

class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.stop_flag = False
        self.executor = None
        self.total_files = 0
        self.processed_files = 0
        self.thread = None
        self.__event_bind()

    def __event_bind(self):
        self.tk_button_start["state"] = "normal"
        self.tk_button_browse["state"] = "normal"

    def start_processing(self):
        self.stop_flag = False
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.thread = Thread(target=self.process_files)
        self.thread.start()

    def browse_path(self):
        path = filedialog.askdirectory()
        self.path_var.set(path)

    def process_files(self):
        path = self.path_var.get()
        if not path:
            return

        font_extensions = (".ttf", ".ttc", ".otf", ".eot", ".fon", ".pfa", ".pfb", ".woff", ".woff2")
        image_extensions = (".png", ".gif", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp", ".svg", ".wmf",
                            ".ico", ".hdr", ".psd")
        font_name = None

        try:
            for root, _, file_list in os.walk(path):
                if self.stop_flag:
                    break

                self.total_files += len(file_list)

                for file_name in file_list:
                    file_path = os.path.join(root, file_name)
                    if file_name.lower().endswith(font_extensions):
                        font_name = os.path.splitext(file_name)[0]
                        self.rename_images(root, font_name, image_extensions)
                        break  # 在找到第一个字体文件后停止搜索其他子目录的字体文件

            if not self.stop_flag:
                self.show_completion_message()

        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {e}")

        self.__event_bind()

    def rename_images(self, directory, new_name, image_extensions):
        image_files = [f for f in os.listdir(directory) if f.lower().endswith(image_extensions)]
        image_files.sort()

        for index, file_name in enumerate(image_files, start=1):
            if self.stop_flag:
                break

            file_path = os.path.join(directory, file_name)
            _, extension = os.path.splitext(file_name)

            if len(image_files) > 1:
                new_file_name = f"{new_name}_{index}{extension}"
            else:
                new_file_name = f"{new_name}{extension}"

            new_file_path = os.path.join(directory, new_file_name)
            shutil.move(file_path, new_file_path)

    def show_completion_message(self):
        messagebox.showinfo("运行完毕", "程序已成功运行完毕！")

    def on_closing(self):
        self.destroy()

if __name__ == "__main__":
    win = Win()
    win.protocol("WM_DELETE_WINDOW", win.on_closing)
    win.mainloop()