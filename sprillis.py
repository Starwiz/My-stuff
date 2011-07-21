#/usr/bin/python
import re, sys, os

print 'PHP source vulnerability scanner.'
print 'Coded by Starwiz.'
print 'Greets to http://greyhat-security.com'
print 'This is version 1.0\n'

LFIex1 = re.compile('(\\$_REQUEST\\[.*?\\] = \'(?:[a-z][a-z0-9_]*)\\.php\')', re.IGNORECASE|re.DOTALL)
LFIex2 = re.compile('(\\$_GET\\[.*?\\] = \'(?:[a-z][a-z0-9_]*)\\.php\')', re.IGNORECASE|re.DOTALL)
LFIex3 = re.compile('(\\$_POST\\[.*?\\] = \'(?:[a-z][a-z0-9_]*)\\.php\')', re.IGNORECASE|re.DOTALL)
RFIex1 = re.compile('(include \\$(\\$?:[a-z][a-z0-9_]*))', re.IGNORECASE|re.DOTALL)
RFIex2 = re.compile('(fopen\\(\\$.*?(?:[a-z][a-z0-9_]*).*?\\))', re.IGNORECASE|re.DOTALL)
RFIex3 = re.compile('(fsockopen\\(\\$.*?(?:[a-z][a-z0-9_]*).*?\\))', re.IGNORECASE|re.DOTALL)
RFIex4 = re.compile('(include_once \\$(\\$?:[a-z][a-z0-9_]*))', re.IGNORECASE|re.DOTALL)
RFIex5 = re.compile('(require \\$(\\$?:[a-z][a-z0-9_]*))', re.IGNORECASE|re.DOTALL)
RFIex6 = re.compile('(require_once (\\$?:[a-z][a-z0-9_]*))', re.IGNORECASE|re.DOTALL)
RFIex7 = re.compile('(file_get_contents\\(\\$(?:[a-z][a-z0-9_]*)\\))', re.IGNORECASE|re.DOTALL)
PHPex = re.compile('((?:[a-z][a-z0-9_]*)\\.php)', re.IGNORECASE|re.DOTALL)
CodeINJex1 = re.compile('(eval\\(".*?" = \\$.*?\\))', re.IGNORECASE|re.DOTALL)
CodeINJex1_2 = re.compile('( = )', re.IGNORECASE|re.DOTALL)
CodeINJex2 = re.compile('(system\\(".*?"\\);)', re.IGNORECASE|re.DOTALL)
CodeINJex3 = re.compile('(popen\\((?:[a-z][a-z0-9_]*)\\))', re.IGNORECASE|re.DOTALL)
XSSex1 = re.compile('(echo \\$_POST\\[\\\'.*?\\\'\\])', re.IGNORECASE|re.DOTALL)
Requestex1 = re.compile('(\\$_GET\\[\\\'.*?\\\'\\])', re.IGNORECASE|re.DOTALL)
Requestex2 = re.compile('(\\$_REQUEST\\[\\\'.*?\\\'\\])', re.IGNORECASE|re.DOTALL)
Requestex3 = re.compile('(\\$_POST\\[\\\'.*?\\\'\\])', re.IGNORECASE|re.DOTALL)
Requestex4 = re.compile('(\\$_COOKIE\\[\\\'.*?\\\'\\])', re.IGNORECASE|re.DOTALL)
InputFilterex = re.compile('((preg_match\\(".*?")).*?(\\))', re.IGNORECASE|re.DOTALL)
LRFIcookex = re.compile('(.(?:[a-z][a-z0-9_]*) = \\$_COOKIE\\[\\\'.*?\\\'\\])', re.IGNORECASE|re.DOTALL)
Cookiesrefex = re.compile('(\\$_COOKIE\\[\\\'.*?\\\'\\])', re.IGNORECASE|re.DOTALL)

fs = []
pes = []
lfinum = []
phpnum = []
phps = []
phpexs = []
codeinj = []
citemp = []
totalreq = []
inpfilter = []
lrficook = []
iio = 0
rfis = []
xsss = []
cookiesref = []

def usage():
    print 'Usage \t\t' + sys.argv[0] + ' directory of php file(s)'
    print 'Example \t' + sys.argv[0] + ' ' + os.getcwd()
    sys.exit()
    

def numFiles():
    for dir, sf, files in os.walk(sys.argv[1]):
        for item in files:
            ldld = dir + '/' + item
            ldld = ''.join(ldld)
            fs.append(ldld)
    print str(len(fs)) + ' files.'


def numPHP():
    for item in fs:
        temp = []
        temp2 = []
        temp = list(item)
        temp2.append(temp[-1])
        temp2.append(temp[-2])
        temp2.append(temp[-3])
        temp2 = ''.join(temp2)
        if temp2 == 'php':
            phps.append(item)
    print str(len(phps)) + ' php files.'
    

def CookiesRef():
    for item in phps:
        rs = []
        lol = open(item, 'r').read()
        rs = Cookiesrefex.findall(lol)
        if len(rs) != 0:
            for i in rs:
                cookiesref.append(str(i) + ' - cookie was called upon in ' + str(item))
    print str(len(cookiesref)) + ' times cookie was called upon.'
    
def PHPcheck():
    for item in phps:
        rs = []
        lol = open(item, 'r').read()
        rs = PHPex.findall(lol)
        if len(rs) != 0:
            for i in rs:
                phpnum.append(str(i) + ' - string "php" was mentioned in ' + str(item))
    print str(len(phpnum)) + ' times "PHP" was mentioned.'
    

def RequestNums():
    for item in phps:
        rs = []
        lol = open(item, 'r').read()
        rs = Requestex1.findall(lol)
        if len(rs) != 0:
            for i in rs:
                totalreq.append(str(i) + ' - request is taken in ' + str(item))
        rs = []
        rs = Requestex2.findall(lol)
        if len(rs) != 0:
            for i in rs:
                totalreq.append(str(i) + ' - request is taken in ' + str(item))
        rs = []
        rs = Requestex3.findall(lol)
        if len(rs) != 0:
            for i in rs:
                totalreq.append(str(i) + ' - request is taken in ' + str(item))
        rs = []
        rs = Requestex4.findall(lol)
        if len(rs) != 0:
            for i in rs:
                totalreq.append(str(i) + ' - request is taken in ' + str(item))
    print str(len(totalreq)) + ' requests the server takes.'
    

def InputFilter():
    for item in phps:
        rs = []
        lol = open(item, 'r').read()
        rs = InputFilterex.findall(lol)
        if len(rs) != 0:
            for i in rs:
                inpfilter.append(str(i) + ' - input filter in ' + str(item))
    print str(len(inpfilter)) + ' times input was called to a filter.'


def LFIcheck():
    for item in phps:
        rs = []
        lol = open(item, 'r').read()
        rs = LFIex1.findall(lol)
        if len(rs) != 0:
            for i in rs:
                lfinum.append(str(i) + ' - possible LFI vuln in ' + str(item))
        rs = []
        re = LFIex2.findall(lol)
        if len(rs) !=0:
            for i in rs:
                lfinum.append(str(i) + ' - possible LFI vuln in ' + str(item))
        rs = []
        re = LFIex3.findall(lol)
        if len(rs) !=0:
            for i in rs:
                lfinum.append(str(i) + ' - possible LFI vuln in ' + str(item))
    print str(len(lfinum)) + ' possible LFI vulnerabilities.'


def CodeINJcheck():
    global citemp
    for item in phps:
        rs = []
        lol = open(item, 'r').read()
        rs = CodeINJex1.findall(lol)
        if len(rs) != 0:
            for i in rs:
                citemp.append(str(i))
        rs = []
        if len(citemp) != 0:
            for i in citemp:
                rs = []
                rs = CodeINJex1_2.findall(i)
                if len(rs) != 0:
                    codeinj.append(str(i) + ' - possible code injection vuln in ' + str(item))
        rs = []
        citemp = []
        rs = CodeINJex2.findall(lol)
        if len(rs) != 0:
            for i in rs:
                codeinj.append(str(i) + ' - possible code injection vuln in ' + str(item))
        
        rs = CodeINJex3.findall(lol)
        if len(rs) != 0:
            for i in rs:
                codeinj.append(str(i) + ' - possible code injection vuln is ' + str(item))
    print str(len(codeinj)) + ' possible code injection vulnerabilities.'


def LRFIcook():
    for item in phps:
        rs = []
        lol = open(item, 'r').read()
        rs = LRFIcookex.findall(lol)
        if len(rs) != 0:
            for i in rs:
                lrficook.append(str(i) + ' - possible path traversal using the cookie vuln in ' + str(item))
    print str(len(lrficook)) + ' possible RFI/LFI vulns using cookies.'


def RFIcheck():
    for item in phps:
        rs = []
        lol = open(item, 'r').read()
        rs = RFIex1.findall(lol)
        if len(rs) !=0:
            for i in rs:
                rfis.append(str(i) + ' - possible RFI exploit in ' + str(item))
        rs = []
        rs = RFIex2.findall(lol)
        if len(rs) !=0:
            for i in rs:
                rfis.append(str(i) + ' - possible RFI exploit in ' + str(item))
        rs = []
        rs = RFIex3.findall(lol)
        if len(rs) !=0:
            for i in rs:
                rfis.append(str(i) + ' - possible RFI exploit in ' + str(item))
        rs = []
        rs = RFIex4.findall(lol)
        if len(rs) !=0:
            for i in rs:
                rfis.append(str(i) + ' - possible RFI exploit in ' + str(item))
        rs = []
        rs = RFIex5.findall(lol)
        if len(rs) !=0:
            for i in rs:
                rfis.append(str(i) + ' - possible RFI exploit in ' + str(item))
        rs = []
        rs = RFIex6.findall(lol)
        if len(rs) !=0:
            for i in rs:
                rfis.append(str(i) + ' - possible RFI exploit in ' + str(item))
        rs = []
        rs = RFIex7.findall(lol)
        if len(rs) !=0:
            for i in rs:
                rfis.append(str(i) + ' - possible RFI exploit in ' + str(item))
    print str(len(rfis)) + ' possible RFI vulnerabilities.'

def XSSnum():
    for item in phps:
        rs = []
        lol = open(item, 'r').read()
        rs = XSSex1.findall(lol)
        if len(rs) !=0:
            for i in rs:
                xsss.append(str(i) + ' - possible RFI exploit in ' + str(item))
    print str(len(xsss)) + ' possible XSS vulnerabilities.'
if len(sys.argv) != 2:
    if len(sys.argv) != 3:
        usage()


if len(sys.argv) == 3:
    iio = sys.argv[2]


numFiles()
numPHP()
RFIcheck()
LFIcheck()
LRFIcook()
CodeINJcheck()
XSSnum()
print ''
PHPcheck()
CookiesRef()
RequestNums()
#InputFilter()

for item in lfinum:
    pes.append(item)
for item in rfis:
    pes.append(item)
for item in codeinj:
    pes.append(item)
for item in lrficook:
    pes.append(item)
for item in xsss:
    pes.append(item)
for item in cookiesref:
    pes.append(item)

if iio == 1:
    for item in phpnum:
        pes.append(item)
    for item in totalreq:
        pes.append(item)
    for item in inpfilter:
        pes.append(item)

if len(pes) != 0:
    pe = open('possible.txt', 'w')
    pe.write("If you don't know how to secure these, visit http://www.owasp.org/index.php and search for the issue (It will be beside the file with the possible vulnerability) \n\n")
    for item in pes:
        pe.write(str(item) + '\n')
    pe.close()

print '\nCheck possible.txt for output'
print 'Please remember this is an alpha and should not be relied upon for full testing.'
print 'If you want to contribute, or report an error please contact me at lp951@hotmail.com'
