import smtpd

from email_validate import validate
from GradeHubPlus.Config.settings import EMAIL, PW, SERVER, PORT
from GradeHubPlus.Handlers.Global.h_common import GHCommon


class GHEmailNotify(GHCommon):

    def __init__(self):
        super().__init__()

        self.from_email = EMAIL
        self.email_pw = PW
        self.server = SERVER
        self.server_port = PORT
    