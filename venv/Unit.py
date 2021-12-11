import time
import datetime
import psycopg2 as psql

class Unit:
    def __init__(self, dbname, user, password, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port

        # Start connection and define curser
        conn = psql.connect(f"dbname ={dbname} user = {user} password = {password} port = {port} ")
        cur = conn.cursor()
        slp = time.sleep(0.4)

        rows = cur.execute("select id,description from sellables WHERE unit_id IS NULL and description IS NOT NULL;")
        # fetch all rows that in sellable table and don't have unit_id
        rows = cur.fetchall()

        def clean_str(txt):
            txt = str(txt)
            txt = txt.replace(',', '')
            txt = txt.replace('(', '')
            txt = txt.replace(')', '')
            txt = txt.replace("'", '')
            return txt

        for elementList in rows:
            ID = elementList[0]
            elementList = elementList[1]
            curr_element = str(elementList)
            ID = clean_str(str(ID))
            list_current_element = curr_element.split(' ')
            slp

            for indexList in list_current_element:
                ele = indexList
                only_alpha = ''
                only_numeric = ''
                curr_time = ''

                for char in ele:
                    # checking whether the char is an alphabet or not using chr.isalpha() method
                    if char.isalpha():
                        only_alpha += char
                    elif char.isnumeric():
                        only_numeric += char

                if (only_numeric == '') or (only_alpha == ''):
                    slp
                    print("empty")
                    only_alpha = set('')
                    only_numeric = set('')

                else:
                    time.sleep(0.1)
                    print("Find result")
                    slp
                    unit_id = cur.execute(
                        f"SELECT id FROM units WHERE (name = '{only_numeric}') AND (measurement = '{only_alpha}');")
                    unit_id = cur.fetchone()
                    unit_id = str(unit_id)

                    if (unit_id != '') and (unit_id != 'None'):
                        unit_id = clean_str(unit_id)
                        curr_element = clean_str(curr_element)
                        print(f"Find the unit id ={unit_id}\nfor name: {only_numeric} measurement: {only_alpha}"
                              f" Description: {curr_element} ID: {id}")
                        slp
                        print("Start update value stage: ")

                        try:
                            curr_time = datetime.datetime.now()
                            curr_time = curr_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                            cur.execute(f"UPDATE sellables SET unit_id = '{unit_id}', updated_at = '{curr_time}' "
                                        f" WHERE id = '{ID}';")
                            conn.commit()
                            print('complete update')
                            print("========================================End OF CURRENT ELEMENT======================================== ")
                            slp
                        except:
                            print("There is Error-Found")
                            slp

                    else:
                        curr_element = clean_str(curr_element)
                        slp
                        print(f"Not found unit id for description = {curr_element} in Units table")

        cur.close()
        conn.close()
        print("End of execution Unit id")
        print("Exit...")
