# Sentiment Analyzer Dashboard 🔍

A real-time AI-powered web application for text sentiment analysis with intelligent history tracking and PostgreSQL integration.

![Sentiment Analyzer](https://img.shields.io/badge/Sentiment-AI--Powered-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-red)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-green)

## 🚀 Features

### 🤖 Core Analysis

- **Real-time Sentiment Detection** - Instant POSITIVE/NEGATIVE classification
- **Confidence Scoring** - Percentage-based confidence levels and positive/negative score visualization
- **AI-Powered Backend** - Hugging Face Transformers integration

### 📊 History & Analytics

- **Analysis History** - Sidebar for analysis history
- **PostgreSQL Integration** - Persistent storage with FastAPI
- **One-Click Reload** - Revisit previous analyses instantly
- **Bulk Management** - Individual or bulk history deletion

## 🛠️ Tech Stack

### Frontend

- **HTML5** - Semantic markup
- **CSS3** - Modern gradients, flexbox, and animations
- **JavaScript ES6+** - Async/await, Fetch API, DOM manipulation

### Backend

- **Python** - Core programming language
- **FastAPI** - Modern, fast web framework
- **PostgreSQL** - Cloud based relational database (Neon DB)
- **Hugging Face** - Pre-trained sentiment analysis model

## 📦 Installation

### Backend Setup

```bash
# Clone repository
git clone https://github.com/Akhilesh2306/Sentiment-Analyzer-Dashboard.git
cd sentiment-analyzer

# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your database credentials

# Start FastAPI server
uvicorn main:app --reload
```
