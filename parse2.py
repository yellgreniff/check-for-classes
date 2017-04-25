from twilio.rest import Client
import urllib2
import re
import time

Account_SID = ""
Auth_TOKEN = ""
myTwilioNumber = ""
myNumber = ""
initialTime = round(time.clock())
keepRunning = True


def notify(message): #texts me with message
    client = Client(Account_SID, Auth_TOKEN)
    client.messages.create(
        to= myNumber,
        from_ = myTwilioNumber,
        body=message
    )

url = "https://ntst.umd.edu/soc/search?courseId=HIST289y&sectionId=&termId=201708&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on"
sections = {'0': '0'} #dictionary of sections

response = urllib2.urlopen(url)
html = response.read()
html = html.decode("utf8")
print("started running")

#regex to find all sections
while keepRunning:
    print("running in while loop")

    counter = 1

    for m in re.finditer('<span class="open-seats-count">', html): #finds all occurrences
        sections[counter] = html[m.end()] #put in dictionary
        counter+=1

    for k, v in sections.items():
        print time.asctime(time.localtime(time.time())) #prints current time
        print(str(k) + "section:" + str(v)) #prints each section
        if not v == '0':
            print("Done!")
            notify("a seated opened up in section " + str(k))
            keepRunning = False #stops the bot from running


    time.sleep(60)#checks for open seats every 30 seconds
    print("It's been a minute")
    currentTime = round(time.clock())
    if currentTime-initialTime >= 14400: #messages the user that bot is still running after every 4 hours
        initialTime = round(time.clock())
        notify("It's been 4 hours, bot is still checking for seats")
notify("The script ended")
