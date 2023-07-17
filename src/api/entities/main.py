import sys

from flask import Flask,request, jsonify
from flask_cors import CORS

sys.path.append('/shared')
from db_connection import connect_to_db_rel



PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

@app.route('/api/tournaments', methods=['GET'])
def get_tournaments():
    page = int(request.args.get('page'))
    PAGE_SIZE = int(request.args.get('pageSize'))
    offset = (page-1)*PAGE_SIZE

    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute("SELECT id,name FROM tournaments LIMIT %s OFFSET %s", (PAGE_SIZE,offset))
            tournaments = cur.fetchall()
            tournaments = [{"id": tournament[0], "name": tournament[1]} for tournament in tournaments]
            connection.commit()
    return jsonify(tournaments)

@app.route('/api/create/tournaments', methods=['POST'])
def create_tournaments():
    id = request.args.get('id')
    name = request.args.get('name')
    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute("INSERT INTO tournaments (id,name) VALUES (%s,%s) ON CONFLICT DO NOTHING", (id,name))
            connection.commit()

            return jsonify("OK")

@app.route('/api/delete/tournaments', methods=['PUT'])
def delete_tournaments():
    id = request.args.get('id')
    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute("DELETE From tournaments WHERE id=%s", (id,))
            connection.commit()

            return jsonify("OK")

@app.route('/api/update/tournaments/<int:id>', methods=['PUT'])
def update_tournaments(id):
    name = request.args.get('name')
    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute("UPDATE tournaments set name=%s WHERE id=%s", (name,id))
            connection.commit()

            return jsonify("OK")

@app.route('/api/tournaments/count/', methods=['GET'])
def get_tournaments_count():
    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM tournaments")
            count = cur.fetchone()[0]
   
    return jsonify(count)


@app.route('/api/countries', methods=['GET'])
def get_countries():
    page = int(request.args.get('page'))
    PAGE_SIZE = int(request.args.get('pageSize'))
    offset = (page-1)*PAGE_SIZE

    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute("SELECT id,name FROM countries LIMIT %s OFFSET %s", (PAGE_SIZE,offset))
            countries = cur.fetchall()
            countries = [{"id": country[0], "name": country[1]} for country in countries]
    
    return jsonify(countries)

@app.route('/api/create/countries', methods=['POST'])
def create_countries():
    id = request.args.get('id')
    name = request.args.get('name')
    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute("INSERT INTO countries (id,name) VALUES (%s,%s) ON CONFLICT DO NOTHING", (id,name))
            connection.commit()
    return jsonify("OK")

@app.route('/api/delete/countries', methods=['PUT'])
def delete_countries():
    id = request.args.get('id')
    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute("DELETE From countries WHERE id=%s", (id,))
            connection.commit()

    return jsonify("OK")

@app.route('/api/update/countries/<int:id>', methods=['PUT'])
def update_countries(id):
    name = request.args.get('name')
    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute("UPDATE countries set name=%s WHERE id=%s", (name,id))
            connection.commit()

    return jsonify("OK")

@app.route('/api/countries/count/', methods=['GET'])
def get_countries_count():
    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM countries")
            count = cur.fetchone()[0]
    
    return jsonify(count)

@app.route('/api/games', methods=['GET'])
def get_games():
    page = int(request.args.get('page'))
    PAGE_SIZE = int(request.args.get('pageSize'))
    offset = (page-1)*PAGE_SIZE

    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute(f"SELECT games.id, games.tournament_id, games.date, games.home_team, games.away_team, games.score, "
                        f"games.city, tournaments.name as tournament_name, countries.name as country_name FROM games "
                        f"INNER JOIN tournaments ON games.tournament_id = tournaments.id "
                        f"INNER JOIN countries ON games.country_id = countries.id LIMIT %s OFFSET %s", (PAGE_SIZE,offset))
            games = cur.fetchall()
            games = [{"id": game[0], "tournament_id": game[1], "date": game[2], "home_team": game[3], 
                        "away_team": game[4], "score": game[5] ,"city": game[6], "tournament_name": game[7], 
                        "country_name": game[8]} for game in games]
  
    return jsonify(games)

@app.route('/api/games/count/', methods=['GET'])
def get_games_count():
    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM games")
            count = cur.fetchone()[0]
    
    return jsonify(count)

@app.route('/api/tournaments/<int:tournament_id>/games/', methods=['GET'])
def get_games_by_tournament(tournament_id):
    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute("SELECT * FROM games WHERE tournament_id = %s", (tournament_id,))
            games = cur.fetchall()
            games = [{"id": game[0], "tournament_id": game[1], "date": game[2], "home_team": game[3], "away_team": game[4], "score": game[5] ,"city": game[6] } for game in games]

    return jsonify(games)

@app.route('/api/create/games', methods=['POST'])
def create_games():
    id              = request.args.get('id')
    tournament_id   = request.args.get('tournament_id')
    date            = request.args.get('date')
    home_team       = request.args.get('home_team')
    away_team       = request.args.get('away_team')
    score           = request.args.get('score')
    city            = request.args.get('city')
    country_id      = request.args.get('country_id')

    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute(f"INSERT INTO games (id,tournament_id,date,home_team,away_team,score,city,country_id) "
                        f"VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (id,tournament_id,date,home_team,away_team,score,city,country_id))
            connection.commit()
    return jsonify("OK")

@app.route('/api/delete/games', methods=['PUT'])
def delete_games():
    id = request.args.get('id')
    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute("DELETE FROM games WHERE id=%s", (id,))
            connection.commit()

    return jsonify("OK")

@app.route('/api/update/games/<int:id>', methods=['PUT'])
def update_games(id):
    tournament_id   = request.args.get('tournament_id')
    date            = request.args.get('date')
    home_team       = request.args.get('home_team')
    away_team       = request.args.get('away_team')
    score           = request.args.get('score')
    city            = request.args.get('city')
    country_id      = request.args.get('country_id')
    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute(f"UPDATE games set tournament_id=%s, date=%s, home_team=%s, away_team=%s, "
                        f"score=%s, city=%s, country_id=%s WHERE id=%s"
                        , (tournament_id,date,home_team,away_team,score,city,country_id,id))
            connection.commit()

    return jsonify("OK")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)