from linkedin import get_jobs
import time
def main():



    # Get user input or use default values
    keywords = "Software Engineer"
    #job type “F”, “C”, “P”, “T”, “I”, “V”, “O” (full-time, contract, part-time, temporary, internship, volunteer and “other”, respectively)
    job_type = "I"
    #experience “1”, “2”, “3”, “4”, “5” and “6” (internship, entry level, associate, mid-senior level, director and executive, respectively)
    experience = "1"
    #number of job listings to return, must be an integer
    limit = 1

    
    jobs = get_jobs(keywords, job_type, experience, limit)
    
    if jobs:
        print("\nJob Listings:")
        for job in jobs:
            print(f"\nJob Title: {job['title']}")
            print(f"Description: {job['description']}")
            print(f"Posted: {job['posting_time']}")
            print(f"Link: {job['link']}")
    else:
        print("No jobs found with the provided search criteria.")

if __name__ == "__main__":
    main()
