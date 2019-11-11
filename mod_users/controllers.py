from flask import Blueprint, render_template, request, flash, redirect, url_for
from database import db
from mod_users.models import Users, get_user, edit_user
from mod_users.forms import UserForm

mod_users = Blueprint('users', __name__, url_prefix='/users')

#
# Routes
#


@mod_users.route('/', methods=['GET'])
def index():
    users = Users.query.all()
    return render_template('users/index.html',users=users)

@mod_users.route('/<int:_id>', methods=['GET'])
def show(_id):
    user = get_user(_id)
    return render_template('users/show.html',user=user)

@mod_users.route('/edit/<int:_id>', methods=['GET','POST'])
def edit(_id):
    user = get_user(_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
      save_result = edit_user(_id,
                              form.default_drink_location_city.data,
                              form.default_drink_location_country.data,
                              form.default_drink_date.data)
      if save_result['status']:
        flash(u'Updated successfully!', 'success')
        return redirect(url_for('.edit',_id=_id))
      else:
        flash(u'Unable to update user. Error: %s' % save_result['message'], 'error')

    return render_template('users/edit.html'
                            ,form=form
                            ,user=user)    


@mod_users.route('/make', methods=['GET'])
def make():
    user_entry = Users(
      name='Parry',
      uses_full_drink_date=False)
    db.session.add(user_entry)
    db.session.commit()
    return render_template('users/index.html')

