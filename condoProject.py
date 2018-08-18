import re
import os
import requests


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
    print "Createing " + i +" directory."
    print "Collecting MLS#" + i + " images." 
#Create a directory with the MLS number and download the first image named exactly
#as the MLS itself Cddddddd.jpg
    os.mkdir(i)
    f = open('%s/%s.jpg'%(i,i),'wb')
    f.write(requests.get(Formula%("1",i[5:],i)).content)
    f.close()
#Counter starts from two because (see example link above)
    counter = 2

#This breaker was very helpful if there is a break in the images sequence
#Sometimes images was e.g. (Cddddddd_3 then Cddddddd_5)
#The script search for Cddddddd_4 and then for Cddddddd_5 more photos and break
#in the second as breaker value become True
    breaker = False
    while counter < 21:
        image = requests.get(Formula%(counter,i[5:],i+"_"+str(counter)))
        if image.status_code == 200:
            f = open('%s/%s.jpg'%(i,i+"_"+str(counter)),'wb')
            try:
                img = requests.get(Formula%(counter,i[5:],i+"_"+str(counter)))
                f.write(img.content)
                f.close()
                counter = counter + 1
            except ChunkedEncodingError:
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
    print "Found " + str(len([name for name in os.listdir(i)])) + " images.\n"
        
    
    
    

