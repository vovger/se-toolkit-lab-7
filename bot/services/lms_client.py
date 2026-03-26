import httpx
from config import settings
from typing import Optional, List, Dict, Any

class LMSClient:
    def __init__(self):
        self.base_url = settings.lms_api_base_url
        self.api_key = settings.lms_api_key
        self.timeout = getattr(settings, 'timeout_seconds', 5)

    def _request(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Make authenticated GET request to LMS API."""
        url = f"{self.base_url}{endpoint}"
        headers = {"api-key": self.api_key}
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.get(url, headers=headers)
                resp.raise_for_status()
                return resp.json()
        except httpx.ConnectError:
            raise Exception(f"Connection refused to {self.base_url}. Check that backend is running.")
        except httpx.TimeoutException:
            raise Exception(f"Timeout connecting to {self.base_url} (>{self.timeout}s).")
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP {e.response.status_code}: {e.response.text[:200]}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

    def _post(self, endpoint: str, data: dict = None) -> Optional[Dict[str, Any]]:
        """Make authenticated POST request to LMS API."""
        url = f"{self.base_url}{endpoint}"
        headers = {"api-key": self.api_key, "Content-Type": "application/json"}
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.post(url, json=data or {}, headers=headers)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            raise Exception(f"POST error: {str(e)}")

    def get_items(self) -> List[Dict[str, Any]]:
        data = self._request("/items/")
        return data if isinstance(data, list) else []

    def get_learners(self) -> List[Dict[str, Any]]:
        data = self._request("/learners/")
        return data if isinstance(data, list) else []

    def get_scores(self, lab: str) -> Dict[str, Any]:
        return self._request(f"/analytics/scores?lab={lab}")

    def get_pass_rates(self, lab: str) -> Dict[str, Any]:
        return self._request(f"/analytics/pass-rates?lab={lab}")

    def get_timeline(self, lab: str) -> Dict[str, Any]:
        return self._request(f"/analytics/timeline?lab={lab}")

    def get_groups(self, lab: str) -> Dict[str, Any]:
        return self._request(f"/analytics/groups?lab={lab}")

    def get_top_learners(self, lab: str, limit: int = 5) -> Dict[str, Any]:
        return self._request(f"/analytics/top-learners?lab={lab}&limit={limit}")

    def get_completion_rate(self, lab: str) -> Dict[str, Any]:
        return self._request(f"/analytics/completion-rate?lab={lab}")

    def trigger_sync(self) -> Dict[str, Any]:
        return self._post("/pipeline/sync", {})
