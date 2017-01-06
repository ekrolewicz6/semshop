import sys
sys.path.append("../")
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(128))
    name = db.Column(db.String(1024))
    url = db.Column(db.Text)

    def __init__(self, sku=None, name=None, url=None):
        self.sku = sku
        self.name = name
        self.url = url

    def __repr__(self):
        return '<Product %r>' % self.sku

    def json(self):
        return {
            'id'         : self.id,
            'name': self.name,
            'sku': self.sku,
            'url': self.url
        }


class ProductPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product',
        backref=db.backref('prices', lazy='dynamic'))
    price = db.Column(db.Float)
    pub_date = db.Column(db.DateTime)

    def __init__(self, product, price, pub_date=None):
        self.product = product
        self.price = price
        if pub_date is None:
            self.pub_date = datetime.utcnow()

    def __repr__(self):
        return '<Product %r>' % self.produt

    def json(self):
        return {
            'id'         : self.id,
            'product_id': self.product_id,
            'product': self.product.json(),
            'price': self.price,
            'date': dump_datetime(self.pub_date)
        }


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

    def json(self, include_genes=True):
        result = {
            'id'         : self.id,
            'name': self.name,
        }
        if include_genes:
            result.update({'genes': [g.json(include_category=False) for g in self.genes]})
        return result


class Gene(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
        backref=db.backref('genes', lazy='dynamic'))
    name = db.Column(db.String(128))

    def __init__(self, category, name):
        self.category = category
        self.name = name

    def __repr__(self):
        return '<Gene %r>' % self.name

    def json(self, include_category=True):
        result = {
            'id'         : self.id,
            'category_id': self.category_id,
            'name': self.name
        }
        if include_category:
            result.update({'category'  : self.category.json()})
        return result



class ProductGenes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product',
        backref=db.backref('genes', lazy='dynamic'))
    gene_id = db.Column(db.Integer, db.ForeignKey('gene.id'))
    genes = db.relationship('Gene')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category')

    def __init__(self, product, gene, category):
        self.product = product
        self.category = category
        self.gene = gene

    def __repr__(self):
        return '<Gene %r>' % self.name