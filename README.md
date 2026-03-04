# 📅 ContentCalendar — Social Media Post Planner

A full-stack social media content planner with a Kanban board UI, platform filtering, and an AI-powered hashtag suggester.

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Backend:** Python (Flask) + Flask-CORS
- **Database:** SQLite
- **Hashtag Engine:** Custom NLP keyword-matching algorithm (Python)

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/contentcalendar.git
cd contentcalendar
```

### 2. Set up the backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
> Backend runs on http://localhost:5000

### 3. Open the frontend
Open `frontend/index.html` in your browser.
> Or use Live Server in VS Code for best experience.

---

## ✨ Features

| Feature | Description |
|---|---|
| Kanban Board | 4 columns: To Write → Draft → Ready → Posted |
| Drag & Drop | Move posts between columns |
| Platform Badges | Tag posts as Instagram / Twitter / LinkedIn |
| Hashtag Suggester | Type a topic, get relevant hashtags instantly |
| Filter by Platform | View posts per social media channel |
| Edit & Delete | Full CRUD for all posts |
| Scheduled Dates | Set a target publish date per post |

---

## 📁 Project Structure
```
contentcalendar/
├── backend/
│   ├── app.py              # Flask REST API
│   ├── hashtag_engine.py   # Hashtag suggestion logic
│   ├── requirements.txt
│   └── database.db         # Auto-created on first run
├── frontend/
│   └── index.html          # Single-file frontend
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/posts` | Get all posts (filter with `?platform=instagram`) |
| POST | `/api/posts` | Create new post |
| PUT | `/api/posts/:id` | Update a post |
| DELETE | `/api/posts/:id` | Delete a post |
| PATCH | `/api/posts/:id/status` | Update post status (for drag & drop) |
| POST | `/api/hashtags` | Get hashtag suggestions for a topic |

---

## 💡 Interview Talking Points
- Built a RESTful Flask API with full CRUD operations
- Designed a normalized SQLite schema with proper migrations
- Implemented a custom NLP keyword-extraction hashtag engine
- Built a drag-and-drop Kanban board in pure JavaScript
- Handled CORS, error states, and graceful offline/demo mode
- Clean separation of concerns: backend logic, data layer, frontend

---

## 🌐 Deployment
- **Backend:** Deploy on [Render](https://render.com) (free tier)
- **Frontend:** Deploy on [GitHub Pages](https://pages.github.com) or [Vercel](https://vercel.com)
- Update `const API` in `index.html` to point to your deployed backend URL

---

Made by Tanya · Portfolio Project
