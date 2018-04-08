import sys

from peewee import BooleanField, CharField, IntegerField, Model, SqliteDatabase

db = SqliteDatabase('brain.sqlite')


class User(Model):
    id = IntegerField()
    admin = BooleanField(default=False)
    name = CharField()
    langpair = CharField(default="__|__")

    class Meta:
        database = db


def get_user(user_id):
    try:
        user = User.get(User.id == user_id)
    except User.DoesNotExist:
        user = User.get(User.id == 0)
    return user

if __name__ == "__main__":
    if User.table_exists():
        print("Database Already Exists")
        sys.exit()

    db.connect()
    db.create_tables([User])

    User.insert_many([
        {"id": 0, "name": "Invlid User", "langpair": "!!|!!"},
        {"id": 120755813, "name": "Boris", "langpair": "ru|en"},
        {"id": 93649293, "name": "Elizaveta", "langpair": "ru|en"},
        {"id": 77815902, "name": "James", "langpair": "en|ru"},
        {"id": 68382468, "name": "Jill", "langpair": "en|ru"},
        {"id": 82080280, "name": "Kyle", "langpair": "en|ru", "admin": True},
        {"id": 117778855, "name": "Mickey", "langpair": "en|ru"},
        {"id": 97384423, "name": "Nataly", "langpair": "__|__"},
        {"id": 96351689, "name": "Transbotor", "langpair": "!!|!!"},
    ]).execute()
    db.close()
