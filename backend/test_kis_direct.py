"""Direct KIS API test to diagnose 403 error."""
import asyncio
import httpx
from app.db.session import AsyncSessionLocal
from sqlalchemy import select
from app.models.user import User

async def test_kis_api():
    """Test KIS API with user credentials from database."""
    # Get user from database
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.id == 2))
        user = result.scalar_one_or_none()

        if not user:
            print("User not found")
            return

        print(f"Testing KIS API for user: {user.email}")
        print(f"Account Number: {user.kis_account_number}")
        print(f"Account Code: {user.kis_account_code}")
        print(f"Trading Mode: {user.kis_trading_mode}")
        print(f"App Key (first 10 chars): {user.kis_app_key[:10]}...")
        print(f"App Secret (first 10 chars): {user.kis_app_secret[:10]}...")
        print()

        # Determine base URL
        base_url = "https://openapivts.koreainvestment.com:29443"  # MOCK
        if user.kis_trading_mode == "REAL":
            base_url = "https://openapi.koreainvestment.com:9443"

        url = f"{base_url}/oauth2/tokenP"

        payload = {
            "grant_type": "client_credentials",
            "appkey": user.kis_app_key,
            "appsecret": user.kis_app_secret,
        }

        print(f"Request URL: {url}")
        print(f"Request Payload:")
        print(f"  grant_type: {payload['grant_type']}")
        print(f"  appkey: {payload['appkey'][:10]}...")
        print(f"  appsecret: {payload['appsecret'][:10]}...")
        print()

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)

                print(f"Response Status Code: {response.status_code}")
                print(f"Response Headers:")
                for key, value in response.headers.items():
                    print(f"  {key}: {value}")
                print()
                print(f"Response Body:")
                print(response.text)
                print()

                if response.status_code == 200:
                    data = response.json()
                    print("✅ SUCCESS!")
                    print(f"Access Token (first 20 chars): {data.get('access_token', '')[:20]}...")
                    print(f"Token Type: {data.get('token_type')}")
                    print(f"Expires In: {data.get('expires_in')} seconds")
                else:
                    print(f"❌ ERROR: HTTP {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"Error Details: {error_data}")
                    except:
                        print(f"Error Text: {response.text}")

        except Exception as e:
            print(f"❌ Exception occurred: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_kis_api())
