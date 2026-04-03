"""Модель учебной группы.

Этот модуль содержит класс Group для представления учебной группы
и вспомогательные функции для работы с данными группы.
"""

from typing import Dict, Any, Optional, Tuple
from models.base_entity import BaseEntity


class Group(BaseEntity):
    """Класс для представления учебной группы.
    
    Атрибуты:
        _name (str): Название группы (например, "ИВТ-201").
        _size (int): Количество студентов в группе.
        _curator (str): Куратор группы (ФИО преподавателя).
    
    Пример:
        >>> group = Group(name="ИВТ-201", size=25, curator="Петров И.И.")
        >>> print(group.name)
        ИВТ-201
    """
    
    def __init__(self, name: str, size: int, curator: str, entity_id: Optional[str] = None) -> None:
        """Инициализация учебной группы.
        
        Args:
            name: Название группы.
            size: Количество студентов в группе.
            curator: ФИО куратора группы.
            entity_id: Опциональный ID сущности. Если не указан, генерируется автоматически.
        """
        super().__init__(entity_id)
        self._name: str = ""
        self._size: int = 0
        self._curator: str = ""
        # Устанавливаем значения через сеттеры для валидации
        self.name = name
        self.size = size
        self.curator = curator
    
    @property
    def name(self) -> str:
        """Получить название группы."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Установить название группы с валидацией.
        
        Args:
            value: Новое название группы.
            
        Raises:
            ValueError: Если название пустое или не является строкой.
        """
        if not isinstance(value, str):
            raise ValueError("Название группы должно быть строкой")
        if not value.strip():
            raise ValueError("Название группы не может быть пустым")
        self._name = value.strip()
    
    @property
    def size(self) -> int:
        """Получить количество студентов в группе."""
        return self._size
    
    @size.setter
    def size(self, value: int) -> None:
        """Установить количество студентов в группе с валидацией.
        
        Args:
            value: Новое количество студентов.
            
        Raises:
            ValueError: Если размер не является положительным числом.
        """
        if not isinstance(value, int):
            raise ValueError("Размер группы должен быть целым числом")
        if value <= 0:
            raise ValueError("Размер группы должен быть положительным числом")
        self._size = value
    
    @property
    def curator(self) -> str:
        """Получить ФИО куратора группы."""
        return self._curator
    
    @curator.setter
    def curator(self, value: str) -> None:
        """Установить ФИО куратора группы с валидацией.
        
        Args:
            value: Новое ФИО куратора.
            
        Raises:
            ValueError: Если куратор пустой или не является строкой.
        """
        if not isinstance(value, str):
            raise ValueError("Куратор должен быть строкой")
        if not value.strip():
            raise ValueError("Куратор не может быть пустым")
        self._curator = value.strip()
    
    def _validate(self) -> bool:
        """Проверить валидность данных группы.
        
        Возвращает True, если все поля корректны.
        
        Returns:
            bool: True если данные валидны, иначе False.
        """
        try:
            # Проверяем, что все поля корректны
            if not self._name or not self._curator:
                return False
            if self._size <= 0:
                return False
            # Дополнительная проверка на тип (на случай обхода сеттеров)
            if not all(isinstance(x, str) for x in [self._name, self._curator]):
                return False
            if not isinstance(self._size, int):
                return False
            return True
        except Exception:
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Сериализовать группу в словарь.
        
        Returns:
            Dict[str, Any]: Словарь с данными группы.
        """
        base_dict = super().to_dict()
        base_dict.update({
            'name': self._name,
            'size': self._size,
            'curator': self._curator
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Group":
        """Создать группу из словаря.
        
        Args:
            data: Словарь с данными группы.
            
        Returns:
            Group: Новый экземпляр группы.
        """
        return cls(
            name=data.get('name', ''),
            size=data.get('size', 0),
            curator=data.get('curator', ''),
            entity_id=data.get('id')
        )
    
    def __str__(self) -> str:
        """Строковое представление группы.
        
        Returns:
            str: Форматированная строка с информацией о группе.
        """
        return f"{self._name} ({self._size} студ.), Куратор: {self._curator}"


def format_group_info(group_data: Dict[str, Any]) -> str:
    """Отформатировать информацию о группе в строку.
    
    Чистая функция для форматирования данных группы.
    
    Args:
        group_data: Словарь с ключами 'name', 'size', 'curator'.
        
    Returns:
        str: Форматированная строка с информацией о группе.
        
    Example:
        >>> data = {'name': 'ИВТ-201', 'size': 25, 'curator': 'Петров И.И.'}
        >>> format_group_info(data)
        'Группа: ИВТ-201 | Студентов: 25 | Куратор: Петров И.И.'
    """
    name = group_data.get('name', 'Не указано')
    size = group_data.get('size', 0)
    curator = group_data.get('curator', 'Не указано')
    return f"Группа: {name} | Студентов: {size} | Куратор: {curator}"


def parse_group_input(name: str, size: Any, curator: str) -> Tuple[bool, str, Dict[str, Any]]:
    """Валидировать и подготовить входные данные для создания группы.
    
    Чистая функция для проверки и нормализации входных данных.
    
    Args:
        name: Название группы.
        size: Количество студентов (может быть строкой или числом).
        curator: ФИО куратора.
        
    Returns:
        Tuple[bool, str, Dict[str, Any]]: Кортеж из (успешность, сообщение, данные).
    """
    errors = []
    
    # Валидация названия
    if not isinstance(name, str) or not name.strip():
        errors.append("Название группы должно быть непустой строкой")
    
    # Валидация размера
    try:
        size_int = int(size)
        if size_int <= 0:
            errors.append("Размер группы должен быть положительным числом")
    except (ValueError, TypeError):
        errors.append("Размер группы должен быть целым числом")
        size_int = 0
    
    # Валидация куратора
    if not isinstance(curator, str) or not curator.strip():
        errors.append("Куратор должен быть непустой строкой")
    
    if errors:
        return False, "; ".join(errors), {}
    
    return True, "Данные валидны", {
        'name': name.strip(),
        'size': size_int,
        'curator': curator.strip()
    }
