const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { execFile } = require('child_process');
const axios = require('axios');
const app = express();
const port = process.env.PORT || 3001;

const TMDB_API_KEY = '106707b0047077d02bcb4285c4350683'; // Replace with your TMDb API key
const TMDB_API_URL = 'https://api.themoviedb.org/3/discover/movie';

app.use(cors()); // Add this line
app.use(bodyParser.json({ limit: '10mb' }));

// Mapping emotions to TMDb genres
const emotionToGenre = {
    happy: '35', // Comedy
    sad: '18', // Drama
    angry: '28', // Action
    surprise: '53', // Thriller
    fear: '27', // Horror
    disgust: '80', // Crime
    neutral: '10749' // Romance
};

app.get('/api', (req, res) => {
    res.send('Hello from the backend!');
});

app.post('/api/analyze', (req, res) => {
    const { image } = req.body;

    if (!image) {
        return res.status(400).json({ error: 'No image provided' });
    }

    execFile('/usr/bin/python3', ['emotion_recognition.py', image], (error, stdout, stderr) => {
        if (error) {
            console.error('Error running Python script:', error);
            return res.status(500).json({ error: 'Error processing image' });
        }

        const cleanedOutput = stdout.toString().split('\n').filter(line => line.trim() !== '').pop();
        console.log('Python script result:', cleanedOutput);

        // Fetch movies from TMDb based on emotion
        const genreId = emotionToGenre[cleanedOutput.toLowerCase()] || '35';

        axios.get(TMDB_API_URL, {
            params: {
                api_key: TMDB_API_KEY,
                with_genres: genreId,
                sort_by: 'popularity.desc',
                language: 'en-US',
                page: 1
            }
        }).then(response => {
            const movies = response.data.results.slice(0, 10).map(movie => ({
                title: movie.title,
                overview: movie.overview,
                poster_path: `https://image.tmdb.org/t/p/w500${movie.poster_path}`
            }));

            res.json({ emotion: cleanedOutput, movies });
        }).catch(err => {
            console.error('Error fetching movies from TMDb:', err);
            res.status(500).json({ error: 'Error fetching movies' });
        });
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
