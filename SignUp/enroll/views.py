from django.shortcuts import render,HttpResponseRedirect,HttpResponse,redirect
from enroll.models import Scheduled,Selectoptions,expired_scheduledList,weather_ackno
from .forms import SignUpForm,select,your_list,Sendingmail,searchquery,Authenticate,Setpassword,uniquekey
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User
from datetime import datetime
import pytz
import tzlocal
from sqlite3 import connect
import csv
from tablib import Dataset
from .resources import ScheduledResource


from enroll.models import Room,Message,Grp_admin,user_involved,waiting_users,seen,Pin_Unpin
from django.http import HttpResponse, JsonResponse

# Create your views here.

def sel(request):
    return render(request,'enroll/sel.html')


def home(request):
   # sound = AudioSegment.from_wav('SignUp/enroll/mv.wav')
   # play(song)
    return render(request,'enroll/home.html')


def help(request):

    return render(request,'enroll/help.html')

def pinnedJ(request):
    if request.method == 'POST':
        id_pin = request.POST['id_pin']
        print("||id_pin||",id_pin)
        return JsonResponse({'id':id_pin})

def pinned(request,id):
    if request.method == 'POST':
        #print("request.POST['task'] :",request.POST['task'])
        #print("request.POST['t'] :",request.POST['t'])
        print("request.POST['pinn'] :",request.POST.get('pinn',False))
        print("id selected is : ",id)
        User_b = User.objects.get(username = request.user)    
        if request.POST.get('pinn',False) == 'on':    
            x = Pin_Unpin.objects.create(pin_id=id,pin_permission=1,pin_ka_id = User_b.id)
            x.save()
        else:
            Pin_Unpin.objects.filter(pin_id=id).delete() 

        return HttpResponseRedirect('/profile/')
    

def adm_reaction(request):

    adm_a=request.POST['accept']
    adm_r=request.POST['reject']
    apt=request.POST['apt']
    print("adm_a:",adm_a)
    print("adm_r:",adm_r)
    print('apt:',apt)
    roomname_kay_h =  waiting_users.objects.filter(users_name=apt)
    for i in roomname_kay_h:
        roomname_h = i.name_of_room
    waiting_users.objects.filter(users_name=apt).delete()
    print("waiting user deleted !!")
    if adm_a != " ":
        sn=seen.objects.create(users_ka_name=apt,special_id=adm_a,roomnm=roomname_h,time_of_reject=0)
        sn.save()

    elif adm_r != " ":
        x = datetime.now(pytz.timezone('Asia/Kolkata'))
        sn = seen.objects.create(users_ka_name=apt, special_id=adm_r, roomnm=roomname_h, time_of_reject=x)
        sn.save()


    #for i in w_u:
    #    u_u=waiting_users(name_of_room=i.name_of_room,users_message=i.users_message,special_id=adm_a)

    return HttpResponse('Message sent successfully')

def userinwait(request):
       print("Hello")
       if  request.user.is_authenticated:
           print("inside request.user.is_authenticated")
           if Grp_admin.objects.filter(G_a = request.user).exists():
               print("Grp_admin.objects.filter(G_a = request.user).exists()")
               Grp = Grp_admin.objects.filter(G_a=request.user)
               for i in Grp:
                   x = i.he_is_adm_of
                   x1=i.G_a
               print("request.user is username is :", x1)
               print("request.user is he_is_adm_of :", x)
               print("heeeeeeeeeee")
               ZE = waiting_users.objects.filter(name_of_room = x)
               print("ZE :",ZE)
               for i in ZE:
                   print(i.name_of_room)
                   print(i.users_message)
               print(JsonResponse({"messages":list(ZE.values())}))
               return JsonResponse({"messages":list(ZE.values())})

           else:
               print("flase")
               return redirect("C_home")

def syfr(request):
            if Grp_admin.objects.filter(G_a=request.user).exists():
                print("Grp_admin.objects.filter(G_a = request.user).exists()")
                Grp = Grp_admin.objects.filter(G_a=request.user)
                for i in Grp:
                    x = i.he_is_adm_of
                print("request.user is he_is_adm_of :",x)
                user_i = user_involved.objects.filter(user_ka_name=request.user)
                for i in user_i:
                    y = i.Room_ka_name
                if x == str(1):
                    print("heeeeeeeeeee")
                    ZE = waiting_users.objects.filter(name_of_room=y)
                    print("ZE :", ZE)
                    for i in ZE:
                        print(i.name_of_room)
                        print(i.users_message)
                    print(JsonResponse({"messages": list(ZE.values())}))
                    return JsonResponse({"messages": list(ZE.values())})
                else:
                    return JsonResponse({"m":0})
            else:
                print("flase")
                return JsonResponse({"m":0})

def C_home(request):
  cef=0
  YUP = 0
  if request.user.is_authenticated:
    if request.method == 'POST':
      if request.POST['username'] == " " and request.POST['RM'] != " ":
          RM = request.POST['RM']
          UN = request.POST['UN']
          print("RM:", RM)
          print("UN:", UN)
          l_r = RM
          cont = 0
          if len(l_r) == 5:
              print("_" * 34)
              if l_r[0] == '$' or l_r[len(l_r) - 1] == '$':
                  for i in range(1, len(l_r) - 1):
                      if l_r[i].isupper() and l_r[i].isalpha():
                          cont = cont + 1
                      else:
                          break
                  if cont == 3:
                      if seen.objects.filter(users_ka_name=request.user).exists():
                        checking = seen.objects.filter(users_ka_name=request.user)
                        us=0
                        for i in checking:
                            if i.roomnm == RM:
                              if seen.objects.filter(special_id=str(-1)).exists():
                                  tor = i.time_of_reject
                                  tor = tor.split('.')
                                  z0 = datetime.strptime(tor[0], '%Y-%m-%d %H:%M:%S')
                                  ct0 = datetime.now(pytz.timezone('Asia/Kolkata'))
                                  ct = str(ct0)
                                  ct = ct.split('.')
                                  z1 = datetime.strptime(ct[0], '%Y-%m-%d %H:%M:%S')
                                  dif = z1 - z0
                                  print("dif.total_seconds():", dif.total_seconds())
                                  print("min : ", dif.total_seconds() / 60)
                                  if dif.total_seconds() / 60 > 1:
                                      seen.objects.filter(users_ka_name=request.user).delete()
                                      messages.error(request, 'Your follow request have been send successfully !')
                                      YUP = 1
                                  else:
                                      messages.error(request,
                                                     "🤔 As we told you that your request had been Rejected by Grp. Admin.")
                                      YUP = 1
                            else:
                                us+=1
                        if us == len(checking):
                            x = waiting_users.objects.create(name_of_room=RM, users_message=UN,
                                                             users_name=str(request.user))
                            x.save()
                            messages.success(request, 'Your follow request have been send successfully !')
                            cef = 1

                      else:
                          x = waiting_users.objects.create(name_of_room=RM, users_message=UN,
                                                           users_name=str(request.user))
                          x.save()

                          messages.success(request, 'Your follow request have been send successfully !')
                          cef = 1
                  else:
                      print("|" * 20)
                      print("Invalid Room Name")
                      messages.error(request, 'Invalid Room Name, Plz read RULES Carefully !')
              else:
                  print("|" * 20)
                  print("Invalid Room Name")
                  messages.error(request, 'Invalid Room Name, Plz read RULES Carefully !')
          else:
              print("|" * 20)
              print("Invalid Room Name")
              messages.error(request, 'Invalid Room Name, Plz read RULES Carefully !')


      elif request.POST['username']!= " " and request.POST['RM']==" ":
        RM = request.POST['RM']
        UN = request.POST['UN']
        room_name = request.POST['room_name']
        username = request.POST['username']
        print("room :",room_name)
        print("username :",username)
        print("RM:", RM)
        print("UN:", UN)
        if request.user.is_authenticated:
            if str(request.user)==username:
                print("YES")
                print("R A J N E E S H")
                if Room.objects.filter(Room_name=room_name).exists():
                    print("yes exists")
                    rm = Room.objects.filter(Room_name=room_name)
                    c=0
                    if len(rm) > 0:
                        print(len(rm))
                        if user_involved.objects.filter(user_ka_name=username).exists():
                          print("True")
                          #R = user_involved.objects.filter(user_ka_name=username)
                          S=  user_involved.objects.filter(user_ka_name=str(request.user))
                          for j in S:
                              print("j.Room_ka_name :",j.Room_ka_name)
                              if room_name == j.Room_ka_name:
                                   print("This exists :",j.Room_ka_name)
                                   print("Room Exist")
                                   c=1
                                   return redirect('inside_r/' + room_name + '/?username=' + username)

                          if c!=1:
                              #messages.error(request,'Not eligible')
                              if seen.objects.filter(users_ka_name=username).exists():
                                  sen = seen.objects.filter(users_ka_name=username)
                                  us=0
                                  for i in sen:
                                    if i.roomnm == room_name:
                                      if i.special_id == str(1):
                                          user_involve = user_involved.objects.create(Room_ka_name=room_name,
                                                            user_ka_name=username)
                                          user_involve.save()
                                          i.delete()
                                          #######seen.objects.filter(users_ka_name=username).delete()
                                          return redirect('inside_r/' + room_name + '/?username=' + username)

                                      else:
                                          print("E L S E")
                                          print("User :",i.users_ka_name)
                                          tor = i.time_of_reject
                                          tor=tor.split('.')
                                          z0 = datetime.strptime(tor[0],'%Y-%m-%d %H:%M:%S')
                                          ct = datetime.now(pytz.timezone('Asia/Kolkata'))
                                          ct = str(ct)
                                          ct = ct.split('.')
                                          z1 = datetime.strptime(ct[0],'%Y-%m-%d %H:%M:%S')
                                          dif = z1 - z0
                                          print("dif.total_seconds():", dif.total_seconds())
                                          print("min : ",dif.total_seconds()/60)
                                          if dif.total_seconds()/60 > 1:
                                              seen.objects.filter(users_ka_name=username).delete()
                                              messages.error(request,
                                                             "🤔 This room already have user/s. If you want to still use this chat's room, You have to send follow request to them . . .")
                                              mes = 1

                                              if Grp_admin.objects.filter(G_a=str(request.user)).exists():
                                                  if Grp_admin.objects.filter(preference=str(1)).exists():
                                                      x = Grp_admin.objects.filter(G_a=str(request.user))
                                                      for i in x:
                                                          userN = i.G_a
                                                  else:
                                                      userN = ""
                                              else:
                                                  userN = ""

                                              return render(request, 'enroll/C_home.html',
                                                            {'mes': mes, 'userN': userN, 'us_p': str(request.user)})
                                          else:
                                           messages.error(request,
                                                         "🤔 As we told you that your request had been Rejected by Grp. Admin.")
                                           YUP = 1

                                    else:
                                        us+=1
                                  if us == len(sen):
                                      us=0
                                      messages.error(request,
                                                     "🤔 This room already have user/s. If you want to still use this chat's room, You have to send follow request to them . . .")
                                      mes = 1

                                      if Grp_admin.objects.filter(G_a=str(request.user)).exists():
                                          if Grp_admin.objects.filter(preference=str(1)).exists():
                                              x = Grp_admin.objects.filter(G_a=str(request.user))
                                              for i in x:
                                                  userN = i.G_a
                                          else:
                                              userN = ""
                                      else:
                                          userN = ""

                                      return render(request, 'enroll/C_home.html',
                                                    {'mes': mes, 'userN': userN, 'us_p': str(request.user)})

                              else:
                                      messages.error(request, "🤔 This room already have user/s. If you want to still use this chat's room, You have to send follow request to them . . .")
                                      mes = 1

                                      if Grp_admin.objects.filter(G_a=str(request.user)).exists():
                                          if Grp_admin.objects.filter(preference=str(1)).exists():
                                              x = Grp_admin.objects.filter(G_a=str(request.user))
                                              for i in x:
                                                  userN = i.G_a
                                          else:
                                              userN = ""
                                      else:
                                          userN = ""

                                      return render(request, 'enroll/C_home.html',
                                                    {'mes': mes, 'userN': userN, 'us_p': str(request.user)})
                        else:
                            if seen.objects.filter(users_ka_name=username).exists():
                                sen = seen.objects.filter(users_ka_name=username)
                                us=0
                                for i in sen:
                                    if i.roomnm == room_name:
                                        if i.special_id == str(1):
                                            user_involve = user_involved.objects.create(Room_ka_name=room_name,
                                                                                        user_ka_name=username)
                                            user_involve.save()
                                            i.delete()
                                            return redirect('inside_r/' + room_name + '/?username=' + username)

                                        else:
                                            print("E L S E")
                                            messages.error(request,
                                                           "🤔 As we told you that your request had been Rejected by Grp. Admin.")
                                            YUP = 1
                                    else:
                                        us+=1
                                if us == len(sen):
                                        messages.error(request,
                                                       "🤔 This room already have user/s. If you want to still use this chat's room, You have to send follow request to them . . .")
                                        mes = 1

                                        if Grp_admin.objects.filter(G_a=str(request.user)).exists():
                                            if Grp_admin.objects.filter(preference=str(1)).exists():
                                                x = Grp_admin.objects.filter(G_a=str(request.user))
                                                for i in x:
                                                    userN = i.G_a
                                            else:
                                                userN = ""
                                        else:
                                            userN = ""

                                        return render(request, 'enroll/C_home.html',
                                                      {'mes': mes, 'userN': userN, 'us_p': str(request.user)})

                            else:
                                messages.error(request,
                                           "🤔 This room already have user/s. If you want to still use this chat's room, You have to send follow request to them . . .")
                                mes = 1

                                if Grp_admin.objects.filter(G_a=str(request.user)).exists():
                                   if Grp_admin.objects.filter(preference=str(1)).exists():
                                      x = Grp_admin.objects.filter(G_a=str(request.user))
                                      for i in x:
                                        userN = i.G_a
                                   else:
                                    userN = ""
                                else:
                                     userN = ""

                                return render(request, 'enroll/C_home.html',
                                          {'mes': mes, 'userN': userN, 'us_p': str(request.user)})
                else:
                  l_r = room_name
                  cont = 0
                  if len(l_r)==5:
                    print("_"*34)
                    if l_r[0]=='$' or l_r[len(l_r)-1]=='$':
                      for i in range(1,len(l_r)-1):
                          if l_r[i].isupper() and l_r[i].isalpha():
                               cont = cont + 1
                          else:
                              break
                      if cont == 3:
                            us = User.objects.filter(username=str(request.user))
                            for i in us:
                              usr_id = i.id
                            new_room = Room.objects.create(Room_name=room_name,user_inv_id=usr_id)
                            new_room.save()

                            GA = Grp_admin.objects.all()
                            G_A = Grp_admin.objects.create(G_a=username,preference=1,he_is_adm_of=room_name,related_room_id=usr_id)
                            G_A.save()
                            user_involve = user_involved.objects.create(Room_ka_name=room_name,user_ka_name=username)
                            user_involve.save()
                            return redirect('inside_r/' + room_name + '/?username=' + username)
                      else:
                          print("|"*20)
                          print("Invalid Room Name")
                          messages.error(request,' 🥺 Invalid Room Name, Plz read RULES Carefully !')
                    else:
                        print("|" * 20)
                        print("Invalid Room Name")
                        messages.error(request, ' 🥺 Invalid Room Name, Plz read RULES Carefully !')
                  else:
                      print("|" * 20)
                      print("Invalid Room Name")
                      messages.error(request, ' 🥺 Invalid Room Name, Plz read RULES Carefully !')

            else:
                print("NO")
                messages.error(request, " 🧐 I think your username is "+str(request.user)+" ! ")
                return redirect('C_home')



    if seen.objects.filter(users_ka_name=request.user).exists():
        x= seen.objects.filter(users_ka_name = request.user)
        for i in x:
            print("sending it yaar")
            if YUP != 1:
                if i.special_id == str(-1):
                    tor = i.time_of_reject
                    tor = tor.split('.')
                    z0 = datetime.strptime(tor[0], '%Y-%m-%d %H:%M:%S')
                    ct = datetime.now(pytz.timezone('Asia/Kolkata'))
                    ct = str(ct)
                    ct = ct.split('.')
                    z1 = datetime.strptime(ct[0], '%Y-%m-%d %H:%M:%S')
                    dif = z1 - z0
                    print("dif.total_seconds():", dif.total_seconds())
                    print("min : ", dif.total_seconds() / 60)
                    if dif.total_seconds() / 60 > 1:
                          pass
                          messages.success(request,"As your request was Rejected for Room's named : "+i.roomnm+" , You may try Again !")
                    else:
                       print("i.special_id 1:",i.special_id)
                       messages.success(request,'Sorry, Your Follow request has been Rejected by Grp. Adm.,You may try a new Room Name.')
                elif i.special_id == str(1):
                    print("i.special_id 2:",i.special_id)
                    messages.success(request,'Your Follow request has been Accepted by Grp. Adm.')
    YUP = 0
    if Grp_admin.objects.filter(G_a=request.user).exists():

        x=waiting_users.objects.all()
        print(x)
        count=0
        for i in x:
            count=count+1
        print("count:",count)
        if count > 0:
           DEAF = 1
        else:
            DEAF=0
    else:
        DEAF = 0



    if Grp_admin.objects.filter(G_a=str(request.user)).exists():
        if Grp_admin.objects.filter(preference = str(1)).exists():
            x=Grp_admin.objects.filter(G_a=str(request.user))
            for i in x:
                userN=i.G_a
        else:
            userN=""
    else:
        userN=""

    return render(request,'enroll/C_home.html',{'userN':userN,'us_p':str(request.user)})
  else:
      return HttpResponseRedirect('/login/11/')


def room_created(request):
    std = Room.objects.values()
    print("_"*50)
    print(std)
    print(len(std))
    std_room = list(std)
    return JsonResponse({'std_room':std_room,'room_avl':len(std)})


##############################################################################################
def usermanage(request):
    if request.method == 'POST':
        USRN = request.POST['managedata']
        print("USRN : ",USRN)
        if request.method == "POST":
           if user_involved.objects.filter(user_ka_name = str(request.user)).exists():
                xy = user_involved.objects.filter(user_ka_name = str(request.user))
                print('xy : ',xy)
                if Grp_admin.objects.filter(G_a=str(request.user)).exists():
                   grp_creted_by = Grp_admin.objects.filter(G_a=str(request.user))
                   for i in grp_creted_by:
                       rm_k_n = i.he_is_adm_of
                       if USRN == i.he_is_adm_of:
                           return JsonResponse({'status':-1,'say':'Access Denied ! If You want to Left, Plz Choose Delete User Section & Delete Yourself !'})
                for i in xy:
                    print(i.user_ka_name)
                    print(USRN)
                    print(i.Room_ka_name)
                    if i.Room_ka_name == USRN:
                        i.delete()
                        c=1
                        print(": deleted :")
                    else:
                        c=0
                        print("N m")
                print("_"*20)
                Room_d = Room.objects.filter(Room_name = USRN)
                for i in Room_d:
                    rm_id = i.user_inv_id
                print("rm_id:",rm_id)
                if Message.objects.filter(user=str(request.user).upper()).exists():
                    print("*" * 100)
                    Message_of_user = Message.objects.filter(user=str(request.user).upper())
                    for i in Message_of_user:
                        if i.user == str(request.user).upper():
                            print("True")
                            print("i.belongs_to_room:",i.belongs_to_room)
                            print("rm_id:",rm_id)
                            if int(i.belongs_to_room) == int(rm_id):
                                  print("Yes deleted successfully !")
                                  i.delete()

                        # print("MATCH FOUND")
                        # user_involved.objects.filter(user_ka_name=USRN).delete()

                    match_status = "deleted successfully"
                    return JsonResponse(
                            {'status': 1, 'user_data': request.POST['managedata'], 'MATCHED': match_status})
                if c==1:
                    match_status = "deleted successfully"
                    return JsonResponse(
                        {'status': 1, 'user_data': request.POST['managedata'], 'MATCHED': match_status})
                else:
                        c=0
                if c==0:
                    return JsonResponse({'status': 0})
           else:
               return JsonResponse({'say': 'Plz, Enter a Valid Room name !'})


##############################################################################################################################

def room_am_in(request):
    print("`"*20)
    if user_involved.objects.filter(user_ka_name=str(request.user)).exists():
        xy = user_involved.objects.filter(user_ka_name=str(request.user))
        std = xy.values()
        print("=>"*20)
        print("std:",std)
        std_user = list(std)
        if Grp_admin.objects.filter(G_a=str(request.user)):
            for_room = Grp_admin.objects.filter(G_a=str(request.user))
            for i in for_room:
                name_of_room = i.he_is_adm_of
            return JsonResponse({'std_user_manage': std_user,'stc':1,'name_of_room':name_of_room})
        else:
            return JsonResponse({'std_user_manage': std_user,'stc':1,'name_of_room':' '})

    else:
        return JsonResponse({'stc': 0})

##############################################################################################################################


def userdelete(request):
  if request.method == 'POST':
      USRN = request.POST['searchdata']
      if request.method == "POST":
          if Grp_admin.objects.filter(G_a=str(request.user)).exists():
              print("Your are admin")
              xy = Grp_admin.objects.filter(G_a=str(request.user))
              print(xy)
              for i in xy:
                 yx= i.he_is_adm_of
              yz = user_involved.objects.filter(Room_ka_name = yx)
              print("yyyyyyyyyyyyyyyyyy :",yz)
              for i in yz:
                  print(i.user_ka_name)
                  print(USRN)
                  if  USRN == 'You':
                      USRN = str(request.user)
                      Room_d = Room.objects.filter(Room_name=yx)
                      for i in Room_d:
                          rm_id = i.user_inv_id
                      print("rm_id:", rm_id)

                      if Message.objects.filter(user=USRN.upper()).exists():
                          print("*" * 100)
                          Message_of_user = Message.objects.filter(belongs_to_room=rm_id)
                          for i in Message_of_user:
                                      i.delete()
                      print("MATCH FOUND")
                      Room.objects.filter(Room_name=yx).delete()
                      u_i = user_involved.objects.filter(Room_ka_name=yx)
                      print("u_i :",u_i)
                      for i in u_i:
                             i.delete()
                      print("You are deleted !")
                      c = 'Y'
                      return JsonResponse(
                          {'status': 'Y', 'user_data': request.POST['searchdata'],'nothing':'nothing'})

                              # user_involved.objects.filter(user_ka_name=USRN).delete()

                  else:
                      if i.user_ka_name == USRN:
                          i.delete()
                          c=1
                      else:
                          c = 0

                      print("~"*30)
                      print("yx:",yx)
                      u_i = user_involved.objects.filter(Room_ka_name=yx)
                      print("u_i :",u_i)
                      for i in u_i:
                          print("()"*20)
                          print("i.user_ka_name:",i.user_ka_name)
                          print("USRN:",USRN)
                          if i.user_ka_name == USRN:
                              print("="*20)
                              i.delete()

                      Room_d = Room.objects.filter(Room_name = yx)
                      for i in Room_d:
                            rm_id = i.user_inv_id
                      print("rm_id:",rm_id)
                      if Message.objects.filter(user=USRN.upper()).exists():
                          print("*" * 100)
                          Message_of_user = Message.objects.filter(user=USRN.upper())
                          for i in Message_of_user:
                              if i.user == USRN.upper():
                                  print("True")
                                  print("i.belongs_to_room:", i.belongs_to_room)
                                  print("rm_id:", rm_id)
                                  if int(i.belongs_to_room) == int(rm_id):
                                      print("Yes deleted successfully !")
                                      i.delete()
                              else:
                                  print("not equal")
                                  print("i.user:",i.user)
                                  print("USRN.upper:",USRN.upper)

                              print("MATCH FOUND")
                                #user_involved.objects.filter(user_ka_name=USRN).delete()
                          match_status = "deleted successfully"
                          return JsonResponse({'status': 1, 'user_data': request.POST['searchdata'], 'MATCHED': match_status})
                      else:
                          print("!"*100)
              if c==1:
                  match_status = "deleted successfully"
                  return JsonResponse({'status': 1, 'user_data': request.POST['searchdata'], 'MATCHED': match_status})

              if c==0:
                  return JsonResponse({'status': 0})
          else:
              return JsonResponse({'status': 0})

##############################################################################################

def user_in_ur_room(request):
    if Grp_admin.objects.filter(G_a=str(request.user)).exists():
        y = Grp_admin.objects.filter(G_a=str(request.user))

        for i in y:
            xd = i.he_is_adm_of
            name_of_adm = i.G_a
        print(i.G_a)
        print("xd :",xd)
        x = user_involved.objects.filter(Room_ka_name = xd)
        std = x.values()
        print("std:",std)
        std_user = list(std)
        return JsonResponse({'std_user': std_user,'status':1,'name_of_adm':name_of_adm})





def room(request,room):
    username = request.GET.get('username')
    print("username :", username)
    print(type(username))
    print("room :", room)
    print(type(room))

    if username != 'None' and room != 'favicon.ico':
      if room == 'profile':
          room = ''
          username = ''
          room_details = ''
      else:
        print("username :",username)
        print(type(username))
        print("room :",room)
        print(type(room))
        #room_details = Room.objects.get(Room_name=room)
        rm_details = Room.objects.filter(Room_name=room)
        for i in rm_details:
            room_details = i.user_inv_id
        print("username:",username)
        print("room_details::",room_details)
        print("room::",room)
    else:
        room = ''
        username = ''
        room_details = ''

    #for i in room_details:
    #    print("i.id:",i.Room_name)

    return render(request,'enroll/room.html',{'username': username,
        'room': room,'room_details': room_details})

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    print('room_id :',room_id)
    username=username.upper()
    x = datetime.now(pytz.timezone('Asia/Kolkata'))
    z = x.strftime('%d-%m-%Y %I:%M %p')
    new_message = Message.objects.create(message_content=message, user=username,belongs_to_room=room_id,message_date=z)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    print("room name :",room)
    room_details = Room.objects.filter(Room_name=room)
    for i in room_details:
        room_d = i.user_inv_id
    print("room_details.id:",room_d)
    messages = Message.objects.filter(belongs_to_room=room_d)
    for i in messages:
        print("i.user:",i.user)
    print("messages:",messages)

    return JsonResponse({"messages":list(messages.values())})



# View func. for Sign_up
def sign_up(request):
    if request.method=="POST":
        fm = SignUpForm(request.POST)
        gmm = select(request.POST)
        #print(type(gmm))
        E=Selectoptions.objects.filter(phone_no=request.POST['phone_no'])
        c=0
        for i in E:
           c=c+1
        if c == 0:
                if fm.is_valid() and gmm.is_valid():
                    fm.save()

                    user_name =fm.cleaned_data['username']
                    U=User.objects.filter(username=user_name)
                    for i in U:
                        x = Selectoptions(user_id=i.id, city_name=gmm.cleaned_data['city_name'], phone_no=gmm.cleaned_data['phone_no'],
                                          unique_key=str(0), date_time=1, combKey=1, time_check=1
                                          )

                        x.save()#for sacing onetooneField
                    messages.success(request, "Your Account Created Successfully, We have Send You an Email as Registration Successful !")

                    user_name =fm.cleaned_data['username']
                    x = User.objects.get(username=user_name)
                    """import smtplib as s
                    ob = s.SMTP("smtp.gmail.com", 587)
                    ob.starttls()
                    ob.login("SENDER MAIL", "SENDER PASS")
                    current_local_time = datetime.now(pytz.timezone('Asia/Kolkata'))
                    current_utc_time = x.date_joined
                    g = current_utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata'))
                    subject = "Registration Successful for SE-L (Smart E - List)"
                    body = " Thankyou :) "+x.username+" for  Registering on SE-L on/at "+str(g)+" ( Smart E - List ). Now You can Login & Dive Inside. [ from SE-L Team,  Thankyou :) ]"
                    message = "Subject:{}\n\n{}".format(subject, body)
                    listofaddress = [x.email]
                    ob.sendmail("SENDER MAIL", listofaddress, message)
                    ob.quit()"""
                    fm = SignUpForm()
                    gmm = select()
        else:
               messages.error(request, "Duplicacy of PhoneNo. Cannot be tolerated, Please Try Another ! ")
    else:
        fm = SignUpForm()
        gmm = select()
    stud = User.objects.all()
    h={}
    for i in stud:
#          print(i.username)
 #         print(i.date_joined)
  #        print(type(i.date_joined))

          current_local_time = datetime.now(pytz.timezone('Asia/Kolkata'))
   #       print(current_local_time)
          current_utc_time = i.date_joined
    #      print(current_utc_time)
     #     local_timezone = tzlocal.get_localzone()
     #     print("local_timezone : ", local_timezone)
          print("Current UTC Time to Local Time : ",
                g:=current_utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata')))

          print("c.strftime('%b %d,%Y,%H:%M %p'):",g:=g.strftime('%a, %b. %d, %Y, %H:%M %p.'))
          #b=g.strftime('%a, %b. %d, %Y, %H:%M %p.')
          print("type(c):",type(g))

          h[i.username]=str(g)
      #print("Current Users :",h)

    x=User.objects.all()

    return render(request,'enroll/signup.html',{'form':fm,"gorm":gmm,'x':len(x),'childs':h})

def gen_unique_key(request,id):
    if request.method =='POST':
        print("||request.user post:||", request.user)
        USER_ID=id
        print("USER_ID",USER_ID)
        uk=uniquekey(request.POST)
        print(request.POST['Username'])
        x1 = User.objects.filter(id=int(USER_ID))
        for i in x1:
            if str(request.POST['Username'])!=i.username:
                messages.error(request,'Hey, Enter Your Username & not of Any one else !')
            else:
                x1=User.objects.filter(username=str(request.POST['Username']))
                for i in x1:
                    print(i.id)
                    print(type(i.id))
                x2=Selectoptions.objects.filter(user_id=i.id)
                l=[]
                for i in range(len(x2)):
                   l.append(x2[i])
                print(l)
                print(l[0].user_id)
                print(l[0].city_name)
                print(l[0].phone_no)

                if uk.is_valid():
                    x = Selectoptions(user_id=l[0].user_id, city_name=l[0].city_name, phone_no=l[0].phone_no,
                                      unique_key=str(uk.cleaned_data['unique_key']),date_time=1,combKey=1,time_check=1
                                      )

                    x.save()
                    return redirect('login',id=11)
                else:
                   print("Not Valid")
                   if uk['unique_key'].errors:
                       messages.error(request, uk['unique_key'].errors)


    else:
        uk=uniquekey()
    return render(request,'enroll/gen_uk.html',{'form':uk})


# view func. for Login
def user_login(request,id):
  if not request.user.is_authenticated:
      U_id=id
      if request.method == "POST":
        print("request.post :  ",request.POST)
        fm = Authenticate(request=request,data=request.POST)
        gm = uniquekey(request.POST)
        if U_id == 1:
         if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                print("valid")
         else:
            messages.error(request,'Invalid Username/Password')
            return HttpResponseRedirect('/login/1/')


        ob1 = User.objects.filter(username=str(request.POST['username']))
        for d in ob1:
            print(c := d.id)
            ob2 = Selectoptions.objects.filter(user_id=c)
        for i in ob2:
            print("ob :", i.unique_key)
            if  i.unique_key == '0':
                return redirect('gen_uk',id=c)


        if U_id == 12:
            ob1 = User.objects.filter(username=str(request.POST['username']))
            for d in ob1:
                print(c := d.id)

                ob2 = Selectoptions.objects.filter(user_id=c)
                if  i.date_time != '1':
                    print(current_local_time := datetime.now(pytz.timezone('Asia/Kolkata')))
                    print(type(current_local_time))
                    w=i.date_time.split("+")
                    y=str(current_local_time).split("+")

                    print("datetime.strptime('%Y-%m-%d %H:%M:%S.%f')",
                          datetime.strptime(w[0],'%Y-%m-%d %H:%M:%S.%f'))
                    print(type(datetime.strptime(w[0],'%Y-%m-%d %H:%M:%S.%f')))
                    print("|i.date_time|", w[0])
                    diff=datetime.strptime(y[0],'%Y-%m-%d %H:%M:%S.%f')-datetime.strptime(w[0],'%Y-%m-%d %H:%M:%S.%f')
                    print("|diff|",diff)
                    print("|diff.total_seconds()|",diff.total_seconds())
                    print("|diff.total_seconds()/60|",diff.total_seconds()/60)
                    print("|diff.total_seconds()/3600|",diff.total_seconds()/3600)
                    if diff.total_seconds()/3600 > .1 :
                      print(current_local_time := datetime.now(pytz.timezone('Asia/Kolkata')))

                      for i in ob2:
                            x = Selectoptions(user_id=i.user_id, city_name=i.city_name, phone_no=i.phone_no,
                                              unique_key=str(i.unique_key), incr=1, date_time=1,combKey=1,time_check=1
                                             )
                            x.save()

            ob1 = User.objects.filter(username=str(request.POST['username']))
            for d in ob1:
                print(c := d.id)
                C=d.email
                ob2 = Selectoptions.objects.filter(user_id=c)

            for i in ob2:
                I = i.incr
            count=I
            if 1 <= int(I) <= 3:
                        uqk = request.POST['unique_key']
                        if fm.is_valid():
                                uname= fm.cleaned_data['username']
                                upass= fm.cleaned_data['password']
                                if uqk != i.unique_key:
                                    messages.error(request, 'Invalid UniqueKey, You are not an Authenticated User !',
                                                   extra_tags='incorrect')
                                    if str(I) != str(3):
                                        messages.error(request,
                                                       'Your Attempt : ' + str(I) + ", " + "Now your only " + str(
                                                           3 - int(str(I))) +
                                                       " attempt left !")
                                    else:
                                        messages.error(request, 'Your Attempt : ' + str(I) + ", " + "No Attempt left !")

                                    ob1 = User.objects.filter(username=str(request.POST['username']))
                                    for d in ob1:
                                        print(c := d.id)
                                        ob2 = Selectoptions.objects.filter(user_id=c)
                                    print(current_local_time := datetime.now(pytz.timezone('Asia/Kolkata')))

                                    for i in ob2:
                                        print("i.incr :", I := i.incr)
                                        I = int(I) + 1
                                        x = Selectoptions(user_id=i.user_id, city_name=i.city_name, phone_no=i.phone_no,
                                                          unique_key=str(i.unique_key), incr=I,
                                                          date_time=str(current_local_time),combKey=1,
                                                          time_check=1
                                                          )
                                        x.save()

                                else:
                                    user = authenticate(username=uname, password=upass)

                                    if user is not None:
                                      login(request,user)
                                      ob1 = User.objects.filter(username=str(request.POST['username']))
                                      for d in ob1:
                                        print(c := d.id)
                                        ob2 = Selectoptions.objects.filter(user_id=c)
                                      print(current_local_time := datetime.now(pytz.timezone('Asia/Kolkata')))

                                      for i in ob2:
                                        print("i.incr :", I := i.incr)
                                        x = Selectoptions(user_id=i.user_id, city_name=i.city_name, phone_no=i.phone_no,
                                                          unique_key=str(i.unique_key), incr=I,
                                                          date_time=str(current_local_time),combKey=1,
                                                          time_check=1
                                                          )
                                        x.save()
                                      return HttpResponseRedirect('/profile/')

            else:
                messages.error(request,'Your Account has been Blocked as to Keep it Safe !')
                print(current_local_time := datetime.now(pytz.timezone('Asia/Kolkata')))

                import smtplib as s

                ob = s.SMTP("smtp.gmail.com", 587)
                ob.starttls()
                ob.login("SENDER MAIL", "SENDER PASS")
                subject = "Your SE-L Account is Blocked !"
                body = "Dear " + str(request.POST['username']) + " ! It Seems, someone is Trying to access your account." \
                " To protect, we have blocked your account. Don't worry you can access your profile after 1 Hr from the Time : "+str(current_local_time)+ \
                ". When Your Account is Unblocked, You Please change Your Password to prevent Further Unauthorised Access or Your Account blockage." + " [ from SE-LTeam,Thankyou :) ]"
                message = "Subject:{}\n\n{}".format(subject, body)
                print("message:", message)
                listofaddress = [C]
                ob.sendmail("SENDER PASS", listofaddress, message)
                ob.quit()
                print("message send successfully")


        else:
            return redirect('login', id=12)

      else:
            fm=Authenticate()
            gm=uniquekey()
            print('U_id:',U_id)
      return render(request,'enroll/userlogin.html',{'form':fm,'gorm':gm,'v':id})

  else:
      return HttpResponseRedirect('/profile/')


# view func. for Profile
def user_profile(request):

  if request.user.is_authenticated:
      x = User.objects.filter(username=str(request.user))
      for i in range(len(x)):
          C = Selectoptions.objects.filter(user_id=x[i].id)
      ff = 0
      if request.method =='POST':
        try:
             if request.POST['task'] == 'yes':
                     print("request.POST['task']:", request.POST['task'])
                     x = User.objects.filter(username=str(request.user))
                     for i in x:
                         ui_d = i.id
                     print("user ka id h :",ui_d)
                     y=weather_ackno.objects.filter(user_id=ui_d)
                     print(len(y))
                     for i in y:
                         i.messages_alert = 0
                         i.save()
                     ff = 1

        except:
          if request.POST['schedule_date'] != '':
                  sch_date=request.POST['schedule_date']
                  z = datetime.strptime(sch_date,'%Y-%m-%d')
                  current_local_time = datetime.now()
                  current_utc_time = datetime.utcnow()
                  local_timezone = tzlocal.get_localzone()
                  #Not to confuse here , this running perfectly because we are working with date.As date will be same in case of UTC or IST time,
                  #so we need not have to convert time into current_local_time = datetime.now( pytz.timezone('Asia/Kolkata'))
                  print("Current UTC Time to Local Time : ",
                        x := current_utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone))
                  x = x.strftime('%Y-%m-%d')
                  x = datetime.strptime(x, '%Y-%m-%d')
                  differen=z-x
                  hm = your_list(request.POST)
                  if hm.is_valid():
                        x = User.objects.filter(username=str(request.user))
                        for i in x:
                            print("i :",i.id)
                            break
                        h = hm.save(commit=False)
                        h.user_id = i.id
                        h.save()

                        messages.success(request,'You have Successfully Scheduled for '+str(hm.cleaned_data['schedule_items'])+' on '
                                         +str(hm.cleaned_data['schedule_date'])+' at '+str(hm.cleaned_data['schedule_time']))

                        hm = your_list()
                  else:
                      if hm['schedule_date'].errors:
                          messages.error(request, hm['schedule_date'].errors)
                      elif hm['schedule_items'].errors:
                         ''' messages.error(request, hm['schedule_items'].errors),This
                             gives error message that -> This field is  required.
                         '''
                         messages.error(request, "Hey ! :( Enter  Something in Scheduled item's Box ):")

                      elif hm['schedule_time'].errors:
                            if differen.total_seconds() > 0:
                              if not hm.is_valid():
                                  x=User.objects.get(username=str(request.user))
                                  ol = Scheduled(schedule_items=request.POST['schedule_items'],
                                        schedule_date=request.POST['schedule_date'],schedule_time=request.POST['schedule_time'],user_id=x.id)
                                  ol.save()
                            else:
                              messages.error(request, hm['schedule_time'].errors)

                  hm = your_list()

      else:
          hm = your_list()
      x = User.objects.filter(username=str(request.user))
      for i in x:
              i.id
              print("i.id:",i.id)
              print("type - i.id:",type(i.id))
              break

      xx = expired_scheduledList.objects.filter(user_id=i.id)

      data1 = Scheduled.objects.filter(user_id=i.id)
      data2 = data1.order_by('schedule_date')
      ############################################################################################################
      for_id_of_user = User.objects.filter(username=str(request.user))
      for i in for_id_of_user:
          user_id_of_user = i.id
      getting_weather_messages = weather_ackno.objects.filter(user_id=user_id_of_user)
      dictionary_to_show = {}
      MESSAG_ALERTNESS = 0
      MSA = 0
      for i in getting_weather_messages:
          MESSAG = i.messages
          breaking_MESSAG = MESSAG.split('`')
          print(breaking_MESSAG)
          AGAIN_breaking_MESSAG = breaking_MESSAG[1].split('.')
          z = datetime.strptime(AGAIN_breaking_MESSAG[0],'%Y-%m-%d %H:%M:%S')
          dictionary_to_show[breaking_MESSAG[0]]=z
          if int(i.messages_alert) == 1:
              MSA = MSA + 1
      if MSA > 0:
          messages_alert = 1
      else:
          messages_alert = 0

      print("dictionary_to_show:",dictionary_to_show)

      print("_"*50)
      xyle=len(dictionary_to_show)

      user_database = User.objects.filter(username=str(request.user))
      for i in user_database:
          usr_ka_id = i.id
      user_ka_data_at_database = weather_ackno.objects.filter(user_id=usr_ka_id)
      for i in user_ka_data_at_database:
            user_time_at_database = i.time_of_message
            let = user_time_at_database.split('.')
            user_ka_time_at_d = datetime.strptime(let[0], '%Y-%m-%d %H:%M:%S')
            currently = datetime.now(pytz.timezone('Asia/Kolkata'))
            curr = str(currently).split('.')
            currently = datetime.strptime(curr[0], '%Y-%m-%d %H:%M:%S')
            diff = currently - user_ka_time_at_d
            print("diff.totaldifference() : ", diff.total_seconds())
            if diff.total_seconds()/60 > 5:
                i.delete()

      if ff == 1:
          hm = your_list
      else:
          hm = your_list
      
      finding_pin_user = User.objects.get(username=request.user)
      PIN = Pin_Unpin.objects.filter(pin_ka_id=finding_pin_user.id)
      lis=[]
      for i in PIN:  
        if i.pin_permission == str(1):  
          lis.append(i.pin_id)
      print("lis : ",lis)

      len_PIN = len(lis)

      return render(request, 'enroll/profile.html',
                        {'name': request.user, 'horm': hm, 'data': data2, 'city_name': C,'xx':xx,'lx':len(xx)
                        ,'messages_len':xyle,'messages_in':dictionary_to_show,'message_alert':messages_alert,'pin_d':lis,'len_PIN':len_PIN})

  else:
    return HttpResponseRedirect('/login/11/')


# view func. for Change Password with  Old Password
def user_password(request):
 #if request.user.is_authenticated:
  if request.method =="POST":
    fm = PasswordChangeForm(user=request.user,data=request.POST)
    if fm.is_valid():
      fm.save()
      update_session_auth_hash(request,fm.user)
      messages.success(request,'Password Changed Successfully')
      return HttpResponseRedirect('/profile/')
  else:
    fm = PasswordChangeForm(user=request.user)
  return render(request,'enroll/changepass.html')
# else:
 #  return HttpResponseRedirect('/login/')

def user_password1(request):## view func. for Change Password without  Old Password
 if request.user.is_authenticated:
  if request.method =="POST":
    fm = Setpassword(user=request.user,data=request.POST)
    if fm.is_valid():
      fm.save()
      update_session_auth_hash(request,fm.user)
      messages.success(request,'Password Changed Successfully')

  else:
    fm = Setpassword(user=request.user)
  return render(request,'enroll/changepass1.html',{'uorm':fm})
 else:
   return HttpResponseRedirect('/login/')


def update_data(request,id):
    if request.method =='POST':
      sch_date = request.POST['schedule_date']
      z = datetime.strptime(sch_date, '%Y-%m-%d')
      current_local_time = datetime.now()
      current_utc_time = datetime.utcnow()
      local_timezone = tzlocal.get_localzone()
      print("Current UTC Time to Local Time : ",
            x := current_utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone))
      x = x.strftime('%Y-%m-%d')
      x = datetime.strptime(x, '%Y-%m-%d')
      differen = z - x
      pi = Scheduled.objects.get(id=id)
      sch_date = request.POST['schedule_date']
      fm = your_list(request.POST,instance=pi)
      if fm.is_valid():
        fm.save()
        messages.success(request, "Scheduled Data Updated Successfully !" )
      else:
          if fm['schedule_items'].errors:
              # messages.error(request, hm['schedule_items'].errors),This
              #    gives error message that -> This field is  required.

              messages.error(request, "Hey ! :( Enter  Something in Scheduled item's Box ):")


          elif fm['schedule_date'].errors:
              messages.error(request, fm['schedule_date'].errors)

          #elif fm['schedule_time'].errors:
           #   messages.error(request, fm['schedule_time'].errors)

          elif fm['schedule_time'].errors:
              if differen.total_seconds() > 0:
                  if not fm.is_valid():
                      x = User.objects.get(username=str(request.user))
                      ol = Scheduled(schedule_items=request.POST['schedule_items'],
                                     schedule_date=request.POST['schedule_date'],
                                     schedule_time=request.POST['schedule_time'], id=id,user_id=x.id)
                      ol.save()
                      messages.success(request, "Scheduled Data Updated Successfully !")

              else:
                  messages.error(request, fm['schedule_time'].errors)


    else:
      pi = Scheduled.objects.get(id=id)
      fm = your_list(instance=pi)
      print(fm)
    return render(request,'enroll/updatestudent.html',{'form':fm})

#This func will delete
def delete_data(request,id):
  if request.method == 'POST':
    pi=Scheduled.objects.get(id=id)
    pi.delete()
  return HttpResponseRedirect('/profile/')

def export_data(request):
      if request.method == 'POST':
        file_format = request.POST['file-format']
        scheduled_resource=ScheduledResource()
        data1 = Scheduled.objects.filter(user__username=str(request.user))
        dataset = scheduled_resource.export(data1)
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv,content_type='test/CSV')
            response['Content-Disposition'] = 'attachment;filename="exported_data.csv"'
            return response
        if file_format == 'JSON':
            response = HttpResponse(dataset.json,content_type='application/json')
            response['Content-Disposition'] = 'attachment;filename="exported_data.json"'
            return response
        if file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls,content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename="exported_data.xls"'
            return response
        if file_format == 'YAML':
            response = HttpResponse(dataset.yaml,content_type='application/x-yaml')
            response['Content-Disposition'] = 'attachment;filename="exported_data.yaml"'
            return response
        if file_format == 'HTML':
          response = HttpResponse(dataset.html, content_type='text/html')
          response['Content-Disposition'] = 'attachment;filename="exported_data.html"'
          return response
        if file_format == 'Choose format ...':
            messages.warning(request, " Oye ! You Haven't Chosen a file.")
      return render(request,'enroll/export.html')

def importandsee(request):
    if request.method == 'POST':
        x=0
        file_format = request.POST['file-format']
        print("file format:",file_format)
        scheduled_resource = ScheduledResource()
        dataset = Dataset()
        new_schedule = request.FILES['importData']
        print("new_schedule:", new_schedule)
        print(type(new_schedule))
        imported_data=''
        if file_format == 'CSV':
               k=str(new_schedule)
               print(k:=k.split("."))
               print("k[1]:",k[1])
               print("k[1].upper()",k[1].upper())
               fn=new_schedule
               print("fn:",fn)

               ff=file_format
               if k[1].upper()==file_format:
                   imported_data=dataset.load(new_schedule.read().decode('utf-8'),format='csv')
                   print("imported_data :",imported_data)
                   print(imported_data)
                   result = scheduled_resource.import_data(dataset,dry_run=True)
                   print("Result :",result)
               else:
                   messages.error(request,'Ensure that you Choose correct format.')

        elif file_format == 'JSON':
            k = str(new_schedule)
            print(k := k.split("."))
            print("k[1]:", k[1])
            print("k[1].upper()", k[1].upper())
            fn = new_schedule
            print("fn:", fn)

            ff = file_format
            if k[1].upper() == file_format:
               imported_data=dataset.load(new_schedule.read().decode('utf-8'),format='json')
               result = scheduled_resource.import_data(dataset,dry_run=True)
               print("imported_data JSON :",imported_data)
            else:
                messages.error(request, 'Ensure that you Choose correct format.')

        elif file_format == 'XLS (Excel)':
            k = str(new_schedule)
            print(k := k.split("."))
            print("k[1]:", k[1])
            print("k[1].upper()", k[1].upper())
            fn = new_schedule
            print("fn:", fn)

            ff = file_format
            e=ff[0]+ff[1]+ff[2]
            print("e:",e)
            if k[1].upper() == e:
               imported_data=dataset.load(new_schedule.read(),format='xls')
               result = scheduled_resource.import_data(dataset,dry_run=True)
               print("imported_data XLS :",imported_data)
            else:
                messages.error(request, 'Ensure that you Choose correct format.')

        elif file_format == 'YAML':
               x=1
               k = str(new_schedule)
               print(k := k.split("."))
               print("k[1]:", k[1])
               print("k[1].upper()", k[1].upper())
               fn = new_schedule
               print("fn:", fn)

               ff = file_format
               if k[1].upper() == file_format:
                   imported_data = dataset.load(new_schedule.read().decode('utf-8'), format='yaml')
                   result = scheduled_resource.import_data(dataset, dry_run=True)
                   # print("new_schedule.read().decode('utf-8'):",imported_data)
               else:
                   messages.error(request,'Ensure that you Choose correct format.')


        elif file_format=='Choose format ...':
                        messages.warning(request," Oye ! You Haven't Chosen a file format."  )
                        fn = ''
                        ff = ''




    else:
        imported_data=''
        x=0
        fn = ''
        ff = ''

    return render(request, 'enroll/import.html',{'imported':imported_data,'x':x,
                    'fn':fn,'ff':ff})

def update_city(request,id):#Update your City

    if request.method =='POST':
          pi = Selectoptions.objects.get(user_id=id)
          fm = select(request.POST,instance=pi)
          fm.fields['phone_no'].disabled=True
          if fm.is_valid():
            fm.save()
            messages.success(request,"City & PhoneNo. Updated Successfully")

    else:
          pi = Selectoptions.objects.get(user_id=id)
          fm = select(instance=pi)
          fm.fields['phone_no'].disabled = True
          print(fm)

    return render(request,'enroll/City Update.html',{'corm':fm})


def sending_email(request):
    if request.method=='POST':

        print(request.POST)
        fm=Sendingmail(request.POST)
        #new_schedule = request.FILES['importData']
        #print('new_schedule:',new_schedule)
        #print('type(new_schedule):',type(new_schedule))
        #print('type(new_schedule):',type(str(new_schedule)))


        if fm.is_valid():
            print(fm)
            sed = fm.cleaned_data['Sender_Email_id']
            spwd = fm.cleaned_data['Password']
            red = fm.cleaned_data['Receiver_Email_id']
            subject=fm.cleaned_data['Subject']
            body=fm.cleaned_data['Body']
            #print("attachment:",request.FILES['importData'])
            print("attachment-input:",request.POST['file-location'])
            x=request.POST['file-location']


            #attachment=request.FILES['importData']
            '''
            import smtplib as s
            ob = s.SMTP("smtp.gmail.com", 587)
            ob.starttls()
            print("started . . .")
            ob.login(str(sed),str(spwd))#
            print("wait")
            subject = subject
            body = body
            message = "Subject:{}\n\n{}".format(subject, body)
            print("Message :", message)

            listofaddress = [str(red)]
            ob.sendmail(str(sed), listofaddress, message,attachment)
            print("Message Send Successfully")
            ob.quit()
            messages.success(request, 'Mail Send Successfully !')

            '''
            #fm = Sendingmail()

            #new_schedule = request.FILES['importData']

            #Raju's Email sending code -
            #try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from email.mime.base import MIMEBase
            from email import encoders

            email_user = sed
            email_password = spwd
            email_send = red

            subject = subject

            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_send
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            #filename = new_schedule

            filename = str(x)
            if filename!="":
                g = str(x)
                g = g.split(".")
                print("g:", g)
                gn = '.' + g[1]
                gn = 'Attachment' + gn
                print("gn:", gn)
                print("type gn:", type(gn))

                print("hhhhhhh")

                attachment = open(filename,'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= " + gn)
                msg.attach(part)
                text = msg.as_string()

            else:
                text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_password)

            server.sendmail(email_user, email_send, text)
            server.quit()
            messages.success(request,'Mail send Successfully !')

            #except:
            #    messages.error(request,'Ooh . . Try Again, File path / Password may be Incorrect !')

        else:
            messages.error(request,'Some error occured')

    else:
        fm = Sendingmail()

    return render(request, 'enroll/email.html', {'form': fm})

# view func. for Logout
def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/login/1/')


def AboutMe(request):
    return render(request, 'enroll/abc.html')

def scrape(request):
   if request.user.is_authenticated:
      if request.method=="POST":
          pi = User.objects.get(username=request.user)
          city = Selectoptions.objects.get(user_id=pi.id)
          sm=searchquery(request.POST)
          if sm.is_valid():
             place = sm.cleaned_data['place']
             search = sm.cleaned_data['search']
             print(place,search)
             print(type(place))
             print(type(search))

             import urllib
             from bs4 import BeautifulSoup
             import requests
             T = search
             place = place

             place = place.split(" ")
             p1=''
             for i in place:
                 p1=p1+i


             T = T.split(" ")
             T1 = ''
             for i in T:
                 T1 = T1 + i
             cit = request.POST['cityname']
             if " " not in cit:
                 print(cit)
                 url = 'https://www.google.com/search?safe=strict&rlz=1C1PRFI_enIN903IN903&biw=1017&bih=730&tbm=lcl&ei=LJuNX-XVKpOC4-EPgbuY-Ag&q=' + 'list' + 'of' + T1 + 'in' + p1 + cit
             else:
                 cit=cit.split(" ")
                 st=''
                 for i in cit:
                     st=st+i

                 url = 'https://www.google.com/search?safe=strict&rlz=1C1PRFI_enIN903IN903&biw=1017&bih=730&tbm=lcl&ei=LJuNX-XVKpOC4-EPgbuY-Ag&q=' + 'list' + 'of' + T1 + 'in' + p1 + st

             headers = {
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
             req = urllib.request.Request(url=url, headers=headers)
             page = urllib.request.urlopen(req).read()
             page_soup = BeautifulSoup(page, 'html.parser')
             containers = page_soup.find_all('div', attrs={'class': 'VkpGBb'})
             print("containers :: ",containers)
             c = 0
             list = []

             for container in containers:
                 try:
                     shop_name = container.findAll('div', {'class': 'cXedhc uQ4NLd'})
                     print("shop_name ::",shop_name)
                     list.append([])
                     # Logic for Shop Name
                     XX = shop_name[0].find('div', {'class': 'dbg0pd'})
                     print("XX ::",XX)
                     print("XX.stripped_strings ::",XX.stripped_strings)
                     for i in XX.stripped_strings:
                         print("XX.stripped_strings ::", i)
                     for i in XX.stripped_strings:
                         list[c].append(i)

                     # Logic for Other details of Shop
                     YY = shop_name[0].find('div', {'class': 'rllt__details'})
                     print("YY ::", YY)
                     print("YY.stripped_strings ::", YY.stripped_strings)

                     # print("  Type shop_name[0].findAll(('div',{'class':'rllt__details lqhpac'})):",type(shop_name[0].find('span',{'class':'rllt__details lqhpac'})))
                     for i in YY.stripped_strings:
                         list[c].append(i)
                     c = c + 1
                 except:
                     shop_name = container.findAll('div', {'class': 'cXedhc'})
                     list.append([])
                     # Logic for Shop Name
                     XX = shop_name[0].find('div', {'class': 'dbg0pd'})
                     for i in XX.stripped_strings:
                         list[c].append(i)

                     # Logic for Other details of Shop
                     YY = shop_name[0].find('span', {'class': 'rllt__details lqhpac'})
                     # print("  Type shop_name[0].findAll(('div',{'class':'rllt__details lqhpac'})):",type(shop_name[0].find('span',{'class':'rllt__details lqhpac'})))
                     for i in YY.stripped_strings:
                         list[c].append(i)

                     c = c + 1
             #list=[['Ayushman Nursing', 'Home', '4.0', '(14)', '· Hospital', 'Open now'], ['Aayushman', 'multispeciality hospital', '5.0', '(1)', '· Hospital', 'Open 24 hours'], ['CRU, Ranchi', 'Homoeopathy', 'No reviews · Hospital', 'Bank Of India Building, Kanke Block Chowk Rd'], ['Oplus Heart Center', '4.6', '(22)', '· Heart hospital', 'Kanke, Jharkhand', 'Open 24 hours', '·', '062048 00421'], ['Yashi Surgical &', 'Children Hospital', '5.0', '(13)', '· Hospital', 'Kanke, Jharkhand', 'Open 24 hours'], ['davis hospital', 'No reviews · Hospital', 'state, Jharkhand'], ['Bethel Mission', 'Hospital', 'No reviews · Hospital', 'Ranchi, Jharkhand', '080923 95001'], ['Chandra Hospital', '3.2', '(10)', '· Hospital', 'Ranchi, Jharkhand', 'Open 24 hours'], ['Atharva Care', '5.0', '(6)', '· Hospital', 'Ranchi, Jharkhand', 'Open 24 hours'], ['Shristi Hospital &', 'Research Centre', '5.0', '(3)', '· Hospital', 'Ranchi, Jharkhand'], ['DAVIS INSTITUTE OF', 'NEUROPSYCHIATRY', '3.8', '(57)', '· Hospital', 'Ranchi, Jharkhand', 'Open ⋅ Closes 5PM', '·', '0651 245 1112'], ['Vet hospital', 'No reviews · Hospital', 'Ranchi, Jharkhand'], ['Anand Nursing Home', '3.0', '(2)', '· Hospital', 'Ranchi, Jharkhand', 'Open ⋅ Closes 9PM', '·', '093347 23092'], ['THE ADVANCE', 'PATHOLOGY & IMAG CENT', 'No reviews · Hospital', 'Ranchi, Jharkhand'], ['davis family trust', '4.0', '(1)', '· Hospital', 'Kanke, Jharkhand'], ['Sanat heart centre', 'No reviews · Hospital', 'Ranchi, Jharkhand'], ['C.H.C Kanke Hospital', '3.8', '(5)', '· Hospital', 'Kanke, Jharkhand', 'Open 24 hours'], ['SS Raju Ward (DAC)', '5.0', '(1)', '· Hospital', 'Ranchi, Jharkhand'], ['Hill View Hospital &', 'Research Center', '4.0', '(221)', '· General hospital', 'Ranchi, Jharkhand', 'Open 24 hours', '·', '094311 04724'], ['Department of', 'Radiology, CIP', 'No reviews · Hospital', 'Ranchi, Jharkhand'],[],[],[],[],[],[],[],[],[],[]]
             print("list : ",list)
             print("len list : ",len(list))

             mist=[]
             for i in list:
               if len(i)!=0:
                 mist.append(i)
             print('mist : ',mist)
             l=len(mist)
             if len(list)==0:
                 messages.error(request,' No Searched Result Found ! ')



      else:
        pi = User.objects.get(username=request.user)
        city=Selectoptions.objects.get(user_id=pi.id)

        sm=searchquery()
        print(pi)
        mist,l,search='','',''


      return render(request, 'enroll/scrape.html',{'sm':sm,'city':city.city_name,'list':mist,'l':l,'search':search})

   else:
    return HttpResponseRedirect('/login/')


def r_no_generation(request):
    if request.method =="POST":
        try:
         if request.POST['r']=="on":
          print(request.POST['r'])
          print(request.POST['U_n'])
          print(type(request.POST['U_n']))
          print(request.POST['p_no'])
          x=User.objects.filter(username=request.POST['U_n'])
          print("x:",x)
          c=0
          for i in x:
              c=c+1
          print("length of query set : ",c)
          if c!=0:
              for i in x:
                  X = i.email
                  s = Selectoptions.objects.filter(user_id=i.id)
              print("X",X)
              for i in s:
                  print("i.phone_no:",i.phone_no)
                  if i.phone_no == "+91"+request.POST['p_no']:
                      import secrets
                      import string
                      res = ''.join(
                          secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(5))
                      print(res)
                      print(current_local_time := datetime.now(pytz.timezone('Asia/Kolkata')))

                      V=Selectoptions(user_id=i.user_id,city_name=i.city_name, phone_no=i.phone_no,
                                        unique_key=str(i.unique_key), incr=i.incr,
                                        date_time=i.date_time,combKey=str(res),time_check=str(current_local_time)
                                        )

                      V.save()


                      import smtplib as s

                      ob = s.SMTP("smtp.gmail.com", 587)
                      ob.starttls()
                      ob.login("SENDER MAIL", "SENDER PASS")
                      subject = "Your CombKey"
                      body = "Dear " + request.POST['U_n'] +" Your Combkey is " +str(res)+" & is Valid only for 5 mins. "+ " [ from SE-L Team, Thankyou :) ]"
                      message = "Subject:{}\n\n{}".format(subject, body)
                      print("message:", message)
                      listofaddress = [X]
                      ob.sendmail("SENDER MAIL", listofaddress, message)
                      ob.quit()
                      print("message send successfully")

                  else:
                     messages.error(request,'Invalid Username/PhoneNo.')
          else:
              messages.error(request, 'Invalid Username/PhoneNo.')



        except:
           try:
                if request.POST['r'] == " ":
                     pass

           except:

               x = User.objects.filter(username=request.POST['U_n'])
               print("x:", x)
               c = 0
               for i in x:
                   c = c + 1
               print("length of query set : ", c)
               if c != 0:
                   for i in x:
                       s = Selectoptions.objects.filter(user_id=i.id)

                   for i in s:

                       print(current_local_time := datetime.now(pytz.timezone('Asia/Kolkata')))
                       print(type(current_local_time))
                       w = i.time_check.split("+")
                       y = str(current_local_time).split("+")

                       print("datetime.strptime('%Y-%m-%d %H:%M:%S.%f')",
                             datetime.strptime(w[0], '%Y-%m-%d %H:%M:%S.%f'))
                       print(type(datetime.strptime(w[0], '%Y-%m-%d %H:%M:%S.%f')))
                       print("|i.date_time|", w[0])
                       diff = datetime.strptime(y[0], '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(w[0],
                                                                                                  '%Y-%m-%d %H:%M:%S.%f')
                       print("|diff|", diff)
                       print("|diff.total_seconds()|", diff.total_seconds())
                       print("|diff.total_seconds()/60|", diff.total_seconds() / 60)
                       print("|diff.total_seconds()/3600|", diff.total_seconds() / 3600)
                       if diff.total_seconds() <= 300:
                           if str(request.POST['r_no']) == i.combKey:
                              return redirect('ed_uq',i.user_id)
                           else:
                              messages.error(request, "Please Check Radio by Clicking on it. / Comb.Key Doesn't Matched !")
                       else:
                           messages.error(request, "Timeout, You didn't Fill ' IN ' as Stated !")

               else:
                   messages.error(request, 'Invalid Username/PhoneNo.')

    return render(request,'enroll/rnog.html')

def e_u_key(request,id):
    if request.method=='POST':
        x=User.objects.filter(id=id)
        gm=uniquekey(request.POST)
        for i in x:
            if i.username == request.POST['Username']:
                s=Selectoptions.objects.filter(user_id=id)

                for j in s:
                   if gm.is_valid():
                        x = Selectoptions(user_id=j.user_id, city_name=j.city_name, phone_no=j.phone_no,
                                      unique_key=str(gm.cleaned_data['unique_key']), incr=1, date_time=1, combKey=1,
                                      time_check=1)
                        x.save()
                        return redirect('login',12)
                   else:
                       print("Not Valid")
                       if gm['unique_key'].errors:
                           messages.error(request, gm['unique_key'].errors)
            else:
                messages.error(request,'Hey, Enter Your Username & not of Any one else !')

    else:
        gm = uniquekey()
        print(id)
    return render(request,'enroll/euk.html',{'form':gm})