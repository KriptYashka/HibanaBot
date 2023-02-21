from models.db.role import ReactionRole
from models.db.category import CategoryRole


def init_tables():
    tables = [
        ReactionRole(),
        CategoryRole(),
    ]

    for table in tables:
        table.create_table()


if __name__ == '__main__':
    init_tables()