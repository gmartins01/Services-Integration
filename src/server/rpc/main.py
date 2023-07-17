import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.querys import list_tournaments
from functions.querys import list_games_by_tournament
from functions.querys import count_games_by_tournament
from functions.querys import games_by_country
from functions.querys import count_games_by_country
from functions.querys import list_countries
from functions.querys import games_by_year
from functions.querys import count_games_by_year
from functions.querys import games_by_score
from functions.querys import count_games_by_score
PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

if __name__ == "__main__":
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    with SimpleXMLRPCServer(('0.0.0.0', PORT), requestHandler=RequestHandler) as server:
        server.register_introspection_functions()

        def signal_handler(signum, frame):
            print("received signal")
            server.server_close()

            # perform clean up, etc. here...
            print("exiting, gracefully")
            sys.exit(0)

        # signals
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        # register the functions
        server.register_function(list_tournaments)
        server.register_function(list_games_by_tournament)
        server.register_function(count_games_by_tournament)
        server.register_function(games_by_country)
        server.register_function(count_games_by_country)
        server.register_function(list_countries)
        server.register_function(games_by_year)
        server.register_function(count_games_by_year)
        server.register_function(games_by_score)
        server.register_function(count_games_by_score)

        # start the server
        print(f"Starting the RPC Server in port {PORT}...")
        server.serve_forever()
