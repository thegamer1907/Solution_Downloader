import requests
from bs4 import BeautifulSoup
import os


def html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    return soup


notdone = []
fincnt = 0
location = ''
def text(url,problem):
    trycnt = 0
    while True:
        try:
            soup = html(url)
            table = soup.find_all('table',class_='dataTable')
            td = table[0].tbody.tr.find_all('td')
            lang = td[len(td)-2].renderContents().strip()
            li = td[len(td)-1].ul.li
            href = li.a['href']
            temp = ''
            for i in range(len(href)-1,0,-1):
                if href[i] != '/':
                    temp+=href[i]
                else:
                    break
            temp = temp[::-1]
            url2 = 'https://www.codechef.com/viewplaintext/' + temp
            soup2 = html(url2)
            fin = soup2.pre.text
            ret = [fin,problem,lang]
            fwrite(ret)
            print('done with ' + problem)
            global fincnt
            fincnt+=1
            break
        except:
            if trycnt == 4:
                print('not done with ' + problem)
                notdone.append(problem)
                break
            else:
                print('trying again for ' + problem)
                trycnt+=1

def links(url):
    soup = html(url)
    article = soup.find_all('article')
    article = article[0]
    para = article.find_all('p')
    for i in range(0,len(para)):
        a1 = para[i].find_all('a')
        for a in a1:
            print('started ' + a.text)
            text("https://www.codechef.com" + a['href'],a.text)

def fwrite(fin):
    ext = ''
    if fin[2] == 'PYTH' or fin[2] == 'PYTH 3.5':
        ext = '.py'
    elif fin[2] == 'C':
        ext = '.c'
    else:
        ext = '.cpp'
    filename = location + '\\' + fin[1] + ext
    f = open(filename,"w")
    f.write(fin[0])
    f.close()
#location = 'E:\TEST'
#text('https://www.codechef.com/LTIME51/status/MATPAN,mukesh_10',"MATPAN")
#links('https://www.codechef.com/users/mukesh_10')


while True:
    try:
        profile = input('Enter the link to codechef profile url : ')
        so = html(profile)
        break
    except:
        print('Invalid Link.Please try again.')
    
while True:
    location = input('Enter the folder location for download : ')
    if os.path.isdir(location):
        break
    else:
        print('Invalid Path. Please try again')

links(profile)
print(str(fincnt) + ' solutions were downloaded succesfully')
if len(notdone) > 0:
    print('All Solutions were Downloaded succefully except')
    for h in notdone:
        print(h)

