import json
from services.extract_job import extract_job_info


if __name__ == "__main__":
    job_url = "https://www.linkedin.com/jobs/view/4198535779"
    result_job = extract_job_info(job_url)
    if result_job["status"] in ["success_raw", "success_structured"]:
        print("Job Information:")
        print(json.dumps(result_job["data"], indent=2, ensure_ascii=False))
    else:
        print(f"Error: {result_job['message']}")
        print("Raw Data:", result_job["data"])

    
    
    print(" ############# Extração de vaga concluída. ############# ")
