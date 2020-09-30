import requests
from lxml import html
import os
import PyPDF2
    
number_of_cvs = 5
job_title = "web developer"
n = 10

#counting number of files successfully downloaded
counter = 1

#output file name
opname=""

#url and query for the first page of google search
query = "(filetype:pdf AND (intitle:\"resume\" OR intitle:\"cv\" OR intitle:\"Curripythculum Vitae\") -template -writing) AND intitle:" + job_title
url = "https://google.com/search?q="+query

#setting header
headers= {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"}

#fetching first result page
page = requests.get( url, headers=headers)

#converting the response to tree structure to use xpaths
tree = html.fromstring(page.content)

#debugging statement
print('\n',url, end='\n\n')

#making sure there is a directory for the data to be saved in
if os.path.exists(job_title):
    print(f"Saving to {job_title} dir\n")
else:
    os.mkdir(job_title)
    print(f"Saving to {job_title} dir\n")

for page_number in range(n):

    #every page has 10 links at maximum
    for i in range(1,11):
        
        google_page_number = i

        link = tree.xpath(f'/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[{google_page_number}]/div/div[1]/a/@href')
        
        #checking if there is a link
        if len(link)==0:
            print("No more results found!\n")
            break

        link = link[0]

        #making sure the link is to a .pdf document
        if(link[-4::]=='.pdf'):
            op_file = os.path.join( job_title, f"{opname}{counter}.pdf")
            try:
                #downloading and saving the pdf
                pdf = requests.get(link, timeout=5)
                print(counter, link)
                with open(op_file, "wb") as f:
                   f.write(pdf.content)
                counter+=1
            except:
                print("Some problem with: ", link)
                continue

            try:
                PyPDF2.PdfFileReader(open(op_file, "rb"))
                
                if counter>=number_of_cvs+1:
                    break
            except:
                print("Some problem with: ", link)
                os.remove(op_file)
                counter-=1
                print("deleted", op_file)

    if counter>=number_of_cvs+1:
        break

    #storing link of next page
    p = page_number+3
    next_page = tree.xpath(f'/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[5]/div[2]/span[1]/div/table/tr/td[{p}]/a/@href')

    #making sure there is next link
    if len(next_page)==0:
        print("No more results found!\n")
        break

    url = "https://google.com/"+next_page[0]    
    
    #going to the next page
    print('\n',url, end='\n\n')
    page = requests.get( url, headers=headers)
    tree = html.fromstring(page.content)