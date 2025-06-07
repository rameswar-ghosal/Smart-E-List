import datetime
import pytz
import tzlocal
from sqlite3 import connect
from os import path
ROOT=path.dirname(path.realpath(__file__))
db = connect(path.join(ROOT,'db.sqlite3'))
pb = connect(path.join(ROOT,'db.sqlite3'))

print("ROOT",ROOT)
print("db:",db)


fr = db.execute(" select * from enroll_expired_scheduledlist")
frow = fr.fetchall()

pn_r = db.execute("select * from enroll_pin_unpin")
pn_r_row = pn_r.fetchall()

cur = db.execute(" select * from enroll_scheduled")
row = cur.fetchall()

print("Row:", row)
for i in range(len(row)):
    current_local_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
   # current_utc_time = current_local_time
    #local_timezone = tzlocal.get_localzone()
    #print("Current UTC Time to Local Time : ",
     #     x := current_utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata')))
    x=current_local_time
    x = x.strftime('%Y-%m-%d %H:%M:%S')
    x = datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    xg = 0
    for j in range(len(pn_r_row)):
        if int(row[i][0]) == int(pn_r_row[j][1]):
          if int(pn_r_row[j][2]) == 1:
            xg = 1
            break
        else:
            xg = 0
    if xg != 1:        
            y=row[i][2]+" "+row[i][3]
            y=datetime.datetime.strptime(y,'%Y-%m-%d %H:%M:%S')
            print("scheduled Time :",y)
            print("local time :",x)
            difference = y - x
            print("difference :",difference)
            print("type(difference) :",type(difference))
            print("difference.total_seconds()",difference.total_seconds())
            print("type(difference.total_seconds())",type(difference.total_seconds()))
            if difference.total_seconds()/60 < 0:
                    print()
                    print(difference.total_seconds()/60," delete it")
                    cur.execute(" insert into enroll_expired_scheduledlist(id,schedule_items,schedule_date,schedule_time,user_id)values(?,?,?,?,?)",(row[i][0],row[i][1],row[i][2],row[i][3],row[i][4],))
                    cur.execute(" delete from enroll_scheduled where schedule_time=?",(row[i][3],))
                    db.commit()
            else:
                    print()
                    print(difference.total_seconds()/60," abhi time h")

    else:
        print("PINNED !") 

for i in range(len(frow)):
    current_local_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
   # current_utc_time = current_local_time
    #local_timezone = tzlocal.get_localzone()
    #print("Current UTC Time to Local Time : ",
     #     x := current_utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata')))
    x=current_local_time
    x = x.strftime('%Y-%m-%d %H:%M:%S')
    x = datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    xy=frow[i][2]+" "+frow[i][3]
    xy = datetime.datetime.strptime(xy, '%Y-%m-%d %H:%M:%S')
    df = x - xy
    print()
    print("df.total_seconds()/60 : ",df.total_seconds()/60)
    print()
    if df.total_seconds()/60 > 1:
         cur.execute(" delete from enroll_expired_scheduledlist where schedule_time=?", (frow[i][3],))
         print("delete from expired list")
         db.commit()
    else:
        print("abhi ni :",df.total_seconds()/60)

print("/"*200)

#############################################################################################
# ckeck and deleted first !
connecting_to_db = connect(path.join(ROOT,'db.sqlite3'))
sqlite_select_query = connecting_to_db.execute('DELETE FROM enroll_weather_ackno')
connecting_to_db.commit()



##############################################################################################
# Weather API + its Logic + Mail Acknowledgement

import requests
import json
from sqlite3 import connect
from datetime import datetime
import pytz

LIST=[]

current_local_time = datetime.now(pytz.timezone('Asia/Kolkata'))
xc = current_local_time.strftime('%d-%m-%Y')
xd=xc.split('-')

con = connect(path.join(ROOT,'db.sqlite3'))
cur = con.execute(" select * from enroll_scheduled")
row = cur.fetchall()
print("row:",row)
for i in row:
    print('i[2]:',i[2])
    I=i[1]
    o1=i[2].split("-")
    o2=i[3].split(":")
    print("o1:",i[2].split("-"))
    print("o2:",i[3].split(":"))

    user_id=i[4]

    cr = con.execute(" select city_name from enroll_selectoptions where user_id=?",(i[4],))
    un = con.execute(" select username from auth_user where id=?",(i[4],))
    ue = con.execute(" select email from auth_user where id=?",(i[4],))
    e=ue.fetchone()
    for i in e:email=i
    u=un.fetchone()
    for i in u:user_name=i
    r = cr.fetchone()
    for i in r:city=i
    print("username:",user_name)
    print("city_name:",city)
    print("email:",email)
    #################################################################################################################
    schedule_date = int(o1[2])
    print("schedule_date:",schedule_date)
    schedule_month = int(o1[1])
    print("schedule_month:",schedule_month)
    schedule_year = int(o1[0])
    print("schedule_year:",schedule_year)
    #################################################################################################################
    schedule_hour = int(o2[0])
    print("schedule_hour:",schedule_hour)
    schedule_minute = int(o2[1])
    print("schedule_minute:",schedule_minute)
    #################################################################################################################
    present_date  = int(xd[0])
    print("present_date:",present_date)
    present_date  = int(xd[0])
    present_month = int(xd[1])
    print("present_month:",present_month)
    #################################################################################################################
    #api_address1="https://api.openweathermap.org/data/2.5/weather?appid=61d38a3c289f168e130b1fa745c9a37c&q="
    api_address="https://api.openweathermap.org/data/2.5/forecast?appid=61d38a3c289f168e130b1fa745c9a37c&q="
    url = api_address+city
    json_data=requests.get(url).json()
    json_string = json.dumps(json_data,indent=4)
    data=json.loads(json_string)
    ################################################################################################################
    l=[]
    mon={'lp':{1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31},
    'nlp':{1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}}

    if schedule_year % 100 == 0:
        if schedule_year % 400 == 0:
            mon = mon["lp"]
        else:
            mon = mon["nlp"]
    else:
        if schedule_year % 4 == 0:
            mon = mon["lp"]
        else:
            mon = mon["nlp"]
    print("mon:",mon)
    to_see_for = []
    if schedule_date == 1:
        if present_month == schedule_month -1:
            sm = int(schedule_month) - 1
            having_days = mon[sm]
            for i in range(2):
                to_see_for.append(having_days-i)
    elif schedule_date == 2:
       if present_date + 1 != schedule_date:
         if present_month == schedule_month - 1:
             sm = int(schedule_month) - 1
             having_days = mon[sm]
             to_see_for.append(having_days)
         if schedule_month == present_month + 1:
             to_see_for.append(1)
       else:
           to_see_for.append(1)

    else:
        if present_month == schedule_month:
            having_days = schedule_date
            for i in range(1,3):
                to_see_for.append(having_days-i)

    print("to see for :",to_see_for)
    print("_"*300)
    for i in data['list']:
        print(i)
    print("_"*300)
    extract_weatherdata = []
    for i in range(len(data['list'])):
        weathers_date_time = data['list'][i]['dt_txt']
        weathers_date_time = weathers_date_time.split(" ")
        weathers_date = weathers_date_time[0]
        wsd = weathers_date.split("-")
        wsd_only_date = wsd[2]
        if len(to_see_for)!=0:
           if len(to_see_for) != 1:
             if to_see_for[1] == present_date or to_see_for[0] == present_date :
                if schedule_date == int(wsd_only_date):
                    extract_weatherdata.append(data['list'][i])
           else:
             if to_see_for[0] == present_date :
                if schedule_date == int(wsd_only_date):
                   extract_weatherdata.append(data['list'][i])

    print("extract_weatherdata :",extract_weatherdata)
    for j in extract_weatherdata:
        print(j)
    ##################################################################################################################
    checking_time = schedule_hour + schedule_minute / 100
    print("checking_time:",checking_time)
    print("-"*50)
    #################################################################################################################
    for i in range(len(extract_weatherdata)):
        extract_weathersdata_weathers_date_time = extract_weatherdata[i]['dt_txt']
        extract_weathersdata_weathers_date_time = extract_weathersdata_weathers_date_time.split(" ")
        extract_weathersdata_weathers_time = extract_weathersdata_weathers_date_time[1]
        e_wst = extract_weathersdata_weathers_time.split(":")
        e_wst_only_hour = e_wst[0]
        print("int(e_wst_only_hour) - 3 :",int(e_wst_only_hour) - 3)
        print("checking_time:",checking_time)
        print("int(e_wst_only_hour):",int(e_wst_only_hour))
        if int(e_wst_only_hour) - 3 <= checking_time <= int(e_wst_only_hour):
            if 0 <= schedule_hour < 12:
                gmt = 'A.M'
            elif 12 <= schedule_hour <= 23:
                gmt = 'P.M'

            current_local_time = datetime.now(pytz.timezone('Asia/Kolkata'))

            if extract_weatherdata[i-1]['weather'][0]['description'] == 'clear sky':
                          print(" extract_weatherdata['list'][i-1]['weather'][0]['description'] ",extract_weatherdata[i-1]['weather'][0]['description'])
                          LIST.append("Dear " + user_name + " ! It seems to be " + extract_weatherdata[i-1]['weather'][0]['description'] + " day on your Scheduled Day, As you have scheduled for an item : " + I + " on " + str(
                          schedule_date) + " - " + str(schedule_month) + " - " + str(schedule_year) + " at " + str(schedule_hour) + ":" + str(
                          schedule_minute) + " " + str(gmt) + " [ from SE-LTeam,Thankyou :) ]" + "`" + str(current_local_time))
            else:
                          print("extract_weatherdata['list'][i-1]['weather'][0]['description']",extract_weatherdata[i-1]['weather'][0]['description'])
                          LIST.append("Dear " + user_name + " ! It seems to be " + extract_weatherdata[i - 1]['weather'][0][
                                  'description'] + " day on your Scheduled Day, As you have scheduled for an item : " + I + " on " + str(
                                  schedule_date) + " - " + str(schedule_month) + " - " + str(
                                  schedule_year) + " at " + str(schedule_hour) + ":" + str(
                                  schedule_minute) + " " + str(gmt) + " [ from SE-LTeam,Thankyou :) ]" + "`" + str(
                                  current_local_time))

        elif checking_time > 21 or checking_time == 21.0:
            if int(e_wst_only_hour) == 21:
                if 0 <= schedule_hour < 12:
                          gmt = 'A.M'
                elif 12 <= schedule_hour <= 23:
                          gmt = 'P.M'

                          print("else part 21 ~ 24 ")

                current_local_time = datetime.now(pytz.timezone('Asia/Kolkata'))

                print("extract_weatherdata[i] :",extract_weatherdata[i])
                if extract_weatherdata[i]['weather'][0]['description'] == 'clear sky':
                    print(" extract_weatherdata['list'][i]['weather'][0]['description'] EA",
                          extract_weatherdata[i]['weather'][0]['description'])
                    LIST.append(
                        "Dear " + user_name + " ! It seems to be " + extract_weatherdata[i]['weather'][0][
                            'description'] + " day on your Scheduled Day, As you have scheduled for an item : " + I + " on " + str(
                            schedule_date) + " - " + str(schedule_month) + " - " + str(
                            schedule_year) + " at " + str(schedule_hour) + ":" + str(
                            schedule_minute) + " " + str(gmt) + " [ from SE-LTeam,Thankyou :) ]" + "`" + str(
                            current_local_time))
                else:
                    print("extract_weatherdata['list'][i]['weather'][0]['description'] EB",
                          extract_weatherdata[i]['weather'][0]['description'])
                    LIST.append(
                        "Dear " + user_name + " ! It seems to be " + extract_weatherdata[i]['weather'][0][
                            'description'] + " day on your Scheduled Day, As you have scheduled for an item : " + I + " on " + str(
                            schedule_date) + " - " + str(schedule_month) + " - " + str(
                            schedule_year) + " at " + str(schedule_hour) + ":" + str(
                            schedule_minute) + " " + str(gmt) + " [ from SE-LTeam,Thankyou :) ]" + "`" + str(
                            current_local_time))

    print("user_id :",user_id)
    ###############################################################################################################
    ###############################################################################################################
    if len(LIST)!=0:
        connecting_to_db = connect(path.join(ROOT,'db.sqlite3'))
        current_local_time = datetime.now(pytz.timezone('Asia/Kolkata'))
        sqlite_insert_query =  connecting_to_db.execute("""INSERT INTO enroll_weather_ackno
                                  (user_id, messages, time_of_message, messages_alert)
                                   VALUES(?,?,?,?)""",(user_id,LIST[0],str(current_local_time),1))
        connecting_to_db.commit()
    LIST=[]
    extract_weatherdata=[]
    print("-"*100)
