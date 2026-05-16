const loadMoreBtn = document.getElementById("load-more-btn");
const movieResults = document.getElementById("movie-results");

if (loadMoreBtn) {
  loadMoreBtn.addEventListener("click", function () {
    const query = loadMoreBtn.dataset.query;
    const offset = Number(loadMoreBtn.dataset.offset);

    fetch(`/api/search?query=${encodeURIComponent(query)}&offset=${offset}`)
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        data.movies.forEach(function (movie) {
          const posterPath = movie.poster_path
            ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
            : "/static/images/placeholder.png";

          const releaseYear = movie.release_date
            ? movie.release_date.slice(0, 4)
            : "N/A";

          const movieCard = `
            <div class="col">
              <a href="/movie/${movie.id}" class="text-decoration-none text-white">
                <div class="movie-card">
                  <img
                    src="${posterPath}"
                    class="movie-poster"
                    alt="${movie.title}"
                  />
                  <div class="movie-info">
                    <div class="movie-title">${movie.title}</div>
                    <div class="movie-year">${releaseYear}</div>
                    <div class="movie-rating">${movie.local_avg_rating} ★</div>
                    <div class="movie-reviews">${movie.local_review_count} reviews</div>
                  </div>
                </div>
              </a>
            </div>
          `;

          movieResults.insertAdjacentHTML("beforeend", movieCard);
        });

        loadMoreBtn.dataset.offset = offset + 12;

        if (!data.has_more) {
          loadMoreBtn.style.display = "none";
        }
      })
      .catch(function (error) {
        console.error("Error loading more movies:", error);
      });
  });
}
