import React from 'react';
import { TextField, Button, Box } from '@mui/material';

const SearchBar = ({ query, setQuery, handleSearch }) => {
  return (
    <Box display="flex" alignItems="center" justifyContent="center" mt={4}>
      <TextField
        label="Search"
        variant="outlined"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ marginRight: '10px' }}
      />
      <Button variant="contained" color="primary" onClick={handleSearch}>
        Search
      </Button>
    </Box>
  );
};

export default SearchBar;
