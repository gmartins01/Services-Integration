import sys
import time

import psycopg2
from psycopg2 import OperationalError
from utils import select_data
from utils import insert_data

sys.path.append('/shared')
from db_connection import connect_to_db_rel
from db_connection import connect_to_db_xml

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60


def print_psycopg2_exception(ex):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", ex, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", ex.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", ex.pgerror)
    print("pgcode:", ex.pgcode, "\n")


if __name__ == "__main__":

    
    while True:

        tournaments=countries=games = []
        # Connect to both databases
        db_org = None
        db_dst = None

        try:
            db_org = connect_to_db_xml()
            db_dst = connect_to_db_rel()
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_dst is None or db_org is None:
            continue

        print("Checking updates...")
        with db_org.cursor() as cursor_org:
            # Execute a SELECT query to check for any documents that were not migrated yet
            cursor_org.execute("SELECT id FROM imported_documents WHERE is_migrated = 0 and is_deleted = 0")
            records = cursor_org.fetchall()  
            for record in records:
                id = record
                # Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db
                tournaments,countries,games = select_data(db_org,db_dst,records)
                print(tournaments)
                # Execute INSERT queries in the destination db
                insert_data(db_dst,tournaments, countries, games)
                # Make sure we store somehow in the origin database that certain records were already migrated.
                cursor_org.execute("UPDATE imported_documents SET is_migrated = 1 WHERE id=%s", (id,))
                db_dst.commit()
                db_org.commit()
        

        db_org.close()
        db_dst.close()

        time.sleep(POLLING_FREQ)
