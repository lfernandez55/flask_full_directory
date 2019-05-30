# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db
from app.models.user_models import UserProfileForm


main_blueprint = Blueprint('main', __name__, template_folder='templates')


# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/member')
@login_required  # Limits access to authenticated users
def member_page():
    # return render_template('main/user_page.html')
    return render_template('main/index.html')

@main_blueprint.route('/main/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        result = db.engine.execute("SELECT * FROM users")
        for row in result:
            print(row['email'])
        print('user profile view')



        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/user_profile_page.html',
                           form=form)

@main_blueprint.route('/all_books')
@login_required
def books():
    books = db.engine.execute('SELECT Category.description AS c_description, Book.description AS b_description, * FROM Category INNER JOIN Book ON Category.rowID=Book.category_id  ORDER BY c_description ASC')
    # print(len(books))
    books = [dict(row) for row in books]
    return render_template('main/all_books.html', books=books)

@main_blueprint.route('/seedDB')
@roles_required('admin')
def seedDB():

    result = db.engine.execute("SELECT * FROM users")
    for row in result:
        print(row['email'])

    result = db.engine.execute('DELETE FROM Book')
    result = db.engine.execute('DELETE FROM Category')
    result = db.engine.execute('INSERT INTO Book (author,title,isbn, description, category_id) VALUES ("Mary Shelly","Frankenstein","1", "A horror story written by a romantic.","1")')
    result = db.engine.execute('INSERT INTO Book (author,title,isbn, description, category_id) VALUES ("Henry James","The Turn of the Screw","2", "Another British horror story.","1")')
    result = db.engine.execute('INSERT INTO Book (author,title,isbn, description, category_id) VALUES ("Max Weber","The Protestant Work Ethic and The Spirit of Capitalism","3", "A classic early 20th C. sociology text","2")')
    result = db.engine.execute('INSERT INTO Book (author,title,isbn, description, category_id) VALUES ("Robert Putnam","Bowling Alone","4", "A classic late 20th C. sociology test","2")')
    result = db.engine.execute('INSERT INTO Category (description) VALUES ("Horror")')
    result = db.engine.execute('INSERT INTO Category (description) VALUES ("Sociology")')

    result = db.engine.execute("SELECT * FROM Book")
    for row in result:
        print(row['title'])

    return '<h1>DB Seeded!</h1>'

@main_blueprint.route('/erase_DB')
@roles_required('admin')
def eraseDB():
        sqlQ = db.engine.execute('DELETE FROM Book')
        sqlQ = db.engine.execute('DELETE FROM Category')
        return '<h1>DB Erased!</h1>'

@main_blueprint.route('/addbook', methods={'GET','POST'})
@login_required
def addbook():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        isbn = request.form['isbn']
        description = request.form['description']
        category_field = request.form['category']

        sql = "SELECT * FROM Category WHERE description ='" + category_field + "'"
        categoryID = db.engine.execute(sql)
        categoryID = [dict(row) for row in categoryID]
        if len(categoryID) == 0:
            sql = "INSERT INTO Category (description) VALUES (" + category_field   +")"
            returnStatus = db.engine.execute(sql)
            returnQuery = db.engine.execute('SELECT last_insert_rowid()')
            returnQuery = [dict(row) for row in returnQuery]
            categoryID = returnQuery[0][0]
            # or, instead of above two lines use this one instead:
            # categoryID = execute_sql('SELECT rowid, * FROM Category WHERE description = ? ',[category_field])
        else:
            categoryID = categoryID[0]['id']


        sql = "INSERT INTO Book (author, title, isbn, description, category_id) VALUES ('"+ author +"','"+ title +"',"+ isbn +",'"+ description +"',"+ str(categoryID) +")"
        returnStatus = db.engine.execute(sql)


        return redirect(url_for('main.home_page'))

    categories = db.engine.execute('SELECT * FROM Category ORDER BY description ASC')
    return render_template('main/addbook.html', categories=categories)

@main_blueprint.route('/categories')
@login_required
def categories():
    categories = db.engine.execute('SELECT rowid, * FROM Category ORDER BY description ASC')
    categories = [dict(row) for row in categories]
    for cat in categories:

        print(cat['id'])
    return render_template('main/categories.html', categories=categories)

@main_blueprint.route('/books_in_category/<categoryID>')
@login_required
def books_in_cat(categoryID):
    sql = "SELECT * FROM Category WHERE rowid =" + categoryID
    categories = db.engine.execute(sql)
    categories = [dict(row) for row in categories]
    categoryDescription= categories[0]['description']
    sql= "SELECT * FROM Book WHERE category_id =" + categoryID
    books = db.engine.execute(sql)
    books = [dict(row) for row in books]
    for book in books:
        print('dddd')
    print('debug')
    return render_template('main/books_in_cat.html', books=books, categoryDescription=categoryDescription)

@main_blueprint.route('/sql', methods={'GET','POST'})
@roles_required('admin')
def sql():
    data=""
    if request.method == 'POST':
        sqlField = request.form['sqlField']
        try:
            returnVar = db.engine.execute(sqlField)
            returnVar = [dict(row) for row in returnVar]
        except:
            data="An error occurred. . .look in the console"
        else:
            try:
                for row in returnVar:
                    print('')
                    print(type(row))
                    rowAsDict = dict(row)
                    print(type(rowAsDict))
                    data = data + "\n"
                    for key, value in rowAsDict.items():
                        print(key, ":", value)
                        data= data + key + ":" + str(value) + "\n"
            except:
                 data="Data returned from sql was not iterable"
        return render_template('main/sql.html',data=data)

    return render_template('main/sql.html',data=data)

@main_blueprint.route('/tinker')
def tinker():
    return '<h1>Tinker function executed, check console</h1>'

#Demos Jinja2 extends
@main_blueprint.route('/tink')
def tink():
     return render_template('tink.html')

# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    return render_template('main/index.html')


# The Admin page requires an 'Admin' role.
@main_blueprint.route('/admin')
@roles_required('admin')    # Use of @roles_required decorator
def admin_page():
    return render_template('main/admin.html')


@main_blueprint.context_processor
def example():
    return dict(myexample='This is an example')


@main_blueprint.context_processor
def utility_processor():
    def isAdmin(user):

        roleName = db.engine.execute("SELECT * FROM Roles")
        for role in roleName:
            print('dddd')
            print(role['name'])

        sqlStatement = "SELECT roles.name FROM roles JOIN users_roles ON roles.id=users_roles.role_id JOIN users ON users.id=users_roles.user_id WHERE users.email='" + user + "' AND roles.name='admin'"
        print(sqlStatement)
        roleName = db.engine.execute(sqlStatement)
        # Casting the returned alchemy query object into a list
        # See https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
        roleName = [dict(row) for row in roleName]

        if len(roleName) > 0 and roleName[0]['name'] == 'admin':
            returnValue = 1
        else:
            returnValue = 0
        return returnValue
    return dict(isAdmin=isAdmin)
