# Entry point for the application
from app import create_app, db
from config import Config, TestConfig, DeploymentConfig


print("TMDB Token loaded:", Config.TMDB_ACCESS_TOKEN is not None)  # Check if the TMDB token is loaded correctly

app = create_app(DeploymentConfig)

if __name__ == '__main__':
    app.run(debug=True)