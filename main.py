import requests
from bs4 import BeautifulSoup 
import re
import subprocess
import os
import shutil

#wget command for HTML data

allJobsPath = '/Users/dehaortasari/Documents/projectLaMancha/LaMancha/allJobs'
outputTextPath = '/Users/dehaortasari/Documents/projectLaMancha/LaMancha/output.txt'
filteredJobsPath = '/Users/dehaortasari/Documents/projectLaMancha/LaMancha/filteredJobs'


bash_commandList = ['wget','--directory-prefix', allJobsPath,'-E', '-i', outputTextPath]
pages = []
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
keywords = ["Python"]

urlTemplate = "https://www.rwth-aachen.de/cms/root/Die-RWTH/Arbeiten-an-der-RWTH/~buym/RWTH-Jobportal/lidx/1/?aaaaaaaaaaaaanr=Studentische+Hilfskraft&page="
page_Count = 1
number = 1
url_one = urlTemplate + str(page_Count)
page = requests.get(url_one ,headers = headers)

#10 für irgendwelche Zahl, es wird sowieso nicht mehr als Zehn, kann man später aufhören auf die Zahl, 
# die keine neue Datei erzeugt. (zu faul das zu implementieren [will ich auch nicht])

while(page_Count != 10):
    pages.append(page)
    page_Count += 1
    url_one = urlTemplate + str(page_Count)
    page = requests.get(url_one ,headers = headers)

data = []


for page in pages:

    soup = BeautifulSoup(page.content, "html.parser")
    products = soup.find_all("div", class_= "location")


    re_links = r'<a href="/go/id/kbag/file/(.*?)/" target="_self">'
    prefixLink = 'www.rwth-aachen.de/go/id/kbag/file/'


    for product in products:
        product_html = str(product)
        re_codes= re.findall(re_links, product_html)
        for item in re_codes:
            item = prefixLink + item
            data.append(item)


with open(outputTextPath, "w", encoding ="utf-8") as f:
    for re_codes in data:
        f.write(f"{re_codes}\n")


#pull HTML data from links with wget
subprocess.run(bash_commandList,stdout=subprocess.PIPE)

job_as_string = ""

#search for keyword in html as string to detect if the jobstelle has something I can do
with os.scandir(allJobsPath) as parent:
    for job_stelle in parent:
        with open(job_stelle, 'r') as f:
            if job_stelle.name.endswith(".html") and job_stelle.is_file():
                print(job_stelle.name)
                job_as_string = f.read()
        f.close()
        for keyword in keywords:
            if(keyword in job_as_string):
                command = allJobsPath + '/' + job_stelle.name
                shutil.copy(command, filteredJobsPath)
                continue



