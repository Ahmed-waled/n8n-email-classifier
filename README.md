# Email Automation Dashboard

A minimalist n8n workflow showcase project for categorizing and displaying emails.

## Features

✨ **Email Categorization** - Receives emails categorized into: University, Jobs, Personal, Other
📊 **Analytics Dashboard** - Real-time stats showing email distribution
🎨 **Clean UI** - Simple, responsive design with Vue.js
⚡ **Fast Backend** - Flask API with SQLite database
🔄 **Auto-refresh** - Dashboard updates every 5 seconds

## Project Structure

```
email-automation/
├── backend/          # Flask API
│   ├── app.py       # Main application
│   └── requirements.txt
└── frontend/         # Vue.js Dashboard
    ├── src/
    │   ├── App.vue  # Main component
    │   └── main.js
    ├── package.json
    ├── vite.config.js
    └── index.html
```

## Quick Start

### Backend Setup

```bash
cd backend

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Or with bash/PowerShell
python -m venv venv
source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Frontend runs on `http://localhost:3000`

## Using with n8n

### Webhook Configuration in n8n

1. In your n8n workflow, add a "Webhook" trigger node
2. Configure it with:
   - **Method**: POST
   - **Path**: `/emails` (your webhook URL will be shown in n8n)

3. Add a "Custom Code" node or HTTP Request to send data to your API:

```javascript
// Example n8n Custom Code node
return {
  "sender": $json.from,
  "subject": $json.subject,
  "category": "University" // or dynamically determined
}
```

4. Connect to an HTTP Request node pointing to:
   ```
   POST http://localhost:5000/api/emails
   ```

### Example Webhook Payload

```json
{
  "sender": "professor@university.edu",
  "subject": "Assignment Deadline Extended",
  "category": "University"
}
```

Valid categories: `University`, `Jobs`, `Personal`, `Other`

## API Endpoints

### POST /api/emails
Add a new categorized email

Request:
```json
{
  "sender": "john@example.com",
  "subject": "Email Subject",
  "category": "University"
}
```

### GET /api/emails
Get all emails

### GET /api/analytics
Get email statistics

```json
{
  "total": 15,
  "by_category": {
    "University": 5,
    "Jobs": 4,
    "Personal": 5,
    "Other": 1
  },
  "categories": ["University", "Jobs", "Personal", "Other"]
}
```

### DELETE /api/emails/<id>
Delete an email by ID

## Testing

You can test the API with curl:

```bash
# Add email
curl -X POST http://localhost:5000/api/emails \
  -H "Content-Type: application/json" \
  -d '{"sender":"test@example.com","subject":"Test Email","category":"Personal"}'

# Get all emails
curl http://localhost:5000/api/emails

# Get analytics
curl http://localhost:5000/api/analytics

# Delete email (replace 1 with actual ID)
curl -X DELETE http://localhost:5000/api/emails/1
```

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: Vue.js 3
- **Database**: SQLite
- **Build Tool**: Vite
- **API**: RESTful

## Notes

- The database file `emails.db` is created automatically in the backend folder
- The dashboard auto-refreshes every 5 seconds
- No authentication required (for demo purposes)
- CORS enabled for frontend-backend communication

## Next Steps

1. Set up your n8n workflow to fetch emails
2. Add logic to categorize emails (using LLM or rules)
3. Send categorized emails to the webhook
4. Monitor the dashboard

Enjoy showcasing your n8n automation! 🚀
