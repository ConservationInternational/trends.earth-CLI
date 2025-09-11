"""Authentication utilities for tecli"""

import logging
from datetime import datetime, timedelta

import requests

from tecli import config


def refresh_access_token():
    """Refresh the access token using the refresh token"""
    refresh_token = config.get("refresh_token")
    if not refresh_token:
        logging.debug("No refresh token available, need to login again")
        return False

    try:
        response = requests.post(
            url=config.get("url_api") + "/auth/refresh", json={"refresh_token": refresh_token}
        )

        if response.status_code == 200:
            body = response.json()
            # Update tokens in config
            config.set("JWT", body["access_token"])
            if "refresh_token" in body:
                config.set("refresh_token", body["refresh_token"])

            # Update token expiration time
            if "expires_in" in body:
                expires_at = datetime.now() + timedelta(seconds=body["expires_in"])
                config.set("token_expires_at", expires_at.isoformat())

            logging.debug("Access token refreshed successfully")
            return True
        else:
            logging.debug(f"Token refresh failed with status {response.status_code}")
            # Clear invalid tokens
            config.unset("refresh_token", "")
            config.unset("JWT", "")
            config.unset("token_expires_at", "")
            return False

    except Exception as e:
        logging.debug(f"Error refreshing token: {e}")
        return False


def is_token_expired():
    """Check if the current access token is expired"""
    expires_at_str = config.get("token_expires_at")
    if not expires_at_str:
        return True  # No expiration info, assume expired

    try:
        expires_at = datetime.fromisoformat(expires_at_str)
        # Consider token expired if it expires within 5 minutes
        buffer_time = timedelta(minutes=5)
        return datetime.now() + buffer_time >= expires_at
    except (ValueError, TypeError):
        return True  # Invalid expiration format, assume expired


def get_valid_token():
    """Get a valid access token, refreshing if necessary"""
    # Check if current token is expired
    if is_token_expired():
        logging.debug("Token is expired or about to expire, attempting refresh")
        if not refresh_access_token():
            logging.debug("Token refresh failed, need to login again")
            return None

    return config.get("JWT")


def make_authenticated_request(method, url, **kwargs):
    """Make an authenticated HTTP request with automatic token refresh"""
    token = get_valid_token()
    if not token:
        logging.error("No valid token available. Please login first.")
        return None

    # Add authorization header
    headers = kwargs.get("headers", {})
    headers["Authorization"] = f"Bearer {token}"
    kwargs["headers"] = headers

    # Make the request
    response = getattr(requests, method.lower())(url, **kwargs)

    # If we get a 401, try to refresh the token once and retry
    if response.status_code == 401:
        logging.debug("Got 401 response, attempting to refresh token")
        if refresh_access_token():
            # Update the token in headers and retry
            token = config.get("JWT")
            headers["Authorization"] = f"Bearer {token}"
            kwargs["headers"] = headers
            response = getattr(requests, method.lower())(url, **kwargs)
        else:
            logging.error("Token refresh failed. Please login again.")

    return response
