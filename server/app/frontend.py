import sys
sys.path.append("../")
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

frontend = Blueprint('frontend', __name__,
                        template_folder='templates')

@frontend.route('/')
def index_page():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)