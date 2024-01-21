from GradeHubPlus.Handlers.Global.h_common import GHCommon


class LHStaff(GHCommon):

    def __init__(self):
        super().__init__()

    def add_student(self, full_name: str, direction: str, course: int) -> dict:
        student = self.db_students.fetch({
            'key': full_name,
            'direction': direction,
            'course': course
        })


        if student.items == []:
            self.db_students.put({
                'key': full_name,
                'direction': direction,
                'course': course
            })
            response = {
                'status': 'OK',
                'note': 'Студент успешно добавлен'
            }
        else:
            response = {
                'status': 'ERROR',
                'note': 'Такой студент уже добавлен'
            }
        return response

    def add_subject(self, subject: str) -> dict:
        data = self.db_subjects.fetch({'key': subject})


        if data.items == []:
            self.db_subjects.put({'key': subject})
            response = {
                'status': 'OK',
                'note': 'Предмет успешно добавлен'
            }
        else:
            response = {
                'status': 'ERROR',
                'note': 'Такой предмет уже добавлен'
            }
        return response

    def edit_score(self,
        username: str,
        subject: str,
        students: list,
        mode: str,
        work_type: str,
        score: int
    ):
        score = score if mode == 'Добавить баллы' else -score
        big_data = self.db_data_changes.fetch({'staff_username': username})


        if big_data.items != []:
            for student in students:
                invalid_match = 0

                for value in big_data.items:
                    if (
                        value['student'] == student and 
                        value['subject'] == subject and 
                        value['work_type'] == work_type
                    ):
                        self.__edit_score_update(
                            username, subject, student, work_type,
                            value['score'] + score, value['key']
                        )
                        invalid_match = 0
                        break
                    else: invalid_match = 1
                

                if invalid_match == 1:
                    self.__edit_score_put(
                        username, subject, student, work_type, score
                    )
        else:
            for student in students:
                self.__edit_score_put(
                    username, subject, student, work_type, score
                )

    def __edit_score_update(self,
        username: str,
        subject: str,
        student: str,
        work_type: str,
        score: int,
        key: str
    ):
        self.db_data_changes.update({
            'datetime': self.get_datetime(),
            'staff_username': username,
            'subject': subject,
            'student': student,
            'work_type': work_type,
            'score': score
        }, key)

    def __edit_score_put(self,
        username: str,
        subject: str,
        student: str,
        work_type: str,
        score: int
    ):
        self.db_data_changes.put({
            'datetime': self.get_datetime(),
            'staff_username': username,
            'subject': subject,
            'student': student,
            'work_type': work_type,
            'score': score
        })
    
    # Онулирование баллов
    def zeroing_score(self, 
        username: str, 
        subject: str,
    ):
        big_data = self.db_data_changes.fetch({'staff_username': username})


        if big_data.items != []:
            for value in big_data.items:
                self.__edit_score_update(
                    username, subject, value['work_type'], 
                    value['student'], 0, value['key']
                )
                

    def display_dataframe(self,
        username: str,
        subjects: list,
        students: list,
        work_types: list
    ):
        if subjects == []: subjects = self.all_subjects
        if students == []: students = self.all_students
        if work_types == []: work_types = self.all_wtypes

        dataframe = {
            'Студент': [],
            'Направление': [],
            'Курс': [],
            'Предмет': [],
            'Тип работы': [],
            'Баллы': []
        }
        big_data = self.db_data_changes.fetch({'staff_username': username})
        big_data: list = big_data.items
        
        if big_data != []:
            data = self.__make_df_list(
                big_data, subjects, students, work_types
            )
            dataframe['Студент'] =      [el[0] for el in data]
            dataframe['Направление'] =  [el[1] for el in data]
            dataframe['Курс'] =         [el[2] for el in data]
            dataframe['Предмет'] =      [el[3] for el in data]
            dataframe['Тип работы'] =   [el[4] for el in data]
            dataframe['Баллы'] =        [el[5] for el in data]
            return dataframe
        else: return dataframe
    
    def __make_df_list(self,
        big_data: list,
        subjects: list,
        students: list,
        work_types: list
    ):
        res = []

        while big_data != []:
            value = big_data.pop()
            
            for subject in subjects:
                for student in students:
                    for wtype in work_types:
                        if (
                            value['subject'] == subject and 
                            value['student'] == student and 
                            value['work_type'] == wtype
                        ):
                            full_name, direction, course = student.split(' - ')
                            res += [(
                                full_name, direction, course,
                                subject, wtype, value['score']
                            )]
                            break
        return res
