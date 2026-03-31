# Development Notes

## Running Locally

### Terminal 1 - Backend
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Terminal 2 - Frontend
```powershell
cd frontend
npm install
npm run dev
```

## Database Management

The SQLite database is stored in `backend/emails.db`

To inspect data:
```bash
cd backend
python
>>> import sqlite3
>>> conn = sqlite3.connect('emails.db')
>>> c = conn.cursor()
>>> c.execute('SELECT * FROM emails')
```

## Common Issues

**CORS Errors**: Make sure backend is running on port 5000
**Connection Refused**: Check if Python/Node servers are running
**Database locked**: Delete `emails.db` and restart backend

## Deployment Ready

To deploy:
1. Backend: Use Gunicorn + any Python host
2. Frontend: Build with `npm run build` and serve as static assets
3. Database: SQLite works fine for small deployments, migrate to PostgreSQL for production
