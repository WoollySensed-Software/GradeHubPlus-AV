import streamlit as st

from streamlit_extras.mention import mention


class AboutUI:

    def setupUI(self):
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
