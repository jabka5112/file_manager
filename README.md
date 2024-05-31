# ИНДИВИДУАЛЬНЫЙ ПРОЕКТ ОПРЕЕВА СОФИЯ 23СА1-1

# Описание:

Современный файловый менеджер - это приложение на Python с использованием библиотеки Tkinter для создания графического интерфейса. Приложение предоставляет удобный интерфейс для управления файлами и папками на компьютере. Оно позволяет просматривать содержимое файлов и папок, создавать новые файлы и папки, переименовывать и удалять файлы и папки, а также просматривать изображения.

# Особенности:

Интуитивно понятный пользовательский интерфейс.
Просмотр содержимого файлов и папок.
Создание новых файлов и папок.
Переименование и удаление файлов и папок.
Просмотр изображений.
Инструкции по установке:

При запуске приложения отображается текущий каталог и список файлов и папок в нем.
Для навигации по файловой системе используйте кнопку "Назад" или двойной щелчок мыши на папке.
Для создания новой папки или файла выберите соответствующий пункт в меню "Файл".
Для просмотра содержимого файла или изображения выберите его в списке и нажмите соответствующую кнопку.
Для переименования или удаления файла или папки выберите его в списке и выберите соответствующий пункт в меню "Файл".

# Инициализация и запуск проекта

1. В терминале пишем команду для скачивания всех зависимостей нашего проекта - `pip install -r requirements.txt`

2. Если нужно запустить проект не через .exe, тогда вводим в терминал команду - `python main.py`

# Создание .exe файла

2. Вводим команду, которая позволяет сделать нам .exe нашего приложения - `pyinstaller --onefile main.py`.
   После этого у тебя появятся файл "main.spec" и папки "build", "dist".

   - Папка build: В этой папке хранятся временные файлы, созданные в процессе сборки приложения. Это включает в себя файлы, созданные PyInstaller для временного использования во время процесса сборки.

   - Папка dist: Эта папка содержит окончательные файлы, включая исполняемый файл (exe) вашего приложения, а также все необходимые ресурсы, такие как изображения, шрифты и т. д., которые были включены в сборку.

   - Файл main.spec: Это файл спецификаций PyInstaller, который вы можете создать для настройки процесса сборки вашего приложения. В этом файле вы можете указать дополнительные параметры, такие как включение ресурсов, определение путей поиска модулей и т. д. Он может быть использован.
