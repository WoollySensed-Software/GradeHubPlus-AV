from GradeHubPlus.Handlers.Global.h_common import GHCommon


class LHAdmin(GHCommon):

    def __init__(self):
        super().__init__()
    
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
