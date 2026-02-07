# AI-Powered Grievance Redressal System

A smart governance application for handling citizen grievances with NLP-based sentiment analysis and intelligent routing.

## Features
- 📝 Citizens can submit grievances with AI analysis
- 🤖 Automatic sentiment detection (Positive/Neutral/Negative)
- 🔥 Priority detection (High/Medium/Low)
- 📊 Admin dashboard with analytics
- 🗺️ Heatmap showing complaints by city
- 🏢 Automatic department routing

## Installation

### Local Setup
1. Clone the repository:
```bash
git clone <your-repo-url>
cd ai_grievance-App
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirement.txt
```

4. Run locally:
```bash
streamlit run app3.py
```

Visit `http://localhost:8501` in your browser.

## Deployment on Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit account (connect at streamlit.io)

### Steps
1. Push your code to GitHub:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository, branch, and point to `app3.py`
5. Set environment variable in Streamlit Cloud:
   - Go to Settings → Secrets
   - Add: `ADMIN_PASS = "your_secure_password"`
6. Click "Deploy"

## Environment Variables
- `ADMIN_PASS` - Admin login password (default: "admin")

## File Structure
```
├── app3.py                 # Main application
├── grievances.csv          # Local data storage (git ignored)
├── requirement.txt         # Dependencies
├── .streamlit/config.toml  # Streamlit configuration
└── README.md              # This file
```

## Default Credentials
- **Citizen**: No password required (just select "Citizen" role)
- **Admin**: Password set via `ADMIN_PASS` environment variable

## Notes
- Data is stored locally in `grievances.csv` for development
- For production, consider integrating a cloud database (Firebase, PostgreSQL, etc.)
