# Slack Remote App for Memex - Railway Deployment

Railway deployment components for stable Slack webhook infrastructure.

## 🚂 Railway Deployment Files

### Core Components
- **railway_webhook_server.py** - Production FastAPI webhook server
- **simple_feedback_queue.py** - Feedback coordination system
- **Procfile** - Railway process configuration
- **railway.json** - Health checks and monitoring
- **requirements.txt** - All dependencies

### Configuration
- **.env.example** - Environment variable template
- **railway_deployment_guide.md** - Complete deployment instructions

## 🚀 Quick Deploy to Railway

1. **Connect this repository to Railway**
2. **Set environment variables:**
   ```
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_SIGNING_SECRET=your-signing-secret
   ```
3. **Deploy automatically** - Railway will use Procfile

## 🎯 Purpose

This provides stable 24/7 webhook infrastructure for Memex ↔ Slack integration, replacing unreliable ngrok tunnels with professional hosting.

### Key Features
- **Permanent webhook URL** (never changes)
- **Immediate response processing** (1-3 seconds)
- **Built-in health monitoring**
- **Automatic restarts and scaling**

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Enhanced Slack  │───▶│ get_feedback     │───▶│ Railway Webhook │
│ MCP Server      │    │ Tool             │    │ Server          │
│ (49 tools)      │    │                  │    │ (Production)    │ 
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                          │
                              ▼                          ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Memex waits for │◀───│ Feedback Queue   │◀───│ Slack Events    │
│ response        │    │ Coordination     │    │ API             │
│ (1-3 seconds)   │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

---

**Generated with [Memex](https://memex.tech)**
