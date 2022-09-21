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
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image


with yaspin(Spinners.arc, text="Generating...", color="blue") as sp:

    def dir_path(string):
        if os.path.isdir(string):
            return string
        else:
            raise NotADirectoryError(string)

    ext = ['.jpg','.jpeg','.png']
    def file_img(string):
        if string.endswith(tuple(ext)):
            return string
        else:
            raise FileNotFoundError(string)

    def list_to_string(string):
        str1 = " "
        return (str1.join(string))


    def string_to_list(string):
        li = list(string.split(","))
        return li

    def dataFrame_to_dict(df):
        df = df.set_index('Words').to_dict()['Count']
        return df


    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', help="Type a folder directory containing html files with messages", type=dir_path)
    parser.add_argument('--exclude', '-e', help="Type which words or letters to exclude separated with a comma", type= str)
    parser.add_argument('--image', '-i', help="Type png/jpg file path to create a mask", type=file_img)



    #Assign parameters to variables and check if --exclude exists
    args = parser.parse_args()

    path = args.path
    exclude_para = args.exclude
    png_para = args.image

    if args.exclude is not None:
        parameters_list = string_to_list(exclude_para)


    files_to_combine = list(pathlib.Path(path).glob('*.html'))

    if(os.path.exists(path + "\combined.html")==False):
        with open(path + "\combined.html", "wb") as outfile:
            for f in files_to_combine:
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

    message_with_div = soup.find_all("div", {"class":"_2ph_ _a6-p"})
    message_extracted = [r.text.strip() for r in message_with_div]


    messages = list_to_string(message_extracted)
    messages = re.sub(r"\S*https?:\S*", "", messages)   #Remove links from string

    sp.write("Clensing the div's     -  DONE [3/6]")

    
    #with open(path + r'\test.txt', 'w',encoding="utf8") as f:
    #    f.write(texts2)


    def remove_punctation(st):
        for c in string.punctuation:
            st = st.replace('?',' ').replace('!',' ').replace(',',' ').replace('.',' ').replace('"',' ').replace('/',' ')#.replace(':',' ').replace('(',' ').replace(')',' ')
            return st

    def lower_split(st):
        st = st.lower()
        return st

    def clean_message_string(st):
        st = unidecode(st)
        remove_punctation(st)
        lower_split(st)
        return st

    # Creating an array to fill with the normalized text
    dump = []
    messagesCleansed = clean_message_string(messages)

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

    if args.image is not None:
        if png_para.endswith('.png'):
            foregroud = Image.open(png_para)
            backgroud = Image.new("RGBA", foregroud.size, "WHITE")
            backgroud.paste(foregroud, (0, 0), foregroud)
            mask_img = np.array(backgroud)
        else:
            mask_img = np.array(Image.open(png_para))

    #Generate Word Cloud
    wc = WordCloud(background_color="white", width=1400, height=1000, max_words=300,mask=mask_img,repeat=True,min_font_size=4).generate_from_frequencies(dataFrame_to_dict(df))


    # store to file
    wc.to_file(path + "\WordCloud.png")

    # Remove generated, combined html file
    os.remove(path+"\combined.html")



with yaspin(Spinners.arc, text=" ", color="blue") as spp:
    spp.ok("File generated! [6/6]")


# Display the generated image:
#plt.imshow(wc, interpolation='bilinear')
#plt.axis("off")
#plt.figure()
#plt.imshow(mask_img, cmap=plt.cm.gray, interpolation='bilinear')
#plt.axis("off")
#plt.show()