<template>
  <div class="container">
    <header>
      <h1>📧 Email Automation</h1>
      <p>n8n Workflow Showcase</p>
    </header>

    <div class="content">
      <!-- Analytics Section -->
      <section class="analytics">
        <h2>Analytics</h2>
        <div class="stats">
          <div class="stat-card">
            <div class="stat-value">{{ analytics.total }}</div>
            <div class="stat-label">Total Emails</div>
          </div>
          <div class="stat-card" v-for="cat in ['University', 'Jobs', 'Personal', 'Other']" :key="cat">
            <div class="stat-value">{{ analytics.by_category[cat] || 0 }}</div>
            <div class="stat-label">{{ cat }}</div>
          </div>
        </div>
      </section>

      <!-- Email List Section -->
      <section class="emails-section">
        <h2>Recent Emails</h2>
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="emails.length === 0" class="empty-state">
          <p>No emails yet. Configure your n8n workflow to send emails.</p>
        </div>
        <div v-else class="email-list">
          <div v-for="email in emails" :key="email.id" class="email-item" :class="'cat-' + email.category.toLowerCase()">
            <div class="email-header">
              <div class="email-from">
                <span class="category-badge">{{ email.category }}</span>
                <strong>{{ email.sender }}</strong>
              </div>
              <button @click="deleteEmail(email.id)" class="delete-btn">✕</button>
            </div>
            <div class="email-subject">{{ email.subject }}</div>
            <div class="email-date">{{ formatDate(email.received_at) }}</div>
          </div>
        </div>
      </section>
    </div>

    <!-- Setup Guide -->
    <footer class="setup-guide">
      <details>
        <summary>📋 n8n Webhook Setup</summary>
        <div class="setup-content">
          <p><strong>Webhook URL:</strong></p>
          <code>http://localhost:5000/api/emails</code>
          <p style="margin-top: 10px;"><strong>Request Body (JSON):</strong></p>
          <pre>{
  "sender": "john@example.com",
  "subject": "Email Subject",
  "category": "University"
}</pre>
          <p style="margin-top: 10px;"><small>Categories: <code>University</code>, <code>Jobs</code>, <code>Personal</code>, <code>Other</code></small></p>
        </div>
      </details>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      emails: [],
      analytics: {
        total: 0,
        by_category: {}
      },
      loading: true
    }
  },
  methods: {
    async fetchEmails() {
      try {
        const res = await axios.get('/api/emails')
        this.emails = res.data
      } catch (err) {
        console.error('Error fetching emails:', err)
      }
    },
    async fetchAnalytics() {
      try {
        const res = await axios.get('/api/analytics')
        this.analytics = res.data
      } catch (err) {
        console.error('Error fetching analytics:', err)
      } finally {
        this.loading = false
      }
    },
    async deleteEmail(id) {
      if (!confirm('Delete this email?')) return
      try {
        await axios.delete(`/api/emails/${id}`)
        await this.fetchEmails()
        await this.fetchAnalytics()
      } catch (err) {
        console.error('Error deleting email:', err)
      }
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleString()
    }
  },
  mounted() {
    this.fetchEmails()
    this.fetchAnalytics()

    // Refresh every 5 seconds
    setInterval(() => {
      this.fetchEmails()
      this.fetchAnalytics()
    }, 5000)
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

header {
  text-align: center;
  margin-bottom: 40px;
  padding: 20px 0;
}

header h1 {
  font-size: 2.5em;
  margin-bottom: 5px;
}

header p {
  color: #666;
  font-size: 1.1em;
}

.content {
  display: grid;
  gap: 30px;
}

section h2 {
  margin-bottom: 20px;
  font-size: 1.5em;
}

/* Analytics */
.analytics {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.stat-card:nth-child(2) {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-card:nth-child(3) {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-card:nth-child(4) {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-card:nth-child(5) {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.stat-value {
  font-size: 2em;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9em;
  opacity: 0.9;
}

/* Emails */
.emails-section {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.loading, .empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
  font-size: 1.1em;
}

.email-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.email-item {
  border-left: 4px solid #ddd;
  padding: 15px;
  background: #fafafa;
  border-radius: 4px;
  transition: all 0.2s;
}

.email-item:hover {
  background: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.email-item.cat-university {
  border-left-color: #f5576c;
}

.email-item.cat-jobs {
  border-left-color: #00f2fe;
}

.email-item.cat-personal {
  border-left-color: #43e97b;
}

.email-item.cat-other {
  border-left-color: #fee140;
}

.email-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.email-from {
  display: flex;
  align-items: center;
  gap: 10px;
}

.category-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.8em;
  font-weight: 600;
  color: white;
}

.email-item.cat-university .category-badge {
  background: #f5576c;
}

.email-item.cat-jobs .category-badge {
  background: #00f2fe;
  color: #333;
}

.email-item.cat-personal .category-badge {
  background: #43e97b;
  color: #333;
}

.email-item.cat-other .category-badge {
  background: #fee140;
  color: #333;
}

.email-subject {
  font-weight: 500;
  margin-bottom: 5px;
}

.email-date {
  font-size: 0.85em;
  color: #999;
}

.delete-btn {
  background: none;
  border: none;
  color: #ccc;
  font-size: 1.2em;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.delete-btn:hover {
  background: #f0f0f0;
  color: #f5576c;
}

/* Setup Guide */
.setup-guide {
  margin-top: 40px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.setup-guide details {
  cursor: pointer;
}

.setup-guide summary {
  font-weight: 600;
  padding: 10px;
  user-select: none;
}

.setup-guide summary:hover {
  background: #f5f5f5;
  border-radius: 4px;
}

.setup-content {
  padding: 15px;
  background: #f9f9f9;
  border-radius: 4px;
  margin-top: 10px;
  font-size: 0.95em;
  line-height: 1.6;
}

.setup-content code {
  background: white;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  color: #d63384;
}

.setup-content pre {
  background: white;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  border: 1px solid #ddd;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

p {
  margin: 10px 0;
}
</style>
