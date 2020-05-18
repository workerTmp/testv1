#!/usr/bin/python3
from github import Github
import os,sys
from itertools import islice
from datetime import date
import shutil
import pandas as pd
import csv




def check_env(end_file,folder_name):

    file_name="noname"
    for file in os.listdir(folder_name):
        if file.endswith(end_file):
            file_name=file
    if file_name == "noname":
        print(end_file+" file not found")
        sys.exit()
    file_name=os.path.splitext(file_name)[0]
    return file_name
def down_git(lname,pname,rname):
    foldname = "retdec"
    if os.path.exists(foldname):
        shutil.rmtree(foldname)
    if pname == "nonono":
        os.system("git clone https://github.com/"+lname+"/"+rname+".git "+foldname)
    else:
        os.system("git clone https://"+lname+":"+pname+"@github.com/"+lname+"/"+rname+".git "+foldname)

def down_v1(lname,pname,rname,upname):
    if pname == "nonono":
        g = Github() #may be block if more 60 
    else:
        g = Github(lname,pname)
    nameV="VN" #veronica number
               #VN.c1c aslkdjfkasjdf
    nameVr="VR" #verinica raw 
                #VR.c1c filename;
    nameFF="FFD" #find function declaration 
                #FFD namefunc namefile;
                #-FF namefunc namefile param;
    nameFC="FC" #find call 
                #FCF namefunc namefile;
    nameFL="FLI" #find loop or if or on param (ВОЗМОЖНО НЕ ПОЛНОЕ СОВПАДЕНИЕ...)
                #FCF param namefile;
    nameFFP = "FFP"       
    nameGOW="GOW"
    repo = g.get_repo(lname+"/"+rname)
    issop = repo.get_issues(state='open')
    down_git(lname,pname,rname)
    for i in issop:
        print(i.title)
        if nameGOW in i.title:
            continue
        if nameFF in i.title:
            nfile =i.title.split(";")[0].split(" ")[-1]
            funame =i.title.split(";")[0].split(" ")[-2]
            df = pd.read_csv("retdec/outsee/"+nfile,sep='_;_')
            srpath=df.loc[df['func'].isin([funame])][['src_path','colum_start','colum_end']]
            
            #srpath=df.loc[df['func'].isin([funame])]['src_path'].unique()[0]
            #i1path=df.loc[df['func'].isin([funame])]['colum_start'].unique()[0]
            #i2path=df.loc[df['func'].isin([funame])]['colum_end'].unique()[0]
            #if "retdec" in srpath:
            sp = srpath['src_path']
            cn = srpath['colum_start']
            cne = srpath['colum_end']
            spar=[]
            for ii in sp:
                spar.append(ii)
            cnar=[]
            for ii in cn:
                cnar.append(ii)
            cnare=[]
            for ii in cne:
                cnare.append(ii)
            if len(spar)>0:
                wout="FunDic "+funame+"\n\n"
                for ii in range(len(cnar)):
                    if "retdec" not in spar[ii]:
                        continue
                    filpath=spar[ii].split("retdec")[1]
                    i1=cnar[ii]
                    i1= int(i1)
                    if i1 >5:
                        i1 = i1-5
                    else:
                        i1=0
                    i2=cnare[ii]
                    
                    i2=int(i2)
                    wout=wout+"\n\n"+filpath+":"+str(i1)+"::"+str(i2)
                    wout=wout+"\n"+"```cpp\n"
                    with open("retdec"+filpath,'r') as lines:
                        for line in islice(lines, i1,i2):
                            wout = wout+line
                    wout=wout+"```"
            else:
                wout="\nNO DATA\n"
            today = date.today()
            d1 = today.strftime("%d.%m.%Y")
            i.edit(title=nameGOW+d1+"_"+i.title,body=i.body+wout)         
        elif nameFL in i.title:
            nfile =i.title.split(";")[0].split(" ")[-1]
            parmt =i.title.split(nameFL)[1].split(nfile)[0]
            parmt=parmt[1:-1]
            parmt=parmt.replace("...",",")
            #print(parmt)

            df = pd.read_csv("retdec/outsee/"+nfile,sep='_;_')
            
            srpath=df.loc[df['param'].isin([parmt])][['src_path','colum_start','colum_end']]
            sp = srpath['src_path']
            cn = srpath['colum_start']
            cne = srpath['colum_end']
            spar=[]
            for ii in sp:
                spar.append(ii)
            cnar=[]
            for ii in cn:
                cnar.append(ii)
            cnare=[]
            for ii in cne:
                cnare.append(ii)
            if len(spar)>0:
                wout="LIST WHEAR in "+parmt+"\n\n"
                for ii in range(len(cnar)):
                    if "retdec" not in spar[ii]:
                        continue
                    filpath=spar[ii].split("retdec")[1]
                    i1=cnar[ii]
                    i1=int(i1)
                    if i1 >5:
                        i1 = i1-5
                    else:
                        i1=0
                    i2=cnare[ii]
                    i2=int(i2)
                    wout=wout+"\n\n"+filpath+":"+str(i1)+"::"+str(i2)
                    wout=wout+"\n"+"```cpp\n"
                    with open("retdec"+filpath,'r') as lines:
                        for line in islice(lines, i1,i2):
                            wout = wout+line
                    wout=wout+"```"
            else:
                wout="\n NO DATA \n"
            today = date.today()
            d1 = today.strftime("%d.%m.%Y")
            i.edit(title=nameGOW+d1+"_"+i.title,body=i.body+"\n"+wout)  
        elif nameFC in i.title:
            nfile =i.title.split(";")[0].split(" ")[-1]
            funame =i.title.split(";")[0].split(" ")[-2]
            df = pd.read_csv("retdec/outsee/"+nfile,sep='_;_')
            srpath=df.loc[df['func'].isin([funame])][['src_path','colum_num']]
            #print(srpath)
            sp = srpath['src_path']
            cn = srpath['colum_num']
            spar=[]
            for ii in sp:
                spar.append(ii)
            cnar=[]
            for ii in cn:
                cnar.append(ii)
            if len(spar)>0:    
                wout="LIST CALLs in "+funame+"\n"
                wout=wout+i.title.split(";")[1]+"\n"
                for ii in range(len(cnar)):
                    if "retdec" not in spar[ii]:
                        continue
                    filpath=spar[ii].split("retdec")[1]
                    #print(spar[ii])
                    #print(cnar[ii])
                    i1=cnar[ii]
                    i1=int(i1)
                    if i1>5:
                        i1=i1-5
                    else:
                        i1=0
                    i2=cnar[ii]
                    i2=int(i2)+5
                    wout=wout+"\n\n"+filpath+":"+str(cnar[ii])
                    wout=wout+"\n"+"```cpp\n"
                    
                    
                    with open("retdec"+filpath,'r') as lines:
#todo if i2 end more error see
                        for line in islice(lines, i1,i2):
                            wout = wout+line
                    wout=wout+"```"
            else:
                wout="\nNO DATA\n"
            today = date.today()
            d1 = today.strftime("%d.%m.%Y")
            i.edit(title=nameGOW+d1+"_"+i.title,body=i.body+"\n"+wout)     
        elif nameFFP in i.title:
            nfile =i.title.split(";")[0].split(" ")[-1]
            parmt =i.title.split(nameFFP)[1].split(nfile)[0]
            parmt=parmt[1:-1]
            parmt=parmt.replace("...",",")
            #print(parmt)
            df = pd.read_csv("retdec/outsee/"+nfile,sep='_;_')
            srpath=df.loc[df['param'].isin([parmt])][['src_path','colum_num']]
            #print(srpath)
            sp = srpath['src_path']
            cn = srpath['colum_num']
            spar=[]
            for ii in sp:
                spar.append(ii)
            cnar=[]
            for ii in cn:
                cnar.append(ii)
            if len(spar)>0:    
                wout="LIST CALLs in "+parmt+"\n"
                wout=wout+i.title.split(";")[1]+"\n"
                for ii in range(len(cnar)):
                    if "retdec" not in spar[ii]:
                        continue
                    filpath=spar[ii].split("retdec")[1]
                    i1=cnar[ii]
                    i1=int(i1)
                    if i1>5:
                        i1=i1-5
                    else:
                        i1=0
                    i2=cnar[ii]
                    i2=int(i2)
                    wout=wout+"\n\n"+filpath+":"+str(cnar[ii])
                    wout=wout+"\n"+"```cpp\n"
                    
                    
                    with open("retdec"+filpath,'r') as lines:
                        for line in islice(lines, i1,i2):
                            wout = wout+line
                    wout=wout+"```"
            else:
                wout="\nNO DATA\n"
            today = date.today()
            d1 = today.strftime("%d.%m.%Y")
            i.edit(title=nameGOW+d1+"_"+i.title,body=i.body+"\n"+wout)     
        elif nameV in i.title:
            preline = ""
            lin = "nonono"
            for ll in i.body.split("\n"):
                if "#L" in ll:
                    lin = ll.split("#")[0]+"?raw=true"
                    i1 = int(ll.split("#")[1].split("L")[1].split("-")[0])
                    i2 = int(ll.split("#")[1].split("L")[2])
                    srcname = ll.split('/')[-1].split("#")[0]
                    #ulname =  ll.split("blob")[0].split("/")[-3]
                    #urname =  ll.split("blob")[0].split("/")[-2]
                    preff =  ll.split("blob")[1].split("/")[1]
                    upath = ll.split(preff)[1].split("#")[0]
                else:
                    preline = preline + ll+"\n"
            if os.path.exists("hhh"):
                os.remove("hhh")
            if lin in "nonono":
                continue
            if os.path.exists("retdec"+upath):
                shutil.move("retdec"+upath, "hhh")    
            #os.system("wget -Ohhh "+lin)
            typecnc = i.title.split(" ")[0].split(nameV)[1]
            fname = lname+"_"+rname+"_"+srcname+"_"+str(i1)+"_"+str(i2)+typecnc
            f = open(fname,"w")
            f.write(preline)
            with open('hhh','r') as lines:
                for line in islice(lines, i1-1,i2):
                    f.write(line)
            f.close()
            if os.path.exists(fname):
                
                file7z = fname + ".7z"  
                if os.path.exists(path_to_out+file7z):
                    os.remove(fname)
                    continue
                else:
                    cmdzip="7z a -mhe=on "+file7z+" "+fname+" -p"+upname
                    os.system(cmdzip)
                    os.remove(fname)
                    shutil.move(file7z, path_to_out+file7z)
                    today = date.today()
                    d1 = today.strftime("%d.%m.%Y")
                    i.edit(title=nameGOW+d1+"_"+i.title)
        elif nameVr in i.title:
            preline = ""
            for ll in i.body.split("\n"):
                preline = preline + ll+"\n"
            if os.path.exists("hhh"):
                os.remove("hhh")
            typecnc = i.title.split(" ")[0].split(nameVr)[1]
            fyname = i.title.split(";")[0].split(" ")[1]
            today = date.today()
            fname = lname+"_"+rname+"_"+fyname+"_"+today.strftime("%d.%m.%Y")+typecnc
            f = open(fname,"w")
            f.write(preline)
            f.close()
            if os.path.exists(fname):
                file7z = fname + ".7z"  
                if os.path.exists(path_to_out+file7z):
                    os.remove(fname)
                    continue
                else:
                    cmdzip="7z a -mhe=on "+file7z+" "+fname+" -p"+upname
                    os.system(cmdzip)
                    os.remove(fname)
                    shutil.move(file7z, path_to_out+file7z)
                    today = date.today()
                    d1 = today.strftime("%d.%m.%Y")
                    i.edit(title=nameGOW+d1+"_"+i.title)

def save_repo(lname,pname,rname,ptout):
    os.system("git remote remove origin")
    os.system("git config --global user.name \""+lname+"\"")
    os.system("git config --global user.email "+lname+"@github.com")
    os.system("git remote add -f origin https://"+lname+":"+pname+"@github.com/"+lname+"/"+rname+".git")
    os.system("git checkout master")
    os.system("git add "+ptout)
    os.system("git commit -m \"create 7z\"")
    os.system("git push origin master")


try:
    path_to_in = sys.argv[1]
    path_to_insec = sys.argv[2]
    path_to_out = sys.argv[3]
except IndexError:
    print("Usage: path/in path/insec path/to/out")
    sys.exit(1)


print("check env")    
unzip_name=check_env(".unzip",path_to_insec)
retpo_name=check_env(".repo",path_to_insec)
logi_name=check_env(".login",path_to_insec)
pass_name=check_env(".pass",path_to_insec)
#fretpo_name=check_env(".frepo",path_to_in)
flogi_name=check_env(".flogin",path_to_insec)
fpass_name=check_env(".fpass",path_to_insec)


if os.path.exists(path_to_in+"list.v1repolist"):
    with open(path_to_in+"list.v1repolist") as f:
        content = f.readlines()
    for i in content:
        rname = i.split('/')[-1].split(".git")[0]
        lname = i.split('/')[-2]
        if lname== flogi_name:
            pname = fpass_name
        else:
            pname="nonono"
        down_v1(lname,pname,rname,unzip_name)
        save_repo(logi_name,pass_name,retpo_name,path_to_out)
else:
    print("NO LIST.v1repolist FILE")
    sys.exit()
#os.remove(path_to_in+"list.v1repolist")
