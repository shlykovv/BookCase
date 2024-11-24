from models import (BookAllGet, BookAdd,
                    BookPut, BookSearch,
                    BookDelete)

def get_books():
    """
    Функция для взаимодействия с классом
    BookAllGet, для вывода всех книг из файла json
    """
    books = BookAllGet()
    return books()


def add_book():
    """
    Функция для взаимодействия с классом
    BookAdd, для добавления новой книги
    """
    title = input('Название: ')
    author = input('Автор: ')
    published = input('год выпуска: ')
    book = BookAdd(
        title=title,
        author=author,
        published=published
    )
    add = book.append()
    return add


def search_book(book_item: str):
    """
    Функция для взаимодействия с классом
    BookSearch, для поиска книги в библиотеке
    """
    books = BookSearch()
    books = books.book_search(book_item)
    return books


def put_book():
    """
    Функция для взаимодействия с классом
    BookPut, для изменения статуса у книги
    """
    book_id = input('Введите id книги: ')
    status = input('Введите новый статус: ')
    book = BookPut()
    put = book.path(book_id, status)
    return put


def delete_book():
    """
    Функция для взаимодействия с классом
    BookDelete, для удаления книги по id
    """
    book_id = input('Введите id книги: ')
    book = BookDelete()
    delete = book.book_delete(book_id)
    return delete


if __name__ == '__main__':
    while True:
        answer = input(
            'Вывести данные - 1 / Добавить - 2 / '
            'Поиск - 3 / Обновить - 4 / Удалить - 5 / '
            'Выход - 6: ')
        match answer:
            case '1': print(get_books())
            case '2': print(add_book())
            case '3':
                item = input(
                    'Введите Заголовок, автора или год издания: ').lower()
                print(search_book(item))
            case '4': print(put_book())
            case '5': print(delete_book())
            case '6': break
