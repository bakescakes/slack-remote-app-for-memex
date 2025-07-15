# Railway Deployment Guide

## Option 1: GitHub Integration (Recommended)

### Prerequisites
- Repository: https://github.com/bakescakes/slack-remote-app-for-memex
- Files ready: ✅ All Railway files created locally

### Steps:
1. **Authenticate with GitHub**:
   ```bash
   # Option A: GitHub CLI
   brew install gh
   gh auth login
   
   # Option B: Personal Access Token
   # Go to https://github.com/settings/tokens
   # Create token with repo permissions
   ```

2. **Push to GitHub**:
   ```bash
   cd /Users/scottbaker/Workspace/slack_remote_app_for_memex
   git remote add origin https://github.com/bakescakes/slack-remote-app-for-memex.git
   git add railway_webhook_server.py simple_feedback_queue.py Procfile railway.json requirements.txt
   git commit -m "Add Railway deployment files"
   git push -u origin main
   ```

3. **Deploy to Railway**:
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select: bakescakes/slack-remote-app-for-memex
   - Railway auto-deploys using Procfile

## Option 2: Manual Railway CLI

### If you prefer Railway CLI:
1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. **Initialize and Deploy**:
   ```bash
   cd /Users/scottbaker/Workspace/slack_remote_app_for_memex
   railway init
   railway up
   ```

## Railway Deployment Files ✅

### Files Ready for Deployment:
- ✅ `railway_webhook_server.py` - FastAPI webhook server
- ✅ `simple_feedback_queue.py` - Feedback coordination 
- ✅ `Procfile` - Railway start command
- ✅ `railway.json` - Health checks and monitoring
- ✅ `requirements.txt` - Dependencies (FastAPI, uvicorn, etc.)

### Expected Railway URL:
After deployment: `https://slack-feedback-webhook-production.up.railway.app`

## Next Steps After Deployment:

1. **Get Railway URL** from Railway dashboard
2. **Update Slack App**:
   - Go to https://api.slack.com/apps
   - Event Subscriptions → Request URL
   - Set to: `https://your-railway-url.railway.app/slack/events`
3. **Test integration** with immediate response (1-3 seconds)

## Benefits:
- ✅ Permanent stable URL
- ✅ 24/7 uptime
- ✅ No more ngrok issues
- ✅ Production-ready monitoring