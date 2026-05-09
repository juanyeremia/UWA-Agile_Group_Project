/* ============================================
Load and display now playing movies on the homepage
============================================*/

// Constants
const TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w500';      // Base URL for TMDB images 500px wide
const CACHE_KEY = 'now_playing_movies';                             // Cache key for localStorage

async function loadNowPlayingMovies() {
    /* ==========================
    Check cache for now playing movies
    ========================== */
    const cached  = sessionStorage.getItem(CACHE_KEY);
    let movies;

    if (cached) {                                                                                          // If movie is cached, use it
        movies = JSON.parse(cached);                                                      
    } else {                                                                                                  // If not cached, fetch from API and cache it
        const response = await fetch('/api/movies/now_playing');
        const data = await response.json();
        movies = data.results;
        sessionStorage.setItem(CACHE_KEY, JSON.stringify(movies));        // Cache the movie data in sessionStorage
    }
  
    /* ==========================
    Render first 6 latest movies
    ========================== */
    
}