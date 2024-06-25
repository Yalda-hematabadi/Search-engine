import React, { useState } from 'react';
import axios from 'axios';
import { Container, Typography, Box } from '@mui/material';
import SearchBar from './components/SearchBar';
import SearchResults from './components/SearchResults';

const App = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [total, setTotal] = useState(0);

  const handleSearch = async () => {
    try {
      const response = await axios.get('http://localhost:5000/search', {
        params: { query }
      });
      setResults(response.data.results);  // This should now match the structure expected by SearchResults
      setTotal(response.data.total);
    } catch (error) {
      console.error('Error fetching search results:', error);
      setResults([]);
      setTotal(0);
    }
  };

  return (
    <Container>
      <Typography variant="h2" gutterBottom>
        Elasticsearch UI
      </Typography>
      <SearchBar query={query} setQuery={setQuery} handleSearch={handleSearch} />
      <Box mt={4}>
        <Typography variant="h6" gutterBottom>
          Total Results: {total}
        </Typography>
        <SearchResults results={results} />
      </Box>
    </Container>
  );
};

export default App;