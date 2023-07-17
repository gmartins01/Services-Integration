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


function GamesByTournament() {

    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);

    const [selectedTournament, setselectedTournament] = useState("");
    const [tournaments, setTournaments] = useState([]);
    const [maxDataSize, setMaxDataSize] = useState(0);

    const [procData, setProcData] = useState(null);
    
    useEffect(() => {
        // Fetch the tournaments from the API
        fetch(`http://${process.env.REACT_APP_API_PROC_URL}/api/tournaments`)
            .then(response => response.json())
            .then(data => setTournaments(data));
    }, []);
    

    useEffect(() => {
        setProcData(null);
    
        if (selectedTournament) {
            
            console.log(`fetching from ${process.env.REACT_APP_API_PROC_URL}/api/games_by_tournament?tournament=${selectedTournament}`);
            fetch(`http://${process.env.REACT_APP_API_PROC_URL}/api/games_by_tournament?tournament=${selectedTournament}&page=${page}&pageSize=${PAGE_SIZE}`)
            .then(response => response.json())
            .then(data => {setProcData(data);});
            
            fetch(`http://${process.env.REACT_APP_API_PROC_URL}/api/count/games_by_tournament?tournament=${selectedTournament}`)
            .then(response => response.json())
            .then(jsonData => setMaxDataSize(jsonData));

        }
    }, [selectedTournament,page])


    return (
        <>
            <h1>Games by Tournament</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Options</h2>
                    <FormControl fullWidth>
                        <InputLabel id="tournaments-select-label">Tournament</InputLabel>
                        <Select
                            labelId="tournaments-select-label"
                            id="demo-simple-select"
                            value={selectedTournament}
                            label="Tournament"
                            onChange={(e, v) => {
                                setselectedTournament(e.target.value);
                                setPage(1)
                            }}
                        >
                            {tournaments.map(tournament => (
                                <MenuItem key={tournament.id} value={tournament.id}>
                                    {tournament.name}
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

export default GamesByTournament;
