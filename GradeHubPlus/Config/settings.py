from streamlit import secrets as ss
from datetime import datetime as dt


DETA_KEY = ss['DATABASE']['KEY']
EMAIL = ss['NOTIFY']['EMAIL']
PW = ss['NOTIFY']['PW']
SERVER = ss['NOTIFY']['SERVER']
PORT = ss['NOTIFY']['PORT']

HIDE_FOOTER = '<style>footer {visibility: hidden;}</style>'

_dt = dt.now()
_datetime = (
    f'{_dt.day}.{_dt.month}.{_dt.year}' + 
    ' | ' + 
    f'{_dt.hour+3}:{_dt.minute}'
)
_version = '1.1.6'  # TODO: не забывать менять!
VERSION = f'Версия: {_version}\n\nПатч: {_datetime}'
