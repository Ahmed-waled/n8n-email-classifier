<template>
  <div class="container">
    <header>
      <h1>📧 Email Automation</h1>
      <p>n8n Workflow Showcase</p>
    </header>

    <div class="content">
      <!-- Analytics Section -->
      <section class="analytics">
        <h2>Analytics Dashboard</h2>
        <div class="stats">
          <div class="stat-card total">
            <div class="stat-icon">📬</div>
            <div class="stat-info">
              <div class="stat-value">{{ analytics.total }}</div>
              <div class="stat-label">Total Emails</div>
            </div>
          </div>
          <div class="stat-card" v-for="cat in ['University', 'Jobs', 'Personal', 'Other']" :key="cat" :class="'cat-' + cat.toLowerCase()">
            <div class="stat-icon">📌</div>
            <div class="stat-info">
              <div class="stat-value">{{ analytics.by_category[cat] || 0 }}</div>
              <div class="stat-label">{{ cat }}</div>
            </div>
          </div>
        </div>
        
        <!-- Additional Insights -->
        <div class="insights">
          <div class="insight-card">
            <h3>Most Recent</h3>
            <p v-if="emails.length > 0">{{ formatDate(emails[0].received_at) }}</p>
            <p v-else>No emails yet</p>
          </div>
          <div class="insight-card">
            <h3>Top Category</h3>
            <p v-if="topCategory">{{ topCategory.name }} ({{ topCategory.count }})</p>
            <p v-else>No data</p>
          </div>
          <div class="insight-card">
            <h3>Avg. per Category</h3>
            <p>{{ averagePerCategory }}</p>
          </div>
        </div>
      </section>

      <!-- Email List Section -->
      <section class="emails-section">
        <div class="section-header">
          <h2>Recent Emails</h2>
          <span class="email-count">{{ filteredEmails.length }} emails</span>
        </div>

        <!-- Category Filter -->
        <div class="category-filter">
          <button 
            class="filter-btn" 
            :class="{ active: selectedCategory === null }"
            @click="selectedCategory = null"
          >
            All Categories
          </button>
          <button 
            v-for="cat in ['University', 'Jobs', 'Personal', 'Other']"
            :key="cat"
            class="filter-btn"
            :class="getCategoryFilterClasses(cat)"
            @click="selectedCategory = cat"
          >
            {{ cat }}
            <span class="filter-count">{{ analytics.by_category[cat] || 0 }}</span>
          </button>
        </div>

        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="filteredEmails.length === 0" class="empty-state">
          <p v-if="selectedCategory">No emails in {{ selectedCategory }} category.</p>
          <p v-else>No emails yet. Configure your n8n workflow to send emails.</p>
        </div>
        <div v-else class="email-list">
          <div 
            v-for="email in filteredEmails" 
            :key="email.id" 
            class="email-item" 
            :class="'cat-' + email.category.toLowerCase()"
            @click="selectEmail(email)"
          >
            <div class="email-header">
              <div class="email-from">
                <span class="category-badge">{{ email.category }}</span>
                <div class="email-meta">
                  <strong>{{ email.sender }}</strong>
                  <span class="email-date">{{ formatDate(email.received_at) }}</span>
                </div>
              </div>
              <button @click.stop="deleteEmail(email.id)" class="delete-btn">✕</button>
            </div>
            <div class="email-subject">{{ email.subject }}</div>
            <div class="email-preview">{{ truncate(email.summary, 100) }}...</div>
          </div>
        </div>
      </section>
    </div>

    <!-- Email Detail Modal -->
    <transition name="modal">
      <div v-if="selectedEmail" class="modal-overlay" @click="selectedEmail = null">
        <div class="modal-content" @click.stop>
          <button class="modal-close" @click="selectedEmail = null">✕</button>
          
          <div class="modal-header">
            <span class="modal-category-badge" :class="'cat-' + selectedEmail.category.toLowerCase()">
              {{ selectedEmail.category }}
            </span>
            <div class="modal-title">
              <h2>{{ selectedEmail.subject }}</h2>
              <p class="modal-from">From: {{ selectedEmail.sender }}</p>
            </div>
          </div>

          <div class="modal-meta">
            <div class="meta-item">
              <span class="meta-label">Received</span>
              <span class="meta-value">{{ formatDateTime(selectedEmail.received_at) }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">ID</span>
              <span class="meta-value">#{{ selectedEmail.id }}</span>
            </div>
          </div>

          <div class="modal-summary">
            <h3>Summary</h3>
            <p>{{ selectedEmail.summary }}</p>
          </div>

          <div class="modal-actions">
            <button class="btn btn-delete" @click="deleteEmail(selectedEmail.id)">Delete Email</button>
            <button class="btn btn-close" @click="selectedEmail = null">Close</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Setup Guide -->
    <footer class="setup-guide">
      <details>
        <summary>📋 n8n Webhook Setup</summary>
        <div class="setup-content">
          <p><strong>Webhook URL:</strong></p>
          <code>https://hadley-considerate-dalia.ngrok-free.dev/api/emails</code>
          <p style="margin-top: 10px;"><strong>Request Body (JSON):</strong></p>
          <pre>{
  "sender": "john@example.com",
  "subject": "Email Subject",
  "category": "University",
  "summary": "summary of the email body"
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
      selectedEmail: null,
      selectedCategory: null, // null means show all
      analytics: {
        total: 0,
        by_category: {}
      },
      loading: true
    }
  },
  computed: {
    filteredEmails() {
      if (!this.selectedCategory) return this.emails
      return this.emails.filter(email => email.category === this.selectedCategory)
    },
    topCategory() {
      const categories = this.analytics.by_category
      if (Object.keys(categories).length === 0) return null
      const top = Object.entries(categories).sort((a, b) => b[1] - a[1])[0]
      return { name: top[0], count: top[1] }
    },
    averagePerCategory() {
      if (this.analytics.total === 0) return '0'
      const count = Object.keys(this.analytics.by_category).length
      return (this.analytics.total / count).toFixed(1)
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
    selectEmail(email) {
      this.selectedEmail = email
    },
    async deleteEmail(id) {
      if (!confirm('Delete this email?')) return
      try {
        await axios.delete(`/api/emails/${id}`)
        this.selectedEmail = null
        await this.fetchEmails()
        await this.fetchAnalytics()
      } catch (err) {
        console.error('Error deleting email:', err)
      }
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      const today = new Date()
      const yesterday = new Date(today)
      yesterday.setDate(yesterday.getDate() - 1)
      
      if (date.toDateString() === today.toDateString()) {
        return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
      } else if (date.toDateString() === yesterday.toDateString()) {
        return 'Yesterday'
      } else {
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
      }
    },
    formatDateTime(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleString('en-US', { 
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    truncate(str, length) {
      return str.length > length ? str.substring(0, length) : str
    },
    getCategoryFilterClasses(cat) {
      return {
        active: this.selectedCategory === cat,
        ['cat-' + cat.toLowerCase()]: true
      }
    }
  },
  mounted() {
    this.fetchEmails()
    this.fetchAnalytics()

    // Refresh every 30 seconds
    setInterval(() => {
      this.fetchEmails()
      this.fetchAnalytics()
    }, 30000)
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
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
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.stat-card {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: default;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.stat-card.total {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-card.cat-university {
  background: linear-gradient(135deg, #f5576c 0%, #f93245 100%);
}

.stat-card.cat-jobs {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-card.cat-personal {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-card.cat-other {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.stat-icon {
  font-size: 2em;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 1.8em;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9em;
  opacity: 0.95;
}

.insights {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  padding-top: 20px;
  border-top: 2px solid #f0f0f0;
}

.insight-card {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.insight-card h3 {
  margin: 0 0 8px 0;
  font-size: 0.9em;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.insight-card p {
  margin: 0;
  font-size: 1.3em;
  font-weight: 600;
  color: #333;
}

/* Emails */
.emails-section {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0;
}

.email-count {
  background: #e8eef7;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.9em;
  color: #667eea;
  font-weight: 600;
}

/* Category Filter */
.category-filter {
  display: flex;
  gap: 10px;
  margin-bottom: 25px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 16px;
  border: 2px solid #e0e0e0;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9em;
  font-weight: 500;
  color: #666;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
}

.filter-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.filter-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.filter-btn.cat-university {
  border-color: #f5576c;
}

.filter-btn.cat-university:hover {
  color: #f5576c;
  border-color: #f5576c;
}

.filter-btn.cat-university.active {
  background: #f5576c;
  color: white;
  border-color: #f5576c;
}

.filter-btn.cat-jobs {
  border-color: #00f2fe;
}

.filter-btn.cat-jobs:hover {
  color: #00f2fe;
  border-color: #00f2fe;
}

.filter-btn.cat-jobs.active {
  background: #00f2fe;
  color: #333;
  border-color: #00f2fe;
}

.filter-btn.cat-personal {
  border-color: #43e97b;
}

.filter-btn.cat-personal:hover {
  color: #43e97b;
  border-color: #43e97b;
}

.filter-btn.cat-personal.active {
  background: #43e97b;
  color: #333;
  border-color: #43e97b;
}

.filter-btn.cat-other {
  border-color: #fee140;
}

.filter-btn.cat-other:hover {
  color: #fee140;
  border-color: #fee140;
}

.filter-btn.cat-other.active {
  background: #fee140;
  color: #333;
  border-color: #fee140;
}

.filter-count {
  display: inline-block;
  background: rgba(0, 0, 0, 0.1);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.8em;
  font-weight: 600;
}

.filter-btn.active .filter-count {
  background: rgba(255, 255, 255, 0.3);
}

.loading, .empty-state {
  text-align: center;
  padding: 60px 20px;
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
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  transition: all 0.2s;
  cursor: pointer;
  position: relative;
}

.email-item:hover {
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-left-width: 6px;
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
  align-items: flex-start;
  margin-bottom: 10px;
}

.email-from {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.email-meta {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.email-meta strong {
  color: #333;
  font-size: 0.95em;
}

.category-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75em;
  font-weight: 700;
  color: white;
  white-space: nowrap;
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
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
  font-size: 1em;
}

.email-preview {
  font-size: 0.85em;
  color: #666;
  line-height: 1.4;
}

.email-date {
  font-size: 0.8em;
  color: #999;
}

.delete-btn {
  background: none;
  border: none;
  color: #ccc;
  font-size: 1.2em;
  cursor: pointer;
  padding: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
  flex-shrink: 0;
}

.delete-btn:hover {
  background: #f0f0f0;
  color: #f5576c;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  position: relative;
}

.modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
  z-index: 1001;
}

.modal-close:hover {
  background: #f0f0f0;
  color: #333;
}

.modal-header {
  padding: 30px 30px 20px 30px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  gap: 15px;
  align-items: flex-start;
}

.modal-category-badge {
  padding: 6px 14px;
  border-radius: 12px;
  font-size: 0.8em;
  font-weight: 700;
  color: white;
  white-space: nowrap;
  flex-shrink: 0;
}

.modal-category-badge.cat-university {
  background: #f5576c;
}

.modal-category-badge.cat-jobs {
  background: #00f2fe;
  color: #333;
}

.modal-category-badge.cat-personal {
  background: #43e97b;
  color: #333;
}

.modal-category-badge.cat-other {
  background: #fee140;
  color: #333;
}

.modal-title {
  flex: 1;
}

.modal-title h2 {
  margin: 0 0 8px 0;
  font-size: 1.5em;
  color: #333;
}

.modal-from {
  margin: 0;
  color: #666;
  font-size: 0.95em;
}

.modal-meta {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  padding: 20px 30px;
  background: #f9f9f9;
  border-bottom: 1px solid #f0f0f0;
}

.meta-item {
  display: flex;
  flex-direction: column;
}

.meta-label {
  font-size: 0.75em;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
  font-weight: 600;
}

.meta-value {
  font-size: 0.95em;
  color: #333;
  font-weight: 500;
}

.modal-summary {
  padding: 30px;
}

.modal-summary h3 {
  margin: 0 0 15px 0;
  font-size: 1.1em;
  color: #333;
}

.modal-summary p {
  margin: 0;
  color: #666;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.modal-actions {
  padding: 20px 30px;
  background: #f9f9f9;
  border-top: 1px solid #f0f0f0;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 0.95em;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-delete {
  background: #f5576c;
  color: white;
}

.btn-delete:hover {
  background: #e94556;
}

.btn-close {
  background: #e8eef7;
  color: #667eea;
}

.btn-close:hover {
  background: #d4dce8;
}

/* Modal Transition */
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.2s;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

/* Setup Guide */
.setup-guide {
  margin-top: 40px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.setup-guide details {
  cursor: pointer;
}

.setup-guide summary {
  font-weight: 600;
  padding: 10px;
  user-select: none;
  transition: all 0.2s;
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
