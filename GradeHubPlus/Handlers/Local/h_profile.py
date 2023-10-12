from GradeHubPlus.Handlers.Global.h_common import GHCommon


class LHProfile(GHCommon):

    def __init__(self):
        super().__init__()
    
    def change_password(self, username: str,old_pw: str, new_pw: str) -> dict:
        users = self.db_users.fetch()
        for user in users.items:
            valid = self.check_pw(user['password'], old_pw)
            if valid:
                new_pw = self.hash_pw(new_pw)
                self.db_users.update({'password': new_pw}, username)
                response = {
                    'status': 'OK',
                    'note': 'Пароль успешно изменен'
                }
                break
            else:
                response = {
                    'status': 'ERROR',
                    'note': 'Вы ввели неверный старый пароль'
                }
                continue
        return response
