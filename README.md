# Databricks Job Monitor 🔄

A Streamlit web application for monitoring, triggering, and managing Databricks jobs. This app provides stakeholders with real-time visibility into specific jobs, their run history, and the ability to trigger or cancel job runs.

## Features

- 📊 **Monitor Multiple Jobs**: Track status of specific Databricks jobs
- 📈 **Run History**: View last 10 runs with timestamps and status
- ▶️ **Trigger Jobs**: Start job runs on-demand
- ⏹️ **Cancel Runs**: Stop currently running jobs
- 🔄 **Auto-Refresh**: Automatic status updates with configurable intervals
- 🎨 **Color-Coded Status**: Easy-to-read status indicators

## Prerequisites

- Python 3.8 or higher
- Access to a Databricks workspace
- Databricks Personal Access Token

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your Databricks Credentials

#### A. Databricks Workspace URL
1. Log into your Databricks workspace in a web browser
2. Copy the URL from the browser address bar
3. It will look like: `https://adb-1234567890123456.7.azuredatabricks.net` (Azure) or `https://dbc-xxxxxxxx-xxxx.cloud.databricks.com` (AWS)

#### B. Personal Access Token
1. In Databricks UI, click on your username in the top-right corner
2. Select **User Settings**
3. Go to **Access Tokens** tab
4. Click **Generate New Token**
5. Give it a name (e.g., "Job Monitor App") and optional expiry
6. Click **Generate**
7. **Important**: Copy the token immediately (you won't be able to see it again!)

### 3. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` file and add your credentials:
   ```
   DATABRICKS_HOST=https://your-workspace-url.cloud.databricks.com
   DATABRICKS_TOKEN=dapi1234567890abcdef1234567890ab
   ```

### 4. Find Your Job IDs

You have two options to find job IDs:

#### Option A: From Databricks UI
1. Go to Databricks UI
2. Click on **Workflows** in the left sidebar
3. Click on **Jobs**
4. Click on the job you want to monitor
5. Look at the URL in your browser - it will be like: `https://your-workspace.com/jobs/123456789`
6. The number at the end (e.g., `123456789`) is your Job ID

#### Option B: Using a Python Script
Create a file called `list_jobs.py` with this content:

```python
from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv
import os

load_dotenv()

client = WorkspaceClient(
    host=os.getenv('DATABRICKS_HOST'),
    token=os.getenv('DATABRICKS_TOKEN')
)

print("Available Jobs:")
print("-" * 80)
for job in client.jobs.list():
    print(f"Job ID: {job.job_id:12} | Name: {job.settings.name}")
```

Run it:
```bash
python list_jobs.py
```

### 5. Configure Jobs to Monitor

1. Open `config.yaml` in a text editor
2. Replace the example job IDs with your actual job IDs:

```yaml
jobs:
  - job_id: 123456789
    display_name: "Daily ETL Pipeline"
    
  - job_id: 987654321
    display_name: "Weekly Report Generation"
    
  # Add more jobs as needed
  - job_id: YOUR_JOB_ID
    display_name: "Your Job Name"
```

**Tips:**
- `job_id`: Required - the numeric ID from Databricks
- `display_name`: Optional - a friendly name to show in the app (if not provided, will use the job name from Databricks)

## Running the Application

Once configured, start the app with:

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## Using the Application

### Main Interface

- **Job Cards**: Each monitored job is displayed in an expandable card showing:
  - Job name and ID
  - Latest run status
  - Trigger and Cancel buttons
  - Last 10 runs with details

### Sidebar Controls

- **Refresh Now**: Manually refresh all job statuses
- **Auto-Refresh Toggle**: Enable/disable automatic refreshing
- **Refresh Interval**: Set how often to auto-refresh (10-300 seconds)
- **Connection Status**: Shows if Databricks credentials are configured correctly

### Actions

#### Trigger a Job Run
1. Find the job card you want to trigger
2. Click the **▶️ Trigger Run** button
3. The app will show a success message with the Run ID
4. The status will update automatically

#### Cancel a Running Job
1. Find the job card with a running job
2. Click the **⏹️ Cancel** button (only visible when a job is running)
3. The app will cancel the run and show a confirmation

### Status Indicators

- 🔵 **RUNNING**: Job is currently executing
- ✅ **SUCCESS**: Job completed successfully
- ❌ **FAILED**: Job failed
- 🚫 **CANCELED**: Job was cancelled
- ⏱️ **TIMEOUT**: Job exceeded time limit
- ⚠️ **ERROR**: Internal error occurred

## Troubleshooting

### "Missing Databricks credentials" Error
- Make sure you created a `.env` file (not `env.example`)
- Verify `DATABRICKS_HOST` and `DATABRICKS_TOKEN` are set correctly
- Check there are no extra spaces or quotes around the values

### "config.yaml not found" Error
- Ensure `config.yaml` exists in the same directory as `app.py`
- Check the file name is exactly `config.yaml` (not `config.yml`)

### "Error fetching job" Message
- Verify the job ID is correct
- Make sure your access token has permission to view the job
- Check that the job still exists in Databricks

### Connection Issues
- Verify your Databricks workspace URL is correct (should start with `https://`)
- Ensure your access token hasn't expired
- Check your network can reach the Databricks workspace

## File Structure

```
.
├── app.py              # Main Streamlit application
├── config.yaml         # Job configuration
├── .env               # Your credentials (create from env.example)
├── env.example        # Template for .env file
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Security Notes

- **Never commit your `.env` file** to version control
- Keep your access token secure
- Consider using tokens with limited scope and short expiry
- Rotate tokens regularly for security

## Support

For issues or questions:
1. Check the Databricks SDK documentation: https://docs.databricks.com/dev-tools/sdk-python.html
2. Verify your credentials and permissions
3. Check the Streamlit logs for detailed error messages

## Deployment to Streamlit Community Cloud

### Prerequisites
- GitHub account
- Your Databricks credentials (host URL and access token)

### Deployment Steps

1. **Push to GitHub**
   - Initialize git repository (if not already done): `git init`
   - Add all files: `git add .`
   - Commit: `git commit -m "Initial commit"`
   - Create a new repository on GitHub
   - Push: `git remote add origin YOUR_GITHUB_REPO_URL && git push -u origin main`

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository, branch (main/master), and `app.py` as the main file
   - Click "Advanced settings"
   - In the "Secrets" section, add your credentials in TOML format:
     ```toml
     DATABRICKS_HOST = "https://your-workspace-url.cloud.databricks.com"
     DATABRICKS_TOKEN = "dapi1234567890abcdef"
     ```
   - Click "Deploy"

3. **Access Your App**
   - Your app will be live at: `https://[your-app-name].streamlit.app`
   - Share this URL with your stakeholders

### Managing Your Deployed App
- Access the Streamlit Cloud dashboard to:
  - View logs and app health
  - Update secrets
  - Restart the app
  - Monitor usage

### Updates
When you make changes to your code:
1. Push changes to GitHub: `git add . && git commit -m "Update" && git push`
2. Streamlit Cloud will automatically redeploy your app

## License

This tool is provided as-is for monitoring Databricks jobs.

