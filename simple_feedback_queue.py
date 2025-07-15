#!/usr/bin/env python3
"""
Simple Feedback Queue for Railway deployment
Stores feedback requests in memory (for demo) or could use Redis/DB for production
"""

import asyncio
import time
from typing import Dict, Optional
from datetime import datetime
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class FeedbackRequest:
    """Simple feedback request"""
    id: str
    user_id: str
    message: str
    created_at: str
    timeout_seconds: int
    status: str = "waiting"
    response_text: Optional[str] = None

class SimpleFeedbackQueue:
    """Simple in-memory feedback queue"""
    
    def __init__(self):
        self.requests: Dict[str, FeedbackRequest] = {}
        self.events: Dict[str, asyncio.Event] = {}
    
    async def create_request(self, user_id: str, message: str, timeout_seconds: int = 300) -> str:
        """Create feedback request"""
        request_id = f"feedback_{user_id}_{int(time.time())}"
        
        request = FeedbackRequest(
            id=request_id,
            user_id=user_id,
            message=message,
            created_at=datetime.now().isoformat(),
            timeout_seconds=timeout_seconds
        )
        
        self.requests[request_id] = request
        self.events[request_id] = asyncio.Event()
        
        logger.info(f"Created feedback request {request_id}")
        return request_id
    
    async def wait_for_response(self, request_id: str) -> Optional[str]:
        """Wait for response"""
        if request_id not in self.events:
            return None
        
        try:
            request = self.requests.get(request_id)
            if not request:
                return None
            
            # Wait for response or timeout
            await asyncio.wait_for(self.events[request_id].wait(), timeout=request.timeout_seconds)
            
            # Get response
            if request.status == "completed":
                return request.response_text
            return None
            
        except asyncio.TimeoutError:
            logger.warning(f"Timeout for request {request_id}")
            return None
    
    async def submit_response(self, user_id: str, response_text: str) -> bool:
        """Submit response"""
        # Find pending request for user
        for request in self.requests.values():
            if request.user_id == user_id and request.status == "waiting":
                request.status = "completed"
                request.response_text = response_text
                
                # Notify waiting coroutine
                if request.id in self.events:
                    self.events[request.id].set()
                    logger.info(f"Response submitted for {request.id}")
                    return True
        
        logger.warning(f"No pending request for user {user_id}")
        return False

# Global instance
feedback_queue = SimpleFeedbackQueue()

# Convenience functions
async def create_feedback_request(user_id: str, message: str, timeout_seconds: int = 300) -> str:
    return await feedback_queue.create_request(user_id, message, timeout_seconds)

async def wait_for_feedback_response(request_id: str) -> Optional[str]:
    return await feedback_queue.wait_for_response(request_id)

async def submit_feedback_response(user_id: str, response_text: str) -> bool:
    return await feedback_queue.submit_response(user_id, response_text)