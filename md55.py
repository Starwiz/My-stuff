#!/usr/bin/python
import hashlib, sys

if len(sys.argv) != 3:
    print 'Usage: ', sys.argv[0], ' WORDLIST_FILE MD5_TO_CRACK'
    sys.exit()


if len(sys.argv[2]) != 32:
    print 'Hash isn\'t an MD5'
    sys.exit

l = []
wl = open(sys.argv[1])
words = wl.readlines()
wl.close()

md5tc = sys.argv[2]

print str(len(words)) + ' words in your wordlist.'
for item in words:
    if hashlib.md5(item.rstrip()).hexdigest() == md5tc:
        print item, ' is the decrypted MD5!'
        sys.exit()

print 'Sorry, looks like your hash wasn\'t in the wordlist.. \nTry getting a larger wordlist?'
