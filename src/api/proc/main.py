import sys
import xmlrpc.client
from flask_cors import CORS

from flask import Flask,request, jsonify

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000


app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

@app.route('/api/tournaments', methods=['GET'])
def get_tournaments():
    server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
    result = server.list_tournaments()
    return jsonify(result)

@app.route('/api/countries', methods=['GET'])
def get_countries():
    server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
    result = server.list_countries()
    return jsonify(result)

@app.route('/api/games_by_tournament', methods=['GET'])
def get_games_by_tournament():
    tournament = request.args.get('tournament')
    page = int(request.args.get('page'))
    PAGE_SIZE = int(request.args.get('pageSize'))
    offset = (page-1)*PAGE_SIZE

    server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
    result = server.list_games_by_tournament(tournament,offset,PAGE_SIZE)

    return jsonify(result)

@app.route('/api/count/games_by_tournament', methods=['GET'])
def count_games_by_tournament():
    tournament = request.args.get('tournament')
    server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
    result = server.count_games_by_tournament(tournament)
    return jsonify(result)


@app.route('/api/games_by_country', methods=['GET'])
def games_by_country():
    country= request.args.get('country')
    page = int(request.args.get('page'))
    PAGE_SIZE = int(request.args.get('pageSize'))
    offset = (page-1)*PAGE_SIZE

    server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
    results = server.games_by_country(country,offset,PAGE_SIZE)

    return jsonify(results)


@app.route('/api/count/games_by_country', methods=['GET'])
def count_games_by_country():
    country = request.args.get('country')
    server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
    result = server.count_games_by_country(country)
    return jsonify(result)

@app.route('/api/games_by_year', methods=['GET'])
def games_by_year():
    year= request.args.get('year')
    page = int(request.args.get('page'))
    PAGE_SIZE = int(request.args.get('pageSize'))
    offset = (page-1)*PAGE_SIZE

    server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
    results = server.games_by_year(year,offset,PAGE_SIZE)

    return jsonify(results)

@app.route('/api/count/games_by_year', methods=['GET'])
def count_games_by_year():
    year= request.args.get('year')
    server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
    results = server.count_games_by_year(year)

    return jsonify(results)

@app.route('/api/games_by_score', methods=['GET'])
def games_by_score():
    score= request.args.get('score')
    page = int(request.args.get('page'))
    PAGE_SIZE = int(request.args.get('pageSize'))
    offset = (page-1)*PAGE_SIZE

    server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
    results = server.games_by_score(score,offset,PAGE_SIZE)

    return jsonify(results)

@app.route('/api/count/games_by_score', methods=['GET'])
def count_games_by_score():
    score= request.args.get('score')
    server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
    results = server.count_games_by_score(score)

    return jsonify(results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
