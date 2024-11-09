# linkedin.py
import os
import re
import time
from linkedin_api import Linkedin
from dotenv import load_dotenv

load_dotenv()

def get_jobs(keywords="Software Engineer", job_type="I", experience="1", limit=3):
    api = Linkedin(os.getenv("LINKEDIN_EMAIL"), os.getenv("LINKEDIN_PASSWORD"))
    
    joblist = api.search_jobs(
        keywords=keywords,
        job_type=[job_type],
        experience=[experience],
        limit=limit,
    )

    jobs = []
    for job in joblist:
        job_id_regex = re.findall(r"jobPosting:(\d+)", job["trackingUrn"])
        job_id = job_id_regex[0]
        job_data = api.get_job(job_id)
        
        job_info = {
            "title": job["title"],
            "description": job_data["description"]["text"].replace("\n", "<br>"),
            "link": f'https://www.linkedin.com/jobs/view/{job_id}',
            "posting_time": time.strftime(
                "%a, %d %b %Y %H:%M:%S +0000", 
                time.localtime(job_data["listedAt"] / 1000)
            ),
        }
        jobs.append(job_info)
    return jobs
