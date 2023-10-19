from GradeHubPlus.Handlers.Global.h_common import GHCommon


class LHUser(GHCommon):

    def __init__(self):
        super().__init__()

    def display_dataframe(self, 
        student: str,
        subjects: list,
        staff: list,
        work_types: list
    ):
        if subjects == []: subjects = self.all_subjects
        if work_types == []: work_types = self.all_wtypes
        
        
        if staff == []: 
            staff = self.all_staff
        else:
            staff_data = self.db_users.fetch({'staff': 'Yes'})
            staff = [(el['key'], el['full_name']) for el in staff_data.items]
        

        dataframe = {
            'Преподаватель': [],
            'Предмет': [],
            'Тип работы': [],
            'Баллы': []
        }
        student = self.db_students.get(student)


        if student is not None:
            student = (
                f'{student["key"]} - '+
                f'{student["direction"]} - '+
                f'{student["course"]}'
            )
            big_data = self.db_data_changes.fetch({'student': student})
            big_data: list = big_data.items


            if big_data != []:
                data = self.__make_df_list(
                    big_data, subjects, staff, work_types
                )
                dataframe['Преподаватель'] =    [el[0] for el in data]
                dataframe['Предмет'] =          [el[1] for el in data]
                dataframe['Тип работы'] =       [el[2] for el in data]
                dataframe['Баллы'] =            [el[3] for el in data]
                return dataframe
            else: return dataframe
        else: return dataframe

    def __make_df_list(self,
        big_data: list,
        subjects: list,
        staff: list,
        work_types: list
    ):
        res = []

        while big_data != []:
            value = big_data.pop()
            
            for subject in subjects:
                for person in staff:
                    for wtype in work_types:
                        if (
                            value['staff_username'] == person[0] and
                            value['subject'] == subject and 
                            value['work_type'] == wtype
                        ):
                            res += [(
                                person[1], subject, wtype, value['score']
                            )]
                            break
        return res
