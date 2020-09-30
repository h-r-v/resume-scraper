import requests as r
from lxml import html
import os
from bs4 import BeautifulSoup
import weasyprint
from math import ceil

# bug when the job title is lawyer
class livecareerResumeUtill():

    def __init__(self, number_of_cvs, job_title, counter=1, opname=''):
        self.counter = counter
        self.number_of_cvs = number_of_cvs + self.counter - 1
        self.job_title = job_title
        self.base_url = "https://www.livecareer.com"
        self.opname=opname

    def fetch(self):
        url = self.base_url + "/resume-search/search?jt=" + self.job_title.replace(" ", "%20")

        page = r.get(url)
        tree = html.fromstring(page.content)

        if os.path.exists(self.job_title):
            print(f"Saving to {self.job_title} dir\n")
        else:
            os.mkdir(self.job_title)
            print(f"Saving to {self.job_title} dir\n")
        
        try:
            number_of_pages = tree.xpath("/html/body/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[1]/ul/li[1]/h4/text()")[0]
        except:
            print("ERROR")
            return 0

        if not number_of_pages:
            print("ERROR")
            return 0

        number_of_pages = number_of_pages.split()[0]
        number_of_pages = int(number_of_pages)
        number_of_pages = ceil(number_of_pages/10)
        number_of_pages = max(number_of_pages,1)

        for i in range(1,number_of_pages+1):
            self.scrape(url + f"&pg={i}")

        return self.counter 

    def scrape(self, url):

        page = r.get(url)
        tree = html.fromstring(page.content)

        links = tree.xpath("/html/body/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/ul/li/a/@href")

        for link in links:
            if self.counter>self.number_of_cvs:
                return

            self.download(self.base_url+link)

    def download(self, link):
        print(self.counter, link)

        page = r.get(link)
        soup = BeautifulSoup(page.text, 'html.parser') 

        soup.find('body').contents = soup.find('div', {'id':'divResumeHTML'}).contents

        with open("f.html", 'w') as f:
            f.write(str(soup.contents[1]))

        with open("f.html", 'rb') as f:
            pdf = weasyprint.HTML(f).write_pdf()

        file_ = os.path.join(self.job_title, f"{self.opname}{self.counter}.pdf")

        with open(file_, 'wb') as f:
            f.write(pdf)

        self.counter+=1

        

if __name__=="__main__":
    x=livecareerResumeUtill(50, "potty", opname="lawyer")
    print(x.fetch())