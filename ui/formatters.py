"""
Модуль чистых функций для форматирования и отображения данных расписания.
Не содержит состояния и побочных эффектов (кроме print).
"""

from typing import List, Dict, Any, Optional
from models.base_entity import BaseEntity
from core.schedule_slot import ScheduleSlot


def resolve_schedule_slots(
    slots: List[ScheduleSlot],
    entities: Dict[str, List[BaseEntity]]
) -> List[Dict[str, str]]:
    """
    Преобразует список объектов ScheduleSlot в список словарей с человеко-читаемыми данными.
    
    Заменяет UUID сущностей на их имена/названия. Если сущность не найдена (битая ссылка),
    подставляет заглушку.
    
    Args:
        slots: Список объектов занятий.
        entities: Словарь со всеми загруженными сущностями по типам 
                  ('groups', 'subjects', 'teachers', 'classrooms').
    
    Returns:
        Список словарей с ключами: day, time, group, subject, teacher, classroom.
    """
    # Создаем быстрые словари доступа по ID для каждой категории
    lookup = {
        'groups': {e.id: e.name for e in entities.get('groups', [])},
        'subjects': {e.id: e.name for e in entities.get('subjects', [])},
        'teachers': {e.id: getattr(e, 'full_name', str(e)) for e in entities.get('teachers', [])},
        'classrooms': {e.id: getattr(e, 'number', str(e)) for e in entities.get('classrooms', [])},
    }
    
    resolved = []
    days_map = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    
    for slot in slots:
        # Безопасное получение имен с fallback на заглушку
        group_name = lookup['groups'].get(slot.group_id, "<Удалено>")
        subject_name = lookup['subjects'].get(slot.subject_id, "<Удалено>")
        teacher_name = lookup['teachers'].get(slot.teacher_id, "<Удалено>")
        classroom_num = lookup['classrooms'].get(slot.classroom_id, "<Удалено>")
        
        day_name = days_map[slot.day_of_week - 1] if 1 <= slot.day_of_week <= 7 else "???"
        time_str = f"{slot.start_time} - {slot.end_time}"
        
        resolved.append({
            'day': day_name,
            'time': time_str,
            'group': group_name,
            'subject': subject_name,
            'teacher': teacher_name,
            'classroom': classroom_num
        })
    
    return resolved


def print_schedule_table(resolved_slots: List[Dict[str, str]]) -> None:
    """
    Выводит отформатированную таблицу расписания в консоль.
    
    Args:
        resolved_slots: Список словарей, возвращенный resolve_schedule_slots().
    """
    if not resolved_slots:
        print("\nРасписание пусто.")
        return

    headers = ["День", "Время", "Группа", "Предмет", "Преподаватель", "Аудитория"]
    
    # Вычисляем максимальную ширину колонок динамически
    widths = [len(h) for h in headers]
    for row in resolved_slots:
        for i, key in enumerate(['day', 'time', 'group', 'subject', 'teacher', 'classroom']):
            widths[i] = max(widths[i], len(str(row[key])))
    
    # Формируем строку формата: "{:<width} | {:<width} ..."
    row_format = " | ".join(f"{{:<{w}}}" for w in widths)
    separator = "-+-".join("-" * w for w in widths)
    
    print("\n" + row_format.format(*headers))
    print(separator)
    
    for row in resolved_slots:
        print(row_format.format(
            row['day'],
            row['time'],
            row['group'],
            row['subject'],
            row['teacher'],
            row['classroom']
        ))
    print()