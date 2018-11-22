#checking the Platform
import os
import platform 
try :
    from termcolor import colored    
    import requests
    from bs4 import BeautifulSoup
    import urllib2
except ImportError:
    quit("Install The required Libraries stated in the README.md")

#define your chunk size
chunk_size = 200
# defines the parentDirectory 
scriptDirectory = os.path.dirname(os.path.realpath(__file__))
#downloads assignments
def Assignment(x,newpath,filename):
    print colored('\033[1m'+"Assignment!",'white')
    # print(x.text)
    current = session.get(x)
    # print(current.url)
    if(current.url!=x):
        # print('pdf')
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        os.chdir(os.path.dirname(os.path.abspath(__file__))+'/'+newpath)        
        if not os.path.exists(scriptDirectory+'/'+newpath+'/'+filename):
            download_file(current.url,filename)
        os.chdir(scriptDirectory)
    else:
        # print('page')    
        currentPage = BeautifulSoup(current.content,'html.parser')
        print ('\033[1m'+currentPage.find('h2').text)
        print ('\033[1m'+currentPage.find('div',attrs={'class':'no-overflow'}).text)
        divs = currentPage.findAll('div',attrs={'box generalbox boxaligncenter'})
        rel = divs[0]
        gref= rel.findAll('a')
        for part in gref:
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            os.chdir(os.path.dirname(os.path.abspath(__file__))+'/'+newpath)
            fileurl=part.get('href')
            name=part.text
            if not os.path.exists(scriptDirectory+'/'+newpath+'/'+name):
                download_file(fileurl,name)
            os.chdir(scriptDirectory)
            
#download slides from the main page
def Notices(x,newpath):
    print colored('\033[1m'+"Notices!",'white')
    li = x.find('li',attrs={'aria-label':'Notice Section'}).findAll('div',attrs={'class':'activityinstance'})
    for elements in li:
        if elements.find('span',attrs={'class':'accesshide '}).text == " Page":
            #  print "Page"
            current = session.get(elements.find('a').get('href'))
            currentPage = BeautifulSoup(current.content,'html.parser')
            section = currentPage.find('div',attrs={'role':'main'})
            print ('\033[1m'+section.find('h2').text)
            for content in section.findAll('p'):
               print colored('\033[1m'+content.text,'green')
            print("----------------------------------------------------------------------------")
        else:
            # print "No Page"
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            os.chdir(os.path.dirname(os.path.abspath(__file__))+'/'+newpath)
            #download to a specific directory
            fileid = elements.find('a').get('href')
            filename = elements.find('span',attrs={'class':'instancename'}).text
            if not os.path.exists(scriptDirectory+'/'+newpath+'/'+filename):
                download_file(fileid,filename)
            os.chdir(scriptDirectory)

def download_file(download_url,name):
    #downloads html instead of Files
    r = session.get(download_url, stream=True)
    with open(name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    #completed download session     
def downloadSlide(x,newpath):
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    Allcurrent = x.findAll('div',attrs={'class':'content'})
    for i in range(2,Allcurrent.__len__()):
        currentPage = Allcurrent[i].findAll('div',attrs={'class':'activityinstance'})
        for elements in currentPage:
            fileid = elements.find('a').get('href')
            filename = elements.find('span',attrs={'class':'instancename'}).text
            os.chdir(os.path.dirname(os.path.abspath(__file__))+'/'+newpath)
            #download to a specific directory
            if not os.path.exists(scriptDirectory+'/'+newpath+'/'+filename):
                download_file(fileid,filename)
            os.chdir(scriptDirectory)
def Announcement(x,newpath):
    currentPage = x.find('div',attrs={'class':'activityinstance'}).find('a').get('href')
    # moves to announcement 
    present = session.get(currentPage)
    #it is the announcement page
    pCont = BeautifulSoup(present.content,'html.parser')
    an_head = pCont.findAll('td',attrs={'class':'topic starter'})
    if len(an_head)==0:
        print colored('\033[1m'+"No Announcement Yet!",'blue')
    else:
        for e in an_head:
            current = BeautifulSoup(session.get(e.find('a').get('href')).content,'html.parser')
            print colored('\033[1m'+current.find('h3',attrs={'class','discussionname'}).text,'yellow')
            print current.find('div',attrs={'class':'posting fullpost'}).text
            print("----------------------------------------------------------------------------")
            # check for ppy in the Announements
            checkPPT=current.find('div',attrs={'class':'attachments'})
            if(checkPPT):
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                os.chdir(os.path.dirname(os.path.abspath(__file__))+'/'+newpath)
                currentPPT=checkPPT.findAll('a')[1].get('href')
                currentName = checkPPT.findAll('a')[1].text
                #download to a specific directory
                if not os.path.exists(scriptDirectory+'/'+newpath+'/'+currentName):
                    download_file(currentPPT,currentName)
            os.chdir(scriptDirectory)
                
# url to the website
Details = {'username':'XXXX@pilani.bits-pilani.ac.in',
           'password':'XXXX'}
#creating a single session 
try:
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
    CourseName = courseList.findAll('a')
    for x in range(1,len(CourseName)):
        print colored("press %s for %s" %(x,CourseName[x].text),"cyan")
    print colored("press 0 for Every Notice","cyan")
    
    print ("Give Input for the desired Course")
    c = input()
    # print(x)
    if c==0:
        for elements in courseList.findAll('a'):
        #print(courseList.findAll('a')[1].text)
            print colored('\033[1m'+elements.text,'red')
            # print(elements.get('href'))
            current = session.get(elements.get('href'))
            currentText = BeautifulSoup(current.content,'html.parser')
            # print(currentText.findAll('li',attrs={'aria-label':'Assignment'}))          
            if(currentText.findAll('li',attrs={'aria-label':'Assignment'})):
                AsignList=currentText.findAll('li',attrs={'aria-label':'Assignment'})
                Asigndiv = AsignList[0].findAll('div',attrs={'class':'activityinstance'})
                for x in Asigndiv:
                    # print(x.find('a').get('href'))
                    if(x.find('a').get('href')):
                        Assignment(x.find('a').get('href'),elements.text,x.find('a').text)
            Announcement(currentText,elements.text)
            Notices(currentText,elements.text)
            downloadSlide(currentText,elements.text)
    else:
        print colored('\033[1m'+CourseName[c].text,'red')
        current = session.get(CourseName[c].get('href'))
        currentText = BeautifulSoup(current.content,'html.parser')
            # print(currentText.findAll('li',attrs={'aria-label':'Assignment'}))          
        if(currentText.findAll('li',attrs={'aria-label':'Assignment'})):
            AsignList=currentText.findAll('li',attrs={'aria-label':'Assignment'})
            Asigndiv = AsignList[0].findAll('div',attrs={'class':'activityinstance'})
            for x in Asigndiv:
                # print(x.find('a').get('href'))
                if(x.find('a').get('href')):
                    Assignment(x.find('a').get('href'),CourseName[c].text,x.find('a').text)
        Announcement(currentText,CourseName[c].text)
        Notices(currentText,CourseName[c].text)
        downloadSlide(currentText,CourseName[c].text)
#catch all the exceptions 
except KeyboardInterrupt:
    quit("Damn That was an abrupt close")
except requests.exceptions.ConnectionError:
    quit("You know how internet is here right :(")
except IOError:
    quit("The Force is not with you right now")
