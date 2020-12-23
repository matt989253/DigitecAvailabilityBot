from src.botDB.db import Database

def main():
    database = Database("db.json")
    database.set("user", "me")
    database.set("user", "you")
    database.append("test", "test")



if __name__ == '__main__':
    main()
