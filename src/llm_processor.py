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

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        )
    )
    
    return response.text

def draft_inquiry_email(job_details: dict) -> str:
    """Drafts a professional inquiry email to the PI based on extracted job details."""
    
    institution = job_details.get('institution', 'your institution')
    pi_name = job_details.get('pi_name', 'Professor')
    
    # Safely handle the experiments list if the LLM returned it differently than expected
    experiments_list = job_details.get('experiments', [])
    if isinstance(experiments_list, list):
        experiments = ", ".join(experiments_list)
    else:
        experiments = str(experiments_list)
    
    prompt = f"""
    Write a brief, highly professional academic email to {pi_name} at {institution}.
    
    Goal: Ask if the recently posted postdoctoral position is still available and if applications are still receiving full consideration.
    
    My Context: I am an experimental high-energy physicist currently working as a postdoc at Fermilab and New Mexico State University. My recent work focuses on experimental data analysis using C++, Python, and ROOT, with involvement in experiments like DUNE and SpinQuest. 
    
    Job Context: The job description mentions {experiments}. 
    
    Instructions:
    - Keep it under 150 words.
    - Do not write a full cover letter.
    - Tone must be concise, academic, and respectful.
    - Only output the email body and a suggested subject line separated by "SUBJECT_LINE: " and "BODY: ".
    """
    
    # Updated to use the modern google-genai client syntax
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    return response.text

if __name__ == "__main__":
    if "GEMINI_API_KEY" in os.environ:
        print("API Key found. Loading test jobs from INSPIRE-HEP...\n")
    else:
        print("Warning: GEMINI_API_KEY environment variable not set.")
        print("Please ensure you have run: export GEMINI_API_KEY='your_api_key_here'\n")

    test_job_posting = """
    Postdoctoral Research Associate -- CMS Experiment
    Northeastern University is seeking a postdoctoral researcher to work on the CMS experiment. 
    The successful candidate will work closely with Prof. Louise Skinnari. 
    Interested applicants should send their materials to l.skinnari@northeastern.edu. 
    The deadline for applications is April 15, 2026.
    """

    print("Stage 2: Analyzing Job...")
    print("-" * 40)
    
    try:
        # Run the extraction
        extraction_result = extract_job_details(test_job_posting)
        
        # Parse the JSON string into a Python dictionary
        parsed_job_details = json.loads(extraction_result)
        print("LLM Extraction Successful! Here is the structured data:\n")
        print(json.dumps(parsed_job_details, indent=4))
        
        print("\n" + "=" * 40 + "\n")
        
        print("Stage 3: Drafting Inquiry Email...")
        print("-" * 40)
        
        # Pass the parsed dictionary into the email drafting function
        email_draft = draft_inquiry_email(parsed_job_details)
        print(email_draft)
        
    except Exception as e:
        print(f"An error occurred during processing: {e}")
