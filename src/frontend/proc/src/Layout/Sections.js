import GamesByTournament from "../Procedures/GamesByTournament";
import GamesByCountry from "../Procedures/GamesByCountry";
import GamesByYear from "../Procedures/GamesByYear";
import GamesByScore from "../Procedures/GamesByScore";
const Sections = [


    {
        id: "games-by-tournament",
        label: "Games by Tournament",
        content: <GamesByTournament/>
    },

    {
        id: "games-by-country",
        label: "Games by Country",
        content: <GamesByCountry/>
    },

    {
        id: "games-by-year",
        label: "Games by Year",
        content: <GamesByYear/>
    },
    {
        id: "games-by-score",
        label: "Games by Score",
        content: <GamesByScore/>
    }

];

export default Sections;