import requests
from lxml import html
import os
import PyPDF2
    
class googleResumeUtill:
    def __init__(self, number_of_cvs, job_title, counter=1, opname=''):
        '''
        number_of_cvs: Maximum number of CVs to be fetched.
        job_title: job title used for google search for fetching the CVs.
        opname: out put file names. Files saved as "<job_title>/<opname><counter>.pdf"
        counter: set the value of counter so that you don't overwrite previously downloaded files
        n: maximum number of google pages needed to be scraped
        '''
        self.start_count = counter
        self.counter = counter
        self.number_of_cvs = number_of_cvs
        self.job_title = job_title
        self.n = 100
        self.opname = opname
        self.headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"}



    def fetch(self):
        """
        init the class then call this funtion to start scraping
        """
        self.query = "(filetype:pdf AND (intitle:\"resume\" OR intitle:\"cv\" OR intitle:\"Curripythculum Vitae\") -template -writing) AND intitle:" + self.job_title
        self.url = "https://google.com/search?q=" + self.query

        self.page = requests.get( self.url, headers=self.headers)

        self.tree = html.fromstring(self.page.content)

        if self.number_of_cvs <= 0:
            return 0

        #print('\n',self.url, end='\n\n')

        #making sure there is a directory for the data to be saved in
        if os.path.exists(self.job_title):
            print(f"Saving to {self.job_title} dir\n")
        else:
            os.mkdir(self.job_title)
            print(f"Saving to {self.job_title} dir\n")

        for page_number in range(self.n):
            for i in range(1,11):
                self.counter = self.scrape(i)
                if self.counter>=self.number_of_cvs+self.start_count+1:
                    return self.counter

            self.p = page_number+3
            self.next_page = self.tree.xpath(f'/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[5]/div[2]/span[1]/div/table/tr/td[{self.p}]/a/@href')

            if len(self.next_page)==0:
                #print("No more results found!\n")
                return self.counter

            self.url = "https://google.com/"+self.next_page[0]    
            
            print('\n',page_number, self.url, end='\n\n')
            self.page = requests.get( self.url, headers=self.headers)
            self.tree = html.fromstring(self.page.content)



    def scrape(self, item_no):
        """
        """
        self.link = self.tree.xpath(f'/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[{item_no}]/div/div[1]/a/@href')
        
        if len(self.link)==0:
            #print("No more results found!\n")
            return self.counter

        self.link = self.link[0]

        self.counter = self.downloadPDF(self.link)
        return self.counter



    def downloadPDF(self, link):
        """
        """
        self.link = link
        if(self.link[-4::]=='.pdf'):
            self.op_file = os.path.join( self.job_title, f"{self.opname}{self.counter}.pdf")
            try:
                self.pdf = requests.get(self.link, timeout=5)
                print(self.counter, self.link)

                with open(self.op_file, "wb") as f:
                   f.write(self.pdf.content)

                self.counter+=1
            except:
                #print("Some problem with: ", self.link)
                return self.counter

            try:
                PyPDF2.PdfFileReader(open(self.op_file, "rb"))
                
                if self.counter>=self.number_of_cvs+1:
                    return self.counter
            except:
                #print("Some problem with: ", self.link)
                os.remove(self.op_file)
                self.counter-=1
                print("deleted", self.op_file)
        return self.counter

        
        
if __name__=="__main__":
    x = googleResumeUtill(10, "hr analyst", counter=24)
    print(x.fetch())