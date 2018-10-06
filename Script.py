import os
from termcolor import colored
import requests
from bs4 import BeautifulSoup
import urllib2
# defines the parentDirectory 
scriptDirectory = os.path.dirname(os.path.realpath(__file__))

def download_file(download_url,name):
    response = urllib2.urlopen(download_url)
    file = open(name, 'w')
    file.write(response.read())
    file.close()
    # print("Completed")

def Announcement(x,newpath):
    currentPage = x.find('div',attrs={'class':'activityinstance'}).find('a').get('href')
    # moves to announcement 
    present = session.get(currentPage)
    #it is the announcement page
    pCont = BeautifulSoup(present.content,'html.parser')
    an_head = pCont.findAll('td',attrs={'class':'topic starter'})
    if len(an_head)==0:
        print colored('\033[1m'+"No Announcements Yet!",'blue')
    else:
        for e in an_head:
            current = BeautifulSoup(session.get(e.find('a').get('href')).content,'html.parser')
            print colored('\033[1m'+current.find('h3',attrs={'class','discussionname'}).text,'yellow')
            print(current.find('div',attrs={'class':'posting fullpost'}).text)
            print("----------------------------------------------------------------------------")
            checkPPT=current.find('div',attrs={'class':'attachments'})
            if(checkPPT):
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                os.chdir(os.path.dirname(os.path.abspath(__file__))+'/'+newpath)
                currentPPT=checkPPT.findAll('a')[1].get('href')
                currentName = checkPPT.findAll('a')[1].text
                #download to a specific directory
                download_file(currentPPT,currentName)
            os.chdir(scriptDirectory)    
# url to the website
Details = {'username':'f2016070@pilani.bits-pilani.ac.in',
           'password':'bansalfamily007'}
#creating a single session 
 
session  = requests.session()

#url to the Nalanda 
url = "http://nalanda.bits-pilani.ac.in/"

# current page
c_page = urllib2.urlopen(url)

# storing the scraped page
innerHTML = BeautifulSoup(c_page,'html.parser')

# login button 
login = (innerHTML.find('span', attrs={'class':'login'})).find('a').get('href')

# login Page
loginPage = urllib2.urlopen(login)

req = session.post(login,data=Details)

# current url is => req.url

innerHTML = BeautifulSoup(req.content,'html.parser')
courseList = innerHTML.find('ul',attrs={'class':'unlist'})
for elements in courseList.findAll('a'):
#print(courseList.findAll('a')[1].text)
    print colored('\033[1m'+elements.text,'red')
    current = session.get(elements.get('href'))
    currentText = BeautifulSoup(current.content,'html.parser')
    Announcement(currentText,elements.text)