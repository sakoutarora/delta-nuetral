import psycopg2
import json
from dependencies.utils import is_non_emplty_list

class DataBaseManager:
    def __init__(self) -> None:
        dev_config = {'database':'postgres', 'user':'postgres', 'password':'admin', 'host':'localhost', 'port':5432}
        self.con  = psycopg2.connect(**dev_config)

        cursor = self.con.cursor()
        cursor.execute('SELECT * FROM public.posdb LIMIT 1')
        self.column_names = [desc[0] for desc in cursor.description]

    def today_status(self, stamp):
        cursor = self.con.cursor()
        if stamp:
            print(f'TODAYS DATA {stamp}')
            cursor.execute(f"SELECT * from public.posdb where session_id = (SELECT max(session_id) from public.posdb where pos = true and session_id >= '{stamp}')")
            datas = cursor.fetchall()
            if is_non_emplty_list(datas):
                return datas[0]
            else:
                return None
        return None