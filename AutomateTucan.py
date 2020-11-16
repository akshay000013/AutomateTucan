#! python3
import bs4
import smtplib
import requests
from webbot import Browser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

web = Browser() # open a new window
web.go_to('https://www.tucan.tu-darmstadt.de') # go to the url
web.type('your username' , into='usrname' , id='field_user') # enter username
web.click('NEXT' , tag='span') # tab to go to password field
web.type('your password' , into='pass' , id='field_pass') # enter password
web.click('Anmelden') # login
web.click('Prüfungen') # go to the tab Prüfungen
web.click('Leistungsspiegel') # go to the tab Leistungsspiegel

htmlsource = web.get_page_source() # Download the page source

myList = [] # a list to add elements
cmpList = [] # a list to compare the above list with in order to check for changes
available = False

with open('tucan.txt') as file:  # save a .txt file first and then read it
    data = file.read()

soup = bs4.BeautifulSoup(htmlsource,features="lxml") # get all the content from htmlsource
everything = soup.find_all("td") # find all tags with td and return. td contains all the information from the Leistungsspiegel

for change in everything: # add all the content in the cmpList
    cmpList.append(str(change.text.strip()))

# if the .txt file has the same content, no changes and no new grade available
# else content not same and a new grade is available
for change in everything:
    if data == str(cmpList):
        pass
    else:
        myList.append(str(change.text.strip()))
        with open('tucan.txt', 'w') as file: 
            file.write(str(myList))

try:
    requests.get('https://www.tucan.tu-darmstadt.de') # check if website is up
    if data == str(cmpList):
        print("You are logged in ^_^")
        print(myList)
        print("No changes")
    else:
        print("You are logged in ^_^")
        print(myList)
        print("New grade available")
        available = True
except requests.exceptions.ConnectTimeout:
    print("The request timed out")
except requests.exceptions.ConnectionError:
    print("A connection error occurred")
except requests.exceptions.HTTPError:
    print("'An HTTP error occurred")

# initialising the email
sender = "example@gmail.com"
reciever = "example@gmail.com"
subject = 'Attention! New Grade Available'

message = MIMEMultipart('')
message['Subject'] = subject
message['From'] = sender
message['To'] = reciever

text = 'A new grade is available, please check your grades. Viel Erfolg!'

part1 = MIMEText(text, 'plain')
#part2 = MIMEText(html, 'html')

message.attach(part1)
#message.attach(part2)

# if new grade is available, an email will be sent
if available == True:
    conn = smtplib.SMTP('smtp.gmail.com', 587) # smtp address and port
    conn.ehlo() # call this to start the connection
    conn.starttls() # starts tls encryption. When we send our password it will be encrypted.
    conn.login('example@gmail.com', 'your email password')
    conn.sendmail(sender, reciever, message.as_string())
    conn.quit()
    print('\nSent notificaton e-mails for the following recipients:')
    print(reciever)
else:
    print('No new grade is available.')


