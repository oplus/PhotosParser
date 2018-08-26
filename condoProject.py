import re
import os
import requests
import time
import random
    
#===========================================
# Below creates text file titled with      =
# MLS number containing string of the ad   =
#===========================================   
text = open("MLS.txt", "r+")
new_text = text.readlines()

#Spot indexes of the break point repeated before every post ("Links:\n")
indices = [i-1 for i, x in enumerate(new_text) if x =="Links:\n"]

del new_text[:indices[0]] #Delete the header at the begining

#Spot indexes of the break point again
indices = [i-1 for i, x in enumerate(new_text) if x =="Links:\n"]

#content = new_text[indices[0]:indices[1]]
#MLS = re.findall(r'C{1}[0-9]{7}', "".join(content))[0]

#Takes sliced string #search for MLS value #create a file with the MLS name
#Write the sliced string to the file
def creatorFunc(stri):
    MLS = re.findall(r'C{1}[0-9]{7}', "".join(stri))[0]
    os.mkdir(MLS)
    f = open("%s/%s.txt" %(MLS,MLS), "w")
    f.write("".join(stri))
    f.close()


for i, x in enumerate(indices):
    if i < len(indices)-1:
        section = new_text[indices[i]:indices[i+1]]
        creatorFunc(section)
    else:
        section = new_text[indices[i]:]
        creatorFunc(section)


#===========================================
# Below download photos and save to        =
# directory created and titled by MLS      =
#===========================================

#Opens and read the MLS.txt that iclude the pasted data
listingFile = open('MLS.txt', 'r')
listingFile = listingFile.read()

#Parse the pasted data and search for MLS numbers with regex Cddddddd
listMLS = re.findall(r'C{1}[0-9]{7}', listingFile)

print "MLS Listing =>>" + str(listMLS) + "\n"


#Example link for a photo using the MLS number parameter
Formula = "http://photos.v3.torontomls.net/Live/photos/FULL/%s/%s/%s.jpg"
#http://photos.v3.torontomls.net/Live/photos/FULL/1/210/C4220210.jpg

#Loop through MLS/s
for i in listMLS:
    delay = 3
    print "Createing " + i +" directory."
    print "Collecting MLS#" + i + " images."
    timeDelay = random.randrange(0, delay)
    time.sleep(timeDelay)
#Create a directory with the MLS number and download the first image named exactly
#as the MLS itself Cddddddd.jpg
    #os.mkdir(i) I deleted this because it is created already above
    f = open('%s/%s.jpg'%(i,i),'wb')
    try:
        f.write(requests.get(Formula%("1",i[5:],i)).content)
    except:
        print "There might be a mistake in this folder, please check manually."
        pass
    f.close()
#Counter starts from two because (see example link above)
    counter = 2

#This breaker was very helpful if there is a break in the images sequence
#Sometimes images was e.g. (Cddddddd_3 then Cddddddd_5)
#The script search for Cddddddd_4 and then for Cddddddd_5 more photos and break
#in the second as breaker value become True
    breaker = False
    while counter < 21: #if more photos increase this
        timeDelay = random.randrange(0, delay)
        time.sleep(timeDelay)
        image = requests.get(Formula%(counter,i[5:],i+"_"+str(counter)))
        if image.status_code == 200:
            f = open('%s/%s.jpg'%(i,i+"_"+str(counter)),'wb')
            try:
                img = requests.get(Formula%(counter,i[5:],i+"_"+str(counter)))
                f.write(img.content)
                f.close()
                counter = counter + 1
            except:
                print "There might be a mistake in this folder, please check manually."
                pass   
        else:
            counter = counter + 1
            if breaker:
                break
            else:
#If no images after two trials the loop breaks (new MLS is conducted)
                breaker = True

#List number of images found using os.listdir               
    print "Found " + str(len([name for name in os.listdir(i)])-1) + " images.\n"


       
