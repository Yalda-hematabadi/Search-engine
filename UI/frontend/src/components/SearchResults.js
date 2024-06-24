import React from 'react';
import { Box, Card, CardContent, Typography } from '@mui/material';

const SearchResults = ({ results }) => {
  return (
    <Box>
      {results.map((result, index) => (
        <Card key={index} style={{ marginBottom: '10px' }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              <a href={result._source.url} target="_blank" rel="noopener noreferrer">
                {result._source.title}
              </a>
            </Typography>
            <Typography variant="body2" color="textSecondary">
              {result._source.content}
            </Typography>
            <Typography variant="caption" color="textSecondary">
              Tags: {result._source.tags.join(', ')}
            </Typography>
            <Typography variant="caption" color="textSecondary" display="block">
              Keywords: {result._source.keywords.join(', ')}
            </Typography>
            <Typography variant="caption" color="textSecondary" display="block">
              Crawled Date: {new Date(result._source.crawled_date).toLocaleString()}
            </Typography>
          </CardContent>
        </Card>
      ))}
    </Box>
  );
};

export default SearchResults;
