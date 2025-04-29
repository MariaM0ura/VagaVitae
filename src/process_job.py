import json
from .services.Job.extract_job import extract_job_info

"""
This script extracts job information from a LinkedIn job posting using the provided URL.
"""

def job_info(job_url):
    
    job_info = extract_job_info(job_url)
    if job_info["status"] in ["success_raw", "success_structured"]:
        print(" ############# Extração de vaga concluída. ############# ")

    else:
        print(f"Error: {job_info['message']}")
        print("Raw Data:", job_info["data"])

    
    return job_info


