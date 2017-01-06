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
top_categories = []
for tag in spans:
	#Create a list of the top level categories (Show Results For)
	top_categories.append(tag.next_sibling.string)

# Change the scope to only the children of div id= leftnav section
leftNav = soup.find(id="leftNav")

#Find all categories
categories = [tag.string for tag in leftNav.find_all("h2")]
cat_tags = leftNav.find_all("h2")
print cat_tags[0].next_sibling, "sibling"

# genes_list = {}

# for category in leftNav.find_all("h2"):
# 	print category, 'category'
# 	print category.next_sibling.children, "children"




