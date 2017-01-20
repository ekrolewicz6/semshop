import sys
sys.path.append("../")
from flask import Blueprint, render_template, abort, request, send_from_directory
from jinja2 import TemplateNotFound
from datetime import datetime
from app.db import *
import json
from parsers import amazon_parser

frontend = Blueprint('frontend', __name__,
                        template_folder='templates', static_url_path='static')

@frontend.route('/')
def index_page():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)

@frontend.route('/add_product', methods=["POST"])
@frontend.route('/semshop.php', methods=["POST"])
def add_data_points():
    try:
    	form_data = json.loads(request.data)
    	product_date = datetime.now()
    	product_sku = form_data['sku']
    	product_url = form_data['site']
    	product_name = form_data['name']
        product_price = form_data['price']
        prod = Product(sku=product_sku, url=product_url, name=product_name)
        prod_price = ProductPrice(product=prod, price=product_price)
        db.session.add(prod)
        db.session.add(prod_price)
        db.session.commit()
        return json.dumps([product_date.isoformat(), product_sku, product_url, product_name, product_price])
        # return render_template('index.html')
    except TemplateNotFound:
        abort(404)

@frontend.route('/get_product_data', methods=["POST"])
def get_product_data():
    url = json.loads(request.data)["url"]
    product_info = amazon_parser.get_product_info(url)
    return json.dumps(product_info)

@frontend.route('/templates/<path:path>')
def send_templates(path):
    try:
        return send_from_directory('templates', path)
    except TemplateNotFound:
        abort(404)

@frontend.route('/static/<path:path>')
def send_static(path):
    try:
        return send_from_directory('static', path)
    except TemplateNotFound:
        abort(404)