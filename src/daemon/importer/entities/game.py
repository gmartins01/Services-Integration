import xml.etree.ElementTree as ET


class Game:

    def __init__(self, date, home_team,away_team,home_score,away_score,city,country):
        Game.counter += 1
        self._id = Game.counter
        self._date = date
        self._home_team = home_team
        self._away_team = away_team
        self._home_score = home_score
        self._away_score = away_score
        self._city = city
        self._country = country

    def to_xml(self):
        el = ET.Element("Game")
        el.set("id", str(self._id))
       
        date_el = ET.SubElement(el, "date")
        date_el.text = self._date

        home_team_el = ET.SubElement(el, "home_team")
        home_team_el.text = self._home_team

        away_team_el = ET.SubElement(el, "away_team")
        away_team_el.text = self._away_team
        
        score_el = ET.SubElement(el, "score")
        score_el.text = f"{self._home_score}-{self._away_score}"
        
        city_el = ET.SubElement(el, "city")
        city_el.text = self._city

        country_el = ET.SubElement(el, "country")
        country_el.set("country_ref", str(self._country.get_id()))

        

        return el

    def __str__(self):
        return f"date: {self._date},home_team: {self._home_team}, away_team: {self._away_team}" \
                f",home_score: {self._home_score},away_score: {self._away_score},country:{self._country}"

Game.counter = 0
