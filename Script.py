from termcolor import colored
import requests
from bs4 import BeautifulSoup
import urllib2

def Announcement(x):
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
    Announcement(currentText)