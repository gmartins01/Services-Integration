import xml.etree.ElementTree as ET

from entities.game import Game


class Tournament:

    def __init__(self, name: str):
        Tournament.counter += 1
        self._id = Tournament.counter
        self._name = name
        self._games = []

    def add_game(self, game: Game):
        self._games.append(game)

    def to_xml(self):
        el = ET.Element("Tournament")
        el.set("id", str(self._id))
        el.set("name", self._name)

        games_el = ET.Element("Games")
        for game in self._games:
            games_el.append(game.to_xml())

        el.append(games_el)

        return el

    def __str__(self):
        return f"{self._name} ({self._id})"


Tournament.counter = 0
