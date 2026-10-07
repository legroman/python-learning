import logging

from app.database import create_tasks_table, create_categories_table
from app.task_manager import main

logging.basicConfig(level=logging.INFO)

create_categories_table()
create_tasks_table()


if __name__ == "__main__":
    main()
