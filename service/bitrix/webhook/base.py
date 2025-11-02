from typing import Optional, Dict, Any

class Lead:
    def __init__(self, id: int, name: str, phone: Optional[str], date_create: str):
        self.id = id
        self.name = name
        self.phone = phone
        self.date_create = date_create

    @classmethod
    def from_bitrix(cls, data: Dict[str, Any]):
        """
        Parse Bitrix lead JSON into a Lead instance.
        """
        # Bitrix API sometimes wraps result in "result", sometimes not
        result = data.get("result", data)

        # Extract phone if exists
        phone = None
        if result.get("PHONE"):
            # PHONE is usually a list of dicts with VALUE key
            phone = result["PHONE"][0].get("VALUE")

        # Use TITLE first, fallback to NAME
        name = result.get("TITLE") or result.get("NAME") or "N/A"

        return cls(
            id=int(result.get("ID")),
            name=name,
            phone=phone,
            date_create=result.get("DATE_CREATE")
        )



# service/bitrix/api/base.py
# service/bitrix/api/base.py
import httpx

INCOMING_WEBHOOK_URL = "https://b24-6fsyot.bitrix24.kz/rest/1/ngb9akw3fcdnxrob"

async def get_lead_by_id(lead_id: int) -> Optional[Dict[str, Any]]:
    """
    Fetch full lead info from Bitrix24 using the fixed incoming webhook URL.
    """
    url = f"{INCOMING_WEBHOOK_URL}/crm.lead.get.json"
    params = {"ID": lead_id}

    async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("result")
        except httpx.HTTPStatusError as e:
            print(f"Bitrix API error {e.response.status_code} for ID {lead_id}")
        except Exception as e:
            print(f"Bitrix API request failed: {e}")
    return None

