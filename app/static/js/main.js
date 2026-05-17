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

    // Set hero backdrop image from a random featured movie
    const featured = movies[Math.floor(Math.random() * movies.length)];                     // Randomly select a featured movie from the now playing list
    if (featured.backdrop_path) {                                                                                  // If the featured movie has a backdrop image, set it as the hero background
        const heroUrl = `https://image.tmdb.org/t/p/original${featured.backdrop_path}`;
        $('.hero-section').css('background-image', `url(${heroUrl})`);
    }

    const latest = movies.slice(0,6)                                        // Take first 6 movies

    /* ==========================
    Fetch ratings for the 6 movies in local db
    ========================== */
    const ids = latest.map(movie => movie.id).join(',')                                     // Loops through Movies and extracts the `id` from each then join them separated by comma
    const ratingsResponse = await fetch(`/api/movies/ratings?ids=${ids}`);      // Fetch local ratings from db
    const ratings = await ratingsResponse.json();
  
    /* ==========================
    Render first 6 latest movies
    ========================== */
    $('#latest-movies-container').html('');                                     // Create empty container for latest movies

    latest.forEach(movie => {                                      // Loop through first 6 movies
        const year = movie.release_date ? movie.release_date.split('-')[0] : 'N/A';    // Extract release year or set to 'N/A' if not available
        const poster = movie.poster_path
            ? `${TMDB_IMAGE_BASE}${movie.poster_path}`                                                // Construct poster URL if available
            : '/static/images/placeholder.png';                                                        // Use placeholder if no poster

            // Check if this movie has ratings in local db
            const localRating = ratings[movie.id];                                                                     // Look up rating by movie ID
            const ratingHTML = localRating
                ?  `<div class="movie-rating">${localRating.avg_rating} ★</div>
                    <div class="movie-reviews">${localRating.review_count} reviews</div>`
                :   `<div class="movie-rating">0 ★</div>
                    <div class="movie-reviews">No reviews</div>`;                                                                                                                        // Show nothing if no reviews in local db
        
            $('#latest-movies-container').append(`
            <div class="col">
                <a href="/movie/${movie.id}" class="movie-card-link">
                    <div class="movie-card">
                        <img src="${poster}" class="movie-poster" alt="${movie.title}">
                        <div class="movie-info">
                            <div class="movie-title">${movie.title}</div>
                            <div class="movie-year">${year}</div>
                            ${ratingHTML}
                        </div>
                    </div>
                </a>
            </div>
        `);                                                                                              // Append movie card HTML to container
    });
}

/* ============================================
Load and display highest rated mvoies on the homepage
============================================*/

const HIGHEST_RATED_CACHE_KEY = 'highest_rated_movies';                             // Cache key for highest rated movies

async function loadHighestRatedMovies() {
    /* ==========================
    Fetch highest rated movie IDs from local DB
    ========================== */
    const response = await fetch('/api/movies/highest_rated');
    const ratedMovies = await response.json();                                           // Fetch highest rated movies from API                                 

    $('#highest-rated-movies-container').html('');                                     // Create empty container for highest rated movies

    /* ==========================
    If no rated movies, display message
    ========================== */
    if (ratedMovies.length === 0) {
        $('#highest-rated-movies-container').html('<p>No rated movies yet.</p>');
        return;
    }

    /* ==========================
    For each movie_id, check cache or call TMDB
    ========================== */
    for (const rated of ratedMovies) {
        const cacheKey = `movie_detail_${rated.movie_id}`;                             // Cache key for individual movie details
        let movieData;

        const cached = sessionStorage.getItem(cacheKey);
        if (cached) {                                                                                          // If movie details are cached, use them
            movieData = JSON.parse(cached);
        } else {                                                                                                  // If not cached, fetch from TMDB API and cache it
            const tmdbResponse = await fetch(`/api/movies/${rated.movie_id}`);      // Fetch movie details from TMDB API (in routes.py, this will check cache first before calling TMDB)
            movieData = await tmdbResponse.json();
            sessionStorage.setItem(cacheKey, JSON.stringify(movieData));        // Cache the movie details in sessionStorage
        }

        // Extract necessary details for rendering the movie card
        const year = movieData.release_date ? movieData.release_date.split('-')[0] : 'N/A';    // Extract release year or set to 'N/A' if not available
        const poster = movieData.poster_path
            ? `${TMDB_IMAGE_BASE}${movieData.poster_path}`                                                // Construct poster URL if available
            : '/static/images/placeholder.png';                                                        // Use placeholder if no poster
        
        // Append movie card HTML to container
        $('#highest-rated-movies-container').append(`
            <div class="col">
                <a href="/movie/${rated.movie_id}" class="movie-card-link">
                    <div class="movie-card">
                        <img src="${poster}" class="movie-poster" alt="${movieData.title}">
                        <div class="movie-info">
                            <div class="movie-title">${movieData.title}</div>
                            <div class="movie-year">${year}</div>
                            <div class="movie-rating">${rated.avg_rating} ★</div>
                            <div class="movie-reviews">${rated.review_count} reviews</div>
                        </div>
                    </div>
                </a>
            </div>
        `);
    }
}

/* ============================================
Load and display recent reviews on home page
============================================*/

async function loadRecentReviews() {
    /* ==========================
    For recent reviews from local DB
    ========================== */
    const response = await fetch('/api/reviews/recent');
    let reviews = await response.json();

    $('#recent-reviews-container').html('');                        // Create empty container for recent reviews

    /* ==========================
    If no reviews, display message
    ========================== */
    if (reviews.length === 0) {
         $('#recent-reviews-container').html('<p>No reviews have been submitted yet.</p>')
        return;
    }

    /* ==========================
    For each movie, check cache or call TMDB for movie details
    ========================== */
    for (const review of reviews) {
        const cacheKey = `movie_detail_${review.movie_id}`;                 // Cache key for individual movie details
        let movieData;

        const cached = sessionStorage.getItem(cacheKey)
        if (cached) {                                                                               // If movie details are cached, use them
            movieData = JSON.parse(cached);
        } else {                                                                                       // If not cached, fetch from TMDB API and cache it
            const tmdbResponse = await fetch(`api/movies/${review.movie_id}`)       // Fetch movie details from TMDB
            movieData = await tmdbResponse.json();
            sessionStorage.setItem(cacheKey, JSON.stringify(movieData))                 // Cache the movie details in sessionStorage
        }
        
        // Get movie poster data 
        const poster = movieData.poster_path
            ? `${TMDB_IMAGE_BASE}${movieData.poster_path}`
            : ``;                                                                                           // If no image, leave empty

            // Build 'flag' button
            let flagBtn = '';
            if (IS_AUTHENTICATED) {          // Check if user is authenticated
                if (review.flagged) {              // If review is flagged
                    flagBtn = `<button class="btn btn-sm btn-secondary" disabled>🚩 Flagged</button>`;
                } else {
                    flagBtn = `<button class="btn btn-sm btn-outline-danger flag-btn" data-id="${review.id}" data-flagged="false">🚩 Flag</button>`;
                }
             }
            

             $('#recent-reviews-container').append(`
                <div class="review-item">
                    <a href="/movie/${review.movie_id}">
                        <img src="${poster}" class="review-poster" alt="${movieData.title}">
                    </a>
                    <div class="review-content">
                        <div class="review-header">
                            <p class="reviewer-name">${review.username}</p>
                            <p class="review-movie">${movieData.title}</p>
                            <p class="review-rating">${review.rating}/5</p>
                        </div>
                        <p class="review-text">${review.body}</p>
                        ${flagBtn}
                    </div>
                </div>    
            `);
    }
}

// Load functions in document
$(document).ready(function() {
    loadNowPlayingMovies();
    loadHighestRatedMovies();
    loadRecentReviews();

    // Handle flag button click event
    $(document).on('click', '.flag-btn', function() {
        const reviewId = $(this).data('id');
        const btn = $ (this);

        $.post(`/flag_review/${reviewId}`)          // Send POST request to flag the review
            .done(function() {
                btn.replaceWith(`<button class="btn btn-sm btn-secondary" disabled>🚩 Flagged</button>`);
                })
                .fail(function() {
                    alert('Something went wrong. Please try again.');
                });
        });
    });