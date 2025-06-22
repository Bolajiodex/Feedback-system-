# Caleb University Feedback System Deployment

This folder contains all necessary files to deploy the Caleb University Feedback & Grievance System using Streamlit.

## Included Files
- `caleb_enhanced_app.py`: Main Streamlit application.
- `requirements.txt`: Python dependencies for the app.
- `assets/`: Folder for static assets (e.g., logo).
- `README.md`: This documentation file.

## How to Deploy

1. **Install Python 3.8+** (if not already installed).
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```bash
   streamlit run caleb_enhanced_app.py
   ```
4. **Access the app:**
   Open your browser and go to the local URL provided by Streamlit (usually http://localhost:8501).

## Notes
- The app uses a local SQLite database (`feedback_database.db`). For a fresh deployment, the database will be created automatically.
- Place any additional static files (images, etc.) in the `assets/` folder.
- For production, consider using Streamlit Cloud, Heroku, or another cloud platform. 