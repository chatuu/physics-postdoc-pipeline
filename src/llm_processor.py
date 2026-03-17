import os
import json
from google import genai
from google.genai import types

# The client automatically detects the GEMINI_API_KEY environment variable.
client = genai.Client()

def extract_job_details(job_description: str) -> str:
    """Extracts structured data from a physics postdoc job description."""
    
    prompt = f"""
    Extract the following information from the physics postdoc job description:
    - institution: The university or lab offering the position.
    - pi_name: The Principal Investigator or main contact person.
    - email: The contact email address.
    - experiments: A list of specific physics experiments mentioned (e.g., CMS, ATLAS, ALICE).
    - deadline: The application deadline.

    Respond ONLY with a valid JSON object matching these keys.

    Job Description:
    {job_description}
    """

    # We use gemini-2.5-flash as it is the fastest and most cost-effective for extraction tasks
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            # This strictly enforces that the output is formatted as JSON
            response_mime_type="application/json",
        )
    )
    
    return response.text

if __name__ == "__main__":
    # Check for API key to mirror your previous script's startup checks
    if "GEMINI_API_KEY" in os.environ:
        print("API Key found. Loading test jobs from INSPIRE-HEP...\n")
    else:
        print("Warning: GEMINI_API_KEY environment variable not set.")
        print("Please ensure you have run: export GEMINI_API_KEY='your_api_key_here'\n")

    # Mocking the job posting based on your previous console output
    test_job_posting = """
    Postdoctoral Research Associate -- CMS Experiment
    Northeastern University is seeking a postdoctoral researcher to work on the CMS experiment. 
    The successful candidate will work closely with Prof. Louise Skinnari. 
    Interested applicants should send their materials to l.skinnari@northeastern.edu. 
    The deadline for applications is April 15, 2026.
    """

    print("Analyzing Job: Postdoctoral Research Associate -- CMS Experiment...")
    print("-" * 40)
    
    try:
        # Run the extraction
        result = extract_job_details(test_job_posting)
        
        # Parse the JSON string into a Python dictionary to ensure it is valid, 
        # then print it with nice indentation
        parsed_json = json.loads(result)
        print("LLM Extraction Successful! Here is the structured data:\n")
        print(json.dumps(parsed_json, indent=4))
        
    except Exception as e:
        print(f"An error occurred during extraction: {e}")
