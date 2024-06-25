import React from 'react';
import { Box, Card, CardContent, Typography } from '@mui/material';

const SearchResults = ({ results }) => {
  return (
    <Box>
      {results.map((result, index) => (
        <Card key={result.id || index} style={{ marginBottom: '10px' }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              <a href={result.url} target="_blank" rel="noopener noreferrer">
                {result.title}
              </a>
            </Typography>
            <Typography variant="body2" color="textSecondary">
              {result.content}
            </Typography>
            {result.tags && (
              <Typography variant="caption" color="textSecondary">
                Tags: {result.tags.join(', ')}
              </Typography>
            )}
            {result.keywords && (
              <Typography variant="caption" color="textSecondary" display="block">
                Keywords: {result.keywords.join(', ')}
              </Typography>
            )}
            {result.crawled_date && (
              <Typography variant="caption" color="textSecondary" display="block">
                Crawled Date: {new Date(result.crawled_date).toLocaleString()}
              </Typography>
            )}
            <Typography variant="caption" color="textSecondary" display="block">
              Score: {result.score}
            </Typography>
          </CardContent>
        </Card>
      ))}
    </Box>
  );
};

export default SearchResults;