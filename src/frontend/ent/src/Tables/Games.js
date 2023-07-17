import {useEffect, useState} from "react";
import {
    CircularProgress,
    Pagination,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
} from "@mui/material";


function Games() {

    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);
    const [data, setData] = useState(null);

    const [maxDataSize, setMaxDataSize] = useState(0);

    useEffect(() => {
        setData(null);
            console.log(`fetching from ${process.env.REACT_APP_API_ENTITIES_URL}/api/countries`)
            fetch(`http://${process.env.REACT_APP_API_ENTITIES_URL}/api/games?page=${page}&pageSize=${PAGE_SIZE}`)
            .then(response => response.json())
            .then(jsonData => setData(jsonData));
            fetch(`http://localhost:20001/api/games/count`)
            .then(response => response.json())
            .then(jsonData => setMaxDataSize(jsonData));
    }, [page])


    return (
        <>
            <h1>Games ({maxDataSize})</h1>

            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell align="center">Date</TableCell>
                            <TableCell align="center">Home Team</TableCell>
                            <TableCell align="center">Away Team</TableCell>
                            <TableCell align="center">Score</TableCell>
                            <TableCell align="center">Tournament</TableCell>
                            <TableCell align="center">Country</TableCell>
                            <TableCell align="center">City</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            data ?
                                data.map((row) => (
                                    <TableRow
                                        key={row.id}
                                        style={{background: "gray", color: "black"}}
                                    >
                                        <TableCell component="td" align="center">{row.id}</TableCell>
                                        <TableCell component="td" scope="row" align="center">
                                            {row.date}
                                        </TableCell>
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
                                            {row.tournament_name}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.country_name}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.city}
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
                maxDataSize && <div style={{background: "black", padding: "1rem"}}>
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

export default Games;
