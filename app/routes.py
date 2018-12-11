from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from werkzeug.urls import url_parse
from app.models import User, Item, WatchList
from app.forms import LoginForm, RegistrationForm, SearchForm, ItemForm
import urllib.request, json
import random

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
# @login_required
def index():
    if current_user.is_authenticated:
        keywordList = ["macbook+pro", "windows+10", "books", "fishing+pole", "inner+tube"]
        keyword = keywordList[random.randint(0,4)]
        APPID = "PeterMan-peterman-PRD-c13dad11d-1a18c02a"
        url = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SERVICE-VERSION=1.7.0&SECURITY-APPNAME=" + APPID + "&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=" + keyword + "&itemFilter(0).name=ListingType&itemFilter(0).value=All&paginationInput.pageNumber=1"
        itemlist = []
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            x = 0
            while x < 10:
                itemlist.append(data["findCompletedItemsResponse"][0]["searchResult"][0]["item"][x])
                x = x + 1
        return render_template('index.html', title='Home', itemData=itemlist)
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_db')
def reset_db():
   flash("Resetting database: deleting old data and repopulating with dummy data")
   # clear all data from all tables
   meta = db.metadata
   for table in reversed(meta.sorted_tables):
       print('Clear table {}'.format(table))
       db.session.execute(table.delete())
   return render_template('index.html')

if __name__ == '__main__':
    app.run()


@app.route('/getitem', methods=['GET', 'POST'])
def getItem():
    title = request.args.get('title')
    price = request.args.get('price')
    category = request.args.get('category')
    selling_state = request.args.get('state')
    img_url = request.args.get('imgurl')
    site_url = request.args.get('siteurl')
    flash("You added the item to your watchlist: " + title)
    watch_list = WatchList(item_title=title, item_price=price, item_category=category, selling_state=selling_state, ebay_item_url=site_url, img_url=img_url, user_id=current_user.id)
    db.session.add(watch_list)
    db.session.commit()
    return redirect(url_for('search'))


@app.route('/itemSearch', methods=['GET', 'POST'])
def search():
    keyword = "computer+windows+10"
    form = SearchForm(request.form)

    if form.validate_on_submit():
        keyword = form.search_term.data.replace(" ", "+")

    APPID = "PeterMan-peterman-PRD-c13dad11d-1a18c02a"
    url = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SERVICE-VERSION=1.7.0&SECURITY-APPNAME=" + APPID + "&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=" + keyword + "&itemFilter(0).name=ListingType&itemFilter(0).value=All&paginationInput.pageNumber=1"
    itemlist = []
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
        x = 0
        while x < 10:
            itemlist.append(data["findCompletedItemsResponse"][0]["searchResult"][0]["item"][x])
            x = x + 1
        colorList = ["border-danger", "border-success"]

    return render_template('itemSearch.html', title='Item Search', itemData=itemlist, form=form, color=colorList)


    # https://open.api.ebay.com/shopping?callname=GetAccount&appid=PeterMan-peterman-PRD-c13dad11d-1a18c02a&version=1063&siteid=0&responseencoding=JSON




@app.route('/inventory.html', methods=['GET', 'POST'])
def inventory():

    form = ItemForm(request.form)

    if form.validate_on_submit():
        new_item = Item(item_name=form.item_name.data, item_price=form.item_price.data,
                        item_category=form.item_category.data, user_id=current_user.id)
        db.session.add(new_item)
        db.session.commit()
        flash('Item added to inventory')
        return redirect(url_for('inventory'))

    return render_template('inventory.html', title='Inventory', form=form)

@app.route('/watchlist.html', methods=['GET', 'POST'])
def watchlist():
    if current_user.is_authenticated:
        user_id = current_user.id
        items = WatchList.query.filter_by(user_id=user_id).all()

        return render_template('watchlist.html', title='Watch List', items=items)
    return render_template('watchlist.html', title='Watch List')


@app.route('/features.html')
def features():

    return render_template('features.html', title='Features')


@app.route('/pricing.html')
def pricing():

    return render_template('pricing.html', title='Pricing')


@app.route('/about.html')
def about():

    return render_template('about.html', title='About')


@app.route('/contact.html')
def contact():

    return render_template('contact.html', title='Contact')


@app.route('/listings.html')
def listings():

    if current_user.is_authenticated:
        user_id = current_user.id
        items = Item.query.filter_by(user_id=user_id).all()
        return render_template('listings.html', title='Listings', items=items)

    return render_template('listings.html', title='Listings')


@app.route('/deleteItem', methods=['GET','POST'])
def deleteItem():

    id = request.args.get('item_id')
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    flash("item delete")
    return redirect('listings.html')

@app.route('/deleteFromWatchList', methods=['GET','POST'])
def deleteWatchList():

    id = request.args.get('item_id')
    item = WatchList.query.get(id)
    db.session.delete(item)
    db.session.commit()
    flash("Item delete")
    return redirect('watchlist.html')