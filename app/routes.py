from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, TicketForm
from app.models import User, Ticket, Group


@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.role == 'Admin':
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(group_work=current_user.group).all()
    return render_template('index.html', title='Home', tickets=tickets)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page:
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
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    role='Analyst',
                    group=form.group.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/create_ticket', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(note=form.note.data, user_create=current_user.id, group_work=current_user.group)
        db.session.add(ticket)
        db.session.commit()
        flash('Your ticket has been created.')
        return redirect(url_for('index'))
    return render_template('create_ticket.html', title='Create Ticket', form=form)


@app.route('/manage_tickets', methods=['GET', 'POST'])
@login_required
def manage_tickets():
    if current_user.role != 'Admin' and current_user.role != 'Manager':
        return redirect(url_for('index'))
    if current_user.role == 'Admin':
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(group_work=current_user.work).all()
    return render_template('manage_tickets.html', title='Manage Tickets', tickets=tickets)
