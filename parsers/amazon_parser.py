from bs4 import BeautifulSoup

import urllib2

URL = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=printers'


def _create_opener():
	opener = urllib2.build_opener()
	opener.addheaders = [('hellothere', 'Mozilla/5.0')]
	return opener

def extract_genes(soup):
	genes = {}
	for tag in soup.find(id="leftNav").find_all("h2"):
		genes.update({tag.string: [gene.string for gene in tag.next_sibling.next_sibling.find_all("span", class_="refinementLink")]})
	return genes

def extract_categories(soup):
	top_categories = []
	for tag in soup.find_all("span", class_="srSprite backArrow"):
		top_categories.append(tag.next_sibling.string)
	return top_categories

def get_product_info(url):
	opener = _create_opener()
	response = opener.open(url)
	html_contents = response.read()
	soup = BeautifulSoup(html_contents, "lxml")
	return {'genes': extract_genes(soup), 'top': extract_categories(soup)}


print get_product_info(URL)



