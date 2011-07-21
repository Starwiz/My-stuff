#!/usr/bin/python
import urllib, urllib2, re, sys, cookielib, time

username = 'Starwiz'
password = 'lolnotmypassword'
logincheck = 'Thank you for logging in, Starwiz.' #Set to something you'd only see if you were logged in.
logincheck2 = 'Your posts count'

#Login
cookiejar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
baseurl = urllib2.Request('http://doxsters.net/login.php')
loginparams = urllib.urlencode({'do' : 'login', 'vb_login_username' : username, 'vb_login_password' : '', 's' : '', 'securitytoken' : 'guest', 'do' : 'login', 'vb_login_md5password' : 'e78af4f5157a2691af7b363439b3f819', 'vb_login_md5password_utf' : 'e78af4f5157a2691af7b363439b3f819'})
logincon = opener.open(baseurl, loginparams)
loginsrc = logincon.read()

#Makes sure nothing failed with the cookies
if logincheck not in loginsrc:
    print "Login failed."
    sys.exit()
    
print 'Login successful! Continuing with script.'

indexsrc = opener.open('http://doxsters.net/index.php')
indexsrc = indexsrc.read()
howmanytimes = '1' #How many times should you send the message to each person
howmanyusers = '(Welcome to our newest member, <a href="member\\.php\\?u=(\\d*?)("))'
howmanyusers = re.compile(howmanyusers,re.IGNORECASE|re.DOTALL)
howmanyusers1 = re.compile('(\\d+)',re.IGNORECASE|re.DOTALL)

hmu = howmanyusers.findall(indexsrc)
hmu = hmu[0]
hmu = ''.join(hmu)
hmu = howmanyusers1.findall(hmu)
hmu = hmu[0]

print 'There are: ' + hmu + ' users on this forum!'

pmusername = '("1">(?:[a-z][a-z0-9_]*)<)'
pmusername = re.compile(pmusername,re.IGNORECASE|re.DOTALL)
pmusername1 = '(?:[a-z][a-z0-9_]*)'
pmusername1 = re.compile(pmusername1,re.IGNORECASE|re.DOTALL)

messagetitle = 'DEW IT!' #what do you want the message title to be?
messagebody = 'Check out the script this was sent with! http://doxsters.net/showthread.php?t=685' #What do you want the message body to be?
x = 1

print 'Okay..'

#Start the messaging/user enumerating
while x <= hmu:
    if logincheck2 not in indexsrc:
        print "Cookie fail."
        sys.exit()
    tocheckparams = urllib.urlencode({'do' : 'newpm', 'u' : x, 'securitytoken' : '1291329245-0548d4aeb8aa5254f24f0f5dc8bc43dfa464481e'})
    tocheck = opener.open('http://doxsters.net/private.php?', tocheckparams)
    tocheck = tocheck.read()
    pmreceive = pmusername.findall(tocheck)
    lvar = len(pmreceive)
    if lvar < 2:
        x = x + 1
        continue
    pmreceive = pmreceive[1]
    pmreceive = ''.join(pmreceive)
    pmreceive = pmusername1.findall(pmreceive)
    pmreceive = pmreceive[0]
    print 'Sending message to user id: ',  x,  ' username: ',  pmreceive
    pmparams = urllib.urlencode({'do' : 'insertpm', 'pmid' : '', 'recipients' : pmreceive, 'bccrecipients' : '', 'title' : messagetitle, 'message' : messagebody, 'wysiwyg' : '0', 'iconid' : '0', 's' : '', 'securitytoken' : '1291329245-0548d4aeb8aa5254f24f0f5dc8bc43dfa464481e', 'do' : 'insertpm', 'pmid' : '', 'forward' : '', 'sbutton' : 'submit+message', 'savecopy' : '1', 'signature' : '1', 'parseurl' : '1'})
    pmncon = opener.open('http://doxsters.net/private.php?', pmparams)
    x = x + 1
    time.sleep(60)
