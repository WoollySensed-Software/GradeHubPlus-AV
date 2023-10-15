from GradeHubPlus.Handlers.Global.h_common import GHCommon


class LHAdmin(GHCommon):

    def __init__(self):
        super().__init__()
    
    def valid_keys_count(self) -> int:
        return self.db_keys.fetch({'owner': 'Undefined'}).count
    
    def create_key(self, key: str) -> dict:
        keys = self.db_keys.fetch()
        if keys.items != []:
            for value in keys.items:
                valid = self.check_pw(value['key'], key)
                if valid and value['owner'] == 'Undefined':
                    isReady = {
                        'status': 'ERROR',
                        'note': 'Такой ключ уже существует, но не занят'
                    }
                    break
                elif valid and value['owner'] != 'Undefined':
                    isReady = {
                        'status': 'ERROR',
                        'note': 'Такой ключ уже существует и занят '+
                        f'{value["owner"]}'
                    }
                    break
                else:
                    isReady = {
                        'status': 'OK',
                        'note': 'Ключ успешно добавлен в БД'
                    }
                    continue
            
            if isReady['status'] == 'OK':
                datetime = self.get_datetime()
                hashed_key = self.hash_pw(key)
                self.db_keys.put({
                    'key': hashed_key,
                    'datetime': datetime,
                    'owner': 'Undefined'
                })
                return isReady
            elif isReady['status'] == 'ERROR': return isReady
        else:
            datetime = self.get_datetime()
            hashed_key = self.hash_pw(key)
            self.db_keys.put({
                'key': hashed_key,
                'datetime': datetime,
                'owner': 'Undefined'
            })
            isReady = {
                'status': 'OK',
                'note': 'Ключ успешно добавлен в БД'
            }
            return isReady

    def delete_key(self, key: str) -> dict:
        keys = self.db_keys.fetch()
        if keys.items != []:
            for value in keys.items:
                valid = self.check_pw(value['key'], key)
                if valid and value['owner'] == 'Undefined':
                    self.db_keys.delete(value['key'])
                    response = {
                        'status': 'OK',
                        'note': 'Ключ был успешно удален'
                    }
                    break
                elif valid and value['owner'] != 'Undefined':
                    response = {
                        'status': 'ERROR',
                        'note': f'Ключ занят пользователем {value["owner"]}'
                    }
                    break
                else:
                    response = {
                        'status': 'ERROR',
                        'note': 'Неверный ключ'
                    }
                    continue
        return response

    def display_df(self, mode: str):
        if mode == 'users':
            dataframe = {
                'Дата': [],
                'Логин': [],
                'Имя Фамилия': [],
                'Статус': [],
                'Почта': [],
                'Уведомления': []
            }

            big_data = self.db_users.fetch()
            big_data: list = big_data.items
            if big_data != []:
                dataframe['Дата'] = [el['datetime'] for el in big_data]
                dataframe['Логин'] = [el['key'] for el in big_data]
                dataframe['Имя Фамилия'] = [el['full_name'] for el in big_data]
                dataframe['Статус'] = [el['staff'] for el in big_data]
                dataframe['Почта'] = [el['email'] for el in big_data]
                dataframe['Уведомления'] = [el['notify'] for el in big_data]
                return dataframe
            else: return dataframe
        elif mode == 'data_changes':
            dataframe = {
                'Дата': [],
                'Преподаватель': [],
                'Студент': [],
                'Предмет': [],
                'Тип работы': [],
                'Баллы': []
            }
            big_data = self.db_data_changes.fetch()
            big_data: list = big_data.items
            if big_data != []:
                dataframe['Дата'] = [el['datetime'] for el in big_data]
                dataframe['Преподаватель'] = [el['staff_username'] for el in big_data]
                dataframe['Студент'] = [el['student'] for el in big_data]
                dataframe['Предмет'] = [el['subject'] for el in big_data]
                dataframe['Тип работы'] = [el['work_type'] for el in big_data]
                dataframe['Баллы'] = [el['score'] for el in big_data]
                return dataframe
            else: return dataframe
