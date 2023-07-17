import psycopg2

def select_data(db_org, db_dst,records):
    tournament_data = []
    country_data = []
    game_data = []

    for record in records:
        id = record

        # retrieve the data from the XML database
        with db_org.cursor() as cursor_org:
            cursor_org.execute(f"SELECT unnest(xpath('//Tournaments/Tournament/@name', xml)) as name, "
            f"unnest(xpath('//Tournaments/Tournament/@id', xml)) as id "
            f"from imported_documents where is_deleted = 0 and id = %s", (id,))
            tournament_data = cursor_org.fetchall()

            cursor_org.execute("SELECT unnest(xpath('//Countries/Country/@name', xml)) as name, "
            f"unnest(xpath('//Countries/Country/@id', xml)) as id "
            f"from imported_documents where is_deleted = 0 and id = %s", (id,))
            country_data = cursor_org.fetchall()
            
            cursor_org.execute(f"WITH "
                                f"tournaments AS ("
                                    f"SELECT unnest(xpath('//Tournament', xml)) as tournament "
                                    f"FROM imported_documents "
                                    f"WHERE id = %s and is_deleted=0"
                                f"), games AS ("
                                    f"SELECT " 
                                        f"(xpath('/Tournament/@id', tournament))[1]::text::int as tournament_id, "
                                        f"unnest(xpath('//Game', tournament)) as game "
                                    f"FROM tournaments"
                                f") SELECT *, "
                                    f"(xpath('/Game/@id', game))[1]::text::int as game_id, "
                                    f"(xpath('/Game/date/text()', game))[1]::text as date, "
                                    f"(xpath('/Game/home_team/text()', game))[1]::text as home_team, "
                                    f"(xpath('/Game/away_team/text()', game))[1]::text as away_team, "
                                    f"(xpath('/Game/score/text()', game))[1]::text as score, "
                                    f"(xpath('/Game/city/text()', game))[1]::text as city, "
                                    f"(xpath('/Game/country/@country_ref', game))[1]::text::int as country_id "
                                f"FROM "
                                f"games;",(id,))
            game_data = cursor_org.fetchall()


    # create a list to store the tournament data that needs to be migrated
    tournaments_to_migrate = []
    for name,id in tournament_data:
        # check if the tournament already exists in the relational database
        with db_dst.cursor() as cursor_dst:
            cursor_dst.execute("SELECT * FROM tournaments WHERE name = %s", (name,))
            if cursor_dst.fetchone() is None:
                # if the tournament does not exist, add it to the list of tournaments to migrate
                tournaments_to_migrate.append({'name': name, 'id': id})

    countries_to_migrate = []
    for name,id in country_data:
        # check if the country already exists in the relational database
        with db_dst.cursor() as cursor_dst:
            cursor_dst.execute("SELECT * FROM countries WHERE name = %s", (name,))
            if cursor_dst.fetchone() is None:
                # if the country does not exist, add it to the list of tournaments to migrate
                countries_to_migrate.append({'name': name, 'id': id})

    games_to_migrate = []
    for tournament_id, game, game_id, date, home_team, away_team, score, city, country_id in game_data:
        # check if the game already exists in the relational database
        with db_dst.cursor() as cursor_dst:
            cursor_dst.execute("SELECT * FROM games WHERE id = %s", (game_id,))
            if cursor_dst.fetchone() is None:
                # if the game does not exist, add it to the list of games to migrate
                games_to_migrate.append({'tournament_id':tournament_id,'id':game_id,
                                        'date': date, 'home_team': home_team, 
                                        'away_team': away_team,'score': score, 
                                        'city': city, 'country_id': country_id})

    return tournaments_to_migrate,countries_to_migrate,games_to_migrate



def insert_data(db,tournaments, countries, games):

    with db.cursor() as cursor:
        # Insert data into tournaments table
        for tournament in tournaments:
            cursor.execute("INSERT INTO tournaments (id,name) VALUES (%s,%s)", (tournament['id'],tournament['name']))
        
        # Insert data into countries table
        for country in countries:
            cursor.execute("INSERT INTO countries (id,name) VALUES (%s,%s)", (country['id'],country['name']))


        # Insert data into games table
        for game in games:
            cursor.execute(f"INSERT INTO games (id,tournament_id, date, home_team, away_team, score, city, country_id) " 
                        f"VALUES (%s, %s, %s, %s, %s, %s, %s,%s)", 
                        (game['id'],game['tournament_id'], game['date'], 
                        game['home_team'], game['away_team'], game['score'], 
                        game['city'], game['country_id']))
        

    