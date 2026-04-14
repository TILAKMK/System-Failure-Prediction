# Vercel Portal Setup (Non-Disruptive)

This folder is isolated from your Streamlit code and data.

## What this does

- Hosts a lightweight portal on Vercel.
- Redirects users to your Streamlit app URL.
- Does not modify or run your model training/data pipeline.

## Configure

1. Edit `streamlit.config.js`.
2. Replace:

   ```js
   window.STREAMLIT_APP_URL = "https://YOUR-STREAMLIT-APP-URL.streamlit.app";
   ```

   with your real Streamlit URL.

## Deploy in Vercel

1. Push this repository to GitHub.
2. In Vercel, create a new project from this repo.
3. Set **Root Directory** to `system_failure_v14/system_failure_v13/system_failure_v12/system_failure_v6/vercel_app`.
4. Keep default build settings (no framework needed).
5. Deploy.

## Streamlit Impact

No impact, as long as your Streamlit deployment continues to use your existing app entry file and requirements from the original project path.
