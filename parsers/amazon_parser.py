from bs4 import BeautifulSoup
import urllib2

URL = 'https://www.amazon.com/Brother-HL-L2340DW-Monochrome-Wireless-Replenishment/dp/B00LZS5EEI'#'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=printers'


def _create_opener():
	opener = urllib2.build_opener()
	opener.addheaders = [('hellothere', 'Mozilla/5.0')]
	return opener

def extract_genes(soup):
	genes = {}
	try:
		for tag in soup.find(id="leftNav").find_all("h2"):
			genes.update({tag.string: [gene.string for gene in tag.next_sibling.next_sibling.find_all("span", class_="refinementLink")]})
	except:
		pass
	return genes

def extract_categories(soup):
	top_categories = []
	try:
		for tag in soup.find_all("span", class_="srSprite backArrow"):
			top_categories.append(tag.next_sibling.string)
	except:
		pass
	return top_categories

def get_price(soup):
	top_categories = []
	try:
		return float(soup.find("span", id="priceblock_ourprice").text[1:])
	except:
		return 0

def get_name(soup):
	try:
		return soup.find("span", id="productTitle").text.strip()
	except:
		return ''

def get_sku(soup):
	try:
		for tag in soup.find_all("th", class_="prodDetSectionEntry"):
			if tag.text.strip() in ["ASIN", "Item model number"]:
				return tag.next_sibling.next_sibling.text.strip()
	except:
		return ''

def get_product_info(url):
	opener = _create_opener()
	response = opener.open(url)
	html_contents = response.read()
	soup = BeautifulSoup(html_contents, "lxml")
	return {'genes': extract_genes(soup), 'top': extract_categories(soup), 'price': get_price(soup), 'name': get_name(soup), 'sku': get_sku(soup)}


print get_product_info(URL)



