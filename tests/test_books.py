import os
import json
import pytest
from bookcase.models import BookAdd, BookDelete, BookSearch, BookAllGet
from bookcase.storage import JsonBookStorage


TEST_FILE = 'test_books.json'


@pytest.fixture()
def temp_storage(tmp_path):
    test_file = tmp_path / 'test_books.json'
    return JsonBookStorage(filename=str(test_file))
    


def test_add_book_success(temp_storage):
    book = BookAdd(title='1984', author='George Orwell', published='1949', storage=temp_storage)
    result = book.append()
    assert "Книга: 1984 добавлена в библиотеку" in result
    
    # Проверка, что книга сохранена
    all_books = BookAllGet(storage=temp_storage)
    data = all_books()
    assert any(b['title'] == '1984' for b in data.values())


def test_add_book_duplicate(temp_storage):
    book1 = BookAdd(title='1984', author='George Orwell', published='1949', storage=temp_storage)
    book1.append()
    
    book2 = BookAdd(title='1984', author='George Orwell', published='1949', storage=temp_storage)
    
    with pytest.raises(AssertionError, match='Данная книга есть в нашей библиотеке'):
        book2.append()


def test_get_all_book(temp_storage):
    book = BookAdd(title='The Hobbit', author='J.R.R Tolkien', published='1937', storage=temp_storage)
    book.append()
    
    getter = BookAllGet(storage=temp_storage)
    result = getter()
    assert isinstance(result, dict)
    assert len(result) == 1
    assert next(iter(result.values()))['title'] == 'The Hobbit'


def test_delete_book(temp_storage):
    book = BookAdd(title="To Delete", author="Author", published="2000", storage=temp_storage)
    book.append()
    
    deleter = BookDelete(storage=temp_storage)
    result = deleter.book_delete(1)
    assert result == 'Книга удалена из библиотеки'
    
    getter = BookAllGet(storage=temp_storage)
    
    data = getter()
    assert data == {} or "1" not in data
