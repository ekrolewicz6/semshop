from flask import Flask
from app.db import *
from app.backend_endpoints import backend_endpoints
from app.frontend import frontend
import logging
from settings import DB_PATH

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
app.app_context().push()
db.init_app(app)
app.register_blueprint(frontend)
app.register_blueprint(backend_endpoints)

if __name__ == "__main__":
	db.create_all()
	c1 = Category("Department")
	g1 = Gene(c1, "Electronics")
	g2 = Gene(c1, "Books")
	# db.session.add(c1)
	db.session.add(g1)
	db.session.add(g2)
	db.session.commit()
	app.run(threaded=True, host="0.0.0.0", port=5000, debug=True)