"""
Репозиторий для хранения данных расписания в JSON.

Обеспечивает загрузку и сохранение данных сущностей (группы, предметы,
аудитории, преподаватели) и расписания занятий.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Type, Optional

# Импортируем базовый класс для типизации
# Используем строковую аннотацию для избежания циклических зависимостей


def convert_dicts_to_entities(
    data_list: List[Dict[str, Any]], 
    entity_class: Type[Any]
) -> List[Any]:
    """
    Чистая функция для преобразования списка словарей в список сущностей.
    
    Args:
        data_list: Список словарей с данными.
        entity_class: Класс сущности с методом from_dict.
        
    Returns:
        Список экземпляров сущностей.
    """
    entities = []
    for item in data_list:
        try:
            entity = entity_class.from_dict(item)
            entities.append(entity)
        except (KeyError, ValueError) as e:
            print(f"[WARNING] Пропущена некорректная сущность {entity_class.__name__}: {e}", file=sys.stderr)
    return entities


def convert_entities_to_dicts(entities: List[Any]) -> List[Dict[str, Any]]:
    """
    Чистая функция для преобразования списка сущностей в список словарей.
    
    Args:
        entities: Список экземпляров сущностей с методом to_dict.
        
    Returns:
        Список словарей с данными.
    """
    return [entity.to_dict() for entity in entities if hasattr(entity, 'to_dict')]


class ScheduleRepository:
    """
    Репозиторий для работы с данными расписания в формате JSON.
    
    Хранит данные в структуре:
    {
        "teachers": [...],
        "groups": [...],
        "subjects": [...],
        "classrooms": [...],
        "schedule": [...]
    }
    
    Attributes:
        _file_path: Путь к файлу JSON.
        _cache: Кэш загруженных данных.
    """
    
    # Типы сущностей и их ключи в JSON
    ENTITY_TYPES = ['teachers', 'groups', 'subjects', 'classrooms', 'schedule']
    
    def __init__(self, file_path: str):
        """
        Инициализирует репозиторий.
        
        Создает директорию и файл, если они не существуют.
        
        Args:
            file_path: Путь к файлу JSON.
        """
        self._file_path = Path(file_path)
        self._cache: Dict[str, List[Any]] = self._empty_data()
        
        # Создаем директорию, если она не существует
        try:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"[WARNING] Не удалось создать директорию: {e}", file=sys.stderr)
        
        # Создаем пустой файл, если он не существует
        if not self._file_path.exists():
            self._save_raw(self._empty_data())
    
    @staticmethod
    def _empty_data() -> Dict[str, List[Any]]:
        """Возвращает пустую структуру данных."""
        return {
            'teachers': [],
            'groups': [],
            'subjects': [],
            'classrooms': [],
            'schedule': []
        }
    
    def load_data(self) -> Dict[str, Any]:
        """
        Загружает все данные из файла JSON в кэш.
        
        Returns:
            Словарь со всеми данными. При ошибках возвращает пустую структуру.
        """
        try:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content.strip():
                    # Пустой файл
                    self._cache = self._empty_data()
                    return self._cache
                
                data = json.loads(content)
                
                # Валидация структуры
                if not isinstance(data, dict):
                    raise ValueError("Данные должны быть словарем")
                
                # Обновляем только существующие ключи
                for key in self.ENTITY_TYPES:
                    if key in data and isinstance(data[key], list):
                        self._cache[key] = data[key]
                    else:
                        self._cache[key] = []
                        
                return self._cache.copy()
                
        except FileNotFoundError:
            print(f"[WARNING] Файл не найден: {self._file_path}. Используется пустое хранилище.", file=sys.stderr)
            self._cache = self._empty_data()
        except json.JSONDecodeError as e:
            print(f"[WARNING] Ошибка JSON в файле {self._file_path}: {e}. Используется пустое хранилище.", file=sys.stderr)
            self._cache = self._empty_data()
        except KeyError as e:
            print(f"[WARNING] Отсутствует обязательный ключ: {e}. Используется пустое хранилище.", file=sys.stderr)
            self._cache = self._empty_data()
        except Exception as e:
            print(f"[WARNING] Неизвестная ошибка при загрузке: {e}. Используется пустое хранилище.", file=sys.stderr)
            self._cache = self._empty_data()
        
        return self._cache.copy()
    
    def save_data(self, data: Dict[str, Any]) -> None:
        """
        Сохраняет данные в файл JSON.
        
        Args:
            data: Словарь с данными для сохранения.
        """
        try:
            self._save_raw(data)
            # Обновляем кэш после успешного сохранения
            for key in self.ENTITY_TYPES:
                if key in data:
                    self._cache[key] = data[key]
        except Exception as e:
            print(f"[ERROR] Ошибка при сохранении данных: {e}", file=sys.stderr)
            raise
    
    def _save_raw(self, data: Dict[str, Any]) -> None:
        """
        Внутренний метод для записи данных в файл.
        
        Args:
            data: Словарь с данными.
        """
        with open(self._file_path, 'w', encoding='utf-8') as f:
            print(data)
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_all_entities(self, entity_type: str, entity_class: Type[Any]) -> List[Any]:
        """
        Возвращает все сущности указанного типа.
        
        Args:
            entity_type: Тип сущности ('teachers', 'groups', 'subjects', 'classrooms').
            entity_class: Класс сущности для десериализации.
            
        Returns:
            Список экземпляров сущностей.
        """
        if entity_type not in self.ENTITY_TYPES:
            print(f"[WARNING] Неизвестный тип сущности: {entity_type}", file=sys.stderr)
            return []
        
        # Загружаем свежие данные
        self.load_data()
        
        raw_data = self._cache.get(entity_type, [])
        return convert_dicts_to_entities(raw_data, entity_class)
    
    def save_entities(self, entity_type: str, entities: List[Any]) -> None:
        """
        Сохраняет список сущностей указанного типа.
        
        Args:
            entity_type: Тип сущности ('teachers', 'groups', 'subjects', 'classrooms', 'schedule').
            entities: Список экземпляров сущностей.
        """
        if entity_type not in self.ENTITY_TYPES:
            print(f"[WARNING] Неизвестный тип сущности: {entity_type}", file=sys.stderr)
            return
        
        # Загружаем текущие данные, чтобы не перезаписать другие сущности
        self.load_data()
        
        # Преобразуем сущности в словари
        entities_dicts = convert_entities_to_dicts(entities)
        
        # Обновляем кэш
        self._cache[entity_type] = entities_dicts
        
        # Сохраняем все данные
        self.save_data(self._cache.copy())
    
    def get_raw_data(self) -> Dict[str, Any]:
        """
        Возвращает сырые данные кэша (без преобразования в сущности).
        
        Returns:
            Словарь с данными.
        """
        return self._cache.copy()
