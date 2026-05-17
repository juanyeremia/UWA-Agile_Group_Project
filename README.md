# Project Name: 🎬 MoviePulse

## Description

This app is a community-driven movie review web application, where users can discover movies, read reviews from other users, and share their own opinions.

Movie data is sourced from the TMDB (The Movie Database) API, which provides up-to-date information about movies including posters, descriptions, genres, and release dates.

### User Access

Guest users can browse movies and read reviews without creating an account.
Registered users can log in to write reviews, rate movies on a scale of 1 to 5, as well as view other users' profiles and their review history.

### Key Features

- Browse a continuously updated list of movies on the home page
- Search for specific movies by title
- Read reviews left by other users without needing an account
- Create an account to write and submit your own reviews
- Rate movies on a scale of 1 to 5
- View user profiles to see all reviews from a specific user

### Design

The interface follows a card-based layout, making it easy to browse movies and reviews at a glance. The design is clean and minimal, inspired by
platforms like Letterboxd and IMDB, with a focus on readability and ease of navigation.

### Software Used

- Frontend: HTML, CSS, JavaScript, Bootstrap
- Backend: Python, Flask, SQLAlchemy
- Database: Local SQLite database
- External API: TMDB (The Movie Database)

## Group Members

- Juan Yovian - 24911605 - juanyeremia
- Thushamini Chathusika - 24562882 - chathushika2000
- Viktor Kim - 24712039 - sky-A-drum
- Yu Ting Weng - 246222994 - tammyweng1

## How to use the application

1. Clone the repository to your local machine.
2. Navigate to the project directory and install the required dependencies using pip:
   ```
   pip install -r requirements.txt
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/avtivate
   ```
4. Set up the database by running the following command:
   ```
   flask db upgrade
   ```
5. Start the Flask development server:
   ```
   python run.py
   ```
6. Open your web browser and go to `http://localhost:5000` to access the application. You can browse movies, read reviews, and create an account to write your own reviews and rate movies.
7. To stop the server, press `Ctrl + C` in the terminal.

## How to run the tests

1. Ensure you have the testing dependencies installed:
   ```
   pip install -r requirements.txt
   ```
2. Run the tests using the following command:
   ```
   python -m unittest discover app/tests/selenium_tests
   ```
3. Run one Selenium test file:
   ```
   python -m unittest app.tests.selenium_tests.sel_logout
   ```
   or
   ```
   python -m unittest app.tests.selenium_tests.sel_edit_profile
   ```
   **NOTE:** Do not run `python run.py` manually before Selenium tests. The Selenium tests start their own Flask test server.
