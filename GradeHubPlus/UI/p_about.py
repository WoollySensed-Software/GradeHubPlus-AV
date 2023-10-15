import streamlit as st
import time

from streamlit_extras.mention import mention
from streamlit_extras.streaming_write import write


class AboutUI:

    def setupUI(self):
        with st.sidebar:
            st.write('---')
            st.button(
                ':red[Узнать больше о нас]', on_click=self.btn1
            )
            st.button(
                ':red[Руководство для преподавателей]', on_click=self.btn2
            )
            st.button(
                ':red[Руководство для студентов]', on_click=self.btn3
            )
            st.button(
                ':red[Руководство по сайту]', on_click=self.btn4
            )
        
        # Футер
        st.subheader(':red[Связь с нами]', divider='red')
        mention(
            ':red[Почта] - woollysensed.software@gmail.com', 
            'woollysensed.software@gmail.com', 
            'https://cdn-icons-png.flaticon.com/128/732/732200.png')
        mention(
            ':red[Вконтакте] - Данила Расстригин (:red[администратор])', 
            'https://vk.com/huayrav', 
            'https://cdn-icons-png.flaticon.com/128/3536/3536582.png'
        )

    def __sample(self, id: str, speed: float):
        path = f'GradeHubPlus/Resources/Notes/{id}.txt'
        with open(path, 'r', encoding='utf-8') as f:
            line = f.readlines()
            for word in line:
                for el in word.split():
                    yield el + ' '
                    time.sleep(speed)
                else: yield '\n\n'

    def btn1(self):
        pass

    def btn2(self):
        st.header(
            'Руководство для преподавателей',
            divider='red'
        )
        # --- Таблица баллов студентов ---
        st.markdown(
            '<h3 style="text-align: center; color: red;">'+
            'Таблица баллов студентов:</h3>',
            unsafe_allow_html=True
        )
        col_1, col_2 = st.columns(2)
        with col_1:
            st.image('GradeHubPlus/Resources/Images/for_staff_guide_1.png')
        with col_2:
            write(self.__sample(1, 0.05))
        # --- Форма с добавлением студентов ---
        st.markdown(
            '<h3 style="text-align: center; color: red;">'+
            'Форма с добавлением студентов:</h3>',
            unsafe_allow_html=True
        )
        col_3, col_4 = st.columns(2)
        with col_3:
            write(self.__sample(2, 0.05))
        with col_4:
            st.image('GradeHubPlus/Resources/Images/for_staff_guide_2.png')
        # --- Форма с добавлением предметов ---
        st.markdown(
            '<h3 style="text-align: center; color: red;">'+
            'Форма с добавлением предметов:</h3>',
            unsafe_allow_html=True
        )
        col_5, col_6 = st.columns(2)
        with col_5:
            st.image('GradeHubPlus/Resources/Images/for_staff_guide_3.png')
        with col_6:
            write(self.__sample(3, 0.05))
        # --- Форма для работы с баллами ---
        st.markdown(
            '<h3 style="text-align: center; color: red;">'+
            'Форма для работы с баллами:</h3>',
            unsafe_allow_html=True
        )
        col_7, col_8 = st.columns(2)
        with col_7:
            write(self.__sample(4, 0.05))
        with col_8:
            st.image('GradeHubPlus/Resources/Images/for_staff_guide_4.png')
        # --- Напоминание ---
        st.markdown(
            '<h3 style="text-align: center; color: red;">'+
            'Напоминание по работе сайта:</h3>',
            unsafe_allow_html=True
        )
        col_9, col_10 = st.columns(2)
        with col_9:
            st.image('GradeHubPlus/Resources/Media/for_staff_guide_5.gif')
        with col_10:
            write(self.__sample(5, 0.05))
    
    def btn3(self):
        pass

    def btn4(self):
        pass
