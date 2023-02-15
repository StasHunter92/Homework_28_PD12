# Курс 6. Домашняя работа SkyPRO PD 12
______________________________________
### Урок 28. Postgres, Модели с relations и QuerySet
______________________________________

**Критерии выполнения:**

:white_check_mark: В проекте подключен PostgreSQL

:white_check_mark: В моделях есть все поля из CSV

:white_check_mark: В моделях используются ForeignKey и ManyToManyField

:white_check_mark: Во всех моделях определен `class Meta` и переопределен метод `__str__`

:white_check_mark: Картинки, прикрепленные к объявлениям, корректно открываются

:white_check_mark: Использованы ListView, DetailView, CreateView, UpdateView, DeleteView

:white_check_mark: Типы данных в JSON отдаются корректно

:white_check_mark: Методы из спецификации работают

:white_check_mark: Используются атрибут `ordering` и метод `order_by`

:white_check_mark: В списках пользователей и объявлений есть пагинация

:white_check_mark: Локации могут формироваться прямо в методах создания и редактирования пользователей

:white_check_mark: Используется хотя бы один из методов `aggregate` / `annotate`

:white_check_mark: Используется метод `select_relation`

:white_check_mark: Используются методы `get_or_create`, `get_object_or_404`

:white_check_mark: URL разнесены по разным директориям

______________________________________
**Примечания:**

:negative_squared_cross_mark: Заполнение базы через `Homework_28_PD12/import_csv.py` происходит не полностью, адреса
заполнялись вручную