# Quick Start Guide

Get your Databricks Job Monitor running in 5 minutes!

## Step 1: Install Dependencies (1 min)

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Credentials (2 min)

1. **Copy the template:**
   ```bash
   cp env.example .env
   ```

2. **Edit `.env` file and add your credentials:**
   - **DATABRICKS_HOST**: Your workspace URL (copy from browser when logged in)
   - **DATABRICKS_TOKEN**: Generate from Databricks UI → User Settings → Access Tokens

   Example:
   ```
   DATABRICKS_HOST=https://adb-1234567890123456.7.azuredatabricks.net
   DATABRICKS_TOKEN=dapi1234567890abcdef1234567890ab
   ```

## Step 3: Find Your Job IDs (1 min)

**Option A - From UI:**
- Go to Databricks → Workflows → Jobs
- Click a job → Check URL: `jobs/123456789` ← that number is the Job ID

**Option B - Using Script:**
```bash
python list_jobs.py
```

## Step 4: Configure Jobs to Monitor (1 min)

Edit `config.yaml` and replace the example job IDs:

```yaml
jobs:
  - job_id: 123456789        # Replace with your actual Job ID
    display_name: "My Job"   # Give it a friendly name
```

## Step 5: Run the App! (30 sec)

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

## What You'll See

- 📊 Job cards showing status of each configured job
- ✅/❌/🔵 Status indicators (success/failed/running)
- ▶️ Trigger buttons to start jobs
- ⏹️ Cancel buttons to stop running jobs
- 📈 Last 10 runs with timestamps and durations

## Common Issues

**"Missing credentials"**
→ Make sure `.env` file exists (not `env.example`)

**"Error fetching job"**
→ Double-check the Job ID in `config.yaml`

**"config.yaml not found"**
→ Ensure the file is named exactly `config.yaml`

## Next Steps

- Toggle **Auto-Refresh** in sidebar for real-time monitoring
- Adjust refresh interval (10-300 seconds)
- Add more jobs to `config.yaml` as needed

---

For detailed information, see [README.md](README.md)

