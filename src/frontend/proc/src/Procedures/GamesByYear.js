import React, {useEffect, useState} from "react";
import {Box, 
    CircularProgress, 
    Container, 
    FormControl, 
    InputLabel, 
    Pagination,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Input,
    InputAdornment,
    Button
} from "@mui/material";


function GamesByYear() {

    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);
    const [fetchedData, setFetchedData] = useState('')
    const [selectedYear, setselectedYear] = useState("");

    const [maxDataSize, setMaxDataSize] = useState(0);

    const [procData, setProcData] = useState(null);
    
    async function fetchData() {
        setProcData(null);
            if (selectedYear) {
                console.log(`fetching from ${process.env.REACT_APP_API_PROC_URL}/api/games_by_year?year=${selectedYear}`);
                fetch(`http://${process.env.REACT_APP_API_PROC_URL}/api/games_by_year?year=${selectedYear}&page=${page}&pageSize=${PAGE_SIZE}`)
                .then(response => response.json())
                .then(data => {setProcData(data);});
                fetch(`http://${process.env.REACT_APP_API_PROC_URL}/api/count/games_by_year?year=${selectedYear}`)
                .then(response => response.json())
                .then(jsonData => setMaxDataSize(jsonData));
            }
        setFetchedData(procData)
      }
    
      useEffect(() => {
        fetchData()
    }, [selectedYear,page])
    
      const handleSubmit = e => {
        e.preventDefault()
        fetchData()
      }
    

    return (
        <>
            <h1>Games by Year</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Insert the year</h2>
                    <FormControl fullWidth>
                        <form onSubmit={handleSubmit}>
                        <InputLabel id="year-label" >Year</InputLabel>
                        <Input
                            fullWidth
                            id="year-input"
                            value={selectedYear}
                            onChange={e => setselectedYear(e.target.value)}
                            endAdornment={
                            <InputAdornment position="end">
                                <Button type="submit" onClick={handleSubmit}>
                                Search
                                </Button>
                                |
                                <Button onClick={() => { setselectedYear(""); setMaxDataSize(0);}}>
                                    Clear
                                </Button>

                            </InputAdornment>
                            }
                        />
                        </form>

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

export default GamesByYear;
