from resumescraper.googleData.scraperr import googleResumeUtill
from resumescraper.livecareerData.scraper import livecareerResumeUtill
from resumescraper.jobspiderData.scraper import jobspiderResumeUtill
from resumecluster.number_of_pdfs import number_of_pdfs

total_n = 100
job_title = "banking"

left_n = total_n
counter = 0

ld = livecareerResumeUtill( total_n, job_title, counter=1)
counter = ld.fetch()

left_n = total_n - (counter-1)

js = jobspiderResumeUtill( left_n, job_title, counter=counter)
counter = js.fetch()

print(counter)

data = number_of_pdfs(os.path.join(os.getcwd(),job_title))
x,y = data[1]

print(f"{data[0]} types of CVs found.")
for i in x:
    print(f"    type {i} : {y[i]} CVs")
