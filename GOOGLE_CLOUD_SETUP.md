# Google Cloud Setup Guide for Imagen 3

## Prerequisites
1. Google Cloud Account
2. Billing enabled
3. Vertex AI API enabled

## Step-by-Step Setup

### 1. Create Google Cloud Project
1. Go to https://console.cloud.google.com/
2. Create a new project or select existing one
3. Note your **Project ID** (e.g., `my-ai-character-project`)

### 2. Enable Vertex AI API
```bash
gcloud services enable aiplatform.googleapis.com
```

Or via Console:
1. Go to https://console.cloud.google.com/apis/library
2. Search for "Vertex AI API"
3. Click "Enable"

### 3. Create Service Account
```bash
# Create service account
gcloud iam service-accounts create imagen-character-gen \
    --display-name="Imagen Character Generator"

# Grant permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:imagen-character-gen@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Create key
gcloud iam service-accounts keys create ~/imagen-key.json \
    --iam-account=imagen-character-gen@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

### 4. Set Environment Variables
Add to your `.env` file:
```ini
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/imagen-key.json
GOOGLE_CLOUD_LOCATION=us-central1
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. Test Connection
```python
from google.cloud import aiplatform

aiplatform.init(
    project="your-project-id",
    location="us-central1"
)
print("✓ Connected to Vertex AI")
```

## Pricing
- Imagen 3: ~$0.04 per image
- 30 memories + 1 reference = 31 images = ~$1.24 per character

## Troubleshooting
- **Authentication Error**: Check `GOOGLE_APPLICATION_CREDENTIALS` path
- **Permission Denied**: Ensure service account has `aiplatform.user` role
- **API Not Enabled**: Run `gcloud services enable aiplatform.googleapis.com`
