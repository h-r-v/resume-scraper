import requests as r
from lxml import html
import os
from bs4 import BeautifulSoup
import weasyprint
from math import ceil

class jobspiderResumeUtill():

    def __init__(self, number_of_cvs, job_title, counter=1, opname=''):
        self.start_counter = counter
        self.counter = counter
        self.number_of_cvs = number_of_cvs
        self.job_title = job_title
        self.opname=opname
        self.base_url = 'https://www.jobspider.com'

    def fetch(self):
        url = f'''https://www.jobspider.com/job/resume-search-results.asp/words_{self.job_title.replace(" ", "+")}/searchtype_3/page_'''

        if self.number_of_cvs<=0:
            return 1

        page = r.get(url+'1')
        tree = html.fromstring(page.content)

        if os.path.exists(self.job_title):
            print(f"Saving to {self.job_title} dir\n")
        else:
            os.mkdir(self.job_title)
            print(f"Saving to {self.job_title} dir\n")

        try:
            number_of_pages = tree.xpath("/html/body/form/table[2]/tr/td[2]/table/tr[2]/td/table[2]/tr/td/center/table/tr/td/table/tr/td[1]/font/b[1]/font/text()")[0]
        except:
            print("ERROR")
            return 0

        if not number_of_pages:
            print("ERROR")
            return 0

        number_of_pages = number_of_pages.replace(',','')
        number_of_pages = int(number_of_pages)
        number_of_pages = ceil(number_of_pages/50)
        number_of_pages = max(number_of_pages,1)

        for i in range(1,number_of_pages+1):
            self.scrape(url + f"{i}")

        return self.counter 

    def scrape(self, url):
        page = r.get(url)
        tree = html.fromstring(page.content)

        links = tree.xpath("/html/body/form/table[2]/tr/td[2]/table/tr[2]/td/table[2]/tr/td/center/table/tr/td/center/font/table/tr/td[6]/a/@href")

        for link in links:
            if self.counter-self.start_counter>=self.number_of_cvs:
                return

            self.download(self.base_url+link)

    def download(self, link):
        print(self.counter, link)

        page = r.get(link)
        soup = BeautifulSoup(page.text, 'html.parser') 

        soup.find('body').contents = soup.find('table', {'id':'Table3'}).parent.parent.parent

        with open("f.html", 'w') as f:
           f.write(str(soup.contents[4]))

        with open("f.html", 'rb') as f:
            pdf = weasyprint.HTML(f).write_pdf()

        file_ = os.path.join(self.job_title, f"{self.opname}{self.counter}.pdf")

        with open(file_, 'wb') as f:
            f.write(pdf)

        self.counter+=1

        

if __name__=="__main__":
    x=jobspiderResumeUtill(0, "web developer", counter=40)
    print(x.fetch())