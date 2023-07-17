import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from utils.reader import CSVReader
from entities.country import Country
from entities.tournament import Tournament
from entities.game import Game


class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def to_xml(self):
        # read countries
        countries = self._reader.read_entities(
            attr="country",
            builder=lambda row: Country(row["country"])
        )


        # read tournaments
        tournaments = self._reader.read_entities(
            attr="tournament",
            builder=lambda row: Tournament(row["tournament"])
        )

        # read games
        def after_creating_game(game, row):
            # add the game to the appropriate tournament
            tournaments[row["tournament"]].add_game(game)

        self._reader.read_entities(
            attr="date",
            builder=lambda row: Game(
                date=row["date"],
                home_team=row["home_team"],
                away_team=row["away_team"],
                home_score=row["home_score"],
                away_score=row["away_score"],
                city=row["city"],
                country=countries[row["country"]]
            ),
            after_create=after_creating_game
        )

        # generate the final xml
        root_el = ET.Element("InternationalGames")

        tournaments_el = ET.Element("Tournaments")
        for tournament in tournaments.values():
            tournaments_el.append(tournament.to_xml())

        countries_el = ET.Element("Countries")
        for country in countries.values():
            countries_el.append(country.to_xml())
        
        root_el.append(tournaments_el)
        root_el.append(countries_el)

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()

