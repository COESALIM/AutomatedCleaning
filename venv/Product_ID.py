import psycopg2 as psql
import datetime
import time

class products:
    def __init__(self, dbname, user, password, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port

        # start connection
        conn = psql.connect(f"dbname ={dbname} user = {user} password = {password} port = {port} ")
        cur = conn.cursor()
        
        slp = time.sleep(0.4)

        # execute command
        try:
            rows = cur.execute("SELECT product_id, department FROM sellables WHERE (department IS NOT NULL) AND (product_id IS NOT NULL);")
            rows = cur.fetchall()
            print("Completed to find [department not null and product_id not null]")
            slp
        except:
            print("Error in finding [department not null and product_id not null]")
            slp

        #function to clean string from special characters
        def clean_str(txt):
            txt = str(txt)
            txt = txt.replace(',', '')
            txt = txt.replace('(', '')
            txt = txt.replace(')', '')
            txt = txt.replace("'", '')
            return txt

        print("Fetching info .. ")
        for row in rows:
            curr_product_id = row[0]
            curr_department = row[1]

            curr_product_id = clean_str(str(curr_product_id))
            curr_department = clean_str(str(curr_department))
            print("Product_id: ",curr_product_id, "\nCurrent department: ",curr_department)
            slp

            try:
                search_none_product_id = cur.execute(f"SELECT id, department FROM sellables WHERE (department IS NOT NULL) AND (product_id IS NULL);")
                search_none_product_id = cur.fetchall()
                print("Completed to find [department not null and product_id null]")
                slp
            except:
                print("Error in finding [department not null and product_id null]")
                slp
            
            for search_element in search_none_product_id:
                curr_time = ''
                id = search_element[0]
                search_department = search_element[1]
                id = clean_str(id)
                search_department = clean_str(search_department)

                print(f"fetched product_id: {curr_product_id} for:\ndepartment:{search_department}")
                
                if search_department == curr_department:
                    print("There is SKU have same [department] and don't have [product_id]")
                    print(f"Start insert [product_id]:{curr_product_id} for SKU ID: {id} ...")
                    slp
                    
                    try:
                        curr_time = datetime.datetime.now()
                        curr_time = curr_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                        cur.execute(f"UPDATE sellables SET product_id = '{curr_product_id}', updated_at = '{curr_time}' where id = '{id}'")
                        conn.commit()
                        print("Complete Update...")
                        print("==========================================================================")
                        slp
                    except:
                        print("Update value Error...")
                        slp

                else:
                    print("Not found SKU have The same [department] and don't have [product_id]")

        cur.close()
        conn.close()
        print("End execution of Product id")
        print("Exit...")
