import json
import unittest
from unittest.mock import patch, mock_open, Mock

from models import (StatusBook, BookAllGet,
                    BookAdd, BookPut)


class TestBookLibrary(unittest.TestCase):
    """
        Класс для тестирования вывода библиотеки
        """
    @patch(
        'builtins.open',
        new_callable=mock_open,
        read_data=json.dumps({
            "1": {
                'title': 'Book One',
                'author': 'Author A',
                'published': '2020',
                'status': StatusBook.IN_STOCK},
            "2": {
                'title': 'Book Two',
                'author': 'Author B',
                'published': '2021',
                'status': StatusBook.GAVE},
        }))
    def test_read_file(self, mock_file):
        """Функция для тестирования корректного вывода"""
        book_all = BookAllGet()
        self.assertEqual(len(book_all._data), 2)
        self.assertEqual(book_all._data['1']['title'], 'Book One')
        self.assertEqual(book_all._data['2']['title'], 'Book Two')


class TestBookAdd(unittest.TestCase):
    """
    Класс для тестирования добавления новой книги
    """
    def setUp(self):
        self.book = BookAdd(
            title='Преступление и наказание',
            author='Федор Достоевский',
            published='1866'
        )
        self.book._data = {}

    @patch('builtins.open', new_callable=mock_open)
    def test_append_success(self, mock_logger):
        """Тест для добавления книги"""
        self.book._check_title = Mock(return_value=True)
        self.book._check_book = Mock(return_value=False)

        self.book.append()

        self.assertEqual(len(self.book._data), 1)
        self.assertIn(1, self.book._data)
        self.assertEqual(
            self.book._data[1]['title'],
            'Преступление и наказание')

    @patch('builtins.open', new_callable=mock_open)
    def test_append_title_check_failed(self, mock_logger):
        """Тест функция для проверки поля title"""
        with self.assertRaises(ValueError) as context:
            self.book._check_title = Mock(return_value=False)
            self.book.append()
        self.assertEqual(
            *context.exception.args,
            'Ошибка добавления')

    @patch('builtins.open', new_callable=mock_open)
    def test_append_book_check_failed(self, mock_logger):
        """Тест, когда книга не добавлена в библиотеку"""
        self.book._data = {
            1: {
                'title': "Преступление и наказание",
                'author': "Федор Достоевский",
                'published': '1866'
            }
        }
        with self.assertRaises(AssertionError) as context:
            self.book.append()
        self.assertEqual(
            *context.exception.args,
            'Данная книга есть в нашей библиотеке')


class TestBookPut(unittest.TestCase):
    """
    Класс для тестирования
    изменения статуса книги
    """

    def setUp(self):
        self.book = BookPut()
        self.book._data = {
            '1': {'status': StatusBook.IN_STOCK},
            '2': {'status': StatusBook.IN_STOCK},
        }

    @patch('builtins.open', new_callable=mock_open)
    def test_update_status_success(self, mock_logger):
        """
        Тест функция для проверки корректного обновления
        """
        self.book.path(1, StatusBook.GAVE)

        self.assertEqual(
            self.book._data['1']['status'],
            StatusBook.GAVE)

    @patch('builtins.open', new_callable=mock_open)
    def test_update_status_key_error(self, mock_get_logger):
        """
        Тест функция для проверки при неудачном обновление
        """
        with self.assertRaises(KeyError) as context:
            self.book.path(4, StatusBook.GAVE)
        self.assertEqual(
            *context.exception.args,
            'Книга с id: 4 не найдена')


if __name__ == '__main__':
    unittest.main()
