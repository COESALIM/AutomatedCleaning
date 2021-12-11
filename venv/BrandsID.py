import time
import datetime
import psycopg2 as psql

class BrandsId:
    def __init__(self, dbname, user, password, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port

        slp = time.sleep(0.4)

        def rep(txt):
            txt = str(txt)
            txt = txt.replace("'", "")
            return txt


        try:
            conn = psql.connect(f"dbname ={dbname} user = {user} password = {password} port = {port}")
            cur = conn.cursor()
            print("Connected to the Database")
            slp
        except:
            print("The connection fail")
            slp

        # try to fetch name, id from brands table
        try:
            brands = cur.execute("SELECT id,name FROM brands WHERE (id IS NOT NULL) AND ((name IS NOT NULL) AND (name NOT LIKE ''));")
            brands = cur.fetchall()
            print("correct fetching from Brands table")
            slp
        except:
            print("Error fetch from Brands table...")
            slp


        for brand in brands:
            brand_id = str(brand[0])
            brand_name = rep(str(brand[1]))
            brand_name_upper = rep(brand_name.upper())

            print(f"Brand name:{brand_name}", f"Brand id:{brand_id}, upper case :{brand_name_upper}")
            slp

            try:
                # search in name in sellables table
                namesAndDescriptions = cur.execute(f"SELECT id,name,description FROM sellables WHERE ((name LIKE '{brand_name}%') OR (description LIKE '{brand_name_upper}%') AND (brand_id IS NULL));")
                namesAndDescriptions = cur.fetchall()
                print("completed fetch names and description")
                slp

                # search by brands name with names or description in sellables
                for name in namesAndDescriptions:
                    name_id = str(name[0])
                    name_name = rep(str(name[1]))
                    description_name = rep(str(name[2]))

                    print(f" SKU id:{name_id},SKU name:{name_name}, SKU description:{description_name} Key word:{brand_name}")

                    if (brand_name in name_name) or (brand_name_upper in description_name):

                        try:
                            curr_time = datetime.datetime.now()
                            curr_time = curr_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                            cur.execute(
                                f"UPDATE sellables SET brand_id = '{brand_id}', updated_at = '{curr_time}' WHERE id = '{name_id}';")
                            conn.commit()
                            print(f"UPDATE is complete for SKU: {name_id}")
                        except:
                            print("error update...")
                            slp
                    else:
                        print("not found name by name in brands...")
                        slp

            except:
                print("Error fetch from sellables table names...")
                slp

        cur.close()
        conn.close()
        print("End execution of Brand id")
        print("Exit...")