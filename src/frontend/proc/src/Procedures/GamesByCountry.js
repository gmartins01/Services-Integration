import React, {useEffect, useState} from "react";
import {Box, 
    CircularProgress, 
    Container, 
    FormControl, 
    InputLabel, 
    MenuItem, 
    Select,
    Pagination,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
} from "@mui/material";


function GamesByCountry() {

    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);

    const [selectedCountry, setSelectedCountry] = useState("");
    const [countries, setCountries] = useState([]);
    const [maxDataSize, setMaxDataSize] = useState(0);

    const [procData, setProcData] = useState(null);
    
    useEffect(() => {
        fetch(`http://${process.env.REACT_APP_API_PROC_URL}/api/countries`)
            .then(response => response.json())
            .then(data => setCountries(data));
    }, []);
    
    useEffect(() => {
        setProcData(null);
    
        if (selectedCountry) {
            
            console.log(`fetching from ${process.env.REACT_APP_API_PROC_URL}/api/games_by_country?country=${selectedCountry}`);
            fetch(`http://${process.env.REACT_APP_API_PROC_URL}/api/games_by_country?country=${selectedCountry}&page=${page}&pageSize=${PAGE_SIZE}`)
            .then(response => response.json())
            .then(data => {setProcData(data);});
            
            fetch(`http://${process.env.REACT_APP_API_PROC_URL}/api/count/games_by_country?country=${selectedCountry}`)
            .then(response => response.json())
            .then(jsonData => setMaxDataSize(jsonData));

        }
    }, [selectedCountry,page])


    return (
        <>
            <h1>Games by Country</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Options</h2>
                    <FormControl fullWidth>
                        <InputLabel id="countries-select-label">Country</InputLabel>
                        <Select
                            labelId="countries-select-label"
                            id="demo-simple-select"
                            value={selectedCountry}
                            label="Country"
                            onChange={(e, v) => {
                                setSelectedCountry(e.target.value);
                                setPage(1)
                            }}
                        >
                            {countries.map(country => (
                                <MenuItem key={country.id} value={country.id}>
                                    {country.name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Box>
            </Container>

           <h3>Number of results: {maxDataSize}</h3>
            <TableContainer component={Paper} style={{marginTop: 20}}>
                <Table sx={{minWidth: 650}} aria-label="simple table" >
                    <TableHead>
                        <TableRow>
                            <TableCell align="center">Home Team</TableCell>
                            <TableCell align="center">Away Team</TableCell>
                            <TableCell align="center">Score</TableCell>
                            <TableCell align="center">Date</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            procData ?
                            procData.map((row,index) => (
                                    <TableRow
                                        key={index}
                                        style={{background: "gray", color: "black"}}
                                    >
                                        <TableCell component="td" align="center" scope="row">
                                            {row.home_team}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.away_team}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.score}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.date}
                                        </TableCell>
                                    </TableRow>
                                ))
                                :
                                <TableRow>
                                    <TableCell colSpan={3}>
                                        <CircularProgress/>
                                    </TableCell>
                                </TableRow>
                        }
                    </TableBody>
                </Table>
            </TableContainer>

            {
                <div style={{background: "black", padding: "1rem"}}>
                    <Pagination style={{color: "black"}}
                                variant="outlined" shape="rounded"
                                color={"primary"}
                                onChange={(e, v) => {
                                    setPage(v)
                                }}
                                page={page}
                                count={Math.ceil(maxDataSize / PAGE_SIZE)}
                    />
                </div>
            }

        </>
    );
}

export default GamesByCountry;
