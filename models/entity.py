from models.db.category import CategoryRole


class Category:
    def __init__(self,
                 obj_id: int = None,
                 guild_id: int = None,
                 title: str = None,
                 description: str = None,
                 mutually_exclusive: bool = None,
                 ):
        self.id = obj_id
        self.guild_id = guild_id
        self.title = title
        self.description = description
        self.mutually_exclusive = mutually_exclusive

    def check(self):
        pass


class Role:
    def __init__(self,
                 obj_id: int = None,
                 guild_id: int = None,
                 role_id: int = None,
                 category_id: int = None,
                 emoji: str = None,
                 ):
        self.id = obj_id
        self.guild_id = guild_id
        self.role_id = role_id
        self.category_id = category_id
        self.emoji = emoji


def main():
    c = Category(1)
    c["k"] = 5


if __name__ == '__main__':
    main()
