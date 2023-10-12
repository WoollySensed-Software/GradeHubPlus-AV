import os, hashlib

from datetime import datetime as dt
from GradeHubPlus.Handlers.Global.h_database import GHDatabase


class GHCommon(GHDatabase):

    def __init__(self):
        super().__init__()

        self.all_students = self.__get_all_students()
        self.all_subjects = self.__get_all_subjects()
        self.all_staff = self.__get_all_staff()
        self.all_directions = self.__get_all_directions()
        self.all_users_email = self.__get_all_users_email()
        self.all_wtypes = (
            'Лекция', 
            'Семинар', 
            'Лабораторная', 
            'Практика'
        )

    def hash_pw(self, _password: str) -> str:
        salt = os.urandom(32).hex()
        return hashlib.sha256(
            salt.encode() + _password.encode()
        ).hexdigest() + ':' + salt
    
    def check_pw(self, _hash: str, _password: str) -> bool:
        password, salt = _hash.split(':')
        return password == hashlib.sha256(
            salt.encode() + _password.encode()
        ).hexdigest()
    
    def get_datetime(self) -> str:
        _dt = dt.now()
        return (
            f'{_dt.day}.{_dt.month}.{_dt.year}'+
            ' | '+
            f'{_dt.hour+3}:{_dt.minute}:{_dt.second}'
        )

    def __get_all_students(self) -> list:
        students = self.db_students.fetch()
        if bool(students.items):
            res = []
            for value in students.items:
                res.append(
                    f'{value["key"]} - {value["direction"]} '+
                    f'- {value["course"]}'
                )
            return res
        else: return []

    def __get_all_subjects(self) -> list:
        subjects = self.db_subjects.fetch()
        if bool(subjects.items):
            res = [el['key'] for el in subjects.items]
            return res
        else: return []

    def __get_all_staff(self) -> list:
        staff = self.db_users.fetch()
        if bool(staff.items):
            res = []
            for value in staff.items:
                if value['staff'] == 'Yes':
                    res.append((value['key'], value['full_name']))
            return res
        else: return []

    def __get_all_directions(self) -> list:
        dirs = self.db_students.fetch()
        res = []
        if bool(dirs.items):
            for value in dirs.items:
                res.append(value['direction'])
            
            res = list(set(res))
            res.insert(0, 'Указать самостоятельно')
            return res
        else: return ['Указать самостоятельно']
    
    def __get_all_users_email(self):
        users = self.db_users.fetch()
        res = []
        if bool(users.items):
            for value in users.items:
                if value['email'] != 'Undefined' and value['notify'] == 'Yes':
                    res.append(value['email'])
            return res
        else: return []
