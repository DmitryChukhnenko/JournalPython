"""Модель предмета (дисциплины).

Этот модуль содержит класс Subject для представления учебного предмета
и вспомогательные функции для работы с данными предмета.
"""

from typing import Dict, Any, Optional, Tuple
from models.base_entity import BaseEntity


class Subject(BaseEntity):
    """Класс для представления учебного предмета.
    
    Атрибуты:
        _name (str): Название предмета.
        _code (str): Код предмета (например, "MATH-101").
        _hours (int): Количество часов по предмету.
    
    Пример:
        >>> subject = Subject(name="Высшая математика", code="MATH-101", hours=72)
        >>> print(subject.name)
        Высшая математика
    """
    
    def __init__(self, name: str, code: str, hours: int, entity_id: Optional[str] = None) -> None:
        """Инициализация учебного предмета.
        
        Args:
            name: Название предмета.
            code: Код предмета.
            hours: Количество часов по предмету.
            entity_id: Опциональный ID сущности. Если не указан, генерируется автоматически.
        """
        super().__init__(entity_id)
        self._name: str = ""
        self._code: str = ""
        self._hours: int = 0
        # Устанавливаем значения через сеттеры для валидации
        self.name = name
        self.code = code
        self.hours = hours
    
    @property
    def name(self) -> str:
        """Получить название предмета."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Установить название предмета с валидацией.
        
        Args:
            value: Новое название предмета.
            
        Raises:
            ValueError: Если название пустое или не является строкой.
        """
        if not isinstance(value, str):
            raise ValueError("Название предмета должно быть строкой")
        if not value.strip():
            raise ValueError("Название предмета не может быть пустым")
        self._name = value.strip()
    
    @property
    def code(self) -> str:
        """Получить код предмета."""
        return self._code
    
    @code.setter
    def code(self, value: str) -> None:
        """Установить код предмета с валидацией.
        
        Args:
            value: Новый код предмета.
            
        Raises:
            ValueError: Если код пустой или не является строкой.
        """
        if not isinstance(value, str):
            raise ValueError("Код предмета должен быть строкой")
        if not value.strip():
            raise ValueError("Код предмета не может быть пустым")
        self._code = value.strip()
    
    @property
    def hours(self) -> int:
        """Получить количество часов по предмету."""
        return self._hours
    
    @hours.setter
    def hours(self, value: int) -> None:
        """Установить количество часов по предмету с валидацией.
        
        Args:
            value: Новое количество часов.
            
        Raises:
            ValueError: Если количество часов не является положительным числом.
        """
        if not isinstance(value, int):
            raise ValueError("Количество часов должно быть целым числом")
        if value <= 0:
            raise ValueError("Количество часов должно быть положительным числом")
        self._hours = value
    
    def _validate(self) -> bool:
        """Проверить валидность данных предмета.
        
        Возвращает True, если все поля корректны.
        
        Returns:
            bool: True если данные валидны, иначе False.
        """
        try:
            # Проверяем, что все поля корректны
            if not self._name or not self._code:
                return False
            if self._hours <= 0:
                return False
            # Дополнительная проверка на тип (на случай обхода сеттеров)
            if not all(isinstance(x, str) for x in [self._name, self._code]):
                return False
            if not isinstance(self._hours, int):
                return False
            return True
        except Exception:
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Сериализовать предмет в словарь.
        
        Returns:
            Dict[str, Any]: Словарь с данными предмета.
        """
        base_dict = super().to_dict()
        base_dict.update({
            'name': self._name,
            'code': self._code,
            'hours': self._hours
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Subject":
        """Создать предмет из словаря.
        
        Args:
            data: Словарь с данными предмета.
            
        Returns:
            Subject: Новый экземпляр предмета.
        """
        return cls(
            name=data.get('name', ''),
            code=data.get('code', ''),
            hours=data.get('hours', 0),
            entity_id=data.get('id')
        )
    
    def __str__(self) -> str:
        """Строковое представление предмета.
        
        Returns:
            str: Форматированная строка с информацией о предмете.
        """
        return f"{self._code}: {self._name} ({self._hours} ч.)"


def format_subject_info(subject_data: Dict[str, Any]) -> str:
    """Отформатировать информацию о предмете в строку.
    
    Чистая функция для форматирования данных предмета.
    
    Args:
        subject_data: Словарь с ключами 'name', 'code', 'hours'.
        
    Returns:
        str: Форматированная строка с информацией о предмете.
        
    Example:
        >>> data = {'name': 'Высшая математика', 'code': 'MATH-101', 'hours': 72}
        >>> format_subject_info(data)
        'Предмет: Высшая математика | Код: MATH-101 | Часов: 72'
    """
    name = subject_data.get('name', 'Не указано')
    code = subject_data.get('code', 'Не указано')
    hours = subject_data.get('hours', 0)
    return f"Предмет: {name} | Код: {code} | Часов: {hours}"


def parse_subject_input(name: str, code: str, hours: Any) -> Tuple[bool, str, Dict[str, Any]]:
    """Валидировать и подготовить входные данные для создания предмета.
    
    Чистая функция для проверки и нормализации входных данных.
    
    Args:
        name: Название предмета.
        code: Код предмета.
        hours: Количество часов (может быть строкой или числом).
        
    Returns:
        Tuple[bool, str, Dict[str, Any]]: Кортеж из (успешность, сообщение, данные).
    """
    errors = []
    
    # Валидация названия
    if not isinstance(name, str) or not name.strip():
        errors.append("Название предмета должно быть непустой строкой")
    
    # Валидация кода
    if not isinstance(code, str) or not code.strip():
        errors.append("Код предмета должен быть непустой строкой")
    
    # Валидация количества часов
    try:
        hours_int = int(hours)
        if hours_int <= 0:
            errors.append("Количество часов должно быть положительным числом")
    except (ValueError, TypeError):
        errors.append("Количество часов должно быть целым числом")
        hours_int = 0
    
    if errors:
        return False, "; ".join(errors), {}
    
    return True, "Данные валидны", {
        'name': name.strip(),
        'code': code.strip(),
        'hours': hours_int
    }
