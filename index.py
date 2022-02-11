from cowin_api import CoWinAPI
import pywhatkit as pk
import time
import smtplib

mail=smtplib.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
sender='SENDER EMAIL ADDRESS'
recipient='RECEIVER EMAIL ADDRESS'
mail.login(sender,'PASSWORD')
header='To:'+recipient+'\n'+'From:'+sender+'\n'+'subject:ALERT!!\n'
content=header+"VACCINE AVAILABLE!!"


pin_code = "PINCODE"

cowin = CoWinAPI()

flag=0

while(1):
    available_centers = cowin.get_availability_by_pincode(pin_code)

    centers = available_centers['centers']

    sessions = ""

    for i in centers:
        if(i['center_id']==667673):
            sessions = i['sessions']

    for i in sessions:
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


