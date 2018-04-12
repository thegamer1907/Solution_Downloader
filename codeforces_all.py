import requests
from bs4 import BeautifulSoup
import os
from collections import Counter
import csv
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
import urllib2
import pandas as pd
from pandas import DataFrame

def visualize(address,username) :
	df = pd.read_csv(address+'/'+username+'_data.csv')
	#pie chart for solved
	plt.pie(df['Solved'],labels=df['Tag'],autopct='%1.02f%%', pctdistance=1.45, labeldistance=1.6)
	plt.savefig(address+'/'+'pie.png',bbox_inches = 'tight')
	#barh
	plt.clf()
	plt.barh(df['Tag'],df['Solved'])
	plt.suptitle("Tags VS Count")
	plt.savefig(address+'/'+'barh.png',bbox_inches = 'tight')
	#compa
	plt.clf()
	plt.suptitle("Performance")
	legend = ['Recommended','Solved']
	col = ['red','green']
	plt.barh(df['Tag'],df['Rec'], color = 'r')
	plt.barh(df['Tag'],df['Solved'] ,color = 'g')
	plt.legend(legend)
	plt.savefig(address+'/'+'preformance.jpg',bbox_inches = 'tight')

all_tag = []


def html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    return soup


def fwrite(fin,location):
    ext = ''
    if fin[2] == 'Python 2' or fin[2] == 'Python 3':
        ext = '.py'
    elif fin[2] == 'GNU C':
        ext = '.c'
    else:
        ext = '.cpp'
    filename = location + '\\' + fin[1] + ext
    f = open(filename,"w")
    f.write(fin[0])
    f.close()

def add_tag(url):
    #print url
    soup = html(url)
    div = soup.find_all('div',class_='roundbox ')
    for i in range(len(div)):
        all_tag.append(div[i].span.text.strip())
        #print div[i].span.text.strip()

def download(fin,location):
    url = 'http://codeforces.com/contest/' + str(fin[1]) + '/submission/' + str(fin[0])
    soup = html(url)
    if fin[3] == 'Python 2' or fin[3] == 'Python 3' or fin[3] == 'PyPy 2':
        pre = soup.find_all('pre',class_='prettyprint lang-py program-source')
    else:
        pre = soup.find_all('pre',class_='prettyprint lang-cpp program-source')
    code =  pre[0].text
    te = [code.strip(),fin[2],fin[3].strip()]
    fwrite(te,location)
    print 'done with ' + fin[2]
    

def run():
    while True:
        location = raw_input('Enter the folder location for download : ')
        if os.path.isdir(location):
            break
        else:
            print 'Invalid Path. Please try again'
    while True:
        try:
            username = raw_input('Enter the username on codeforces : ')
            url = 'http://codeforces.com/submissions/' + username
            soup = html(url)
            break
        except:
            print 'Invalid Username.Please try again.'

    div = soup.find_all('div',class_='pagination')
    li = div[1].ul.find_all('li')
    totpage = int(li[len(li)-2].a.text)
    for i in range(1,totpage+1):
        nurl = url + '/page/' + str(i)
        soup = html(nurl)
        table = soup.find_all('table',class_='status-frame-datatable')
        tr1 = table[0].find_all('tr')
        
        for j in range(1,len(tr1)): #change after debug to len(tr1)
            try:
                td = tr1[j].find_all('td')
                if td[2].a.text != username:
                    continue
                try:
                    if td[5].span.span.text != 'Accepted':
                        continue
                except:
                    continue
                try:
                    subid = int(td[0].span.text)
                    problemlink = td[3].a['href']
                except:
                    subid = int(td[0].a.text)
                    problemlink = td[3].a['href']
                probtext = td[3].a.text.strip()
                temp = ''
                temp2 = ''
                problemlink = r'http://codeforces.com' + problemlink
                #print problemlink
                for p in probtext:
                    if p.isdigit():
                        temp+=p
                        temp2+=p
                    else:
                        temp2+=p
                        break
                probid = int(temp)
                download([subid,probid,temp2,td[4].text.strip()],location)
                add_tag(problemlink)
            except:
                print i,j
                print [subid,probid,temp2,td[4].text]



    fin  = Counter(all_tag)
    ofile = open(location + '\\' + username + '_data.csv',"wb")
    writer = csv.writer(ofile)

    orec = open('rec_tags.csv',"rb")
    reader = csv.reader(orec)

    recdic = {}

    for row in reader:
        f = row[0].split('\t')
        recdic[f[0]] = f[1]

    orec.close()

    writer.writerow(['Tag','Solved','Rec'])
    for key,value in fin.items():
        try:
            recvalue = recdic[key]
        except:
            recvalue = 50
            print key
        writer.writerow([key,value,recvalue])
    ofile.close()
    visualize(location,username)

run()