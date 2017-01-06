from bs4 import BeautifulSoup

import urllib2
opener = urllib2.build_opener()
opener.addheaders = [('hellothere', 'Mozilla/5.0')]
response = opener.open('https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=printers')
html_contents = response.read()
soup = BeautifulSoup(html_contents, "lxml")
# Find all spans
spans = soup.find_all("span", class_="srSprite backArrow")
#for each span, make a list of their sibling
categories = []
for tag in spans:
	#Create a list of the highest level categories
	categories.append(tag.next_sibling.string)

