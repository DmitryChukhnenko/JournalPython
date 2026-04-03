"""Модель аудитории.

Этот модуль содержит класс Classroom для представления учебной аудитории
и вспомогательные функции для работы с данными аудитории.
"""

from typing import Dict, Any, Optional, Tuple
from models.base_entity import BaseEntity


class Classroom(BaseEntity):
    """Класс для представления учебной аудитории.
    
    Атрибуты:
        _number (str): Номер аудитории (например, "301").
        _building (str): Название корпуса (например, "Главный корпус").
        _capacity (int): Вместимость аудитории (количество мест).
    
    Пример:
        >>> classroom = Classroom(number="301", building="Главный корпус", capacity=30)
        >>> print(classroom.number)
        301
    """
    
    def __init__(self, number: str, building: str, capacity: int, entity_id: Optional[str] = None) -> None:
        """Инициализация учебной аудитории.
        
        Args:
            number: Номер аудитории.
            building: Название корпуса.
            capacity: Вместимость аудитории.
            entity_id: Опциональный ID сущности. Если не указан, генерируется автоматически.
        """
        super().__init__(entity_id)
        self._number: str = ""
        self._building: str = ""
        self._capacity: int = 0
        # Устанавливаем значения через сеттеры для валидации
        self.number = number
        self.building = building
        self.capacity = capacity
    
    @property
    def number(self) -> str:
        """Получить номер аудитории."""
        return self._number
    
    @number.setter
    def number(self, value: str) -> None:
        """Установить номер аудитории с валидацией.
        
        Args:
            value: Новый номер аудитории.
            
        Raises:
            ValueError: Если номер пустой или не является строкой.
        """
        if not isinstance(value, str):
            raise ValueError("Номер аудитории должен быть строкой")
        if not value.strip():
            raise ValueError("Номер аудитории не может быть пустым")
        self._number = value.strip()
    
    @property
    def building(self) -> str:
        """Получить название корпуса."""
        return self._building
    
    @building.setter
    def building(self, value: str) -> None:
        """Установить название корпуса с валидацией.
        
        Args:
            value: Новое название корпуса.
            
        Raises:
            ValueError: Если название корпуса пустое или не является строкой.
        """
        if not isinstance(value, str):
            raise ValueError("Название корпуса должно быть строкой")
        if not value.strip():
            raise ValueError("Название корпуса не может быть пустым")
        self._building = value.strip()
    
    @property
    def capacity(self) -> int:
        """Получить вместимость аудитории."""
        return self._capacity
    
    @capacity.setter
    def capacity(self, value: int) -> None:
        """Установить вместимость аудитории с валидацией.
        
        Args:
            value: Новая вместимость аудитории.
            
        Raises:
            ValueError: Если вместимость не является положительным числом.
        """
        if not isinstance(value, int):
            raise ValueError("Вместимость должна быть целым числом")
        if value <= 0:
            raise ValueError("Вместимость должна быть положительным числом")
        self._capacity = value
    
    def _validate(self) -> bool:
        """Проверить валидность данных аудитории.
        
        Возвращает True, если все поля корректны.
        
        Returns:
            bool: True если данные валидны, иначе False.
        """
        try:
            # Проверяем, что все поля корректны
            if not self._number or not self._building:
                return False
            if self._capacity <= 0:
                return False
            # Дополнительная проверка на тип (на случай обхода сеттеров)
            if not all(isinstance(x, str) for x in [self._number, self._building]):
                return False
            if not isinstance(self._capacity, int):
                return False
            return True
        except Exception:
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Сериализовать аудиторию в словарь.
        
        Returns:
            Dict[str, Any]: Словарь с данными аудитории.
        """
        base_dict = super().to_dict()
        base_dict.update({
            'number': self._number,
            'building': self._building,
            'capacity': self._capacity
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Classroom":
        """Создать аудиторию из словаря.
        
        Args:
            data: Словарь с данными аудитории.
            
        Returns:
            Classroom: Новый экземпляр аудитории.
        """
        return cls(
            number=data.get('number', ''),
            building=data.get('building', ''),
            capacity=data.get('capacity', 0),
            entity_id=data.get('id')
        )
    
    def __str__(self) -> str:
        """Строковое представление аудитории.
        
        Returns:
            str: Форматированная строка с информацией об аудитории.
        """
        return f"Ауд. {self._number} ({self._building}), {self._capacity} мест"


def format_classroom_info(classroom_data: Dict[str, Any]) -> str:
    """Отформатировать информацию об аудитории в строку.
    
    Чистая функция для форматирования данных аудитории.
    
    Args:
        classroom_data: Словарь с ключами 'number', 'building', 'capacity'.
        
    Returns:
        str: Форматированная строка с информацией об аудитории.
        
    Example:
        >>> data = {'number': '301', 'building': 'Главный корпус', 'capacity': 30}
        >>> format_classroom_info(data)
        'Аудитория: 301 | Корпус: Главный корпус | Вместимость: 30 мест'
    """
    number = classroom_data.get('number', 'Не указано')
    building = classroom_data.get('building', 'Не указано')
    capacity = classroom_data.get('capacity', 0)
    return f"Аудитория: {number} | Корпус: {building} | Вместимость: {capacity} мест"


def parse_classroom_input(number: str, building: str, capacity: Any) -> Tuple[bool, str, Dict[str, Any]]:
    """Валидировать и подготовить входные данные для создания аудитории.
    
    Чистая функция для проверки и нормализации входных данных.
    
    Args:
        number: Номер аудитории.
        building: Название корпуса.
        capacity: Вместимость (может быть строкой или числом).
        
    Returns:
        Tuple[bool, str, Dict[str, Any]]: Кортеж из (успешность, сообщение, данные).
    """
    errors = []
    
    # Валидация номера
    if not isinstance(number, str) or not number.strip():
        errors.append("Номер аудитории должен быть непустой строкой")
    
    # Валидация корпуса
    if not isinstance(building, str) or not building.strip():
        errors.append("Название корпуса должно быть непустой строкой")
    
    # Валидация вместимости
    try:
        capacity_int = int(capacity)
        if capacity_int <= 0:
            errors.append("Вместимость должна быть положительным числом")
    except (ValueError, TypeError):
        errors.append("Вместимость должна быть целым числом")
        capacity_int = 0
    
    if errors:
        return False, "; ".join(errors), {}
    
    return True, "Данные валидны", {
        'number': number.strip(),
        'building': building.strip(),
        'capacity': capacity_int
    }
