"""
Модуль занятия (ScheduleSlot).

Связывает сущности (предмет, группа, преподаватель, аудитория) 
с временными параметрами (день недели, время начала и окончания).
"""

from typing import Dict, Any, Optional
import uuid

# Дни недели как константы для удобства
DAYS_OF_WEEK = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота",
    7: "Воскресенье"
}


class ScheduleSlot:
    """
    Класс, представляющий занятие в расписании.
    
    Атрибуты:
        subject_id: ID предмета.
        group_id: ID учебной группы.
        teacher_id: ID преподавателя.
        classroom_id: ID аудитории.
        day_of_week: День недели (1-7).
        start_time: Время начала (HH:MM).
        end_time: Время окончания (HH:MM).
    """
    
    def __init__(
        self,
        subject_id: str,
        group_id: str,
        teacher_id: str,
        classroom_id: str,
        day_of_week: int,
        start_time: str,
        end_time: str,
        slot_id: Optional[str] = None
    ):
        """
        Инициализирует новое занятие.
        
        Args:
            subject_id: ID предмета.
            group_id: ID учебной группы.
            teacher_id: ID преподавателя.
            classroom_id: ID аудитории.
            day_of_week: День недели (1-7).
            start_time: Время начала в формате HH:MM.
            end_time: Время окончания в формате HH:MM.
            slot_id: Опциональный ID занятия. Если не указан, генерируется автоматически.
        """
        # Приватные атрибуты для инкапсуляции
        self._id: str = slot_id if slot_id else str(uuid.uuid4())
        self._subject_id: str = subject_id
        self._group_id: str = group_id
        self._teacher_id: str = teacher_id
        self._classroom_id: str = classroom_id
        self._day_of_week: int = day_of_week
        self._start_time: str = start_time
        self._end_time: str = end_time
        
        # Валидация при создании
        self._validate()
    
    # ==================== Properties ====================
    
    @property
    def id(self) -> str:
        """Возвращает ID занятия."""
        return self._id
    
    @property
    def subject_id(self) -> str:
        """Возвращает ID предмета."""
        return self._subject_id
    
    @subject_id.setter
    def subject_id(self, value: str) -> None:
        """Устанавливает ID предмета."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("ID предмета должен быть непустой строкой")
        self._subject_id = value
    
    @property
    def group_id(self) -> str:
        """Возвращает ID группы."""
        return self._group_id
    
    @group_id.setter
    def group_id(self, value: str) -> None:
        """Устанавливает ID группы."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("ID группы должен быть непустой строкой")
        self._group_id = value
    
    @property
    def teacher_id(self) -> str:
        """Возвращает ID преподавателя."""
        return self._teacher_id
    
    @teacher_id.setter
    def teacher_id(self, value: str) -> None:
        """Устанавливает ID преподавателя."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("ID преподавателя должен быть непустой строкой")
        self._teacher_id = value
    
    @property
    def classroom_id(self) -> str:
        """Возвращает ID аудитории."""
        return self._classroom_id
    
    @classroom_id.setter
    def classroom_id(self, value: str) -> None:
        """Устанавливает ID аудитории."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("ID аудитории должен быть непустой строкой")
        self._classroom_id = value
    
    @property
    def day_of_week(self) -> int:
        """Возвращает день недели (1-7)."""
        return self._day_of_week
    
    @day_of_week.setter
    def day_of_week(self, value: int) -> None:
        """
        Устанавливает день недели.
        
        Args:
            value: День недели (1-7).
            
        Raises:
            ValueError: Если значение вне диапазона 1-7.
        """
        if not isinstance(value, int) or value < 1 or value > 7:
            raise ValueError("День недели должен быть целым числом от 1 до 7")
        self._day_of_week = value
    
    @property
    def start_time(self) -> str:
        """Возвращает время начала занятия."""
        return self._start_time
    
    @start_time.setter
    def start_time(self, value: str) -> None:
        """
        Устанавливает время начала занятия.
        
        Args:
            value: Время в формате HH:MM.
            
        Raises:
            ValueError: Если формат времени некорректен.
        """
        if not self._is_valid_time_format(value):
            raise ValueError(f"Некорректный формат времени начала: {value}. Ожидается HH:MM")
        self._start_time = value
    
    @property
    def end_time(self) -> str:
        """Возвращает время окончания занятия."""
        return self._end_time
    
    @end_time.setter
    def end_time(self, value: str) -> None:
        """
        Устанавливает время окончания занятия.
        
        Args:
            value: Время в формате HH:MM.
            
        Raises:
            ValueError: Если формат времени некорректен или время раньше начала.
        """
        if not self._is_valid_time_format(value):
            raise ValueError(f"Некорректный формат времени окончания: {value}. Ожидается HH:MM")
        
        # Проверка, что конец позже начала
        if self._start_time and self._time_to_minutes(value) <= self._time_to_minutes(self._start_time):
            raise ValueError("Время окончания должно быть позже времени начала")
        self._end_time = value
    
    # ==================== Private Methods ====================
    
    @staticmethod
    def _is_valid_time_format(time_str: str) -> bool:
        """
        Проверяет корректность формата времени HH:MM.
        
        Args:
            time_str: Строка времени.
            
        Returns:
            True, если формат корректен.
        """
        import re
        pattern = r"^([01]?[0-9]|2[0-3]):([0-5][0-9])$"
        if not re.match(pattern, time_str):
            return False
        try:
            hours, minutes = map(int, time_str.split(':'))
            return 0 <= hours <= 23 and 0 <= minutes <= 59
        except ValueError:
            return False
    
    @staticmethod
    def _time_to_minutes(time_str: str) -> int:
        """Преобразует время HH:MM в минуты."""
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    
    def _validate(self) -> bool:
        """
        Валидирует все поля занятия.
        
        Returns:
            True, если все поля корректны.
            
        Raises:
            ValueError: При обнаружении ошибок валидации.
        """
        # Проверка ID сущностей
        if not all([self._subject_id, self._group_id, self._teacher_id, self._classroom_id]):
            raise ValueError("Все ID сущностей должны быть указаны")
        
        # Проверка дня недели
        if not isinstance(self._day_of_week, int) or not (1 <= self._day_of_week <= 7):
            raise ValueError("День недели должен быть от 1 до 7")
        
        # Проверка формата времени
        if not self._is_valid_time_format(self._start_time):
            raise ValueError(f"Некорректное время начала: {self._start_time}")
        
        if not self._is_valid_time_format(self._end_time):
            raise ValueError(f"Некорректное время окончания: {self._end_time}")
        
        # Проверка, что конец позже начала
        if self._time_to_minutes(self._end_time) <= self._time_to_minutes(self._start_time):
            raise ValueError("Время окончания должно быть позже времени начала")
        
        return True
    
    # ==================== Public Methods ====================
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Сериализует занятие в словарь.
        
        Returns:
            Словарь с данными занятия.
        """
        return {
            'id': self._id,
            'subject_id': self._subject_id,
            'group_id': self._group_id,
            'teacher_id': self._teacher_id,
            'classroom_id': self._classroom_id,
            'day_of_week': self._day_of_week,
            'start_time': self._start_time,
            'end_time': self._end_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScheduleSlot":
        """
        Десериализует занятие из словаря.
        
        Args:
            data: Словарь с данными занятия.
            
        Returns:
            Экземпляр ScheduleSlot.
            
        Raises:
            KeyError: Если отсутствуют обязательные ключи.
            ValueError: Если данные некорректны.
        """
        required_keys = ['subject_id', 'group_id', 'teacher_id', 'classroom_id', 
                        'day_of_week', 'start_time', 'end_time']
        
        for key in required_keys:
            if key not in data:
                raise KeyError(f"Отсутствует обязательное поле: {key}")
        
        return cls(
            subject_id=data['subject_id'],
            group_id=data['group_id'],
            teacher_id=data['teacher_id'],
            classroom_id=data['classroom_id'],
            day_of_week=data['day_of_week'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            slot_id=data.get('id')  # Опциональный ID
        )
    
    def __str__(self) -> str:
        """
        Возвращает строковое представление занятия.
        
        Returns:
            Форматированная строка с информацией о занятии.
        """
        day_name = DAYS_OF_WEEK.get(self._day_of_week, "Неизвестно")
        return (
            f"Занятие #{self._id[:8]}: {day_name}, {self._start_time}-{self._end_time}, "
            f"Предмет:{self._subject_id}, Группа:{self._group_id}, "
            f"Преподаватель:{self._teacher_id}, Аудитория:{self._classroom_id}"
        )
    
    def __eq__(self, other: object) -> bool:
        """Проверяет равенство занятий по ID."""
        if not isinstance(other, ScheduleSlot):
            return False
        return self._id == other._id
