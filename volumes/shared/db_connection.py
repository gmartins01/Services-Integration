import psycopg2

def connect_to_db_rel():
    try:
        connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database:", error)
        raise error


def connect_to_db_xml():
    try:
        connection = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database:", error)
        raise error
