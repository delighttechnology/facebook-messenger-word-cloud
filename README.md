# Facebook Messenger Word Cloud
Create Facebook Messenger Word Cloud based on the messeges exported from Facebook archive. Script extracts messages from one or multiple "message_x.html" files for a selected folder and transform into PNG (Word Cloud) and CSV (descending words list) containing most frequently used words.

---
## Under construction
---

## Table of contents
* [Example Usage](#Example-Usage)
* [Mask constrains](#Mask-constrains)
* [License](#License)

## Example Usage
Generate rectangular Word Cloud just providing the folder path containing the .html files:
> main.py -p C:\Users\Andrzej\facebook\messages\inbox\username\

Generate rectangular Word Cloud without specified words:
> main.py -p C:\Users\Andrzej\facebook\messages\inbox\username\ -e a,in,an,or,and,no,how,why 

Generate Word Cloud in different shapes (see [Mask constrains](#Mask-constrains) ):
> main.py -p C:\Users\Andrzej\facebook\messages\inbox\username\ -e a,in,an,or,and,no,how,why -i C:\Users\Andrzej\Desktop\like.jpg
	
## Mask constrains
In order to create Word Cloud in various shapes, mask need to be provided in in a certain way. Script accepts only files with .jpg, .jpeg and .png extensions. Additionally, file need to have black `#000000` shape and white `#FFFFFF` background. For .png files background can be transparent.
<p float="left">
  <img src="./images/like.jpg" width="350" />
  <img src="./images/WordCloud.png" width="350" />
</p>


## License

Copyright © 2022, [Andrzej Strzala](https://www.linkedin.com/in/andrzejstrzala/).
