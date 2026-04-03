"""Модель преподавателя.

Этот модуль содержит класс Teacher для представления преподавателя
и вспомогательные функции для работы с данными преподавателя.
"""

from typing import Dict, Any, Optional, Tuple
from models.base_entity import BaseEntity


class Teacher(BaseEntity):
    """Класс для представления преподавателя.
    
    Атрибуты:
        _name (str): Имя преподавателя.
        _email (str): Электронная почта преподавателя.
        _department (str): Кафедра преподавателя.
    
    Пример:
        >>> teacher = Teacher(name="Иван Петров", email="ivan@example.com", department="Кафедра математики")
        >>> print(teacher.name)
        Иван Петров
    """
    
    def __init__(self, name: str, email: str, department: str, entity_id: Optional[str] = None) -> None:
        """Инициализация преподавателя.
        
        Args:
            name: Имя преподавателя.
            email: Электронная почта преподавателя.
            department: Кафедра преподавателя.
            entity_id: Опциональный ID сущности. Если не указан, генерируется автоматически.
        """
        super().__init__(entity_id)
        self._name: str = ""
        self._email: str = ""
        self._department: str = ""
        # Устанавливаем значения через сеттеры для валидации
        self.name = name
        self.email = email
        self.department = department
    
    @property
    def name(self) -> str:
        """Получить имя преподавателя."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Установить имя преподавателя с валидацией.
        
        Args:
            value: Новое имя преподавателя.
            
        Raises:
            ValueError: Если имя пустое или не является строкой.
        """
        if not isinstance(value, str):
            raise ValueError("Имя должно быть строкой")
        if not value.strip():
            raise ValueError("Имя не может быть пустым")
        self._name = value.strip()
    
    @property
    def email(self) -> str:
        """Получить электронную почту преподавателя."""
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        """Установить электронную почту преподавателя с валидацией.
        
        Args:
            value: Новая электронная почта.
            
        Raises:
            ValueError: Если email пустой или не является строкой.
        """
        if not isinstance(value, str):
            raise ValueError("Email должен быть строкой")
        if not value.strip():
            raise ValueError("Email не может быть пустым")
        self._email = value.strip()
    
    @property
    def department(self) -> str:
        """Получить кафедру преподавателя."""
        return self._department
    
    @department.setter
    def department(self, value: str) -> None:
        """Установить кафедру преподавателя с валидацией.
        
        Args:
            value: Новая кафедра.
            
        Raises:
            ValueError: Если кафедра пустая или не является строкой.
        """
        if not isinstance(value, str):
            raise ValueError("Кафедра должна быть строкой")
        if not value.strip():
            raise ValueError("Кафедра не может быть пустой")
        self._department = value.strip()
    
    def _validate(self) -> bool:
        """Проверить валидность данных преподавателя.
        
        Возвращает True, если все поля корректны.
        
        Returns:
            bool: True если данные валидны, иначе False.
        """
        try:
            # Проверяем, что все поля непустые строки
            if not self._name or not self._email or not self._department:
                return False
            # Дополнительная проверка на тип (на случай обхода сеттеров)
            if not all(isinstance(x, str) for x in [self._name, self._email, self._department]):
                return False
            return True
        except Exception:
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Сериализовать преподавателя в словарь.
        
        Returns:
            Dict[str, Any]: Словарь с данными преподавателя.
        """
        base_dict = super().to_dict()
        base_dict.update({
            'name': self._name,
            'email': self._email,
            'department': self._department
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Teacher":
        """Создать преподавателя из словаря.
        
        Args:
            data: Словарь с данными преподавателя.
            
        Returns:
            Teacher: Новый экземпляр преподавателя.
        """
        return cls(
            name=data.get('name', ''),
            email=data.get('email', ''),
            department=data.get('department', ''),
            entity_id=data.get('id')
        )
    
    def __str__(self) -> str:
        """Строковое представление преподавателя.
        
        Returns:
            str: Форматированная строка с информацией о преподавателе.
        """
        return f"{self._name} ({self._email}), {self._department}"


def format_teacher_info(teacher_data: Dict[str, Any]) -> str:
    """Отформатировать информацию о преподавателе в строку.
    
    Чистая функция для форматирования данных преподавателя.
    
    Args:
        teacher_data: Словарь с ключами 'name', 'email', 'department'.
        
    Returns:
        str: Форматированная строка с информацией о преподавателе.
        
    Example:
        >>> data = {'name': 'Иван Петров', 'email': 'ivan@example.com', 'department': 'Кафедра математики'}
        >>> format_teacher_info(data)
        'Преподаватель: Иван Петров | Email: ivan@example.com | Кафедра: Кафедра математики'
    """
    name = teacher_data.get('name', 'Не указано')
    email = teacher_data.get('email', 'Не указано')
    department = teacher_data.get('department', 'Не указано')
    return f"Преподаватель: {name} | Email: {email} | Кафедра: {department}"


def parse_teacher_input(name: str, email: str, department: str) -> Tuple[bool, str, Dict[str, str]]:
    """Валидировать и подготовить входные данные для создания преподавателя.
    
    Чистая функция для проверки и нормализации входных данных.
    
    Args:
        name: Имя преподавателя.
        email: Электронная почта.
        department: Кафедра.
        
    Returns:
        Tuple[bool, str, Dict[str, str]]: Кортеж из (успешность, сообщение, данные).
    """
    errors = []
    
    # Валидация имени
    if not isinstance(name, str) or not name.strip():
        errors.append("Имя должно быть непустой строкой")
    
    # Валидация email
    if not isinstance(email, str) or not email.strip():
        errors.append("Email должен быть непустой строкой")
    
    # Валидация кафедры
    if not isinstance(department, str) or not department.strip():
        errors.append("Кафедра должна быть непустой строкой")
    
    if errors:
        return False, "; ".join(errors), {}
    
    return True, "Данные валидны", {
        'name': name.strip(),
        'email': email.strip(),
        'department': department.strip()
    }
