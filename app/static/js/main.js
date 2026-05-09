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
        movies = data.results;                                                                     // Immediately access the results array from the API response
        sessionStorage.setItem(CACHE_KEY, JSON.stringify(movies));        // Cache the movie data in sessionStorage
    }
  
    /* ==========================
    Render first 6 latest movies
    ========================== */
    const container = document.getElementById('latest-movies-container');
    container.innerHTML = '';                                                                 // Clear existing content

    movies.slice(0, 6).forEach(movie => {                                      // Loop through first 6 movies
        const year = movie.release_date ? movie.release_date.split('-')[0] : 'N/A';    // Extract release year or set to 'N/A' if not available
        const poster = movie.poster_path
            ? `${TMDB_IMAGE_BASE}${movie.poster_path}`                                                // Construct poster URL if available
            : '/static/images/placeholder.png';                                                        // Use placeholder if no poster

        container.innerHTML += `
            <div class="col">
                <a href="/movie/${movie.id}" class="movie-card-link">
                    <div class="movie-card">
                        <img src="${poster}" class="movie-poster" alt="${movie.title}">
                        <div class="movie-info">
                            <div class="movie-title">${movie.title}</div>
                            <div class="movie-year">${year}</div>
                            <div class="movie-rating">${movie.vote_average.toFixed(1)}</div>
                        </div>
                    </div>
                </a>
            </div>
        `;                                                                                              // Append movie card HTML to container
    });
}

loadNowPlayingMovies();                                                                 // Load movies when the page loads