"""
Helper script to list all available jobs in your Databricks workspace.
Use this to find job IDs to add to config.yaml
"""

from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv
import os

def main():
    # Load environment variables from env.example
    load_dotenv('env.example')
    
    host = os.getenv('DATABRICKS_HOST')
    token = os.getenv('DATABRICKS_TOKEN')
    
    if not host or not token:
        print("❌ Error: DATABRICKS_HOST and DATABRICKS_TOKEN must be set in .env file")
        print("\n💡 Steps:")
        print("1. Copy env.example to .env")
        print("2. Fill in your Databricks credentials")
        print("3. Run this script again")
        return
    
    try:
        # Initialize client
        print("🔄 Connecting to Databricks...")
        client = WorkspaceClient(host=host, token=token)
        
        # List all jobs
        print(f"✅ Connected to {host}\n")
        print("=" * 100)
        print(f"{'Job ID':<15} | {'Job Name':<60} | {'Creator':<20}")
        print("=" * 100)
        
        job_count = 0
        for job in client.jobs.list():
            job_id = job.job_id
            job_name = job.settings.name
            creator = job.creator_user_name if job.creator_user_name else "Unknown"
            
            print(f"{job_id:<15} | {job_name:<60} | {creator:<20}")
            job_count += 1
        
        print("=" * 100)
        print(f"\n📊 Total jobs found: {job_count}")
        
        if job_count > 0:
            print("\n💡 To monitor a job, add its ID to config.yaml:")
            print("""
jobs:
  - job_id: YOUR_JOB_ID_HERE
    display_name: "Your Job Name"
            """)
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n💡 Troubleshooting:")
        print("- Verify your DATABRICKS_HOST is correct (should start with https://)")
        print("- Check your DATABRICKS_TOKEN is valid and hasn't expired")
        print("- Ensure you have permission to list jobs in the workspace")


if __name__ == "__main__":
    main()

