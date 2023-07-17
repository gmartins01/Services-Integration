import sys

from flask import Flask, request, jsonify

from flask_cors import CORS

sys.path.append('/shared')
from db_connection import connect_to_db_rel

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

@app.route('/api/games', methods=['GET'])
def get_games():
    neLng = request.args.get('neLng')
    neLat = request.args.get('neLat')
    swLng = request.args.get('swLng')
    swLat = request.args.get('swLat')
    query = f"SELECT games.id, games.tournament_id, games.date, games.home_team, games.away_team, games.score, games.city,ST_X(games.geom) as lng, ST_Y(games.geom) as lat, games.country_id, tournaments.name FROM games JOIN tournaments ON games.tournament_id = tournaments.id WHERE games.geom is not null AND games.geom &&  ST_MakeEnvelope(%s,%s,%s,%s, 4326)"

    with connect_to_db_rel() as connection:
        with connection.cursor() as cur:
            cur.execute(query, (neLng, neLat, swLng, swLat))
            results = cur.fetchall()
    
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    for result in results:
        feature = {
            "type": "feature",
            "geometry": {
                "type": "Point",
                "coordinates": [result[8], result[7]]
            },
            "properties": {
                "id": result[0],
                "coordinates": [result[8], result[7]],
                "tournament_name": result[10],
                "date": result[2],
                "home_team": result[3],
                "away_team": result[4],
                "score": result[5],
                "city": result[6],
                "country_id": result[9],
                "imgUrl": "https://cdn-icons-png.flaticon.com/512/1800/1800944.png"
            }
        }
        
        geojson["features"].append(feature)
    
    return jsonify(geojson)
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
