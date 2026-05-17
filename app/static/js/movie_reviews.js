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
          const template = document.getElementById("review-template");
          const clone = template.content.cloneNode(true);

          clone.querySelector(".review-username").textContent = review.username;
          clone.querySelector(".review-rating").textContent =
            `Rating: ${review.rating}/5`;
          clone.querySelector(".review-body").textContent = review.body;

          const flagContainer = clone.querySelector(".review-flag-container");

          if (review.flagged) {
            flagContainer.innerHTML =
              '<button class="btn btn-sm btn-secondary" disabled>🚩 Flagged</button>';
          } else {
            flagContainer.innerHTML = `<button class="btn btn-sm btn-outline-danger flag-btn" data-id="${review.id}">🚩 Flag</button>`;
          }

          reviewsList.appendChild(clone);
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

// Add the flag to the reviews
document.addEventListener("click", function (event) {
  if (!event.target.classList.contains("flag-btn")) {
    return;
  }

  const button = event.target;
  const reviewId = button.dataset.id;

  if (!IS_AUTHENTICATED) {
    window.location.href = LOGIN_URL;
    return;
  }

  fetch(`/flag_review/${reviewId}`, {
    method: "POST",
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data.success) {
        button.outerHTML =
          '<button class="btn btn-sm btn-secondary" disabled>🚩 Flagged</button>';
      } else {
        alert("Failed to flag review.");
      }
    })
    .catch(function () {
      alert("Something went wrong. Please try again.");
    });
});
