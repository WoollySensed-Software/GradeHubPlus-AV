import streamlit as st

from streamlit_option_menu import option_menu
from streamlit_extras.add_vertical_space import add_vertical_space
from GradeHubPlus.Handlers.Local.h_auth import LHAuthorization
from GradeHubPlus.Handlers.Global.h_email_notify import GHEmailNotify


class AuthorizationUI:

    def __init__(self) -> None:
        self.auth_h = LHAuthorization()
        self.test = GHEmailNotify()

    def setupUI(self):
        selector_menu = option_menu(
            menu_title='Авторизация',
            default_index=1,
            orientation='horizontal',
            options=('Регистрация', 'Вход')
        )


        if selector_menu == 'Регистрация':
            self.__sign_up()
        elif selector_menu == 'Вход':
            self.__sign_in()
    
    def __sign_up(self):
        # --- Регистрация ---
        with st.form('form_create_account'):
            st.markdown(':red[Регистрация]')
            crac_username = st.text_input(
                'Логин', max_chars=32, placeholder='Нужен для входа',
                help='Не используйте пробелы для логина'
            ).strip()
            crac_password = st.text_input(
                'Пароль', max_chars=32, type='password',
                placeholder='Не используйте простой пароль',
                help='Не используйте пробелы для пароля'
            ).strip()
            add_vertical_space(2)
            col_crac_name, col_crac_sname = st.columns(2)
            crac_name = col_crac_name.text_input(
                'Имя', max_chars=64, 
                placeholder='Введите Ваше имя'
            ).strip().capitalize()
            crac_surname = col_crac_sname.text_input(
                'Фамилия', max_chars=64, 
                placeholder='Введите Вашу фамилию'
            ).strip().capitalize()

            with st.expander('Для преподавателей'):
                crac_staff = st.toggle('Вы преподаватель?')
                crac_key = st.text_input(
                    'Ключ активации', max_chars=16, type='password',
                    placeholder='Нужен только для преподавателей',
                    help='Если Вы студент, то просто пропустите это поле'
                )


            if st.form_submit_button(':red[Зарегистрироваться]'):
                if crac_username != '' and crac_password != '':
                    if crac_name != '' and crac_surname != '':
                        crac_full_name = f'{crac_name} {crac_surname}'
                        if crac_staff and crac_key != '':
                            _state = self.auth_h.create_account(
                                crac_username, crac_password, crac_full_name, 
                                crac_staff, key=crac_key
                            )


                            if _state['status'] == 'OK':
                                st.success(_state['note'], icon='✔️')
                            elif _state['status'] == 'ERROR':
                                st.error(_state['note'], icon='❌')
                        elif not crac_key:
                            _state = self.auth_h.create_account(
                                crac_username, crac_password, crac_full_name, 
                                crac_staff
                            )


                            if _state['status'] == 'OK':
                                st.success(_state['note'], icon='✔️')
                            elif _state['status'] == 'ERROR':
                                st.error(_state['note'], icon='❌')
                        else: st.warning(
                            'Для преподавателей нужен еще и ключ', icon='⚠️'
                        )
                    else: st.warning(
                        'Необходимо указать имя и фамилию', icon='⚠️'
                    )
                else: st.warning(
                    'Необходимо указать логин и пароль', icon='⚠️'
                )

    def __sign_in(self):
        # --- Вход ---
        with st.form('form_login_account'):
            st.markdown(':red[Вход в аккаунт]')
            loac_username = st.text_input(
                'Логин', max_chars=32, 
                placeholder='Введите логин'
            ).strip()
            loac_password = st.text_input(
                'Пароль', max_chars=32, type='password',
                placeholder='Введите пароль'
            ).strip()


            if st.form_submit_button(':red[Войти]'):
                if loac_username != '':
                    if loac_password != '':
                        _state = self.auth_h.login_account(
                            loac_username, loac_password
                        )


                        if _state['auth_status']:
                            st.session_state['auth_status'] = True
                            st.session_state['full_name'] = _state['full_name']
                            st.session_state['username'] = _state['username']
                            st.session_state['staff_value'] = _state['staff_value']
                            st.session_state['selector_options'] = (
                                'Главная', 'Профиль', 'Информация'
                            )
                            st.toast('Вы успешно вошли!', icon='✔️')
                        else:
                            st.error('Неудачная попытка входа', icon='❌')
                    else: st.warning('Вы забыли указать пароль', icon='⚠️')
                else: st.warning('Вы забыли указать логин', icon='⚠️')
        
        
        if st.session_state['auth_status']:
            # Заглушка
            st.button('Нажмите, чтобы **продолжить**', type='primary')
