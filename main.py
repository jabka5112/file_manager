import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog, scrolledtext
from PIL import Image, ImageTk

class FileManagerApp:
    def __init__(self, root):
        """
        Инициализация приложения файлового менеджера.

        :param root: Tkinter корневое окно.
        """
        self.root = root
        self.root.title("Современный файловый менеджер")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c2c2c")  # Цвет фона

        self.current_directory = tk.StringVar()
        self.current_directory.set(os.getcwd())

        self.create_widgets()
        self.load_file_list()

    def create_widgets(self):
        """
        Создание виджетов пользовательского интерфейса.
        """
        style = ttk.Style()
        style.theme_use("clam")  # Используем тему clam для более современного вида

        # Фрейм для отображения текущего каталога и файлов
        self.directory_frame = ttk.Frame(self.root, padding=(10, 10))
        self.directory_frame.pack(fill=tk.BOTH, expand=True)

        # Поле для отображения текущего каталога
        self.current_directory_label = ttk.Label(self.directory_frame, textvariable=self.current_directory, foreground="white", background="#2c2c2c", font=("Arial", 10, "bold"))
        self.current_directory_label.pack(side=tk.TOP, fill=tk.X)

        # Список файлов и папок в текущем каталоге
        self.file_treeview = ttk.Treeview(self.directory_frame, columns=("type", "size"), selectmode="extended", show="tree")
        self.file_treeview.heading("#0", text="Имя файла", anchor="w")
        self.file_treeview.heading("type", text="Тип", anchor="w")
        self.file_treeview.heading("size", text="Размер", anchor="w")
        self.file_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Скроллбар для списка файлов
        self.scrollbar = ttk.Scrollbar(self.directory_frame, orient=tk.VERTICAL, command=self.file_treeview.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_treeview.config(yscrollcommand=self.scrollbar.set)

        # Кнопка "Назад"
        self.back_button = ttk.Button(self.directory_frame, text="Назад", command=self.go_back)
        self.back_button.pack(side=tk.TOP, fill=tk.X)

        # Кнопка "Просмотреть"
        self.view_button = ttk.Button(self.directory_frame, text="Просмотреть изображение", command=self.view_file)
        self.view_button.pack(side=tk.TOP, fill=tk.X)

        # Кнопка "Просмотр содержимого"
        self.view_content_button = ttk.Button(self.directory_frame, text="Просмотр содержимого", command=self.view_file_content)
        self.view_content_button.pack(side=tk.TOP, fill=tk.X)

        # Кнопки выбора диска
        self.drive_buttons_frame = ttk.Frame(self.root)
        self.drive_buttons_frame.pack(side=tk.TOP, fill=tk.X)
        for drive in self.get_available_drives():
            button = ttk.Button(self.drive_buttons_frame, text=drive, command=lambda d=drive: self.on_drive_selected(d))
            button.pack(side=tk.LEFT, padx=5)

        # Добавим меню
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Создать папку", command=self.create_folder)
        file_menu.add_command(label="Создать файл", command=self.create_file)
        file_menu.add_command(label="Переименовать", command=self.rename_file_or_folder)
        file_menu.add_command(label="Удалить", command=self.delete_file_or_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        # Обновление списка файлов при выборе нового каталога
        self.file_treeview.bind("<Double-1>", self.on_file_double_click)

        # Темная тема
        style.configure("Treeview", background="#383838", foreground="white")
        style.configure("Treeview.Heading", background="#383838", foreground="white")
        style.map("Treeview", background=[("selected", "#005f87")])

    def load_file_list(self):
        """
        Загрузка списка файлов и папок в текущем каталоге.
        """
        self.file_treeview.delete(*self.file_treeview.get_children())
        current_dir = self.current_directory.get()
        try:
            for item in os.listdir(current_dir):
                path = os.path.join(current_dir, item)
                type_ = "Папка" if os.path.isdir(path) else "Файл"
                size = self.get_file_size(path)
                self.file_treeview.insert("", "end", text=item, values=(type_, size))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить список файлов: {str(e)}")

    def on_file_double_click(self, event):
        """
        Обработчик двойного щелчка на файле или папке.
        """
        selection = self.file_treeview.selection()
        if selection:
            item = self.file_treeview.item(selection[0])
            filename = item["text"]
            path = os.path.join(self.current_directory.get(), filename)
            if os.path.isdir(path):
                self.current_directory.set(path)
                self.load_file_list()
            else:
                self.view_file()

    def create_folder(self):
        """
        Создание новой папки.
        """
        new_folder = filedialog.askdirectory(initialdir=self.current_directory.get(), title="Выберите место для создания папки")
        if new_folder:
            folder_name = simpledialog.askstring("Новая папка", "Введите имя новой папки:")
            if folder_name:
                folder_path = os.path.join(new_folder, folder_name)
                try:
                    os.mkdir(folder_path)
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось создать папку: {str(e)}")
                else:
                    self.load_file_list()

    def create_file(self):
        """
        Создание нового файла.
        """
        new_file = filedialog.asksaveasfilename(initialdir=self.current_directory.get(), title="Выберите место для создания файла", defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")])
        if new_file:
            try:
                with open(new_file, "w"):
                    pass
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось создать файл: {str(e)}")
            else:
                self.load_file_list()

    def delete_file_or_folder(self):
        """
        Удаление выбранных файлов или папок.
        """
        selection = self.file_treeview.selection()
        if selection:
            confirmed = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранные файлы или папки?")
            if confirmed:
                for item in selection:
                    filename = self.file_treeview.item(item)["text"]
                    path = os.path.join(self.current_directory.get(), filename)
                    try:
                        if os.path.isdir(path):
                            shutil.rmtree(path)
                        else:
                            os.remove(path)
                    except Exception as e:
                        messagebox.showerror("Ошибка", f"Не удалось удалить {filename}: {str(e)}")
                self.load_file_list()

    def rename_file_or_folder(self):
        """
        Переименование выбранного файла или папки.
        """
        selection = self.file_treeview.selection()
        if selection:
            item = self.file_treeview.item(selection[0])
            filename = item["text"]
            path = os.path.join(self.current_directory.get(), filename)
            new_name = simpledialog.askstring("Переименование", f"Введите новое имя для {filename}:")
            if new_name:
                new_path = os.path.join(self.current_directory.get(), new_name)
                try:
                    os.rename(path, new_path)
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось переименовать: {str(e)}")
                else:
                    self.load_file_list()

    def view_file(self):
        """
        Просмотр выбранного файла (предполагается, что это изображение).
        """
        selection = self.file_treeview.selection()
        if selection:
            item = self.file_treeview.item(selection[0])
            filename = item["text"]
            path = os.path.join(self.current_directory.get(), filename)
            if os.path.isfile(path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    try:
                        image = Image.open(path)
                        image.show()
                    except Exception as e:
                        messagebox.showerror("Ошибка", f"Не удалось открыть изображение: {str(e)}")
                else:
                    messagebox.showinfo("Просмотр файла", f"Файл {filename} не является изображением.")

    def view_file_content(self):
        """
        Просмотр содержимого выбранного файла (предполагается, что это текстовый файл).
        """
        selection = self.file_treeview.selection()
        if selection:
            item = self.file_treeview.item(selection[0])
            filename = item["text"]
            path = os.path.join(self.current_directory.get(), filename)
            if os.path.isfile(path):
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        content = file.read()
                        self.show_text_view(content, filename)
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось открыть файл: {str(e)}")
            else:
                messagebox.showinfo("Просмотр файла", f"Файл {filename} не существует или является директорией.")

    def show_text_view(self, content, filename):
        """
        Показывает окно для просмотра содержимого текстового файла.

        :param content: Содержимое текстового файла.
        :param filename: Имя файла.
        """
        view_window = tk.Toplevel(self.root)
        view_window.title(f"Просмотр содержимого файла: {filename}")
        view_window.geometry("600x400")

        text_widget = scrolledtext.ScrolledText(view_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, content)
        text_widget.configure(state="disabled")

    def go_back(self):
        """
        Переход на уровень вверх в файловой системе.
        """
        current_dir = self.current_directory.get()
        parent_dir = os.path.dirname(current_dir)
        if parent_dir:
            self.current_directory.set(parent_dir)
            self.load_file_list()

    def get_file_size(self, path):
        """
        Получение размера файла или папки.

        :param path: Путь к файлу или папке.
        :return: Размер файла или папки.
        """
        if os.path.isdir(path):
            return "<Папка>"
        size = os.path.getsize(path)
        for unit in ["байт", "Кб", "Мб", "Гб"]:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0

    def get_available_drives(self):
        """
        Получение списка доступных дисков.

        :return: Список доступных дисков.
        """
        drives = []
        for drive in range(ord("A"), ord("Z") + 1):
            drive_name = chr(drive) + ":\\"
            if os.path.exists(drive_name):
                drives.append(drive_name)
        return drives

    def on_drive_selected(self, drive):
        """
        Обработчик выбора диска.

        :param drive: Выбранный диск.
        """
        self.current_directory.set(drive)
        self.load_file_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()
