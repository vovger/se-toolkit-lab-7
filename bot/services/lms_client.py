import httpx
from config import settings
from typing import Optional, List, Dict, Any

class LMSClient:
    def __init__(self):
        self.base_url = settings.lms_api_base_url
        self.api_key = settings.lms_api_key
        self.timeout = settings.timeout_seconds

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

    def get_items(self) -> List[Dict[str, Any]]:
        """Fetch all items (labs and tasks)."""
        data = self._request("/items/")
        return data if isinstance(data, list) else []

    def get_pass_rates(self, lab: str) -> Dict[str, Any]:
        """Fetch pass rates for a specific lab."""
        return self._request(f"/analytics/pass-rates?lab={lab}")

    def get_health(self) -> bool:
        """Check if backend is reachable and has data."""
        try:
            items = self.get_items()
            return len(items) > 0
        except Exception:
            return False
