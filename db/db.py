import psycopg2
from data.config import HOST, USER, PORT_ID, DB_NAME, PASSWORD, ssh_host, ssh_port, ssh_user, ssh_password
from datetime import datetime, timezone
from sshtunnel import SSHTunnelForwarder
from data.models.user import User

TABLE_NAME = 'users'
F_ID = 'id'
F_FIRST_NAME = 'first_name'
F_LAST_NAME = 'last_name'
F_USER_NAME = 'username'
F_DATE = 'date'
F_IS_BLOCKED = 'isBlocked'
create_script_users = f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        {F_ID}          bigint PRIMARY KEY,
        {F_FIRST_NAME}  varchar(100),
        {F_LAST_NAME}   varchar(100),
        {F_USER_NAME}   varchar(100),
        {F_DATE}        DATE,
        {F_IS_BLOCKED}  BOOLEAN
    )'''
delete_table_script = f'DROP TABLE IF EXISTS {TABLE_NAME}'


class DB:
    def __init__(self):
        self.tunnelConf = SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_password,
            remote_bind_address=(HOST, PORT_ID), )

        self.tunnelConf.start()
        self.db = psycopg2.connect(host=self.tunnelConf.local_bind_host, dbname=DB_NAME, user=USER,
                                   password=PASSWORD,
                                   port=self.tunnelConf.local_bind_port)
        self.sql = self.db.cursor()
        self.users_table()

    def close(self):
        self.db.commit()

    def users_table(self):
        self.sql.execute(create_script_users)
        self.close()

    def has_user(self, user_id):
        self.sql.execute(f"SELECT {F_ID} FROM {TABLE_NAME} WHERE {F_ID}=%s", (user_id,))
        if self.sql.fetchall():
            self.close()
            return True
        else:
            self.close()
            return False

    def add_admin(self, user_id):
        # todo set function
        self.sql.execute("UPDATE users SET admin='True' WHERE user_id={}".format(user_id))
        self.close()

    def insertUser(self, user: User):
        time = datetime.now(timezone.utc)
        insert_value = (
            user.id, user.first_name, user.last_name, user.username, F'{time.year}-{time.month}-{time.day}',
            user.isBlocked,)
        self.sql.execute(
            f'INSERT INTO '
            f'{TABLE_NAME} ({F_ID}, {F_FIRST_NAME}, {F_LAST_NAME}, {F_USER_NAME}, {F_DATE}, {F_IS_BLOCKED}) '
            f'VALUES (%s, %s, %s, %s, %s, %s) RETURNING {F_ID}', insert_value)
        self.close()

    def delete_table(self, dbname):
        self.sql.execute("DROP TABLE {}".format(dbname))
        self.close()

    def delete_admin(self, user_id):
        # todo set function
        self.sql.execute(f"""UPDATE users SET admin=False WHERE id={user_id}""")
        self.close()

    def delete_user(self, user_id):
        # todo set function
        self.sql.execute(f"""DELETE FROM users WHERE user_id={user_id}""")
        self.close()

    def getUser(self, userId: int) -> User:
        self.sql.execute(f"""SELECT * FROM {TABLE_NAME} WHERE {F_ID}={userId}""")
        userData = self.sql.fetchall()[0]
        self.close()
        return User(
            id=userData[0],
            first_name=userData[1],
            last_name=userData[2],
            username=userData[3],
            date=userData[4],
            isBlocked=userData[5],
        )

    def get_users_count(self) -> tuple:
        self.sql.execute(f"SELECT COUNT({F_ID}) FROM {TABLE_NAME} WHERE {F_IS_BLOCKED}=TRUE")
        blockedCount = self.sql.fetchall()[0][0]
        self.sql.execute(f"SELECT COUNT({F_ID}) FROM {TABLE_NAME}")
        usersCount = self.sql.fetchall()[0][0]
        self.close()
        return usersCount, blockedCount

    def get_users_user_id(self):
        self.sql.execute(f"SELECT {F_ID} FROM {TABLE_NAME} WHERE {F_IS_BLOCKED}=FALSE")
        value = self.sql.fetchall()
        self.close()
        return value

    def updateUser(self, user: User):
        updateValue = (user.first_name, user.last_name, user.username, user.isBlocked, user.id,)
        self.sql.execute(
            f"UPDATE {TABLE_NAME} SET {F_FIRST_NAME}=%s, {F_LAST_NAME}=%s, {F_USER_NAME}=%s, {F_IS_BLOCKED}=%s "
            f"WHERE {F_ID}=%s", updateValue)
        self.close()

    def updateUserBlocked(self, userId: int, isBlocked: bool):
        updateValue = (isBlocked, userId,)
        self.sql.execute(
            f"UPDATE {TABLE_NAME} SET {F_IS_BLOCKED}=%s "
            f"WHERE {F_ID}=%s", updateValue)
        self.close()

    def readAllUsers(self):
        self.sql.execute(f"SELECT * FROM {TABLE_NAME}")
        value = self.sql.fetchall()
        self.close()
        return value

    def users_txt(self):
        # todo set function
        d = self.readAllUsers()
        count = 0
        with open('files/users.txt', 'w', encoding='utf-8') as file:
            file.write("    Foydalanuvchilar haqida ma'lumot!!!\n")
        with open('files/users.txt', 'a', encoding='utf-8') as file:
            for i in d:
                count += 1
                s = str(f"{count}) ")
                s += str(f"{i[0]} : ")
                s += str(f"{i[1]} : ")
                s += str(f"{i[2]} : ")
                s += str(f"{i[3]} : ")
                s += str(f"{i[4]} : ")
                s += str(f"{i[5]} : ")
                s += str(f"{i[7]}\n")
                file.write(s)
            file.write(f"Umumiy: {count}")


if __name__ == "__main__":
    db = DB()
    print(db.readAllUsers())
    db.delete_table(TABLE_NAME)
    db.users_table()
    print(db.readAllUsers())
