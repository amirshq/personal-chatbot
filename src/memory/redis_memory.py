import redis.asyncio as redis
import json 
from typing import List, Dict

"""
# This file contains implementations of a RedisMemory class for managing short-term memory in chatbot applications.
This class uses Redis to store and retrieve conversation messages efficiently and use following advantages of Redis features.

✅ TTL management (auto-expires after 1 hour - perfect for short-term memory)
✅ Uses Redis Lists (rpush/lrange) - perfect for conversation history
✅ decode_responses=True (cleaner code, no manual decoding)
✅ Specific method names (add_message, get_messages) - clear intent
✅ Better data structure (Lists vs simple key-value)
"""

class RedisMemory:
    """
    Redis-based short-term memory for chatbot conversations.
    
    Uses Redis Lists to store conversation messages with automatic expiration.
    Perfect for storing recent conversation context (last N turns).
    """
    def __init__(self, url: str, ttl_seconds: int = 3600):
        """
        Initialize Redis memory client.
        
        url: Redis connection URL (e.g., 'redis://localhost:6379/0')
        ttl_seconds: Time-to-live in seconds (default: 1 hour)
        """
        self.client = redis.from_url(url, decode_responses=True)
        self.ttl = ttl_seconds

    async def add_message(self, session_id: str, role: str, content: str) -> None:
        """Stores a user or assistant message in Redis for short-term conversation context (auto-expires after TTL).
            session_id: Unique session identifier
            role: Message role ('user' or 'assistant')
            content: Message content
        """
        key = f"chat:{session_id}"
        message = json.dumps({"role": role, "content": content})
        
        # Use Redis List (rpush) - perfect for conversation history
        await self.client.rpush(key, message)
        # Set expiration (TTL) - essential for short-term memory
        await self.client.expire(key, self.ttl)

    async def get_messages(self, session_id: str, limit: int = 10) -> List[Dict]:
        """
        Retrieve the last N messages from conversation history.
        
        session_id: Unique session identifier
        limit: Number of recent messages to retrieve
        return: List of message dictionaries
        """
        key = f"chat:{session_id}"
        # Get last N messages from Redis List
        messages = await self.client.lrange(key, -limit, -1)
        
        return [json.loads(m) for m in messages]

    async def clear(self, session_id: str) -> None:
        """
        Clear all messages for a session.
        session_id: Unique session identifier
        """
        await self.client.delete(f"chat:{session_id}")
