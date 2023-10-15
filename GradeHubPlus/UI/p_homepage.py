import streamlit as st

from pandas import DataFrame as df
from streamlit_option_menu import option_menu
from GradeHubPlus.Handlers.Global.h_email_notify import GHEmailNotify
from GradeHubPlus.Handlers.Local.h_staff import LHStaff
from GradeHubPlus.Handlers.Local.h_user import LHUser
from GradeHubPlus.Handlers.Local.h_admin import LHAdmin


class HomepageUI:

    def __init__(self, staff_value: str):
        self.staff_h = LHStaff()
        self.user_h = LHUser()
        self.admin_h = LHAdmin()
        self.enotify_h = GHEmailNotify()
        self.staff_value = staff_value

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
        st.sidebar.write('---')
        st.markdown(
            f'### Добро пожаловать, :red[{st.session_state["full_name"]}]!'
        )

        if self.staff_value == 'Yes':
            self.__staffUI()
        elif self.staff_value == 'Not':
            self.__userUI()
        elif self.staff_value == 'Admin':
            self.__adminUI()
    
    def __staffUI(self):
        # --- Настройка датафрейма ---
        with st.sidebar:
            selected_subjects = st.multiselect(
                'Предметы', options=self.staff_h.all_subjects,
                placeholder='Можно несколько'
            )
            selected_students = st.multiselect(
                'Студенты', options=self.staff_h.all_students,
                placeholder='Можно несколько'
            )
            selected_wtypes = st.multiselect(
                'Тип работы', options=self.staff_h.all_wtypes,
                placeholder='Можно несколько'
            )
        
        # --- Отображение датафрейма ---
        df_data = self.staff_h.display_dataframe(
            st.session_state['username'], selected_subjects,
            selected_students, selected_wtypes
        )
        dataframe = df(df_data)
        dataframe.index += 1
        st.dataframe(dataframe, use_container_width=True)

        # --- Добавление студентов ---
        with st.form('form_add_student', clear_on_submit=True):
            st.markdown(':red[Добавление студентов]')

            col_name, col_sname, col_course = st.columns(3)
            adst_name = col_name.text_input(
                'Имя студента', max_chars=64,
                placeholder='Введите имя'
            ).strip().capitalize()
            adst_surname = col_sname.text_input(
                'Фамилия студента', max_chars=64,
                placeholder='Введите фамилию'
            ).strip().capitalize()
            adst_course = col_course.number_input('Курс (1-5)', 1, 5)
            # Направления, которые уже были добавлены
            adst_directions = st.selectbox(
                'Имеющиеся направления',
                options=self.staff_h.all_directions, index=0
            )
            # Направление, которое указывается самостоятельно
            adst_direction = st.text_input(
                'Направление', max_chars=256, 
                placeholder='Укажите направление подготовки '+
                'или выберите сверху',
                help='Код направления указывать не обязательно'
            ).strip()

            if st.form_submit_button(':red[Добавить]'):
                if adst_name != '' and adst_surname != '':
                    if adst_directions == 'Указать самостоятельно':
                        if adst_direction != '':
                            adst_full_name = f'{adst_name} {adst_surname}'
                            _state = self.staff_h.add_student(
                                adst_full_name, adst_direction, adst_course
                            )
                            if _state['status'] == 'OK':
                                st.toast(_state['note'], icon='✔️')
                            elif _state['status'] == 'ERROR':
                                st.error(_state['note'], icon='❌')
                        else: st.warning(
                            'Вы не указали направление подготовки', icon='⚠️'
                        )
                    else:
                        adst_full_name = f'{adst_name} {adst_surname}'
                        _state = self.staff_h.add_student(
                            adst_full_name, adst_directions, adst_course
                        )
                        if _state['status'] == 'OK':
                            st.toast(_state['note'], icon='✔️')
                        elif _state['status'] == 'ERROR':
                            st.error(_state['note'], icon='❌')
                else: st.warning(
                    'Необходимо указать имя и фамилию студента', icon='⚠️'
                )
        
        # --- Добавление предмета ---
        with st.form('form_add_subject', clear_on_submit=True):
            st.markdown(':red[Добавление предмета]')

            adsu_subject = st.text_input(
                'Предмет', max_chars=256, 
                placeholder='Введите наименование предмета'
            ).strip()

            if st.form_submit_button(':red[Добавить]'):
                if adsu_subject != '':
                    _state = self.staff_h.add_subject(adsu_subject)

                    if _state['status'] == 'OK':
                        st.toast(_state['note'], icon='✔️')
                    elif _state['status'] == 'ERROR':
                        st.error(_state['note'], icon='❌')
                else: st.warning(
                    'Вы не указали наименование предмета', icon='⚠️'
                )
        
        # --- Работа с баллами ---
        with st.form('form_edit_score', clear_on_submit=True):
            st.markdown(':red[Работа с баллами]')

            edsc_subject = st.selectbox(
                'Выберите предмет', options=self.staff_h.all_subjects
            )
            edsc_students = st.multiselect(
                'Выберите студента', options=self.staff_h.all_students,
                placeholder='Можно выбрать несколько'
            )

            col_edsc_mode, col_edsc_wtype, col_edsc_score = st.columns(3)
            edsc_mode = col_edsc_mode.selectbox(
                'Выберите режим', options=('Добавить баллы', 'Вычесть баллы')
            )
            edsc_wtype = col_edsc_wtype.selectbox(
                'Выберите тип работы', options=self.staff_h.all_wtypes
            )
            edsc_score = col_edsc_score.number_input(
                'Баллы (0-100)', 0, 100
            )

            if st.form_submit_button(':red[Выполнить]'):
                if edsc_students != []:
                    self.staff_h.edit_score(
                        st.session_state['username'], edsc_subject,
                        edsc_students, edsc_mode, edsc_wtype, edsc_score
                    )
                    self.enotify_h.send_score_notify(
                        st.session_state['username'], 
                        edsc_subject, edsc_students
                    )
                    st.toast('Изменения внесены в БД', icon='🔥')
                else: st.warning(
                    'Укажите хотя бы одного студента', icon='⚠️'
                )

    def __userUI(self):
        # --- Настройка датафрейма ---
        with st.sidebar:
            selected_subjects = st.multiselect(
                'Предметы', options=self.user_h.all_subjects,
                placeholder='Можно несколько'
            )
            selected_staff = st.multiselect(
                'Преподаватели', options=[el[1] for el in self.user_h.all_staff],
                placeholder='Можно несколько'
            )
            selected_wtypes = st.multiselect(
                'Тип работы', options=self.user_h.all_wtypes,
                placeholder='Можно несколько'
            )
        
        # --- Отображение датафрейма ---
        df_data = self.user_h.display_dataframe(
            st.session_state['full_name'], selected_subjects,
            selected_staff, selected_wtypes
        )
        dataframe = df(df_data)
        dataframe.index += 1
        st.dataframe(dataframe, use_container_width=True)

    def __adminUI(self):
        selector_options = (
            'Ключи',
            'Оповещения',
            'Пользователи'
        )
        selector_menu = option_menu(
            menu_title='Главная', orientation='horizontal',
            options=selector_options
        )
        

        # Ключи
        if selector_menu == selector_options[0]:
            st.write(
                f'Кол-во свободных ключей: {self.admin_h.valid_keys_count()}'
            )
            # --- Добавление/Удаление ключа ---
            with st.form('form_keys_handler', clear_on_submit=True):
                st.markdown('Добавление/Удаление ключа')

                keha_key = st.text_input(
                    'Ключ', max_chars=16, type='password'
                )

                keha_mode = st.radio(
                    'Режим работы', options=['Добавить', 'Удалить'], 
                    horizontal=True
                )

                if st.form_submit_button(':red[Выполнить]'):
                    if keha_key != '':
                        if keha_mode == 'Добавить':
                            keha_state = self.admin_h.create_key(keha_key)
                            if keha_state['status'] == 'OK':
                                st.toast(keha_state['note'], icon='✔️')
                            elif keha_state['status'] == 'ERROR':
                                st.toast(keha_state['note'], icon='❌')
                        elif keha_mode == 'Удалить':
                            keha_state = self.admin_h.delete_key(keha_key)
                            if keha_state['status'] == 'OK':
                                st.toast(keha_state['note'], icon='✔️')
                            elif keha_state['status'] == 'ERROR':
                                st.toast(keha_state['note'], icon='❌')
                    else: st.warning('Необходимо указать ключ', icon='⚠️')
        
        # Оповещения
        elif selector_menu == selector_options[1]:
            # Экспериментальная форма
            # --- Отправить почту ---
            with st.form('form_send_email', clear_on_submit=True):
                st.markdown(':red[Отправка почты]')

                seem_users = st.multiselect(
                    'Кому отправить?', options=self.admin_h.all_users_email
                )
                seem_subject = st.text_input('Заголовок')
                seem_text = st.text_area('Содержание')

                if st.form_submit_button(':red[Отправить]'):
                    if seem_users != [] and seem_subject != '' and seem_text != '':
                        self.enotify_h.send_notify(seem_users, seem_subject, seem_text)
                        st.toast('Письма отправлены', icon='🔥')
                    else: st.warning('Заполните все поля', icon='⚠️')
        # Пользователи
        elif selector_menu == selector_options[2]:
            radio = st.radio('Mode', options=['users', 'data_changes'])
            df_data = self.admin_h.display_df(radio)
            dataframe = df(df_data)
            dataframe.index += 1
            st.dataframe(dataframe, use_container_width=True)
