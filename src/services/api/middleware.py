"""
Implements custom middleware for logging, authentication, and security.

This module defines middleware functions for the FastAPI application to log incoming
requests, validate authentication tokens, and ensure overall security. It can be extended
to include more advanced security checks as needed.

Assumptions:
- The middleware is used with FastAPI.
- Authentication tokens (e.g., JWT) are used for secured endpoints.
"""

import time
import logging
from fastapi import Request, HTTPException

# Configure logger for middleware.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_middleware")

async def logging_middleware(request: Request, call_next):
    """
    Middleware that logs the request method, URL, and processing time.

    Args:
        request (Request): The incoming request object.
        call_next: The next middleware or request handler.

    Returns:
        Response: The response from the downstream service.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # in milliseconds
    logger.info(f"{request.method} {request.url} completed in {process_time:.2f}ms")
    return response

async def authentication_middleware(request: Request, call_next):
    """
    Middleware that checks for the presence of an authentication token in the request headers.
    Raises HTTPException if the token is missing or invalid.

    Args:
        request (Request): The incoming request object.
        call_next: The next middleware or request handler.

    Returns:
        Response: The response from the downstream service.
    """
    token = request.headers.get("Authorization")
    if not token:
        logger.warning("Missing Authorization token")
        raise HTTPException(status_code=401, detail="Unauthorized: Missing token")
    # TODO: Validate token (e.g., using JWT) here.
    # For demonstration, we assume any token is valid.
    response = await call_next(request)
    return response

# To integrate these middleware functions into your FastAPI app, add them as follows:
# app.middleware("http")(logging_middleware)
# app.middleware("http")(authentication_middleware)
