# Facebook Messenger Word Cloud
Create Facebook Messenger Word Cloud based on the messeges exported from Facebook archive. Script extracts messages from one or multiple "message_x.html" files for a selected folder and transform into PNG (Word Cloud) and CSV (descending words list) containing most frequently used words.

## Table of contents
* [Example Usage](#Example-Usage)
* [Custom shape](#Custom shape)
* [Obtaining message files](#Obtaining-message-files)
* [License](#License)

## Example Usage
Generate rectangular Word Cloud just providing the folder path containing the .html files:
> main.py -p C:\Users\Andrzej\facebook\messages\inbox\username\

<img src="./images/WordCloud_rec.png" width="450" />

Generate rectangular Word Cloud without specified words:
> main.py -p C:\Users\Andrzej\facebook\messages\inbox\username\ -e a,in,an,or,and,no,how,why 

Generate Word Cloud in different shapes (see [Custom shape](#Custom shape) ):
> main.py -p C:\Users\Andrzej\facebook\messages\inbox\username\ -e a,in,an,or,and,no,how,why -i C:\Users\Andrzej\Desktop\like.jpg
	
## Custom shape
In order to create Word Cloud in various shapes, mask need to be provided in in a certain way. Script accepts only files with .jpg, .jpeg and .png extensions. Additionally, file need to have black `#000000` shape and white `#FFFFFF` background. For .png files background can be transparent.
<p float="left">
  <img src="./images/like.jpg" width="350">   </img>
  <img src="./images/WordCloud.png" width="350" />
</p>

## Downloading messages files
If you don't know how to download facebook archive, below you can find step by step manual.

Click on you profile picture and select **Setting & Privacy** ⮕ **Settings**
<p float="left">
  <img src="./images/facebook1.png" width="250">  ⮕  </img>
  <img src="./images/facebook2.png" width="250" />
</p>

On the left side of the screen click **Privacy** tab and then **Your Facebook information**
<p float="left">
  <img src="./images/facebook3.png" width="250">  ⮕  </img>
  <img src="./images/facebook4.png" width="250" />
</p>

You will have a list of options to choose from, please select **Download profile information**
<img src="./images/facebook5.png" width="800" />


## License

Copyright © 2022, [Andrzej Strzala](https://www.linkedin.com/in/andrzejstrzala/).
