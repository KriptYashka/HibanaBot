from models.db.roles import ReactionRole, CategoryRole


def init_tables():
    tables = [
        ReactionRole(),
        CategoryRole(),
    ]

    for table in tables:
        table.create_table()


if __name__ == '__main__':
    init_tables()