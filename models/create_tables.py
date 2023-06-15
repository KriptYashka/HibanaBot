from models.db.role import ReactionRole
from models.db.category import CategoryRole, CategoryMessage


def init_tables():
    tables = [
        ReactionRole(),
        CategoryRole(),
        CategoryMessage(),
    ]

    for table in tables:
        table.create_table()


if __name__ == '__main__':
    init_tables()