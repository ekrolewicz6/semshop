import sys
sys.path.append("../")
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import json
from app.db import *
from sqlalchemy import func

backend_endpoints = Blueprint('backend_endpoints', __name__,
                        template_folder='templates')

@backend_endpoints.route('/endpoints/categories')
def get_categories():
    try:
        return json.dumps([c.json() for c in Category.query.all()])
    except TemplateNotFound:
        abort(404)

@backend_endpoints.route('/endpoints/genes/<category_id>')
def get_genes(category_id=None):
    try:
        return json.dumps([g.json(include_category=False) for g in Gene.query.filter(Gene.category_id==category_id).all()])
    except TemplateNotFound:
        abort(404)

@backend_endpoints.route('/endpoints/genes/search/<query>')
def search_genes(query=None):
    try:
        return json.dumps([g.json() for g in Gene.query.filter(Gene.name.ilike("%" + query + "%")).all()])
    except TemplateNotFound:
        abort(404)