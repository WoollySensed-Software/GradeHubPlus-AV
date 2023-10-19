import streamlit as st

from streamlit_option_menu import option_menu
from GradeHubPlus.Config.settings import HIDE_FOOTER, VERSION
from GradeHubPlus.UI.p_about import AboutUI
from GradeHubPlus.UI.p_authorization import AuthorizationUI
from GradeHubPlus.UI.p_homepage import HomepageUI
from GradeHubPlus.UI.p_profile import ProfileUI


# --- Состояние сессии ---
if 'auth_status' not in st.session_state:
    st.session_state['auth_status'] = False
if 'full_name' not in st.session_state:
    st.session_state['full_name'] = ''
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'staff_value' not in st.session_state:
    st.session_state['staff_value'] = ''
if 'selector_options' not in st.session_state:
    st.session_state['selector_options'] = (
        'Авторизация', 'Информация'
    )

# --- Параметры страницы ---
st.set_page_config(
    page_title='GradeHub+',
    page_icon='GradeHubPlus/Resources/Icons/ghp_icon.png', 
    layout='wide'
)
st.markdown(HIDE_FOOTER, unsafe_allow_html=True)

with st.sidebar:
    selector_menu = option_menu(
        menu_title=None, 
        options=st.session_state['selector_options'], 
        styles=None
    )
    st.markdown(VERSION) # Версия и патч

# --- До авторизации ---
if not st.session_state['auth_status']:
    if selector_menu == 'Авторизация':
        st.image(
            'GradeHubPlus/Resources/Images/GHP_full_logo.png', 
            output_format='PNG'
        )
        authorizationUI = AuthorizationUI()
        authorizationUI.setupUI()
    elif selector_menu == 'Информация':
        aboutUI = AboutUI()
        aboutUI.setupUI()
# --- После авторизации ---
else:
    if selector_menu == 'Главная':
        homepageUI = HomepageUI(st.session_state['staff_value'])
        homepageUI.setupUI()
    elif selector_menu == 'Профиль':
        profileUI = ProfileUI()
        profileUI.setupUI()
    elif selector_menu == 'Информация':
        aboutUI = AboutUI()
        aboutUI.setupUI()
