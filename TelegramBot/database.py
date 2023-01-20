import sqlite3

class user_database:
    def __init__(self, database_file):
        #Подключение к БД
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_users(self, status = 1):
        #Получаем всех активных подписчиков бота
        with self.connection:
            return self.cursor.execute("SELECT * FROM `user` WHERE `status` = ?", (status,)).fetchall()

    def get_users_id(self, user_id):
            result = self.cursor.execute('SELECT * FROM `user` WHERE `user_id` = ?', (user_id,)).fetchall()
            return int(result)            

    def user_exists(self, user_id):
        #Проверка, есть ли юзер в БД
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `user` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def user_add(self, user_id, user_full_name, user_nickname):
        #Добавляем нового подписчика
        with self.connection:
            return self.cursor.execute("INSERT INTO `user` (`user_id`, `user_nickname`, `user_name`) VALUES(?,?,?)", (user_id, user_nickname,user_full_name))  

    def close(self):
        #Закрываем соединение с БД
        self.connection.close()              