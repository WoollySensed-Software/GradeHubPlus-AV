import streamlit as st

from streamlit_option_menu import option_menu
from GradeHubPlus.Handlers.Local.h_profile import LHProfile
from GradeHubPlus.Handlers.Global.h_email_notify import GHEmailNotify


class ProfileUI:

    def __init__(self):
        self.profile_h = LHProfile()
        self.enotify_h = GHEmailNotify()
        self.selector_options = (
            'Данные аккаунта',
            'Настройки'
        )
        self.full_name = st.session_state['full_name']
        self.name, self.surname = self.full_name.split(' ')
        self.username = st.session_state['username']
        self.email = self.enotify_h.get_user_email(self.username)

    def logout(self):
        st.session_state['auth_status'] = False
        st.session_state['full_name'] = ''
        st.session_state['username'] = ''
        st.session_state['staff_value'] = ''
        st.session_state['selector_options'] = (
            'Авторизация', 'Информация'
        )

    def setupUI(self):
        st.sidebar.button(':red[Выйти из аккаунта]', on_click=self.logout)

        selector_menu = option_menu(
            menu_title='Профиль',
            default_index=0,
            options=self.selector_options,
            orientation='horizontal'
        )
        # Данные аккаунта
        if selector_menu == self.selector_options[0]:
            self.__option_1()
        # Настройки
        elif selector_menu == self.selector_options[1]:
            self.__option_2()
    
    def __option_1(self):
        st.markdown(f'### Имя: :red[{self.name}]')
        st.markdown(f'### Фамилия: :red[{self.surname}]')
        st.markdown(f'### Логин: :red[{self.username}]')
        if self.email == 'Undefined':
            st.markdown(
                '### Почта: :red[необходимо указать в настройках]'
            )
        else: st.markdown(f'### Почта: :red[{self.email}]')

    def __option_2(self):
        if self.email == 'Undefined':
            # --- Добавить почту ---
            with st.form('form_add_email', clear_on_submit=True):
                st.markdown(':red[Добавить почту]')

                adem_email = st.text_input(
                    'Почта', max_chars=64,
                    placeholder='Введите свою почту'
                ).strip()

                if st.form_submit_button(':red[Добавить]'):
                    if adem_email != '':
                        if self.enotify_h.check_email(adem_email):
                            _state = self.enotify_h.set_email(
                                self.username, adem_email
                            )

                            if _state['status'] == 'OK':
                                st.success(_state['note'], icon='✔️')
                            elif _state['status'] == 'ERROR':
                                st.error(_state['note'], icon='❌')
                        else: st.warning('Невалидная почта', icon='⚠️')
                    else: st.warning('Необходимо указать почту', icon='⚠️')
        else:
            # --- Уведомления ---
            notify_status = self.enotify_h.get_notify_status(self.username)
            if notify_status:
                switch_status = st.toggle(
                    'Получать все уведомления?', value=notify_status
                )
                if not switch_status:
                    self.enotify_h.change_notify_status(self.username)
            else:
                switch_status = st.toggle(
                    'Получать все уведомления?', value=notify_status
                )
                if switch_status:
                    self.enotify_h.change_notify_status(self.username)

            # --- Изменить почту ---
            with st.form('form_change_email', clear_on_submit=True):
                st.markdown(':red[Изменить почту]')

                chem_old_email = st.text_input(
                    'Старая почта', max_chars=64,
                    placeholder='Введите старую почту'
                ).strip()
                chem_new_email_1 = st.text_input(
                    'Новая почта', max_chars=64,
                    placeholder='Введите новую почту'
                ).strip()
                chem_new_email_2 = st.text_input(
                    'Повторите почту', max_chars=64,
                    placeholder='Введите почту еще раз'
                ).strip()

                if st.form_submit_button(':red[Изменить]'):
                    if chem_old_email != '' and chem_new_email_1 != '':
                        if chem_new_email_1 == chem_new_email_2:
                            valid = self.enotify_h.check_email(
                                chem_new_email_1
                            )
                            if valid:
                                _state = self.enotify_h.change_email(
                                    self.username, chem_old_email,
                                    chem_new_email_1
                                )

                                if _state['status'] == 'OK':
                                    st.success(_state['note'], icon='✔️')
                                elif _state['status'] == 'ERROR':
                                    st.error(_state['note'], icon='❌')
                            else: st.warning('Невалидная почта', icon='⚠️')
                        else: st.warning('Почты не совпадает', icon='⚠️')
                    else: st.warning('Заполните все поля', icon='⚠️')

        # --- Смена пароля ---
        with st.form('form_change_password', clear_on_submit=True):
            st.markdown(':red[Смена пароля]')

            chpa_old_pw = st.text_input(
                'Старый пароль', type='password', max_chars=32,
                placeholder='Введите свой старый пароль'
            ).strip()
            col_chpa_1, col_chpa_2 = st.columns(2)
            chpa_new_pw_1 = col_chpa_1.text_input(
                'Новый пароль', type='password', max_chars=32,
                placeholder='Введите новый пароль'
            ).strip()
            chpa_new_pw_2 = col_chpa_2.text_input(
                'Повторите пароль', type='password', max_chars=32,
                placeholder='Повторите новый пароль'
            ).strip()

            if st.form_submit_button(':red[Сменить пароль]'):
                if chpa_old_pw != '' and chpa_new_pw_1 != '':
                    if chpa_new_pw_1 == chpa_new_pw_2:
                        _state = self.profile_h.change_password(
                            st.session_state['username'],
                            chpa_old_pw, chpa_new_pw_1
                        )
                        if _state['status'] == 'OK':
                            st.success(_state['note'], icon='✔️')
                        elif _state['status'] == 'ERROR':
                            st.error(_state['note'], icon='❌')
                    else: st.warning('Пароли не совпадают', icon='⚠️')
                else: st.warning(
                    'Необходимо заполнить все поля', icon='⚠️'
                )
