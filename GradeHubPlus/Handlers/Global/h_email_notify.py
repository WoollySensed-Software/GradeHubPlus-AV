import smtplib

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
    
    def check_email(self, email: str):
        return validate(
            email_address=email,
            check_format=True,
            check_blacklist=True,
            check_dns=True,
            dns_timeout=10,
            check_smtp=False,
            smtp_debug=False
        )
    
    def get_user_email(self, username: str) -> str:
        return self.db_users.get(username)['email']
    
    def set_email(self, username: str, email: str) -> dict:
        if self.get_user_email(username) == 'Undefined':
            self.db_users.update({'email': email}, username)
            finally_dict = {
                'status': 'OK',
                'note': 'Почта успешно добавлена'
            }
        else:
            finally_dict = {
                'status': 'ERROR',
                'note': 'Почта уже указана'
            }
        return finally_dict
    
    def change_email(self,
        username: str,
        old_email: str,
        new_email: str
    ) -> dict:
        if self.get_user_email(username) == old_email:
            self.db_users.update({'email': new_email}, username)
            finally_dict = {
                'status': 'OK',
                'note': 'Почта успешно изменена'
            }
        else:
            finally_dict = {
                'status': 'ERROR',
                'note': 'Неверно указана почта'
            }
        return finally_dict

    def get_notify_status(self, username: str) -> bool:
        notify_status = self.db_users.get(username)['notify']
        return True if notify_status == 'Yes' else False
    
    def change_notify_status(self, username: str):
        notify_status = self.get_notify_status(username)
        if notify_status:
            self.db_users.update({'notify': 'Not'}, username)
        else: self.db_users.update({'notify': 'Yes'}, username)

    def send_notify(self,
        user_email: str,
        subject: str,
        message: str
    ):
        # Кодировка письма
        charset = 'Content-Type: text/plain; charset=utf-8'
        mime = 'MIME-Version: 1.0'

        # Формирование тела письма
        body = '\r\n'.join((
            f'From: {self.from_email}',
            f'To: {user_email}',
            f'Subject: {subject}',
            mime, charset, '', message
        ))

        try:
            # Подключение к почтовому сервису
            smtp = smtplib.SMTP(self.server, self.server_port)
            smtp.starttls()
            smtp.ehlo()
            # Вход в почтовый сервер
            smtp.login(self.from_email, self.email_pw)
            # Отправка письма
            smtp.sendmail(self.from_email, user_email, body.encode('utf-8'))
        except smtplib.SMTPException as error:
            print('Не удалось отправить письмо...')
            raise error
        finally: smtp.quit()

    def send_score_notify(self, 
        staff_username: str, 
        subject: str,
        users: list
    ):
        for user in users:
            full_name = user.split(' - ')[0]
            data = self.db_users.fetch({'full_name': full_name})
            staff_full_name = self.db_users.get(staff_username)['full_name']
            for value in data.items:
                if value['email'] != 'Undefined' and value['notify'] == 'Yes':
                    msg = (
                        f'Здравствуйте, {full_name}, Вы получили это '+
                        'уведомление, потому что подписаны на рассылку.\n\n'+
                        f'{staff_full_name} выставил баллы по {subject}.\n'+
                        'Вы можете проверить это на сайте!\n\n\n\n'+
                        'Если Вы хотите отписаться от рассылки уведомлений, '+
                        'то нужно сделать это в настройках профиля:\n'+
                        'https://gradehu6plus-av.streamlit.app'
                    )
                    self.send_notify(
                        value['email'], 'Уведомление от GradeHub+', msg
                    )
    