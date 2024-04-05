import sys, os, pathlib, argparse       
import string, re                       #pip install regex
import numpy as np                      
import pandas as pd                     
from bs4 import BeautifulSoup           #pip install beautifulsoup4
from unidecode import unidecode         #pip install Unidecode
from wordcloud import WordCloud         #pip install wordcloud
from PIL import Image                   #pip install Pillow

#Verify if provided string is folder directory
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

#Verify if provided file has extension of .jpg, .jpeg or .png
ext = ['.jpg','.jpeg','.png']
def file_img(string):
    if string.endswith(tuple(ext)):
        return string
    else:
        raise FileNotFoundError(string)

#Change list to string
def list_to_string(string):
    str1 = " "
    return (str1.join(string))

#Change string to list
def string_to_list(string):
    li = list(string.split(","))
    return li

#Change dataFrame to dictionary
def dataFrame_to_dict(df):
    df = df.set_index('Words').to_dict()['Count']
    return df

#Replace single characters from the string with space
def remove_punctation(st):
    for c in string.punctuation:
        st = st.replace('?',' ').replace('!',' ').replace(',',' ').replace('.',' ').replace('"',' ').replace('/',' ')#.replace(':',' ').replace('(',' ').replace(')',' ')
        return st

#Lowercase all words
def lower_split(st):
    st = st.lower()
    return st

#Create clean string without ąłćóżę etc.
def clean_message_string(st):
    new = unidecode(st)
    new = remove_punctation(new)
    new = lower_split(new)
    return new

#Clean html file using div classes
def div_decompose(*args, parent_decompose=False, **kwargs):
        for div in soup.find_all(*args, **kwargs):
            if parent_decompose:
                div.parent.decompose()
            else:
                div.decompose()

#List of arguments to provide
parser = argparse.ArgumentParser()
parser.add_argument('--path', '-p', help="Type a folder directory containing html files with messages", type=dir_path)
parser.add_argument('--exclude', '-e', help="Type which words or letters to exclude separated with a comma", type= str)
parser.add_argument('--image', '-i', help="Type png/jpg file path to create a mask", type=file_img)

#Assign parameters to variables and check if --exclude exists
argum = parser.parse_args()

path = argum.path
exclude_para = argum.exclude
img_para = argum.image

if argum.exclude is not None:
    parameters_list = string_to_list(exclude_para)


#Combine all .html files into one
files_to_combine = list(pathlib.Path(path).glob('*.html'))

if(os.path.exists(path + "\combined.html")==False):
    with open(path + "\combined.html", "wb") as outfile:
        for f in files_to_combine:
            with open(f, "rb") as infile:
                outfile.write(infile.read())


print("Combining html files   -    DONE [1/6]")

#Decomposing html file based on div classes
with open(path + "\combined.html",encoding="utf8") as fp:
    soup = BeautifulSoup(fp, 'html.parser')



#Decompose html file using BeautifulSoup
for args, kwargs in [
        (("ul", {'class': '_a6-q'}), {}),
        (("video", {'class': '_a6_o _3-96'}), {}),
        (("audio",), {"attrs": {'class': None}}),
        ((), {"text": re.compile(' IP: '),"parent_decompose": True})
    ]:
            div_decompose(*args, **kwargs)

print("Decomposing div's      -    DONE [2/6]")

#Extract text from the html
message_with_div = soup.find_all("div", {"class":"_2ph_ _a6-p"})
message_extracted = [r.text.strip() for r in message_with_div]

#Remove https links form the string
messages = list_to_string(message_extracted)
messages = re.sub(r"\S*https?:\S*", "", messages)   #Remove links from string


print("Clensing div's         -    DONE [3/6]")


# Creating an array to fill with the normalized text
messages_cleansed = clean_message_string(messages)

print("Remove special chars   -    DONE [4/6]")

# Fill an array with the list of cleansed words
dump = []
messages_cleansed= messages_cleansed.split()
dump.extend(messages_cleansed)

#Creating DataFrame with count of the words and splitted by columns "Words" and "Count"
df = pd.value_counts(np.array(dump)).rename_axis('Words').reset_index(name='Count')

#Remove strage values
df = df[df.Words.str.contains("target=|/>|alt=|<img|<br|<a|[0-9]+|[;][&]gt[;]|[:][&]gt[;]|-|[:][&]lt[;]|\r\n|\r|\n",regex=True)==False]

print("Data Frame created     -    DONE [5/6]")

#Remove values from parameter
if argum.exclude is not None:
    df = df[df.Words.isin(parameters_list) == False]

#Save to CSV file
df.to_csv(path + "\WordCount.csv",index=False)

#Check if .png file contain transparent backgroud and change it to white
if argum.image is not None:
    if img_para.endswith('.png'):
        foregroud = Image.open(img_para).convert("RGBA")
        backgroud = Image.new("RGBA", foregroud.size, "WHITE")
        backgroud.paste(foregroud, (0, 0), foregroud)
        mask_img = np.array(backgroud)
    else:
        mask_img = np.array(Image.open(img_para).convert("RGBA"))
else:
    mask_img = None

#Generate Word Cloud
wc = WordCloud(background_color="white", width=1400, height=1000, max_words=300,mask=mask_img,repeat=True,min_font_size=4).generate_from_frequencies(dataFrame_to_dict(df))

# store to file
wc.to_file(path + "\WordCloud.png")

# Remove generated, combined html file
os.remove(path+"\combined.html")

print("Files generated!      COMPLEATED [6/6]")
