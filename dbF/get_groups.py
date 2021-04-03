import sqlite3

sqlite_connection= sqlite3.connect('db.db')

def get_groups(id_):
    cursor = sqlite_connection.cursor()
    sqlite_select_query = f"""SELECT group_ids from User_info WHERE root_id = {id_}"""
    cursor.execute(sqlite_select_query)

    res = cursor.fetchall()
    cursor.close()

    return res

def add_group(id_, group_ids):
    cursor = sqlite_connection.cursor()
    sqlite_select_query = f"""INSERT INTO User_info VALUES ({id_},'{' '.join([str(x) for x in group_ids])}')"""
    
    cursor.execute(sqlite_select_query)
    sqlite_connection.commit()
    
    cursor.close()

if __name__ == "__main__":
    print(get_groups(22))

