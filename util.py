import mysql.connector

def runSql(sql_query, input_data):
    connection = mysql.connector.connect(host='localhost',
                                                database='bms',
                                                user='root',
                                            password='')
    cursor = connection.cursor()
    '''
    sql_query = """UPDATE bankguarantee SET renewalprocessed=%s WHERE sid=%s"""
    input_data = (value,sid)
    '''   
    cursor.execute(sql_query, input_data)
    connection.commit()
    cursor.close()
    connection.close()