from flask import *
from DB.productDB import *
from DB.clientDB import *
from DB.categoryDB import *

blueprint = Blueprint('main', __name__, template_folder='templates')

# 초기 화면
@blueprint.route('/')
def index():
    return redirect(url_for('main.main'))

# 메인 화면
@blueprint.route('/main')
def main():
    products = ProductDao().get_all_products()
    clients = clientDao().get_all_clients()
    categories = categoryDao().get_all_categories()
    return render_template('home.html', products=products, int=int,clients=clients,categories=categories)