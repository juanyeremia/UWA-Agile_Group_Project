# Entry point for the application
from app import app
from config import Config

print("TMDB Token loaded:", Config.TMDB_ACCESS_TOKEN is not None)  # Check if the TMDB token is loaded correctly

if __name__ == '__main__':
    app.run(debug=True)