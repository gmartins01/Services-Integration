import sys
import time

from getCoordinates import get_data

sys.path.append('/shared')
from db_connection import connect_to_db_rel

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60
ENTITIES_PER_ITERATION = int(sys.argv[2]) if len(sys.argv) >= 3 else 10

if __name__ == "__main__":
   
    while True:
        
        print(f"Getting up to {ENTITIES_PER_ITERATION} entities without coordinates...")
        
        # Retrieve a fixed amount of entities without coordinates
        with connect_to_db_rel() as connection:
            with connection.cursor() as cur:
                cur.execute("SELECT id, city FROM games where geom is null LIMIT %s", (ENTITIES_PER_ITERATION,))
                records = cur.fetchall()
                connection.commit()

        for id,city in records:
            with connect_to_db_rel() as connection:
                with connection.cursor() as cur:
                    # Use the entity information to retrieve coordinates from an external API
                    coordinates = get_data(city)
                    if len(coordinates) > 0:
                        # Update the entity with the retrieved coordinates       
                        cur.execute("UPDATE games SET geom = ST_SetSRID(ST_MakePoint(%s, %s), 4326) WHERE id = %s", (coordinates[0]['lon'],coordinates[0]['lat'], id))
                        # Submit the changes            
                        connection.commit()

        
        time.sleep(POLLING_FREQ)
