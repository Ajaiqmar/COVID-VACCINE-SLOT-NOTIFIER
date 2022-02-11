# IMPORTING THE COWIN API MODULE
from cowin_api import CoWinAPI
import pywhatkit as pk
import time
import smtplib


mail=smtplib.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
# SPECIFY THE EMAIL OF THE SENDER'S ADDRESS. 
sender='[SENDER EMAIL ADDRESS]'
# SPECIFY THE EMAIL OF THE RECEIVER'S ADDRESS. 
recipient='[RECEIVER EMAIL ADDRESS]'
# SPECIFY THE PASSWORD OF THE SENDER'S EMAIL ADDRESS
mail.login(sender,'[PASSWORD]')
header='To:'+recipient+'\n'+'From:'+sender+'\n'+'subject:ALERT!!\n'
content=header+"VACCINE AVAILABLE!!"

# SPECIFY THE PINCODE
pin_code = "PINCODE"

cowin = CoWinAPI()

flag=0

# THE SCRIPT LOOPS INFINITELY WITH A TIME INTERVAL OF 60 SECONDS INORDER TO AVOID OVERLOADING THEIR SERVER.
while(1):
    
    # REQUESTS THE AVAILABLE CENTERS BASED ON PINCODE
    available_centers = cowin.get_availability_by_pincode(pin_code)

    centers = available_centers['centers']

    sessions = ""
    
    # IF YOU HAVE A SPCIFIC CENTER ID, YOU COULD SPECIFY IT, ELSE COMMENT THE CODE.
    for i in centers:
        if(i['center_id']=="[CENTER ID]"):
            sessions = i['sessions']

    for i in sessions:
        # IF THE CONDITION PASSES, INFORM THE USERS THROUGH MAIL AND WHATSAPP.
        if(i['min_age_limit']==18 and i['available_capacity_dose1']>0):
            mail.sendmail(sender,recipient, content)

            t=list(map(int,list(time.localtime(time.time()))))
            if((t[4]+4)>=60):
                t[3]+=1
                t[4]=(t[4]+4)%60
                if(t[3]==24):
                    t[3]=0
            else:
                t[4]=(t[4]+4)%60
            pk.sendwhatmsg("WHATSAPP NUMBER","Vaccine Available",t[3],t[4])

            t=list(map(int,list(time.localtime(time.time()))))
            if((t[4]+4)>=60):
                t[3]+=1
                t[4]=(t[4]+4)%60
                if(t[3]==24):
                    t[3]=0
            else:
                t[4]=(t[4]+4)%60
            pk.sendwhatmsg("WHATSAPP NUMBER","Vaccine Available",t[3],t[4])
            flag=1
            break
    if(flag):
        break

    time.sleep(60)


