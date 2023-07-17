import sys
import psycopg2

sys.path.append('/shared')
from db_connection import connect_to_db_xml

def list_tournaments():

    data = []
    query=("select unnest(xpath('//Tournaments/Tournament/@name',xml))::text as name," +
           " unnest(xpath('//Tournaments/Tournament/@id',xml))::text::int as id" +
            " from imported_documents where is_deleted=0 ORDER BY name;")
    try:
        with connect_to_db_xml() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                tournaments = cursor.fetchall()
                data = [{"id": tournament[1],"name": tournament[0]} for tournament in tournaments]
                connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data:", error)
    return data

def list_countries():
    
    data = []
    query = ("select unnest(xpath('//Countries/Country/@name',xml))::text as name," +
        " unnest(xpath('//Countries/Country/@id',xml))::text::int as id" +
        " from imported_documents where is_deleted=0 ORDER BY name;")

    try:
        with connect_to_db_xml() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                countries = cursor.fetchall()
                data = [{"id": country[1],"name": country[0]} for country in countries]
                connection.commit()

    except(Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)


    return data

def list_games_by_tournament(tournament_id,offset,PAGE_SIZE):

    data = []
    query = ("select awayteam,hometeam, score, date" +
    " from(select unnest(xpath('//Tournaments/Tournament[@id=\"" + tournament_id +"\"]/Games/Game/score/text()', xml))::text as score,"+
    " unnest(xpath('//Tournaments/Tournament[@id=\"" + tournament_id +"\"]/Games/Game/home_team/text()', xml))::text as hometeam," +
    " unnest(xpath('//Tournaments/Tournament[@id=\"" + tournament_id +"\"]/Games/Game/away_team/text()', xml))::text as awayteam," +
    " unnest(xpath('//Tournaments/Tournament[@id=\"" + tournament_id +"\"]/Games/Game/date/text()', xml))::text as date" +
    " from imported_documents where is_deleted=0 LIMIT "+ str(PAGE_SIZE)+  " OFFSET "+ str(offset) +
    " ) as g" +
    " ORDER BY date;")

    try:
        with connect_to_db_xml() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                games = cursor.fetchall()
                data = [{"away_team": game[0], "home_team": game[1],"score":game[2],"date":game[3]} for game in games]
                connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    return data

def count_games_by_tournament(tournament_id):

    count=0
    query = ("SELECT unnest(xpath('count(//Tournaments/Tournament[@id=\"" + tournament_id +"\"]" +
                "/Games/Game/@id)',xml))::text::int  as numero_jogos" +
                " FROM imported_documents WHERE is_deleted = 0"
                )
    try:
        with connect_to_db_xml() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                count = cursor.fetchone()[0]
                connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    return count


def games_by_country(country_id,offset,PAGE_SIZE):

    data=[]
    query = ("SELECT "+
                "unnest(xpath('Game/home_team/text()', games))::text as home_team, " +
                "unnest(xpath('Game/away_team/text()', games))::text as away_team, " +
                "unnest(xpath('Game/score/text()', games))::text as score, " +
                "unnest(xpath('Game/date/text()', games))::text as date " +
            "FROM ("+
                "SELECT unnest(xpath('//Tournaments/Tournament/Games/Game[country/@country_ref=\""+country_id+"\"]', xml)) as games " +
                "FROM imported_documents " +
                "WHERE is_deleted = 0 LIMIT "+ str(PAGE_SIZE)+  " OFFSET "+ str(offset) +
            ") as t")

    try:
        with connect_to_db_xml() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                games = cursor.fetchall()
                data = [{"home_team": game[0], "away_team": game[1],"score":game[2],
                        "date":game[3]
                    } for game in games]
                connection.commit()

    except(Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    return data

def count_games_by_country(country_id):

    count=0
    query = ("select id "+
        "from(Select UNNEST(xpath('count(//Tournaments/Tournament/Games/Game/country[@country_ref=\""+str(country_id)+"\"])',xml))::text as id "+
        "from imported_documents where is_deleted=0 "+
        "group by id) as g group by g.id;")
    try:
        with connect_to_db_xml() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                count = cursor.fetchone()[0]
                connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    
    return count

def games_by_year(year,offset,PAGE_SIZE):

    data=[]
    
    query=("select date,home_team,away_team,score "+ 
            "from (SELECT UNNEST(xpath('//Tournaments/Tournament/Games/Game[substring(date/text(), 1, 4) = \""+str(year)+"\"]/date/text()',xml))::text as date, "+ 
            "UNNEST(xpath('//Tournaments/Tournament/Games/Game[substring(date/text(), 1, 4) = \""+str(year)+"\"]/home_team/text()',xml))::text as home_team, "+
            "UNNEST(xpath('//Tournaments/Tournament/Games/Game[substring(date/text(), 1, 4) = \""+str(year)+"\"]/away_team/text()',xml))::text as away_team, "+ 
            "UNNEST(xpath('//Tournaments/Tournament/Games/Game[substring(date/text(), 1, 4) = \""+str(year)+"\"]/score/text()',xml))::text as score "+
            "from imported_documents where is_deleted=0) as g "+
            "group by g.date,g.home_team,g.away_team,g.score LIMIT "+ str(PAGE_SIZE)+  " OFFSET "+ str(offset) +";")

    try:
        with connect_to_db_xml() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)      
                data = cursor.fetchall()
                data=[{"date":game[0],"home_team":game[1],"away_team":game[2],"score":game[3]} for game in data]
                connection.commit()

    except(Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)


    return data

def count_games_by_year(year):
    query = ("select id "+
        "from(Select UNNEST(xpath('count(//Tournaments/Tournament/Games/Game[substring(date/text(), 1, 4) = \""+str(year)+"\"])',xml))::text as id "+
        "from imported_documents where is_deleted=0 "+
        "group by id) as g group by g.id;")
    try:
        with connect_to_db_xml() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                count = cursor.fetchone()[0]
                connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    
    return count


def games_by_score(score,offset,PAGE_SIZE):

    data=[]
    
    query=("select date,home_team,away_team,score "+ 
            "from (SELECT UNNEST(xpath('//Tournaments/Tournament/Games/Game[substring(score/text(), 1, 4) = \""+str(score)+"\"]/date/text()',xml))::text as date, "+ 
            "UNNEST(xpath('//Tournaments/Tournament/Games/Game[substring(score/text(), 1, 4) = \""+str(score)+"\"]/home_team/text()',xml))::text as home_team, "+
            "UNNEST(xpath('//Tournaments/Tournament/Games/Game[substring(score/text(), 1, 4) = \""+str(score)+"\"]/away_team/text()',xml))::text as away_team, "+ 
            "UNNEST(xpath('//Tournaments/Tournament/Games/Game[substring(score/text(), 1, 4) = \""+str(score)+"\"]/score/text()',xml))::text as score "+
            "from imported_documents where is_deleted=0) as g "+
            "group by g.date,g.home_team,g.away_team,g.score LIMIT "+ str(PAGE_SIZE)+  " OFFSET "+ str(offset) +";")

    try:
        with connect_to_db_xml() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)      
                data = cursor.fetchall()
                data=[{"date":game[0],"home_team":game[1],"away_team":game[2],"score":game[3]} for game in data]
                connection.commit()

    except(Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)


    return data

def count_games_by_score(score):
    query = ("select id "+
        "from(Select UNNEST(xpath('count(//Tournaments/Tournament/Games/Game[substring(score/text(), 1, 4) = \""+str(score)+"\"])',xml))::text as id "+
        "from imported_documents where is_deleted=0 "+
        "group by id) as g group by g.id;")
    try:
        with connect_to_db_xml() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                count = cursor.fetchone()[0]
                connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    
    return count