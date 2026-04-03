"""
Менеджер расписания (ScheduleManager).

Управляет коллекцией занятий, обеспечивает CRUD операции,
проверку конфликтов и взаимодействие с репозиторием.
"""

from typing import List, Dict, Any, Optional
from copy import deepcopy

from core.schedule_slot import ScheduleSlot
from core.validators import detect_schedule_conflicts
from repository.json_repo import ScheduleRepository
from models.group import Group
from models.subject import Subject
from models.teacher import Teacher
from models.classroom import Classroom


class ScheduleManager:
    """
    Класс для управления расписанием занятий и сущностями.
    
    Хранит список занятий и сущностей в памяти, обеспечивает добавление, удаление,
    поиск и проверку конфликтов. Использует репозиторий для сохранения
    и загрузки данных.
    
    Attributes:
        _slots: Приватный список занятий.
        _groups: Приватный список групп.
        _subjects: Приватный список предметов.
        _teachers: Приватный список преподавателей.
        _classrooms: Приватный список аудиторий.
        _repository: Ссылка на репозиторий для сохранения данных.
    """
    
    def __init__(
        self,
        initial_data: Optional[Dict[str, Any]] = None,
        repository: Optional[ScheduleRepository] = None
    ):
        """
        Инициализирует менеджер расписания.
        
        Args:
            initial_data: Начальные данные из репозитория.
            repository: Экземпляр репозитория для сохранения данных.
        """
        self._slots: List[ScheduleSlot] = []
        self._groups: List[Group] = []
        self._subjects: List[Subject] = []
        self._teachers: List[Teacher] = []
        self._classrooms: List[Classroom] = []
        self._repository: Optional[ScheduleRepository] = repository
        
        # Загрузка начальных данных
        if initial_data:
            self._load_from_data(initial_data)
    
    def _load_from_data(self, data: Dict[str, Any]) -> None:
        """Загружает данные из словаря."""
        # Загрузка групп
        for item in data.get('groups', []):
            try:
                self._groups.append(Group.from_dict(item))
            except (KeyError, ValueError):
                pass
        
        # Загрузка предметов
        for item in data.get('subjects', []):
            try:
                self._subjects.append(Subject.from_dict(item))
            except (KeyError, ValueError):
                pass
        
        # Загрузка преподавателей
        for item in data.get('teachers', []):
            try:
                self._teachers.append(Teacher.from_dict(item))
            except (KeyError, ValueError):
                pass
        
        # Загрузка аудиторий
        for item in data.get('classrooms', []):
            try:
                self._classrooms.append(Classroom.from_dict(item))
            except (KeyError, ValueError):
                pass
        
        # Загрузка расписания
        for item in data.get('schedule', []):
            try:
                self._slots.append(ScheduleSlot.from_dict(item))
            except (KeyError, ValueError):
                pass
    
    def _save_all(self) -> None:
        """Сохраняет все данные в репозиторий."""
        if self._repository is None:
            return
        
        all_data = {
            'groups': [g.to_dict() for g in self._groups],
            'subjects': [s.to_dict() for s in self._subjects],
            'teachers': [t.to_dict() for t in self._teachers],
            'classrooms': [c.to_dict() for c in self._classrooms],
            'schedule': [slot.to_dict() for slot in self._slots]
        }
        self._repository.save_data(all_data)
    
    # ==================== Public Methods ====================
    
    def add_slot(
        self,
        subject_id: str,
        group_id: str,
        teacher_id: str,
        classroom_id: str,
        day_of_week: int,
        start_time: str,
        end_time: str
    ) -> ScheduleSlot:
        """
        Добавляет новое занятие в расписание.
        
        Перед добавлением проверяет наличие конфликтов с существующими занятиями.
        При обнаружении конфликтов выбрасывает ValueError.
        
        Args:
            subject_id: ID предмета.
            group_id: ID группы.
            teacher_id: ID преподавателя.
            classroom_id: ID аудитории.
            day_of_week: День недели (1-7).
            start_time: Время начала (HH:MM).
            end_time: Время окончания (HH:MM).
            
        Returns:
            Созданное занятие.
            
        Raises:
            ValueError: Если обнаружены конфликты расписания.
        """
        # Создаем новый слот для проверки конфликтов
        new_slot_dict = {
            'subject_id': subject_id,
            'group_id': group_id,
            'teacher_id': teacher_id,
            'classroom_id': classroom_id,
            'day_of_week': day_of_week,
            'start_time': start_time,
            'end_time': end_time
        }
        
        # Получаем существующие слоты как словари для проверки конфликтов
        existing_slots_dicts = [slot.to_dict() for slot in self._slots]
        
        # Проверка конфликтов через чистую функцию
        conflicts = detect_schedule_conflicts(new_slot_dict, existing_slots_dicts)
        
        if conflicts:
            error_message = "Обнаружены конфликты расписания:\n" + "\n".join(f"  - {c}" for c in conflicts)
            raise ValueError(error_message)
        
        # Если конфликтов нет, создаем и добавляем слот
        new_slot = ScheduleSlot(
            subject_id=subject_id,
            group_id=group_id,
            teacher_id=teacher_id,
            classroom_id=classroom_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time
        )
        
        self._slots.append(new_slot)        
        self._save_all()
        return new_slot
    
    def remove_slot(self, slot_id: str) -> bool:
        """
        Удаляет занятие по ID.
        
        Args:
            slot_id: ID занятия для удаления.
            
        Returns:
            True, если занятие удалено, False если не найдено.
        """
        for i, slot in enumerate(self._slots):
            if slot.id[:8] == slot_id:
                del self._slots[i]
                self._save_all()
                return True
        return False
    
    def get_by_teacher(self, teacher_id: str) -> List[ScheduleSlot]:
        """
        Возвращает все занятия преподавателя.
        
        Args:
            teacher_id: ID преподавателя.
            
        Returns:
            Список занятий преподавателя.
        """
        return [slot for slot in self._slots if slot.teacher_id == teacher_id]
    
    def get_by_group(self, group_id: str) -> List[ScheduleSlot]:
        """
        Возвращает все занятия группы.
        
        Args:
            group_id: ID группы.
            
        Returns:
            Список занятий группы.
        """
        return [slot for slot in self._slots if slot.group_id == group_id]
    
    def get_by_classroom(self, classroom_id: str) -> List[ScheduleSlot]:
        """
        Возвращает все занятия в аудитории.
        
        Args:
            classroom_id: ID аудитории.
            
        Returns:
            Список занятий в аудитории.
        """
        return [slot for slot in self._slots if slot.classroom_id == classroom_id]
    
    def get_all(self) -> List[ScheduleSlot]:
        """
        Возвращает все занятия.
        
        Returns:
            Копия списка всех занятий.
        """
        return deepcopy(self._slots)
    
   
    def check_conflicts(self) -> List[str]:
        """
        Проверяет все занятия на наличие конфликтов между собой.
        
        Полезно для проверки целостности расписания после загрузки
        или ручного редактирования.
        
        Returns:
            Список строк с описанием конфликтов.
        """
        all_conflicts = []
        slots_dicts = [slot.to_dict() for slot in self._slots]
        
        # Проверяем каждое занятие против всех остальных
        for i, slot in enumerate(slots_dicts):
            # Создаем список всех остальных слотов
            others = slots_dicts[:i] + slots_dicts[i+1:]
            conflicts = detect_schedule_conflicts(slot, others)
            all_conflicts.extend(conflicts)
        
        # Убираем дубликаты (каждый конфликт обнаруживается дважды)
        unique_conflicts = list(set(all_conflicts))
        return unique_conflicts
    
    def get_slot_by_id(self, slot_id: str) -> Optional[ScheduleSlot]:
        """
        Возвращает занятие по ID.
        
        Args:
            slot_id: ID занятия.
            
        Returns:
            Занятие или None, если не найдено.
        """
        for slot in self._slots:
            if slot.id[:8] == slot_id:
                return slot
        return None
    
    @property
    def slots_count(self) -> int:
        """Возвращает количество занятий."""
        return len(self._slots)
    
    # ==================== Group Methods ====================
    
    def add_group(self, name: str, size: int, curator: str = "") -> Group:
        """Добавляет новую группу."""
        group = Group(name=name, size=size, curator=curator)
        self._groups.append(group)
        self._save_all()
        return group
    
    def get_all_groups(self) -> List[Group]:
        """Возвращает все группы."""
        return deepcopy(self._groups)
    
    def remove_group(self, group_id: str) -> bool:
        """Удаляет группу по ID."""
        for i, g in enumerate(self._groups):
            if g.id[:8] == group_id:
                del self._groups[i]
                self._save_all()
                return True
        return False
    
    # ==================== Subject Methods ====================
    
    def add_subject(self, name: str, code: str = "", hours: int = 0) -> Subject:
        """Добавляет новый предмет."""
        subject = Subject(name=name, code=code, hours=hours)
        self._subjects.append(subject)
        self._save_all()
        return subject
    
    def get_all_subjects(self) -> List[Subject]:
        """Возвращает все предметы."""
        return deepcopy(self._subjects)
    
    def remove_subject(self, subject_id: str) -> bool:
        """Удаляет предмет по ID."""
        for i, s in enumerate(self._subjects):
            if s.id[:8] == subject_id:
                del self._subjects[i]
                self._save_all()
                return True
        return False
    
    # ==================== Teacher Methods ====================
    
    def add_teacher(self, name: str, email: str = "", department: str = "") -> Teacher:
        """Добавляет нового преподавателя."""
        teacher = Teacher(name=name, email=email, department=department)
        self._teachers.append(teacher)
        self._save_all()
        return teacher
    
    def get_all_teachers(self) -> List[Teacher]:
        """Возвращает всех преподавателей."""
        return deepcopy(self._teachers)
    
    def remove_teacher(self, teacher_id: str) -> bool:
        """Удаляет преподавателя по ID."""
        for i, t in enumerate(self._teachers):
            if t.id[:8] == teacher_id:
                del self._teachers[i]
                self._save_all()
                return True
        return False
    
    # ==================== Classroom Methods ====================
    
    def add_classroom(self, number: str, building: str = "", capacity: int = 0) -> Classroom:
        """Добавляет новую аудиторию."""
        classroom = Classroom(number=number, building=building, capacity=capacity)
        self._classrooms.append(classroom)
        self._save_all()
        return classroom
    
    def get_all_classrooms(self) -> List[Classroom]:
        """Возвращает все аудитории."""
        return deepcopy(self._classrooms)
    
    def remove_classroom(self, classroom_id: str) -> bool:
        """Удаляет аудиторию по ID."""
        for i, c in enumerate(self._classrooms):
            if c.id[:8] == classroom_id:
                del self._classrooms[i]
                self._save_all()
                return True
        return False
    
    # ==================== Lesson/Slot Methods ====================
    
    def get_all_lessons(self) -> List[ScheduleSlot]:
        """Возвращает все занятия (алиас для get_all)."""
        return self.get_all()
    
    def get_lessons_by_group(self, group_id: str) -> List[ScheduleSlot]:
        """Возвращает занятия группы (алиас для get_by_group)."""
        return self.get_by_group(group_id)
    
    def get_lessons_by_teacher(self, teacher_id: str) -> List[ScheduleSlot]:
        """Возвращает занятия преподавателя (алиас для get_by_teacher)."""
        return self.get_by_teacher(teacher_id)
    
    def get_lessons_by_classroom(self, classroom_id: str) -> List[ScheduleSlot]:
        """Возвращает занятия в аудитории (алиас для get_by_classroom)."""
        return self.get_by_classroom(classroom_id)
    
    def get_group_by_id(self, group_id: str) -> Optional[Group]:
        """Возвращает группу по ID."""
        for g in self._groups:
            if g.id == group_id:
                return g
        return None
    
    def get_subject_by_id(self, subject_id: str) -> Optional[Subject]:
        """Возвращает предмет по ID."""
        for s in self._subjects:
            if s.id == subject_id:
                return s
        return None
    
    def get_teacher_by_id(self, teacher_id: str) -> Optional[Teacher]:
        """Возвращает преподавателя по ID."""
        for t in self._teachers:
            if t.id == teacher_id:
                return t
        return None
    
    def get_classroom_by_id(self, classroom_id: str) -> Optional[Classroom]:
        """Возвращает аудиторию по ID."""
        for c in self._classrooms:
            if c.id == classroom_id:
                return c
        return None
    
    def delete_lesson(self, lesson_id: str) -> bool:
        """Удаляет занятие по ID (алиас для remove_slot)."""
        return self.remove_slot(lesson_id)
    
    def check_schedule_conflicts(self) -> List[str]:
        """Проверяет конфликты расписания (алиас для check_conflicts)."""
        return self.check_conflicts()
