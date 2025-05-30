import json
import os
from typing import Dict
from book_logger import logger

class JsonBookStorage:
    def __init__(self, filename='archive_books.json'):
        self.filename = filename
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def load_data(self) -> Dict[str, dict]:
        with open(self.filename, 'r', encoding='utf-8') as f:
            try:
                return json.load(f) if os.stat(self.filename).st_size > 0 else {}
            except json.JSONDecodeError:
                logger.error('Ошибка чтения JSON-файла')
                raise

    def save_data(self, data: Dict[str, dict]):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
