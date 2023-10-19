from GradeHubPlus.Handlers.Global.h_common import GHCommon


class LHAuthorization(GHCommon):

    def __init__(self):
        super().__init__()

    def create_account(self, 
        username: str,
        password: str,
        full_name: str,
        staff: bool,
        *,
        key: str | None = None
    ):
        validation = self.__create_account_handler(
            username, staff, key=key
        )


        if validation['valid_acc'] and validation['valid_key']:
            request = self.__create_account_request(
                username, password, full_name, staff, key=validation['key']
            )


            if request:
                finally_dict = {
                    'status': 'OK',
                    'note': 'Регистрация прошла успешно'
                }
                return finally_dict
            else:
                finally_dict = {
                    'status': 'ERROR',
                    'note': 'Произошла ошибка'
                }
                return finally_dict
        elif validation['valid_acc'] and validation['valid_key'] == False:
            finally_dict = {
                'status': 'ERROR',
                'note': 'Неверно введен ключ'
            }
            return finally_dict
        elif validation['valid_acc'] == False:
            finally_dict = {
                'status': 'ERROR',
                'note': 'Такой пользователь уже существует'
            }
            return finally_dict
        elif validation['valid_acc'] and validation['valid_key'] is None:
            request = self.__create_account_request(
                username, password, full_name, staff, key=validation['key']
            )


            if request:
                finally_dict = {
                    'status': 'OK',
                    'note': 'Регистрация прошла успешно'
                }
                return finally_dict
            else:
                finally_dict = {
                    'status': 'ERROR',
                    'note': 'Произошла ошибка'
                }
                return finally_dict
    
    def __create_account_handler(self,
        username: str,
        staff: bool,
        *,
        key: str | None = None
    ) -> dict:
        validation = {'valid_acc': None, 'valid_key': None, 'key': ''}
        data = self.db_users.fetch()


        if data.items != []:
            if staff:
                if self.db_users.get(username) is None:
                    validation['valid_acc'] = True
                    keys = self.db_keys.fetch().items

                    for el in keys:
                        valid = self.check_pw(el['key'], key)


                        if valid and el['owner'] == 'Undefined':
                            validation['valid_key'] = True
                            validation['key'] = el['key']
                            break
                        else:
                            validation['valid_key'] = False
                            continue
                else: 
                    validation['valid_acc'] = False
                    validation['valid_key'] = False
            else:
                if self.db_users.get(username) is None:
                    validation['valid_acc'] = True
                else: validation['valid_acc'] = False
        else:
            if staff:
                validation['valid_acc'] = True
                keys = self.db_keys.fetch().items

                for el in keys:
                    valid = self.check_pw(el['key'], key)


                    if valid and el['owner'] == 'Undefined':
                        validation['valid_key'] = True
                        validation['key'] = el['key']
                        break
                    else:
                        validation['valid_key'] = False
                        continue
            else: validation['valid_acc'] = True
        return validation

    def __create_account_request(self,
        username: str,
        password: str,
        full_name: str,
        staff: bool,
        *,
        key: str | None = None
    ) -> bool:
        datetime = self.get_datetime()
        password = self.hash_pw(password)


        if staff:
            try:
                self.db_users.put({
                    'key': username,
                    'password': password,
                    'datetime': datetime,
                    'full_name': full_name,
                    'staff': 'Yes',
                    'email': 'Undefined',
                    'notify': 'Not'
                })
                self.db_keys.update({'owner': username}, key)
                return True
            except: return False
        else:
            self.db_users.put({
                'key': username,
                'password': password,
                'datetime': datetime,
                'full_name': full_name,
                'staff': 'Not',
                'email': 'Undefined',
                'notify': 'Not'
            })
            return True
    
    def login_account(self, username: str, password: str) -> dict:
        users = self.db_users.fetch()


        if users.items != []:
            for user in users.items:
                valid = self.check_pw(user['password'], password)

                
                if valid and username == user['key']:
                    finally_dict = {
                        'auth_status': True,
                        'full_name': user['full_name'],
                        'username': user['key'],
                        'staff_value': user['staff']
                    }
                    break
                else:
                    finally_dict = {'auth_status': False}
                    continue
            return finally_dict
        else: return {'auth_status': False}
