"""
Чистые функции валидации для расписания.

Все функции в этом модуле являются чистыми (pure functions):
- Не имеют побочных эффектов
- Не зависят от внешнего состояния
- Возвращают одинаковый результат для одинаковых входных данных
"""

from typing import List, Dict, Any
import re


def validate_time_format(time_str: str) -> bool:
    """
    Проверяет корректность формата времени (HH:MM).
    
    Args:
        time_str: Строка времени в формате "HH:MM".
        
    Returns:
        True, если формат корректен, иначе False.
        
    Examples:
        >>> validate_time_format("09:00")
        True
        >>> validate_time_format("25:00")
        False
        >>> validate_time_format("9:0")
        False
    """
    pattern = r"^([01]?[0-9]|2[0-3]):([0-5][0-9])$"
    if not re.match(pattern, time_str):
        return False
    
    try:
        hours, minutes = map(int, time_str.split(':'))
        return 0 <= hours <= 23 and 0 <= minutes <= 59
    except ValueError:
        return False


def check_time_overlap(start1: str, end1: str, start2: str, end2: str) -> bool:
    """
    Проверяет, пересекаются ли два временных интервала.
    
    Функция предполагает, что время указано в формате HH:MM и принадлежит одному дню.
    
    Args:
        start1: Время начала первого интервала.
        end1: Время окончания первого интервала.
        start2: Время начала второго интервала.
        end2: Время окончания второго интервала.
        
    Returns:
        True, если интервалы пересекаются, иначе False.
        
    Note:
        Граничные значения (когда end1 == start2) не считаются пересечением.
    """
    def time_to_minutes(time_str: str) -> int:
        """Преобразует время HH:MM в количество минут с начала дня."""
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    
    # Преобразуем все времена в минуты для простого сравнения
    s1 = time_to_minutes(start1)
    e1 = time_to_minutes(end1)
    s2 = time_to_minutes(start2)
    e2 = time_to_minutes(end2)
    
    # Проверка на корректность интервалов
    if s1 >= e1 or s2 >= e2:
        return False
    
    # Интервалы НЕ пересекаются, если один заканчивается до начала другого
    # Пересечение есть, если это условие НЕ выполняется
    no_overlap = e1 <= s2 or e2 <= s1
    return not no_overlap


def detect_schedule_conflicts(
    new_slot: Dict[str, Any],
    existing_slots: List[Dict[str, Any]]
) -> List[str]:
    """
    Обнаруживает конфликты между новым занятием и существующими.
    
    Конфликт возникает, если:
    - Одна и та же группа имеет занятия в одно время
    - Один и тот же преподаватель ведет занятия в одно время
    - Одна и та же аудитория занята в одно время
    
    Args:
        new_slot: Словарь с данными нового занятия.
            Обязательные ключи: 'group_id', 'teacher_id', 'classroom_id', 
            'day_of_week', 'start_time', 'end_time'.
        existing_slots: Список словарей с данными существующих занятий.
        
    Returns:
        Список строк с описанием найденных конфликтов. Пустой список, если конфликтов нет.
        
    Example:
        >>> new = {
        ...     'group_id': 1, 'teacher_id': 2, 'classroom_id': 3,
        ...     'day_of_week': 1, 'start_time': '09:00', 'end_time': '10:30'
        ... }
        >>> existing = [{
        ...     'group_id': 1, 'teacher_id': 5, 'classroom_id': 7,
        ...     'day_of_week': 1, 'start_time': '09:00', 'end_time': '10:30'
        ... }]
        >>> conflicts = detect_schedule_conflicts(new, existing)
        >>> len(conflicts) > 0
        True
    """
    conflicts = []
    
    new_day = new_slot.get('day_of_week')
    new_start = new_slot.get('start_time')
    new_end = new_slot.get('end_time')
    new_group_id = new_slot.get('group_id')
    new_teacher_id = new_slot.get('teacher_id')
    new_classroom_id = new_slot.get('classroom_id')
    
    # Валидация входных данных
    if not all([new_day, new_start, new_end]):
        return ["Некорректные данные нового занятия"]
    
    if not validate_time_format(new_start) or not validate_time_format(new_end):
        return ["Некорректный формат времени в новом занятии"]
    
    for slot in existing_slots:
        slot_day = slot.get('day_of_week')
        slot_start = slot.get('start_time', '')
        slot_end = slot.get('end_time', '')
        
        # Пропускаем занятия в другие дни
        if slot_day != new_day:
            continue
        
        # Пропускаем занятия с некорректным временем
        if not validate_time_format(slot_start) or not validate_time_format(slot_end):
            continue
        
        # Проверяем пересечение по времени
        if not check_time_overlap(new_start, new_end, slot_start, slot_end):
            continue
        
        # Есть пересечение по времени - проверяем конфликты ресурсов
        
        # Конфликт группы
        if slot.get('group_id') == new_group_id:
            conflicts.append(
                f"Конфликт группы {new_group_id}: занятие уже запланировано "
                f"на {slot_day} день с {slot_start} до {slot_end}"
            )
        
        # Конфликт преподавателя
        if slot.get('teacher_id') == new_teacher_id:
            conflicts.append(
                f"Конфликт преподавателя {new_teacher_id}: занятие уже запланировано "
                f"на {slot_day} день с {slot_start} до {slot_end}"
            )
        
        # Конфликт аудитории
        if slot.get('classroom_id') == new_classroom_id:
            conflicts.append(
                f"Конфликт аудитории {new_classroom_id}: занятие уже запланировано "
                f"на {slot_day} день с {slot_start} до {slot_end}"
            )
    
    return conflicts
