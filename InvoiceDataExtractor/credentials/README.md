# Gmail API Credentials

Place your OAuth 2.0 credentials here:

1. **`client_secret.json`** — Download from Google Cloud Console  
   (APIs & Services → Credentials → OAuth 2.0 Client ID → Download JSON)

2. **`token.json`** — Auto-generated on first successful authentication  
   (Do not commit this file)

## Setup Steps

1. Go to https://console.cloud.google.com/
2. Create or select a project
3. Enable the **Gmail API** (APIs & Services → Library → search "Gmail API")
4. Configure the **OAuth consent screen** (External, add your email as test user)
5. Create credentials: **OAuth 2.0 Client ID** → Application type: **Desktop app**
6. Download the JSON and save it here as `client_secret.json`
7. Run the app — a browser window will open for authorization on first use
