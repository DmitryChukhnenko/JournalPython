"""
Консольное приложение для управления расписанием.

Предоставляет пользовательский интерфейс для работы с сущностями:
группы, предметы, аудитории, преподаватели и расписание занятий.
"""

import os
import sys
from typing import List, Dict, Any, Optional, Callable

# Импорты из других модулей проекта
from core.schedule_manager import ScheduleManager
from models.group import Group
from models.subject import Subject
from models.teacher import Teacher
from models.classroom import Classroom


# ==================== Чистые функции ввода/вывода ====================

def input_int(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """
    Запрашивает у пользователя целое число с валидацией диапазона.
    
    Args:
        prompt: Текст запроса.
        min_val: Минимально допустимое значение (если есть).
        max_val: Максимально допустимое значение (если есть).
        
    Returns:
        Введенное пользователем целое число.
        
    Raises:
        KeyboardInterrupt: Если пользователь прервал ввод.
    """
    while True:
        try:
            value_str = input(prompt).strip()
            value = int(value_str)
            
            if min_val is not None and value < min_val:
                print(f"[ERROR] Значение должно быть не меньше {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"[ERROR] Значение должно быть не больше {max_val}.")
                continue
            
            return value
        except ValueError:
            print("[ERROR] Введите корректное целое число.")
        except KeyboardInterrupt:
            raise


def input_str(prompt: str, allow_empty: bool = False) -> str:
    """
    Запрашивает у пользователя строку.
    
    Args:
        prompt: Текст запроса.
        allow_empty: Разрешить ли пустую строку.
        
    Returns:
        Введенная строка (без ведущих/замыкающих пробелов).
        
    Raises:
        KeyboardInterrupt: Если пользователь прервал ввод.
    """
    while True:
        try:
            value = input(prompt).strip()
            
            if not value and not allow_empty:
                print("[ERROR] Строка не может быть пустой.")
                continue
            
            return value
        except KeyboardInterrupt:
            raise


def confirm_action(prompt: str) -> bool:
    """
    Запрашивает подтверждение действия у пользователя.
    
    Args:
        prompt: Текст запроса.
        
    Returns:
        True, если пользователь подтвердил (y/yes), иначе False.
    """
    while True:
        try:
            choice = input(f"{prompt} [y/n]: ").lower().strip()
            
            if choice in ('y', 'yes'):
                return True
            elif choice in ('n', 'no', ''):
                return False
            else:
                print("[ERROR] Введите 'y' для подтверждения или 'n' для отмены.")
        except KeyboardInterrupt:
            return False


def clear_screen() -> None:
    """Очищает экран консоли."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str, char: str = "=") -> None:
    """
    Выводит заголовок раздела.
    
    Args:
        title: Текст заголовка.
        char: Символ для рамок.
    """
    width = 60
    print("\n" + char * width)
    print(f"{title:^{width}}")
    print(char * width)


def print_table(headers: List[str], rows: List[List[Any]], col_widths: Optional[List[int]] = None) -> None:
    """
    Выводит данные в виде таблицы.
    
    Args:
        headers: Заголовки столбцов.
        rows: Строки данных.
        col_widths: Опциональная ширина столбцов.
    """
    if not headers:
        print("Нет данных для отображения.")
        return
    
    num_cols = len(headers)
    
    # Вычисляем ширину столбцов, если не передана
    if col_widths is None:
        col_widths = []
        for i in range(num_cols):
            max_len = len(str(headers[i]))
            for row in rows:
                if i < len(row):
                    max_len = max(max_len, len(str(row[i])))
            col_widths.append(min(max_len + 2, 30))  # Ограничиваем ширину
    
    # Формируем строку формата
    format_str = " | ".join(f"{{:<{w}}}" for w in col_widths)
    
    # Выводим заголовки
    print(format_str.format(*[str(h)[:col_widths[i]] for i, h in enumerate(headers)]))
    
    # Выводим разделитель
    separator = "-+-".join("-" * w for w in col_widths)
    print(separator)
    
    # Выводим строки
    if not rows:
        print("  (нет данных)")
        return
    
    for row in rows:
        # Дополняем строку пустыми значениями, если нужно
        padded_row = list(row) + [''] * (num_cols - len(row))
        print(format_str.format(*[str(padded_row[i])[:col_widths[i]] for i in range(num_cols)]))


# ==================== Класс приложения ====================

class ConsoleApp:
    """
    Консольное приложение для управления расписанием.
    
    Предоставляет меню для CRUD операций над сущностями
    и управления расписанием занятий.
    
    Attributes:
        _manager: Менеджер расписания для бизнес-операций.
    """
    
    DAYS_OF_WEEK = ["", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    
    def __init__(self, manager: ScheduleManager):
        """
        Инициализирует приложение.
        
        Args:
            manager: Экземпляр ScheduleManager для выполнения операций.
        """
        self._manager = manager
    
    @property
    def manager(self) -> ScheduleManager:
        """Возвращает менеджер расписания."""
        return self._manager
    
    def run(self) -> None:
        """
        Запускает главный цикл приложения.
        
        Цикл продолжается до выбора пользователем опции выхода.
        """
        while True:
            try:
                clear_screen()
                print_header(" Система управления расписанием")
                
                print("\n[1] Группы")
                print("[2] Предметы")
                print("[3] Аудитории")
                print("[4] Преподаватели")
                print("[5] Расписание")
                print("[0] Выход")
                
                choice = input_int("\nВыберите действие: ", 0, 5)
                
                if choice == 0:
                    print("\n[OK] До свидания!")
                    break
                elif choice == 1:
                    self._menu_groups()
                elif choice == 2:
                    self._menu_subjects()
                elif choice == 3:
                    self._menu_classrooms()
                elif choice == 4:
                    self._menu_teachers()
                elif choice == 5:
                    self._menu_schedule()
                    
            except KeyboardInterrupt:
                print("\n\n[WARNING] Прервано пользователем.")
                break
    
    # ==================== Меню групп ====================
    
    def _menu_groups(self) -> None:
        """Подменю управления группами."""
        while True:
            print_header(" Управление группами")
            
            print("\n[1] + Добавить группу")
            print("[2] - Удалить группу")
            print("[3] [VIEW]  Показать все группы")
            print("[0] [BACK]  Назад")
            
            choice = input_int("\nВыберите действие: ", 0, 3)
            
            if choice == 0:
                break
            elif choice == 1:
                self._add_group()
            elif choice == 2:
                self._delete_group()
            elif choice == 3:
                self._view_groups()
    
    def _add_group(self) -> None:
        """Добавляет новую группу."""
        print_header("+ Добавить группу")
        
        name = input_str("Название группы: ")
        size = input_int("Количество студентов: ", min_val=1)
        curator = input_str("Куратор (ФИО): ", allow_empty=True)
        
        try:
            group = self._manager.add_group(name=name, size=size, curator=curator)
            print(f"\n[OK] Группа '{name}' успешно добавлена (ID: {group.id[:8]}).")
        except ValueError as e:
            print(f"\n[ERROR] Ошибка: {e}")
        
        input("\nНажмите Enter для продолжения...")
    
    def _delete_group(self) -> None:
        """Удаляет группу по ID."""
        groups = self._manager.get_all_groups()
        slots = self._manager.get_all()
        
        if not groups:
            print("\n[WARNING] Нет групп для удаления.")
            input("\nНажмите Enter для продолжения...")
            return
        
        self._view_groups()
        
        group_id = input_str("\nВведите ID группы для удаления: ")
        
        # Поиск группы по ID
        group = next((g for g in groups if g.id[:8] == group_id), None)
        
        if not group:
            print(f"\n[ERROR] Группа с ID '{group_id}' не найдена.")
        elif (any(slot.group_id == group.id for slot in slots)):
            print(f"\n[ERROR] Группа '{group.name}' не может быть удалена, так как она используется в расписании.")
        elif confirm_action(f"Удалить группу '{group.name}'?"):
            try:
                if self._manager.remove_group(group_id):
                    print(f"\n[OK] Группа '{group.name}' удалена.")
                else:
                    print("\n[ERROR] Не удалось удалить группу.")
            except ValueError as e:
                print(f"\n[ERROR] Ошибка: {e}")
        
        input("\nНажмите Enter для продолжения...")
    
    def _view_groups(self) -> None:
        """Показывает список всех групп."""
        groups = self._manager.get_all_groups()
        
        print_header(" Список групп")
        
        if not groups:
            print("\n  (нет групп)")
        else:
            headers = ["ID", "Название", "Студентов", "Куратор"]
            rows = [[g.id[:8], g.name, g.size, g.curator or "-"] for g in groups]
            print_table(headers, rows)
        
        print()
    
    # ==================== Меню предметов ====================
    
    def _menu_subjects(self) -> None:
        """Подменю управления предметами."""
        while True:
            print_header(" Управление предметами")
            
            print("\n[1] + Добавить предмет")
            print("[2] - Удалить предмет")
            print("[3] [VIEW]  Показать все предметы")
            print("[0] [BACK]  Назад")
            
            choice = input_int("\nВыберите действие: ", 0, 3)
            
            if choice == 0:
                break
            elif choice == 1:
                self._add_subject()
            elif choice == 2:
                self._delete_subject()
            elif choice == 3:
                self._view_subjects()
    
    def _add_subject(self) -> None:
        """Добавляет новый предмет."""
        print_header("+ Добавить предмет")
        
        name = input_str("Название предмета: ")
        code = input_str("Код предмета (например, MATH101): ", allow_empty=True)
        hours = input_int("Общее количество часов: ", min_val=1)
        
        try:
            subject = self._manager.add_subject(name=name, code=code, hours=hours)
            print(f"\n[OK] Предмет '{name}' успешно добавлен (ID: {subject.id[:8]}).")
        except ValueError as e:
            print(f"\n[ERROR] Ошибка: {e}")
        
        input("\nНажмите Enter для продолжения...")
    
    def _delete_subject(self) -> None:
        """Удаляет предмет по ID."""
        subjects = self._manager.get_all_subjects()
        slots = self._manager.get_all()
        
        if not subjects:
            print("\n[WARNING] Нет предметов для удаления.")
            input("\nНажмите Enter для продолжения...")
            return
        
        self._view_subjects()
        
        subject_id = input_str("\nВведите ID предмета для удаления: ")
        
        subject = next((s for s in subjects if s.id[:8] == subject_id), None)
        
        if not subject:
            print(f"\n[ERROR] Предмет с ID '{subject_id}' не найден.")
        elif (any(slot.subject_id == subject.id for slot in slots)):
            print(f"\n[ERROR] Предмет '{subject.name}' не может быть удален, так как он используется в расписании.")
        elif confirm_action(f"Удалить предмет '{subject.name}'?"):
            try:
                if self._manager.remove_subject(subject_id):
                    print(f"\n[OK] Предмет '{subject.name}' удален.")
                else:
                    print("\n[ERROR] Не удалось удалить предмет.")
            except ValueError as e:
                print(f"\n[ERROR] Ошибка: {e}")
        
        input("\nНажмите Enter для продолжения...")
    
    def _view_subjects(self) -> None:
        """Показывает список всех предметов."""
        subjects = self._manager.get_all_subjects()
        
        print_header(" Список предметов")
        
        if not subjects:
            print("\n  (нет предметов)")
        else:
            headers = ["ID", "Название", "Код", "Часов"]
            rows = [[s.id[:8], s.name, s.code or "-", s.hours] for s in subjects]
            print_table(headers, rows)
        
        print()
    
    # ==================== Меню аудиторий ====================
    
    def _menu_classrooms(self) -> None:
        """Подменю управления аудиториями."""
        while True:
            print_header(" Управление аудиториями")
            
            print("\n[1] + Добавить аудиторию")
            print("[2] - Удалить аудиторию")
            print("[3] [VIEW]  Показать все аудитории")
            print("[0] [BACK]  Назад")
            
            choice = input_int("\nВыберите действие: ", 0, 3)
            
            if choice == 0:
                break
            elif choice == 1:
                self._add_classroom()
            elif choice == 2:
                self._delete_classroom()
            elif choice == 3:
                self._view_classrooms()
    
    def _add_classroom(self) -> None:
        """Добавляет новую аудиторию."""
        print_header("+ Добавить аудиторию")
        
        number = input_str("Номер аудитории: ")
        building = input_str("Корпус: ", allow_empty=True)
        capacity = input_int("Вместимость (чел.): ", min_val=1)
        
        try:
            classroom = self._manager.add_classroom(number=number, building=building, capacity=capacity)
            print(f"\n[OK] Аудитория '{number}' успешно добавлена (ID: {classroom.id[:8]}).")
        except ValueError as e:
            print(f"\n[ERROR] Ошибка: {e}")
        
        input("\nНажмите Enter для продолжения...")
    
    def _delete_classroom(self) -> None:
        """Удаляет аудиторию по ID."""
        classrooms = self._manager.get_all_classrooms()
        slots = self._manager.get_all()
        
        if not classrooms:
            print("\n[WARNING] Нет аудиторий для удаления.")
            input("\nНажмите Enter для продолжения...")
            return
        
        self._view_classrooms()
        
        classroom_id = input_str("\nВведите ID аудитории для удаления: ")
        
        classroom = next((c for c in classrooms if c.id[:8] == classroom_id), None)
        
        if not classroom:
            print(f"\n[ERROR] Аудитория с ID '{classroom_id}' не найдена.")        
        elif (any(slot.classroom_id == classroom_id.id for slot in slots)):
            print(f"\n[ERROR] Аудитория '{classroom.name}' не может быть удалена, так как она используется в расписании.")
        elif confirm_action(f"Удалить аудиторию '{classroom.number}'?"):
            try:
                if self._manager.remove_classroom(classroom_id):
                    print(f"\n[OK] Аудитория '{classroom.number}' удалена.")
                else:
                    print("\n[ERROR] Не удалось удалить аудиторию.")
            except ValueError as e:
                print(f"\n[ERROR] Ошибка: {e}")
        
        input("\nНажмите Enter для продолжения...")
    
    def _view_classrooms(self) -> None:
        """Показывает список всех аудиторий."""
        classrooms = self._manager.get_all_classrooms()
        
        print_header(" Список аудиторий")
        
        if not classrooms:
            print("\n  (нет аудиторий)")
        else:
            headers = ["ID", "Номер", "Корпус", "Вместимость"]
            rows = [[c.id[:8], c.number, c.building or "-", c.capacity] for c in classrooms]
            print_table(headers, rows)
        
        print()
    
    # ==================== Меню преподавателей ====================
    
    def _menu_teachers(self) -> None:
        """Подменю управления преподавателями."""
        while True:
            print_header(" Управление преподавателями")
            
            print("\n[1] + Добавить преподавателя")
            print("[2] - Удалить преподавателя")
            print("[3] [VIEW]  Показать всех преподавателей")
            print("[0] [BACK]  Назад")
            
            choice = input_int("\nВыберите действие: ", 0, 3)
            
            if choice == 0:
                break
            elif choice == 1:
                self._add_teacher()
            elif choice == 2:
                self._delete_teacher()
            elif choice == 3:
                self._view_teachers()
    
    def _add_teacher(self) -> None:
        """Добавляет нового преподавателя."""
        print_header("+ Добавить преподавателя")
        
        name = input_str("ФИО преподавателя: ")
        email = input_str("Email: ", allow_empty=True)
        department = input_str("Кафедра: ", allow_empty=True)
        
        try:
            teacher = self._manager.add_teacher(name=name, email=email, department=department)
            print(f"\n[OK] Преподаватель '{name}' успешно добавлен (ID: {teacher.id[:8]}).")
        except ValueError as e:
            print(f"\n[ERROR] Ошибка: {e}")
        
        input("\nНажмите Enter для продолжения...")
    
    def _delete_teacher(self) -> None:
        """Удаляет преподавателя по ID."""
        teachers = self._manager.get_all_teachers()
        slots = self._manager.get_all()
        
        if not teachers:
            print("\n[WARNING] Нет преподавателей для удаления.")
            input("\nНажмите Enter для продолжения...")
            return
        
        self._view_teachers()
        
        teacher_id = input_str("\nВведите ID преподавателя для удаления: ")
        
        teacher = next((t for t in teachers if t.id[:8] == teacher_id), None)
        
        if not teacher:
            print(f"\n[ERROR] Преподаватель с ID '{teacher_id}' не найден.")
        elif (any(slot.teacher_id == teacher.id for slot in slots)):
            print(f"\n[ERROR] Преподаватель '{teacher.name}' не может быть удален, так как он используется в расписании.")        
        elif confirm_action(f"Удалить преподавателя '{teacher.name}'?"):
            try:
                if self._manager.remove_teacher(teacher_id):
                    print(f"\n[OK] Преподаватель '{teacher.name}' удален.")
                else:
                    print("\n[ERROR] Не удалось удалить преподавателя.")
            except ValueError as e:
                print(f"\n[ERROR] Ошибка: {e}")
        
        input("\nНажмите Enter для продолжения...")
    
    def _view_teachers(self) -> None:
        """Показывает список всех преподавателей."""
        teachers = self._manager.get_all_teachers()
        
        print_header(" Список преподавателей")
        
        if not teachers:
            print("\n  (нет преподавателей)")
        else:
            headers = ["ID", "ФИО", "Email", "Кафедра"]
            rows = [[t.id[:8], t.name, t.email or "-", t.department or "-"] for t in teachers]
            print_table(headers, rows)
        
        print()
    
    # ==================== Меню расписания ====================
    
    def _menu_schedule(self) -> None:
        """Подменю управления расписанием."""
        while True:
            print_header(" Управление расписанием")
            
            print("\n[1] + Добавить занятие")
            print("[2] - Удалить занятие")
            print("[3] [VIEW]  Показать расписание")
            print("[4] [WARNING]  Проверить конфликты")
            print("[0] [BACK]  Назад")
            
            choice = input_int("\nВыберите действие: ", 0, 4)
            
            if choice == 0:
                break
            elif choice == 1:
                self._add_lesson()
            elif choice == 2:
                self._delete_lesson()
            elif choice == 3:
                self._show_schedule()
            elif choice == 4:
                self._check_conflicts()
    
    def _add_lesson(self) -> None:
        """Добавляет новое занятие."""
        print_header("+ Добавить занятие")
        
        # Проверяем наличие необходимых сущностей
        groups = self._manager.get_all_groups()
        subjects = self._manager.get_all_subjects()
        teachers = self._manager.get_all_teachers()
        classrooms = self._manager.get_all_classrooms()
        
        if not groups:
            print("\n[ERROR] Сначала добавьте хотя бы одну группу.")
            input("\nНажмите Enter для продолжения...")
            return
        if not subjects:
            print("\n[ERROR] Сначала добавьте хотя бы один предмет.")
            input("\nНажмите Enter для продолжения...")
            return
        if not teachers:
            print("\n[ERROR] Сначала добавьте хотя бы одного преподавателя.")
            input("\nНажмите Enter для продолжения...")
            return
        if not classrooms:
            print("\n[ERROR] Сначала добавьте хотя бы одну аудиторию.")
            input("\nНажмите Enter для продолжения...")
            return
        
        # Выбор группы
        print("\n--- Выберите группу ---")
        self._list_entities_short(groups, "Группы")
        group_id = self._select_entity_id(groups, "ID группы: ")
        if not group_id:
            return
        
        # Выбор предмета
        print("\n--- Выберите предмет ---")
        self._list_entities_short(subjects, "Предметы")
        subject_id = self._select_entity_id(subjects, "ID предмета: ")
        if not subject_id:
            return
        
        # Выбор преподавателя
        print("\n--- Выберите преподавателя ---")
        self._list_entities_short(teachers, "Преподаватели")
        teacher_id = self._select_entity_id(teachers, "ID преподавателя: ")
        if not teacher_id:
            return
        
        # Выбор аудитории
        print("\n--- Выберите аудиторию ---")
        self._list_entities_short(classrooms, "Аудитории")
        classroom_id = self._select_entity_id(classrooms, "ID аудитории: ")
        if not classroom_id:
            return
        
        # Выбор дня недели
        print("\n--- День недели ---")
        for i, day in enumerate(self.DAYS_OF_WEEK[1:], 1):
            print(f"  [{i}] {day}")
        day_of_week = input_int("День недели (1-7): ", 1, 7)
        
        # Время начала и окончания
        start_time = input_str("Время начала (HH:MM, например 09:00): ")
        end_time = input_str("Время окончания (HH:MM, например 10:30): ")
        
        try:
            slot = self._manager.add_slot(
                subject_id=subject_id,
                group_id=group_id,
                teacher_id=teacher_id,
                classroom_id=classroom_id,
                day_of_week=day_of_week,
                start_time=start_time,
                end_time=end_time
            )
            print(f"\n[OK] Занятие успешно добавлено (ID: {slot.id[:8]}).")
        except ValueError as e:
            print(f"\n[ERROR] Ошибка: {e}")
        
        input("\nНажмите Enter для продолжения...")
    
    def _delete_lesson(self) -> None:
        """Удаляет занятие по ID."""
        slots = self._manager.get_all()
        
        if not slots:
            print("\n[WARNING] Нет занятий для удаления.")
            input("\nНажмите Enter для продолжения...")
            return
        
        self._print_schedule(slots)
        
        slot_id = input_str("\nВведите ID занятия для удаления: ")
        
        slot = self._manager.get_slot_by_id(slot_id)
        
        if not slot:
            print(f"\n[ERROR] Занятие с ID '{slot_id}' не найдено.")
        elif confirm_action("Удалить это занятие?"):
            if self._manager.remove_slot(slot_id):
                print("\n[OK] Занятие удалено.")
            else:
                print("\n[ERROR] Не удалось удалить занятие.")
        
        input("\nНажмите Enter для продолжения...")
    
    def _show_schedule(self) -> None:
        """Показывает расписание с фильтрацией."""
        print_header("[VIEW]  Просмотр расписания")
        
        print("\n[1] По группе")
        print("[2] По преподавателю")
        print("[3] По аудитории")
        print("[4] Все занятия")
        
        choice = input_int("\nВыберите фильтр: ", 1, 4)
        
        slots = []
        
        if choice == 1:
            groups = self._manager.get_all_groups()
            if not groups:
                print("\n[WARNING] Нет групп.")
                input("\nНажмите Enter для продолжения...")
                return
            self._list_entities_short(groups, "Группы")
            group_id = self._select_entity_id(groups, "ID группы: ")
            if group_id:
                slots = self._manager.get_by_group(group_id)
        
        elif choice == 2:
            teachers = self._manager.get_all_teachers()
            if not teachers:
                print("\n[WARNING] Нет преподавателей.")
                input("\nНажмите Enter для продолжения...")
                return
            self._list_entities_short(teachers, "Преподаватели")
            teacher_id = self._select_entity_id(teachers, "ID преподавателя: ")
            if teacher_id:
                slots = self._manager.get_by_teacher(teacher_id)
        
        elif choice == 3:
            classrooms = self._manager.get_all_classrooms()
            if not classrooms:
                print("\n[WARNING] Нет аудиторий.")
                input("\nНажмите Enter для продолжения...")
                return
            self._list_entities_short(classrooms, "Аудитории")
            classroom_id = self._select_entity_id(classrooms, "ID аудитории: ")
            if classroom_id:
                slots = self._manager.get_by_classroom(classroom_id)
        
        elif choice == 4:
            slots = self._manager.get_all()
        
        if slots:
            self._print_schedule(slots)
        else:
            print("\n  (нет занятий по выбранному фильтру)")
        
        input("\nНажмите Enter для продолжения...")
    
    def _check_conflicts(self) -> None:
        """Проверяет расписание на конфликты."""
        print_header("[WARNING]  Проверка конфликтов")
        
        conflicts = self._manager.check_conflicts()
        
        if conflicts:
            print(f"\n[ERROR] Обнаружено конфликтов: {len(conflicts)}\n")
            for i, conflict in enumerate(conflicts, 1):
                print(f"  {i}. {conflict}")
        else:
            print("\n[OK] Конфликтов не обнаружено. Расписание корректно.")
        
        input("\nНажмите Enter для продолжения...")
    
    # ==================== Вспомогательные методы ====================
    
    def _list_entities_short(self, entities: List[Any], title: str) -> None:
        """Выводит краткий список сущностей."""
        print(f"\n{title}:")
        for entity in entities:
            name_attr = getattr(entity, 'name', None) or \
                       getattr(entity, 'number', None) or \
                       str(entity)
            print(f"  - {entity.id[:8]}: {name_attr}")
    
    def _select_entity_id(self, entities: List[Any], prompt: str) -> Optional[str]:
        """Запрашивает выбор ID сущности из списка."""
        while True:
            entity_id = input_str(prompt).strip()
            
            # Поддержка сокращенного ID (первые 8 символов)
            if len(entity_id) <= 8:
                for entity in entities:
                    if entity.id.startswith(entity_id):
                        return entity.id
            
            # Полный поиск
            for entity in entities:
                if entity.id == entity_id:
                    return entity.id
            
            print("[ERROR] Сущность с таким ID не найдена. Попробуйте снова.")
    
    def _print_schedule(self, slots: List[Any]) -> None:
        """Выводит расписание в виде таблицы."""
        print_header(" Расписание")
        
        if not slots:
            print("\n  (нет занятий)")
            return
        
        # Сортировка по дню и времени
        sorted_slots = sorted(slots, key=lambda s: (s.day_of_week, s.start_time))
        
        headers = ["ID", "День", "Время", "Группа", "Предмет", "Преподаватель", "Аудитория"]
        rows = []

        for slot in sorted_slots:
            # Получаем имена сущностей через менеджер
            group = self._manager.get_group_by_id(slot.group_id)
            subject = self._manager.get_subject_by_id(slot.subject_id)
            teacher = self._manager.get_teacher_by_id(slot.teacher_id)
            classroom = self._manager.get_classroom_by_id(slot.classroom_id)

            day_name = self.DAYS_OF_WEEK[slot.day_of_week] if 1 <= slot.day_of_week <= 7 else "?"

            rows.append([
                slot.id[:8],
                day_name,
                f"{slot.start_time}-{slot.end_time}",
                group.name if group else slot.group_id[:8],
                subject.name if subject else slot.subject_id[:8],
                teacher.name if teacher else slot.teacher_id[:8],
                classroom.number if classroom else slot.classroom_id[:8]
            ])

        print_table(headers, rows)
        print()
