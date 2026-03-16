import requests
import json
import os
import re  # Added for Regular Expression text scanning

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
    
    # This is the pattern that matches standard email formats
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    for job in jobs_data.get('hits', {}).get('hits', []):
        metadata = job.get('metadata', {})
        description = metadata.get('description', 'No description provided.')
        
        # 1. Try to get emails from the structured API contact details
        contacts = metadata.get('contact_details', [])
        api_emails = [contact.get('email') for contact in contacts if contact.get('email')]
        
        # 2. Scan the raw description text for any email addresses
        description_emails = re.findall(email_pattern, description)
        
        # 3. Combine both lists and use set() to remove any duplicates
        all_emails = list(set(api_emails + description_emails))
        
        # 4. Format them into a neat comma-separated string
        contact_emails = ", ".join(all_emails) if all_emails else "No email found"
        
        extracted_jobs.append({
            "id": job.get('id'),
            "title": metadata.get('position', 'Unknown Position'),
            "description": description,
            "deadline": metadata.get('deadline_date', 'No deadline provided'),
            "contact_email": contact_emails
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
            print(f"  Deadline: {job['deadline']}")
            print(f"  Contact(s): {job['contact_email']}\n")
            
        # 3. Save the full output to your resources folder
        output_path = os.path.join("res", "test_jobs_output.json")
        os.makedirs("res", exist_ok=True)
        
        with open(output_path, "w") as f:
            json.dump(jobs, f, indent=4)
            
        print(f"Full job descriptions saved to: {output_path}")

    except Exception as e:
        print(f"An error occurred during testing: {e}")
