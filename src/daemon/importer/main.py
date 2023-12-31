import asyncio
import time
import uuid
import sys

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
import psycopg2

from utils.to_xml_converter import CSVtoXMLConverter

sys.path.append('/shared')
from db_connection import connect_to_db_xml

def get_csv_files_in_input_folder():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(CSV_INPUT_PATH) for f in filenames if
            os.path.splitext(f)[1] == '.csv']

def generate_unique_file_name(directory):
    return f"{directory}/{str(uuid.uuid4())}.xml"

def convert_csv_to_xml(in_path, out_path):
    converter = CSVtoXMLConverter(in_path)
    file = open(out_path, "w")
    file.write(converter.to_xml_str())

class CSVHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path):
        self._output_path = output_path
        self._input_path = input_path
        self._db_conn = connect_to_db_xml()

        # generate file creation events for existing files
        for file in [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_path) for f in filenames]:
            event = FileCreatedEvent(os.path.join(CSV_INPUT_PATH, file))
            event.event_type = "created"
            self.dispatch(event)

    async def convert_csv(self, csv_path):
        # here we avoid converting the same file again
        #check converted files in the database
        if csv_path in await self.get_converted_files():
            return

        print(f"new file to convert: '{csv_path}'")

        # we generate a unique file name for the XML file
        xml_path = generate_unique_file_name(self._output_path)

        # we do the conversion
        convert_csv_to_xml(csv_path, xml_path)
        print(f"new xml file generated: '{xml_path}'")

        f = open(xml_path, "r")
        xml_data = f.read()
        
        # store the XML document into the imported_documents table
        xml_name = os.path.basename(xml_path)
        with self._db_conn.cursor() as cur:
            cur.execute("INSERT INTO imported_documents (file_name,xml) VALUES (%s,%s)", (xml_name,xml_data))
            self._db_conn.commit()
  

        # store the CSV file in the converted_documents table
        file_size = os.stat(csv_path).st_size
        with self._db_conn.cursor() as cur:
            cur.execute("INSERT INTO converted_documents (src,file_size,dst) VALUES (%s,%s,%s)", (csv_path, file_size,xml_path))
            self._db_conn.commit()
        
    async def get_converted_files(self):
        # retrieve from the database the files that were already converted before
        with self._db_conn.cursor() as cur:
            cur.execute("SELECT src FROM converted_documents")
            converted_files = cur.fetchall()
        
        return [file[0] for file in converted_files]

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            asyncio.run(self.convert_csv(event.src_path))


if __name__ == "__main__":

    CSV_INPUT_PATH = "/csv"
    XML_OUTPUT_PATH = "/shared/output"

    # create the file observer
    observer = Observer()
    observer.schedule(
        CSVHandler(CSV_INPUT_PATH, XML_OUTPUT_PATH),
        path=CSV_INPUT_PATH,
        recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
