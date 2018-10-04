import requests
from bs4 import BeautifulSoup
import urllib2

def Announcement(x):
    currentPage = x.find('div',attrs={'class':'activityinstance'}).find('a').get('href')
    # moves to announcement 
    present = session.get(currentPage)
    #it is the announcement page


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

#or elements in courseList.findAll('a'):
current = session.get(courseList.find('a').get('href'))
currentText = BeautifulSoup(current.content,'html.parser')
Announcement(currentText)
