import {Avatar, List, ListItem, ListItemIcon, ListItemText} from "@mui/material";
import ScoreboardIcon from '@mui/icons-material/Scoreboard';
import LocationCityIcon from '@mui/icons-material/LocationCity';
import HomeIcon from '@mui/icons-material/Home';
import LocalAirportIcon from '@mui/icons-material/LocalAirport';
import PictureInPictureAltIcon from '@mui/icons-material/PictureInPictureAlt';
import React from "react";
import {Marker, Popup} from 'react-leaflet';
import {icon as leafletIcon, point} from "leaflet";

const LIST_PROPERTIES = [
    {"key": "home_team", label: "Home Team", Icon: HomeIcon},
    {"key": "away_team", label: "Away Team", Icon: LocalAirportIcon},
    {"key": "score", label: "Score", Icon: ScoreboardIcon},
    {"key": "city", label: "City", Icon: LocationCityIcon},
    {"key": "coordinates", label: "Position", Icon: PictureInPictureAltIcon}
];

export function ObjectMarker({geoJSON}) {
    const properties = geoJSON?.properties
    const {id, imgUrl, tournament_name} = properties;
    const coordinates = geoJSON?.geometry?.coordinates;
 
    return (
        <Marker
            position={coordinates}
            icon={leafletIcon({
                iconUrl: imgUrl,
                iconRetinaUrl: imgUrl,
                iconSize: point(50, 50),
            })}
        >
            <Popup>
                <List dense={true}>
                    <ListItem>
                        <ListItemIcon>
                            <Avatar alt={tournament_name} src={imgUrl}/>
                        </ListItemIcon>
                        <ListItemText primary={tournament_name}/>
                    </ListItem>
                    {
                        LIST_PROPERTIES
                            .map(({key, label, Icon}) =>
                                <ListItem key={key}>
                                    <ListItemIcon>
                                        <Icon style={{color: "black"}}/>
                                    </ListItemIcon>
                                    <ListItemText
                                        primary={<span>
                                        {properties[key]}<br/>
                                        <label style={{fontSize: "xx-small"}}>({label})</label>
                                    </span>}
                                    />
                                </ListItem>
                            )
                    }

                </List>

            </Popup>
        </Marker>
    )
}