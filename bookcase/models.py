import os
import json
from typing import Dict

from bookcase.book_logger import logger
from bookcase.storage import JsonBookStorage


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
    def __init__(self,storage=None):
        self._storage = storage or JsonBookStorage()
        self._data: Dict[str, dict] = self._storage.load_data()
    
    def _save(self):
        self._storage.save_data(self._data)


class Book(BookBase):
    """
    Класс для инициализации полей,
    нужных для дальнейшей работы и с некоторым
    общим функционалом для классов наследников
    """
    def __init__(self, title: str = None, author: str = None, published: str = None, storage=None) -> None:
        super().__init__(storage)
        self.title = title
        self.author = author
        self.published = published
        self.status = StatusBook.IN_STOCK

    def _check_title(self) -> bool:
        return bool(self.title and len(self.title.strip())) > 0

    @staticmethod
    def _check_items(book_item: str, data_items: tuple[str]) -> bool:
        book_item = book_item.lower()
        return any(book_item in item.lower() for item in data_items)

    def _check_book(self) -> bool:
        """
        Функция для проверки наличия книги в
        библиотеке через поле title
        """
        return any(book.get('title') == self.title for book in self._data.values())


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
        if self._check_book():
            logger.info('Данная книга есть в нашей библиотеке')
            raise AssertionError('Данная книга есть в нашей библиотеке')
        book_id: str = str(len(self._data) + 1 if self._data else 1)
        self._data[book_id] = {
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
        if book_id not in self._data:
            logger.error(f'Книга с id: {book_id} не найдена')
            raise KeyError(f'Книга с id: {book_id} не найдена')

        self._data[book_id]['status'] = status
        self._save()
        logger.info('Данные книги с id {book_id} обновлены')
        return f'Данные книги с id {book_id} обновлены'


class BookSearch(Book):
    """
    Класс для поиска книг через заголовок,
    автора или год издания
    """
    def book_search(self, item_book: str):
        found = [
            book for book in self._data.values()
            if self._check_items(item_book, book.values())
        ]
        for book in found:
            print(book)
        if found:
            return f'Кол-во книг: {len(found)}'
        logger.info('-Пусто-')
        return '-Пусто-'


class BookDelete(Book):
    """
    Класс для удаления конкретной книги из библиотеки
    """
    def book_delete(self, book_id: int = None):
        book_id = str(book_id)
        if book_id not in self._data:
            logger.error(f'Книга с id: {book_id} не найдена')
            raise KeyError(f'Книга с id: {book_id} не найдена')

        del self._data[book_id]
        self._save()
        logger.info(f'Книга с id = {book_id} удалена из библиотеки')
        return 'Книга удалена из библиотеки'
