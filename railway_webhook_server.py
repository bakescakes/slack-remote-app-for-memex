#!/usr/bin/env python3
"""
Railway Webhook Server - Production webhook for Slack integration
This version is optimized for Railway deployment with environment variables
"""

import asyncio
import json
import logging
import os
from typing import Dict, Any
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import Response
import uvicorn

# Import our feedback system
from simple_feedback_queue import submit_feedback_response

# Configure logging for Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Slack Feedback Webhook - Railway",
    version="1.0.0",
    description="Production webhook server for Slack feedback integration"
)

@app.post("/slack/events")
async def handle_slack_events(request: Request):
    """Handle Slack event webhooks with proper challenge response"""
    try:
        body = await request.body()
        logger.info(f"Received webhook: {len(body)} bytes")
        
        data = json.loads(body)
        
        # Handle URL verification challenge - MUST return just the challenge value
        if data.get("type") == "url_verification":
            challenge = data.get("challenge")
            logger.info(f"URL verification challenge: {challenge}")
            
            # Return JUST the challenge value as plain text
            return Response(content=challenge, media_type="text/plain")
        
        # Handle events
        if data.get("type") == "event_callback":
            event = data.get("event", {})
            await process_event(event)
            return {"status": "ok"}
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        return {"error": str(e)}

async def process_event(event: Dict[str, Any]):
    """Process Slack events"""
    try:
        event_type = event.get("type")
        user_id = event.get("user")
        text = event.get("text", "")
        
        logger.info(f"Processing event: {event_type} from user {user_id}")
        
        # Skip bot messages
        if event.get("bot_id") or user_id == "U0955NCNTKM":
            logger.info("Skipping bot message")
            return
            
        # Handle direct messages from Scott
        if event_type == "message" and user_id == "U094XRPVBQX":
            logger.info(f"📥 Received message from Scott: {text}")
            
            # Submit to feedback queue
            success = await submit_feedback_response(user_id, text)
            if success:
                logger.info(f"✅ Feedback submitted successfully: {text}")
            else:
                logger.warning(f"⚠️ No pending feedback request found for {user_id}")
                
    except Exception as e:
        logger.error(f"Error processing event: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {
        "status": "healthy",
        "service": "Slack Feedback Webhook",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "environment": "railway"
    }

@app.get("/")
async def root():
    """Root endpoint with service info"""
    return {
        "service": "Slack Feedback Webhook Server",
        "version": "1.0.0",
        "status": "running",
        "environment": "railway",
        "endpoints": {
            "webhooks": "/slack/events",
            "health": "/health"
        },
        "description": "Production webhook server for Memex ↔ Slack feedback integration"
    }

@app.get("/info")
async def get_info():
    """Get server information"""
    return {
        "server_info": {
            "service": "Slack Feedback Webhook",
            "version": "1.0.0",
            "environment": "railway",
            "python_version": sys.version,
            "startup_time": datetime.now().isoformat()
        },
        "integration": {
            "purpose": "Handle Slack webhook events for feedback system",
            "target_user": "U094XRPVBQX",
            "supported_events": ["message", "url_verification"]
        }
    }

if __name__ == "__main__":
    # Railway provides PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    
    logger.info(f"🚂 Starting Railway Webhook Server on port {port}")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )