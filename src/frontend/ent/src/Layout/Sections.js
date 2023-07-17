import Games from "../Tables/Games";
import Countries from "../Tables/Countries";
import Tournaments from "../Tables/Tournaments";


const Sections = [

    {
        id: "games",
        label: "Games",
        content: <Games/>
    },

    {
        id: "tournaments",
        label: "Tournaments",
        content: <Tournaments/>
    },

    {
        id: "countries",
        label: "Countries",
        content: <Countries/>
    }

];

export default Sections;