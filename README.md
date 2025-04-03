
# 🧠 Feedback Sentiment Routing System

This project implements a sentiment-aware feedback pipeline using Google Cloud services and Slack. It routes positive and negative feedback into appropriate Slack channels via sentiment analysis.

---

## 🚀 Architecture Overview

```
User → receive-feedback (Cloud Run)
     → feedback-topic (Pub/Sub)
        ├── positive-sub → positive-feedback (Cloud Run) → #followup
        └── negative-sub → negative-feedback (Cloud Run) → #support
```

---

## 📁 Project Structure

```
feedback-pipeline/
├── receive-feedback/              # Receives user feedback and publishes to Pub/Sub
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── positive-feedback/             # Processes positive feedback and alerts Slack
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── negative-feedback/             # Processes negative feedback and alerts Slack
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
└── README.md
```

---

## 🛠️ Technologies Used

- **Cloud Run** – serverless function hosting
- **Pub/Sub** – message distribution layer
- **Natural Language API** – sentiment analysis
- **Secret Manager** – securely stores Slack token
- **Slack API** – sends messages to #followup and #support

---