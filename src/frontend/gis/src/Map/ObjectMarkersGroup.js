import React, {useEffect, useState} from 'react';
import {LayerGroup, useMap} from 'react-leaflet';
import {ObjectMarker} from "./ObjectMarker";

function ObjectMarkersGroup() {

    const map = useMap();
    const [geom, setGeom] = useState([]);
    const [bounds, setBounds] = useState(map.getBounds());

    useEffect(() => {
        const cb = () => {
            setBounds(map.getBounds());
        }
        map.on('moveend', cb);

        return () => {
            map.off('moveend', cb);
        }
    }, []);

    useEffect(() => {
        console.log("Searching: ",bounds);
        const {_northEast: {lat: neLat, lng: neLng}, _southWest: {lat: swLat, lng: swLng}} = bounds;
        const url = `http://${process.env.REACT_APP_API_GIS_URL}/api/games?neLng=${neLng}&neLat=${neLat}&swLng=${swLng}&swLat=${swLat}`;

        fetch(url)
        .then(response => response.json())
        .then(geoJSON => {setGeom(geoJSON.features)
        })
    .catch(err => console.log(err)); 
    }, [bounds])

    return (
        <LayerGroup>
            {
                geom.map(geoJSON => <ObjectMarker key={geoJSON.properties.id} position={geoJSON.properties.geometry} geoJSON={geoJSON}/>)        
            }
    </LayerGroup>
    );
}

export default ObjectMarkersGroup;