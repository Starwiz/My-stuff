import smtplib, thread

gmailu = '' #The gmail you would like to spam from
gmailp = '' #The password to that gmail
message = "Seeeeeeeeeee it works =D" #The message you would like to spam

#To find the slave's carrier: http://fonefinder.net/
#To find the email to spam if you want to spam an SMS: http://www.makeuseof.com/tag/email-to-sms/

receiver = '' #What is the 'email' you would like to spam
total = 1000 #How many times you would like to send the email
server = smtplib.SMTP('smtp.gmail.com', 587)
howmany = total
currently = 1

def connect():
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(gmailu, gmailp)

def send():
    server.sendmail(gmailu, receiver, message)

def close():
    server.close()
    
def start():
    for currently in range(howmany + 1):
        send()
        print "\tSent message: ", currently, "/", total
    close()

connect()
print "\t\t\tSending messages to", receiver

for item in range(10):
    thread.start_new(start())
