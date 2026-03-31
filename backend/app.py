from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os
from pydantic import BaseModel, Field, ValidationError
from typing import Literal

app = Flask(__name__)
CORS(app)

# Define valid categories
VALID_CATEGORIES = ['University', 'Jobs', 'Personal', 'Other']

# Define email schema
class EmailSchema(BaseModel):
    """Schema for incoming email data"""
    subject: str = Field(..., min_length=1, max_length=500)
    summary: str = Field(..., min_length=1, max_length=5000)
    category: Literal['University', 'Jobs', 'Personal', 'Other']
    sender: str = Field(default="Unknown", max_length=500)

# Database setup
DB_FILE = 'emails.db'

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            subject TEXT NOT NULL,
            category TEXT NOT NULL,
            summary TEXT NOT NULL,
            received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database on startup
init_db()

@app.route('/api/emails', methods=['POST'])
def add_email():
    """Receive email from n8n workflow"""
    try:
        data = request.json
        
        # Validate against schema
        email = EmailSchema(**data)
        
        # Save to database
        conn = get_db()
        c = conn.cursor()
        c.execute(
            'INSERT INTO emails (sender, subject, category, summary) VALUES (?, ?, ?, ?)',
            (email.sender, email.subject, email.category, email.summary)
        )
        conn.commit()
        email_id = c.lastrowid
        conn.close()
        
        return jsonify({'success': True, 'id': email_id}), 201
        
    except ValidationError as e:
        return jsonify({'error': 'Invalid request data', 'details': e.errors()}), 400
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/api/emails', methods=['GET'])
def get_emails():
    """Get all emails"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM emails ORDER BY received_at DESC')
    emails = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return jsonify(emails)

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get email statistics"""
    conn = get_db()
    c = conn.cursor()
    
    # Count by category
    c.execute('''
        SELECT category, COUNT(*) as count 
        FROM emails 
        GROUP BY category
    ''')
    categories = {row[0]: row[1] for row in c.fetchall()}
    
    # Total count
    c.execute('SELECT COUNT(*) FROM emails')
    total = c.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total': total,
        'by_category': categories,
        'categories': VALID_CATEGORIES
    })

@app.route('/api/emails/<int:id>', methods=['DELETE'])
def delete_email(id):
    """Delete an email"""
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM emails WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
