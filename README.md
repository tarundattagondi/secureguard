# secureguard
Security Compliance Dashboard - GRC tool with automated security scanning, CI/CD, and Docker deployment
To start the app locally (development mode):
bashcd ~/Desktop/secureguard
source .venv/bin/activate
python run.py
Then open http://127.0.0.1:5001
To start with Docker (production mode):
bashcd ~/Desktop/secureguard
docker-compose up --build
Then open http://localhost:5001 or http://localhost
To stop Docker:
bashdocker-compose down
To run tests:
bashcd ~/Desktop/secureguard
source .venv/bin/activate
pytest
To push code to GitHub:
bashgit add .
git commit -m "your message here"
git push
That's it. The local Postgres stays running on your Mac in the background so you don't need to start it. If the database ever gives errors, just run:
bashexport FLASK_APP=run.py
flask db upgrade
python scripts/seed_controls.py