# n8n Email Categorization Workflow

This is an example n8n workflow structure for email categorization.

## Workflow Steps

1. **Email Trigger** - Receives email from Gmail/Outlook
2. **Extract Email Data** - Parse sender, subject, body
3. **Categorize** - Use AI (OpenRouter/Claude) or rules to categorize
4. **Send to Dashboard** - POST to webhook

## Code Example for n8n

### Step 1: Email Input (Gmail trigger)
```
Trigger: Gmail - New Email
```

### Step 2: Categorization (Custom Code / AI)
```javascript
// If using Custom Code node
const email = $json;
const categorizeEmail = (sender, subject, body) => {
  const text = `${sender} ${subject} ${body}`.toLowerCase();
  
  if (text.includes('university') || text.includes('class') || text.includes('assignment')) {
    return 'University';
  }
  if (text.includes('job') || text.includes('interview') || text.includes('linkedin')) {
    return 'Jobs';
  }
  if (text.includes('friend') || text.includes('family') || text.includes('personal')) {
    return 'Personal';
  }
  return 'Other';
};

return {
  sender: email.from,
  subject: email.subject,
  category: categorizeEmail(email.from, email.subject, email.body)
};
```

### Step 3: Send to Dashboard
```
HTTP Request node:
- Method: POST
- URL: http://localhost:5000/api/emails
- Body: JSON
  {
    "sender": "{{ $json.sender }}",
    "subject": "{{ $json.subject }}",
    "category": "{{ $json.category }}"
  }
```

## Alternative: Using AI for Categorization

With OpenRouter/Claude:
```javascript
// In a Custom Code node after calling AI API
const classification = $json.categorization; // from AI response

return {
  sender: email.from,
  subject: email.subject,
  category: classification
};
```

## Testing

You can manually trigger this workflow and test the webhook connection to your dashboard.
