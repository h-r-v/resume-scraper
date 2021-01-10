**# Introduction:**

This project is a tool that will help scrape resumes for a given keyword.

Sites scraped:

- Google
- Jobspider
- livecareer

**# Working overview**

This project contains two modules:

1. Resume Cluster:

This is the module which is used to classify downloaded resumes. This module classifies the resumes based on their templates using AI and generates a report for the same.

1. Resume Scraper

This module is used to scrape the above mentioned websites and download them as pdf.

**# Installation and Launching**

1. Installing python 3.8.5

    - wget https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tgz
    - tar -xvf Python-3.8.5.tgz
    - cd Python-3.8.5
    - ./configure
    - make
    - make altinstall

2. Create virtual environment

    - python3 -m venv env\_RP

3. Activate environment and install dependencies:

    - source env\_RP/bin/activate
    - pip install -r requirements.txt

4. Launching and using the tool

    - Open &#39;umbrella.py&#39; in a text editor.
    - Change the job\_title variable as per the requirement and save the file.
    - Launch the umbrella.py file.

**# Directory Structure**

- umbrealla.py: This file is used to combine the &#39;resumecluster&#39; and &#39;resumescraper&#39; modules for ease of access.
- Inside resumecluster dir:

  - number\_of\_pdfs.py: This is the file that uses a pre-trained CNN model to classify the already downloaded pdfs.

- Inside resumescraper dir:

  - googleData: This dir has a scraperr.py file that scrapes and downloads resumes as pdf.

  - jobspiderData: This dir has a scraper.py file that scrapes and downloads resumes as pdf.

  - livecareerData: This dir has a scraper.py file that scrapes and downloads resumes as pdf.

**# Demo Video**

[https://drive.google.com/file/d/164rKe4vd92H8emPFTQxo\_Rwi1nj0u9Gi/view?usp=sharing](https://drive.google.com/file/d/164rKe4vd92H8emPFTQxo_Rwi1nj0u9Gi/view?usp=sharing)
