from models.db.reaction_msg import MessageReaction, SettingRole


def init_tables():
    tables = [
        MessageReaction(),
        SettingRole(),
    ]

    for table in tables:
        table.create_table()


if __name__ == '__main__':
    main()