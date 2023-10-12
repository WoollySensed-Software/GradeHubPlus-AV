from deta import Deta
from GradeHubPlus.Config.settings import DETA_KEY


class GHDatabase:

    def __init__(self):
        self.database = Deta(DETA_KEY)
        self.db_users = self.database.Base('users')
        self.db_keys = self.database.Base('keys')
        self.db_students = self.database.Base('students')
        self.db_subjects = self.database.Base('subjects')
        self.db_data_changes = self.database.Base('data_changes')
