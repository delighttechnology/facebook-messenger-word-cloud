from bs4 import BeautifulSoup           #pip install beautifulsoup4
from unidecode import unidecode         #pip install Unidecode
import sys, os, pathlib, argparse       #pip install argparse
import string
import re                               #pip install regex
import numpy as np                      #pip install numpy
import pandas as pd                     #pip install pandas
import time
from yaspin import yaspin               #pip install --upgrade yaspin
from yaspin.spinners import Spinners


with yaspin(Spinners.arc, text="Generating...", color="blue") as sp:

    def dirPath(string):
        if os.path.isdir(string):
            return string
        else:
            raise NotADirectoryError(string)

    def listToString(string):
        str1 = " "
        return (str1.join(string))


    def stringToList(string):
        li = list(string.split(","))
        return li


    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', help="Type a folder directory containing html files with messages", type=dirPath)
    parser.add_argument('--exclude', '-e', help="Type which words or letters to exclude separated with a comma", type= str)


    #Assign parameters to variables and check if --exclude exists
    args = parser.parse_args()
    path = args.path
    exclude_parameters = args.exclude
    if args.exclude is not None:
        parameters_list = stringToList(exclude_parameters)


    filesToCombine = list(pathlib.Path(path).glob('*.html'))

    if(os.path.exists(path + "\combined.html")==False):                 #do usuniecia jak wgrane na github
        with open(path + "\combined.html", "wb") as outfile:
            for f in filesToCombine:
                with open(f, "rb") as infile:
                    outfile.write(infile.read())


    sp.write("Combining html files   -  DONE [1/6]")



    with open(path + "\combined.html",encoding="utf8") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    for div in soup.find_all("ul", {'class':'_a6-q'}):
        div.decompose()

    for div in soup.find_all("video", {'class':'_a6_o _3-96'}):     
        div.decompose()    

    for div in soup.findAll("audio", attrs={'class': None}):
        div.decompose()

    for div in soup.find_all(text=re.compile(' IP: ')):
        div.parent.decompose()

    sp.write("Decomposing div's      -  DONE [2/6]")

    messageWithDiv = soup.find_all("div", {"class":"_2ph_ _a6-p"})
    messageExtracted = [r.text.strip() for r in messageWithDiv]


    messages = listToString(messageExtracted)
    messages = re.sub(r"\S*https?:\S*", "", messages)   #Remove links from string

    sp.write("Clensing the div's     -  DONE [3/6]")

    
    #with open(path + r'\test.txt', 'w',encoding="utf8") as f:
    #    f.write(texts2)


    def removePunctation(st):
        for c in string.punctuation:
            st = st.replace('?',' ').replace('!',' ').replace(',',' ').replace('.',' ').replace('"',' ').replace('/',' ')#.replace(':',' ').replace('(',' ').replace(')',' ')
            return st

    def lowerSplit(st):
        st = st.lower()
        return st


    # Creating an array to fill with the normalized text
    dump = []
    messagesCleansed = unidecode(messages)             #Normalize text from łąćśżó to łacszo
    messagesCleansed = removePunctation(messagesCleansed)           
    messagesCleansed = lowerSplit(messagesCleansed)

    sp.write("Unidecode/Chars/Lower  -  DONE [4/6]")

    #with open(path + r'\test_2.txt', 'w',encoding="utf8") as f:
    #    f.write(new_text)

    # Fill an array with the list of cleansed words
    messagesCleansed= messagesCleansed.split()
    dump.extend(messagesCleansed)



    #Creating DataFrame with count of the words and splitted by columns "Words" and "Count"
    df = pd.value_counts(np.array(dump)).rename_axis('Words').reset_index(name='Count')


    sp.write("Data Frame created     -  DONE [5/6]")

    #Remove strage values
    df = df[df.Words.str.contains("target=|/>|alt=|<img|<br|<a|[0-9]+|[;][&]gt[;]|[:][&]gt[;]|-|[:][&]lt[;]|\r\n|\r|\n",regex=True)==False]

    #Remove values from parameter
    if args.exclude is not None:
        df = df[df.Words.isin(parameters_list) == False]


    # Printing values
    #pd.set_option('display.min_rows', 200)
    #pd.set_option('display.max_rows', 400)
    #print(df)


    # Save file
    df.to_csv(path + "\word_count.csv",index=False)

    # Remove generated, combined html file
    os.remove(path+"\combined.html")


with yaspin(Spinners.arc, text=" ", color="blue") as spp:
    spp.ok("File generated! [6/6]")
