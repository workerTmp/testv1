import os

PathName=sys.argv[1]
lineForAr=" "

def allLibPath(textIncl):
    os.system("cd "+PathName+" &&find . -name \"*.o\" > tmpin")
    with open(PathName+"/tmpin") as f:
        for line in f:
            linetmp=" "+PathName+line.split("\n")[0]
            if not linetmp in textIncl:
                textIncl+=linetmp
    return textIncl

lineForAr=allLibPath(lineForAr)
os.system("cd "+PathName+" && ar rsc liball1.a "+lineForAr);
