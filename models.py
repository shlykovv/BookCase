import os
import json
from book_logger import logger


class StatusBook:
    """
    Класс создан для дальнейшего использования,
    чтоб можно было не вводить значения статуса,
    а выбирать через выпадающий список
    """
    IN_STOCK: str = 'В наличие'
    GAVE: str = 'Выдана'


class BookBase:
    """
    Базовый класс для работы с библиотекой книг
    """
    _data: dict[int, dict[str]] = None
    _filename: str = 'archive_books.json'

    @classmethod
    def _read_file(cls):
        with open(cls._filename, 'r', encoding='utf-8') as file:
            if os.stat(cls._filename).st_size != 0:
                cls._data = json.loads(file.read())
            else:
                cls._data = {}
        return cls._data

    def __new__(cls, *args, **kwargs):
        if cls._data is None:
            cls._data = cls._read_file()
        return super().__new__(cls)


class Book(BookBase):
    """
    Класс для инициализации полей,
    нужных для дальнейшей работы и с некоторым
    общим функционалом для классов наследников
    """
    def __init__(
            self,
            title: str = None,
            author: str = None,
            published: str = None
    ) -> None:
        self.title = title
        self.author = author
        self.published = published
        self.status = StatusBook.IN_STOCK

    def _check_title(self) -> bool:
        if len(self.title) < 1:
            return False
        return True

    @staticmethod
    def _check_items(
            book_item: str,
            data_items: tuple[str]
    ) -> bool:
        for check in data_items:
            if book_item in check.lower():
                return True
        return False

    def _check_book(self) -> bool:
        """
        Функция для проверки наличия книги в
        библиотеке через поле title
        """
        if self.title is None:
            return True
        for item in self._data:
            if self.title == self._data[item]['title']:
                return True
        return False

    def _save(self):
        try:
            with open(self._filename, 'w', encoding='utf-8') as file:
                file.write(json.dumps(
                    self._data, indent=4, ensure_ascii=False))
        except json.JSONDecodeError:
            logger.error('Ошибка добавления книги в библиотеку')
            raise ValueError('Ошибка добавления книги в библиотеку')


class BookAllGet(Book):
    """
    Вывод всех книги из библиотеки через метод __call__
    """
    def __call__(self, *args, **kwargs):
        return self._data if self._data else 'Список книг пуст'


class BookAdd(Book):
    """
    Класс для добавления книг в библиотеку
    """
    def append(self) -> str:
        """Функция для добавления книги в библиотеку через """
        if not self._check_title():
            logger.error('Ошибка добавления')
            raise ValueError('Ошибка добавления')
        else:
            book_id: int = len(self._data) + 1 if self._data else 1
            if self._check_book():
                logger.info(
                    'Данная книга есть в нашей библиотеке')
                raise AssertionError(
                    'Данная книга есть в нашей библиотеке')
            else:
                self._data[book_id]: dict = {
                    'title': self.title,
                    'author': self.author,
                    'published': self.published,
                    'status': self.status
                }
                self._save()
                logger.info(f'Книга: {self.title} добавлена в библиотеку')
                return f'Книга: {self.title} добавлена в библиотеку'


class BookPut(Book):
    def path(self, book_id: int, status: str):
        book_id = str(book_id)
        try:
            self._data[book_id]['status'] = status
            self._save()
        except KeyError:
            logger.error(f'Книга с id: {book_id} не найдена')
            raise KeyError(f'Книга с id: {book_id} не найдена')
        else:
            logger.info('Данные книги с id {book_id} обновлены')
            return f'Данные книги с id {book_id} обновлены'


class BookSearch(Book):
    """
    Класс для поиска книг через заголовок,
    автора или год издания
    """
    def book_search(self, item_book: str):
        length = 0
        for book_id in self._data:
            data_items = self._data[book_id].values()
            if self._check_items(item_book, data_items):
                print(self._data[book_id])
                length += 1
        if length > 0:
            return f'Количество книг: {length}'
        else:
            logger.info('-Пусто-')
            return '-Пусто-'


class BookDelete(Book):
    """
    Класс для удаления конкретной книги из библиотеки
    """
    def book_delete(self, book_id: int = None):
        try:
            book_id = str(book_id)
            del self._data[book_id]
            self._save()
        except KeyError:
            logger.error(f'Книга с id: {book_id} не найдена')
            raise KeyError(
                f'Книга с id: {book_id} не найдена')
        else:
            logger.info('Книга удалена из библиотеки')
            return 'Книга удалена из библиотеки'
