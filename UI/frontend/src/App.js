import React, { useState } from 'react';
import axios from 'axios';
import { Container, Typography, Box } from '@mui/material';
import SearchBar from './components/SearchBar';
import SearchResults from './components/SearchResults';

const App = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await axios.get('http://localhost:5000/search', {
        params: { query }
      });
      setResults(response.data.hits.hits);  // Adjusted to handle Elasticsearch response structure
    } catch (error) {
      console.error('Error fetching search results:', error);
    }
  };

  return (
    <Container>
      <Typography variant="h2" gutterBottom>
        Elasticsearch UI
      </Typography>
      <SearchBar query={query} setQuery={setQuery} handleSearch={handleSearch} />
      <Box mt={4}>
        <SearchResults results={results} />
      </Box>
    </Container>
  );
};

export default App;
