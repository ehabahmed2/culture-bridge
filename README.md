# 🌐 AI Cultural Translator for Social Media

[![Django](https://img.shields.io/badge/Django==5.2.3-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Stripe](https://img.shields.io/badge/Powered_by-Stripe-635BFF.svg?logo=stripe)](https://stripe.com)
[![Gemini](https://img.shields.io/badge/Google_Gemini_API-0.1.0-orange.svg)](https://ai.google.dev/)
[![Live Demo](https://img.shields.io/badge/demo-live-green.svg)](http://cultureBridge.pythonanywhere.com/)

An AI-powered tool that rewrites social media posts in culturally appropriate tones and dialects, helping users localize content for global audiences. Built with Django and Google Gemini API.

![App Screenshot](https://i.postimg.cc/ydNn5vH2/2025-06-18-18-11-42-Window.png)

## 🚀 Project Overview

The AI Cultural Translator enables users to:
- Input social media posts and translate them into culturally appropriate tones
- Select from various cultural dialects (Egyptian, American, Japanese, etc.)
- Maintain translation history
- Upgrade to premium features via Stripe subscriptions

Perfect for marketers, content creators, and global businesses looking to improve cultural resonance of their social media content.

## ✅ Features

| Feature | Status |
|---------|--------|
| Text input for social media post | ✅ Done |
| Cultural tone selection | ✅ Done |
| Translation via Google Gemini API | ✅ Done |
| Save translation history | ✅ Done |
| Copy and share buttons | ✅ Done |
| User authentication | ✅ Done |
| Stripe payment integration | ✅ Done |
| Loading spinner & error handling | ✅ Done |
| Subscription plans | ✅ Done |
| Rate-limiting for free users | ✅ Done |
| Feedback form | ✅ Done |
| Auto-post scheduling | ❌ Future |

## 📦 Tech Stack

**Backend**  
- Django (Python)
- Django REST Framework
- PostgreSQL (SQLite for development)

**Frontend**  
- Django Templates
- Bootstrap 5
- JavaScript 

**APIs & Services**  
- Google Gemini API (AI translations)
- Stripe API (Payments)
- Render/Heroku (Hosting)

**Development Tools**  
- Poetry (Dependency management)
- Gunicorn (Production server)
- Whitenoise (Static files)

## 💻 Project Structure


## ✨ Key Implementation Details

### 🧠 AI Translation Engine
```python
# translator/gemini_client.py
import google.generativeai as genai

class GeminiTranslator:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def translate_post(self, text, culture):
        prompt = self._load_culture_prompt(culture)
        response = self.model.generate_content(prompt.format(text=text))
        return response.text
```

## 🔒 User Authentication
- Register
- Custom User
- Login

## 💳 Stripe Integration

## 🚧 Roadmap
**Immediate Priorities**

- Implement rate limiting middleware
- Add user feedback system
- Translation quality ratings
- Expand cultural dialect coverage

**Future Enhancements**
- Browser extension integration
- Team collaboration features
- Social media auto-posting

## 📄 License
- This project is licensed under the MIT License. For demonstration purposes only.
