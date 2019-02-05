import sqlite3

def db_write(df_out, fred_id):
    db = sqlite3.connect('./fcast.db')
    df_out.to_sql(f'fcast_{fred_id}', db, index = False, if_exists = 'replace')
    db.close()
# end db_write
