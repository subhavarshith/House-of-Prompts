# Deployment Instructions for Pulse-Guard

The backend and frontend have been combined into a single, Dockerized container for easy deployment to Google Cloud Run. We have packaged the Vite production build into the FastAPI `static/` folder.

Since `gcloud` is not installed on this machine or not in your PATH, you can deploy it directly via the Google Cloud Console or by installing the `gcloud` CLI.

## Option 1: Deploy using Google Cloud Console
1. Ensure your Google Cloud Project has the **Cloud Run built-in** enabled and a connected repository (or just upload the zip).
2. The recommended way is to push this `Pulse-Guard` folder to a GitHub repository.
3. In the Google Cloud Console, navigate to **Cloud Run**.
4. Click **Deploy Container** -> **Service**.
5. Choose **"Continuously deploy new revisions from a source repository"**.
6. Connect your GitHub repository.
7. Under **Variables & Secrets**, add the Gemini API Key:
   - Name: `GEMINI_API_KEY`
   - Value: `YOUR_GENERATE_GEMINI_API_KEY` (Keep this secret!)
8. Deploy! The service will automatically build using the `Dockerfile` provided.

## Option 2: Deploy using gcloud CLI
If you install the `gcloud` CLI, simply open a terminal in the `Pulse-Guard` directory and run:

```powershell
gcloud run deploy pulse-guard `
  --source . `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars="GEMINI_API_KEY=YOUR_API_KEY"
```

This will automatically build the container via Cloud Build and output your **Cloud Run URL**.
