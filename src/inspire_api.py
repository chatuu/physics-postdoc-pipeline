import requests
import json
import os

def fetch_physics_jobs():
    # INSPIRE-HEP Jobs API endpoint
    url = "https://inspirehep.net/api/jobs"
    
    # Query parameters: targeting experimental particle/nuclear physics
    params = {
        "q": "experimental AND (particle OR nuclear)",
        "rank": "POSTDOC", 
        "size": 5, # Just fetch 5 for testing
        "sort": "mostrecent"
    }
    
    print("Fetching jobs from INSPIRE-HEP...")
    response = requests.get(url, params=params)
    response.raise_for_status() # This will throw an error if the API is down
    
    jobs_data = response.json()
    extracted_jobs = []
    
    for job in jobs_data.get('hits', {}).get('hits', []):
        metadata = job.get('metadata', {})
        description = metadata.get('description', 'No description provided.')
        
        extracted_jobs.append({
            "id": job.get('id'),
            "title": metadata.get('position', 'Unknown Position'),
            "description": description
        })
        
    return extracted_jobs

# --- TEST BLOCK ---
# This code only runs if you execute THIS specific file directly.
if __name__ == "__main__":
    try:
        # 1. Run the function
        jobs = fetch_physics_jobs()
        
        # 2. Print a quick summary to the terminal
        print(f"Successfully fetched {len(jobs)} jobs!\n")
        for job in jobs:
            print(f"- {job['title']} (ID: {job['id']})")
            
        # 3. Save the full output to your resources folder to inspect the raw descriptions
        # We use a relative path assuming you are running this from the root of your repo
        output_path = os.path.join("res", "test_jobs_output.json")
        
        # Ensure the res directory exists just in case
        os.makedirs("res", exist_ok=True)
        
        with open(output_path, "w") as f:
            json.dump(jobs, f, indent=4)
            
        print(f"\nFull job descriptions saved to: {output_path}")

    except Exception as e:
        print(f"An error occurred during testing: {e}")
