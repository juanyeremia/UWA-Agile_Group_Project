const loadMoreReviewsBtn = document.getElementById("load-more-reviews-btn");
const reviewsList = document.getElementById("reviews-list");

if (loadMoreReviewsBtn) {
  loadMoreReviewsBtn.addEventListener("click", function () {
    const movieId = loadMoreReviewsBtn.dataset.movieId;
    const page = Number(loadMoreReviewsBtn.dataset.page);

    fetch(`/api/movie/${movieId}/reviews?page=${page}`)
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        data.reviews.forEach(function (review) {
          const reviewCard = `
            <div class="card mb-3">
              <div class="card-body">
                <h5 class="card-title">${review.username}</h5>
                <h6 class="card-subtitle mb-2 text-body-secondary">
                  Rating: ${review.rating}/5
                </h6>
                <p class="card-text">${review.body}</p>
              </div>
            </div>
          `;

          reviewsList.insertAdjacentHTML("beforeend", reviewCard);
        });

        loadMoreReviewsBtn.dataset.page = page + 1;

        if (!data.has_more) {
          loadMoreReviewsBtn.style.display = "none";
        }
      })
      .catch(function (error) {
        console.error("Error loading more reviews:", error);
      });
  });
}
