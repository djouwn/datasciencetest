import os
import logging
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING
from pymongo.collection import Collection


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


class FacebookAPIError(Exception):
    """Exception raised when the Meta Graph API returns an error."""


class FacebookConnector:
    """
    Connector responsible for communicating with the Meta Graph API.
    """

    def __init__(
        self,
        access_token: str,
        api_version: str = "vXX.X",
        timeout: int = 20
    ):
        self.access_token = access_token
        self.base_url = f"https://graph.facebook.com/{api_version}"
        self.timeout = timeout

    def _request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        params = params or {}
        params["access_token"] = self.access_token

        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.get(
                url,
                params=params,
                timeout=self.timeout
            )
        except requests.RequestException as exc:
            raise FacebookAPIError(
                f"Network error while calling Meta API: {exc}"
            ) from exc

        if not response.ok:
            try:
                error = response.json().get("error", {})
            except ValueError:
                error = {}

            message = error.get(
                "message",
                response.text
            )

            raise FacebookAPIError(
                f"Meta API error: {message}"
            )

        return response.json()

    def get_post(
        self,
        post_id: str
    ) -> Dict[str, Any]:

        fields = ",".join([
            "id",
            "message",
            "created_time",
            "permalink_url",
            "full_picture",
            "attachments",
            "from"
        ])

        return self._request(
            post_id,
            {"fields": fields}
        )

    def get_comments(
        self,
        post_id: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:

        fields = ",".join([
            "id",
            "message",
            "created_time",
            "from"
        ])

        data = self._request(
            f"{post_id}/comments",
            {
                "fields": fields,
                "limit": limit
            }
        )

        return data.get("data", [])

    def collect_posts(
        self,
        page_id: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:

        fields = ",".join([
            "id",
            "message",
            "created_time",
            "permalink_url",
            "full_picture",
            "attachments",
            "from"
        ])

        response = self._request(
            f"{page_id}/posts",
            {
                "fields": fields,
                "limit": limit
            }
        )

        return response.get("data", [])