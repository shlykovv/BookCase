# Тестовое задание - BookCase

****BookCase - проект позволяет:****

- Добавлять книги в библиотеку
- Просматривать все книги данной библиотеки
- Изменять статус книги
- Выполнять поиск по названию, автору и году выпуска книг
- Удалять книги из библиотеки

### **Стек**
![python version](https://img.shields.io/badge/Python-3.11-green)

## Инструкции по установке

1. Клонируйте репозиторий и перейдите в него через командную строку:
```bash
git clone https://github.com/shlykovv/BookCase.git
```
2. Создайте виртуальное окружение venv:
```bash
python -m venv venv
```
Для Linux или MacOs
```bash
source venv/Scripts/activate
```
для Windows
```bash
. /venv/Scripts/activate
```
3. Обновите менеджер пакетов pip:
```bash
python -m pip install --upgrade pip
```
4. Установите зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```
```bash
# * - примечание: в случае если что-то не установится или будет какая-то ошибка,
# то устанавливайте по одному пакету из файла requirements.txt
```
5. Запустите файл books.py для проверки работы
```bash
python books.py
```
# Тестирование
**В данный проект добавлено несколько тестов для проверки работоспособности**
1. TestBookLibrary - тест "вывода данных из библиотеки"
2. TestBookAdd - тест "добавления новой книги"
3. TestBookPut - тест "изменение статуса книги"

# Для запуска тестов, перейдите в директорию с проектом и  используйте команду:
```commandline
python -m unittest -v tests
```

