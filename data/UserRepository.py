from data.DefaultDataBase import DefaultDataBase


class UserRepository(DefaultDataBase):
    def __init__(self):
        super().__init__()

    # ALL USERS 

    def add_user(self, user_id, username, firstname, lang_key):
        query = "INSERT INTO `users` (user_id, username, firstname, lang_key) VALUES (%s, %s, %s, %s);"
        return self._insert(query, (user_id, username, firstname, lang_key))

    def get_user(self, user_id):
        query = "SELECT * FROM `users` WHERE `user_id` = %s;"
        return self._select_one(query, (user_id, ))
    
    # APP 1 - Gates Of Olympus
    
    def add_user_app1_olympus(self, user_id, username, firstname, lang_key, client_url):
        query = "INSERT INTO `app1_olympus_users` (user_id, username, firstname, lang_key, url) VALUES (%s, %s, %s, %s, %s);"
        return self._insert(query, (user_id, username, firstname, lang_key, client_url))

    def get_user_app1_olympus(self, user_id):
        query = "SELECT * FROM `app1_olympus_users` WHERE `user_id` = %s;"
        return self._select_one(query, (user_id, ))

    # def get_users(self):
    #     query = "SELECT * FROM `users` WHERE `role` = %s;"
    #     return self._select(query, (USER,))
    #
    # def get_all_users(self):
    #     query = "SELECT * FROM `users`;"
    #     return self._select(query)
    #
    # def get_users_in_team(self):
    #     query = "SELECT u.* FROM `users` u LEFT JOIN `access` a ON u.`telegram_id` = a.`user_id` WHERE a.`user_id` IS NOT NULL AND u.`role` = %s;"
    #     return self._select(query, (USER,))
    #
    # def get_users_by_team_id(self, team_id):
    #     query = "SELECT u.* FROM `users` u LEFT JOIN `access` a ON u.`telegram_id` = a.`user_id` WHERE a.`user_id` IS NOT NULL AND u.`role` = %s AND `team_id` = %s;"
    #     return self._select(query, (USER, team_id))
    #
    # def get_users_no_team(self):
    #     query = "SELECT u.* FROM `users` u LEFT JOIN `access` a ON u.`telegram_id` = a.`user_id` WHERE a.`user_id` IS NULL AND u.`role` = %s;"
    #     return self._select(query, (USER,))
    #
    # def is_banned(self, telegram_id):
    #     query = "SELECT `banned` FROM `users` WHERE `telegram_id` = %s;"
    #     return self._select_one(query, (telegram_id,))
    #
    # def user_role_by_id(self, telegram_id):
    #     query = "SELECT `role` FROM `users` WHERE `telegram_id` = %s;"
    #     return self._select_one(query, (telegram_id,))
    #
    # def get_admins(self):
    #     query = "SELECT * FROM `users` WHERE `role` = %s;"
    #     return self._select(query, (ADMIN,))
    #
    # def ban_user_by_id(self, telegram_id, ban_message=None):
    #     query = "UPDATE `users` SET `banned` = 1, `ban_message` = %s WHERE `telegram_id` = %s;"
    #     return self._update(query, (ban_message, telegram_id))
    #
    # def ban_user_by_username(self, username, ban_message=None):
    #     query = "UPDATE `users` SET `banned` = 1, `ban_message` = %s WHERE `username` = %s;"
    #     return self._update(query, (ban_message, username))
    #
    # def list_of_banned_users(self):
    #     query = "SELECT * FROM `users` WHERE `banned` = 1;"
    #     return self._select(query)
    #
    # def unban_user_by_id(self, telegram_id):
    #     query = "UPDATE `users` SET `banned` = 0, `ban_message` = null WHERE `telegram_id` = %s;"
    #     return self._update(query, (telegram_id,))
    #
    # def change_lang(self, telegram_id, lang):
    #     query = "UPDATE `users` SET `lang` = %s WHERE `telegram_id` = %s;"
    #     return self._update(query, (lang, telegram_id))
