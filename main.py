#!/usr/bin/env python3
"""
Точка входа в приложение University Schedule.

Инициализирует репозиторий, менеджер расписания и запускает консольный интерфейс.
Обеспечивает корректное сохранение данных при завершении работы.
"""

import sys
import os
from pathlib import Path

# Добавляем корень проекта в path для корректного импорта модулей
# Это позволяет запускать скрипт из любой директории
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from repository.json_repo import ScheduleRepository
from core.schedule_manager import ScheduleManager
from ui.console_app import ConsoleApp

# Константы
DATA_DIR = "data"
DATA_FILE = "schedule.json"


def main() -> None:
    """
    Основная функция запуска приложения.
    
    Инициализирует компоненты, обрабатывает прерывания и сохраняет данные при выходе.
    """
    repo = None
    app = None
    
    try:
        # 1. Инициализация репозитория
        # Создаем полный путь к файлу данных
        data_path = project_root / DATA_DIR / DATA_FILE
        
        # Репозиторий автоматически создаст папку и файл при необходимости
        repo = ScheduleRepository(str(data_path))
        
        # 2. Загрузка данных
        # Если файл пуст или отсутствует, load_data() вернет структуру с пустыми списками
        raw_data = repo.load_data()
        
        # 3. Инициализация менеджера расписания
        # Менеджер принимает начальные данные и репозиторий для сохранения
        manager = ScheduleManager(initial_data=raw_data, repository=repo)
        
        # 4. Создание и запуск UI
        app = ConsoleApp(manager=manager)
        
        print("Запуск системы управления расписанием...")
        app.run()
        
    except KeyboardInterrupt:
        print("\n\nПолучен сигнал прерывания (Ctrl+C). Завершение работы...")
    except Exception as e:
        print(f"\n[ERROR] Произошла непредвиденная ошибка: {e}")
        print("Подробности могут быть в логах (если настроены) или выше.")
        return 1                
    return 0


if __name__ == "__main__":
    sys.exit(main())