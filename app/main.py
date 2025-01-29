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

    # 페이지네이션
    page = int(request.args.get('page', 1))
    per_page = 8
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(products) + per_page - 1) // per_page
    current_products = products[start:end]
    pages = get_pagination(page, total_pages)
    
    return render_template('home.html', 
                            products=current_products, 
                            int=int,
                            clients=clients,
                            categories=categories,
                            page=page, 
                            pages=pages, 
                            total_pages=total_pages
                            )
@blueprint.route('/search')    
def search():
    query = request.args.get('query', '')
    products = ProductDao().get_all_products()
    clients = clientDao().get_all_clients()
    categories = categoryDao().get_all_categories()
    if query:
        products = ProductDao().search_products_by_query(query)
    else:
        products = ProductDao().get_all_products()

    # 페이지네이션
    page = request.args.get('page', 1, type=int)
    per_page = 8
    total_pages = (len(products) - 1) // per_page + 1
    paginated_list = products[(page - 1) * per_page: page * per_page]
    pages = get_pagination(page, total_pages)

    return render_template('home.html', 
                            clients=clients,
                            categories=categories,
                            products=paginated_list , 
                            page=page, 
                            pages=pages, 
                            total_pages=total_pages,
                            query=query,
                            int=int)

def get_pagination(page, total_pages, max_visible=10):
    if total_pages <= max_visible:
        return list(range(1, total_pages + 1))

    visible_pages = []
    visible_pages.append(1)
    if page > 3:
        visible_pages.append('...')

    start = max(2, page - 1)
    end = min(total_pages - 1, page + 1)
    visible_pages.extend(range(start, end + 1))

    if page < total_pages - 2:
        visible_pages.append('...')
        visible_pages.append(total_pages)

    return visible_pages