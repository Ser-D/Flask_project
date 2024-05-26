from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, TicketForm, TicketAdminForm
from app.models import User, Ticket, Group


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home', user=current_user)



@app.route('/view_tickets')
@login_required
def view_tickets():
    if current_user.role == 'Admin':
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(group_work=current_user.group).all()

    tickets_with_creators = []
    for ticket in tickets:
        creator = User.query.filter_by(id=ticket.user_create).first()

        ticket_info = (ticket, creator)

        tickets_with_creators.append(ticket_info)
    return render_template('view_tickets.html', title='Tickets', data=tickets_with_creators, user=current_user)


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
    if current_user.role == 'Admin':
        form = TicketAdminForm()
        if form.validate_on_submit():
            ticket = Ticket(note=form.note.data, user_create=current_user.id, group_work=form.group.data)
            db.session.add(ticket)
            db.session.commit()
            flash('Your ticket has been created.')
            return redirect(url_for('index'))
    else:
        form = TicketForm()
        if form.validate_on_submit():
            ticket = Ticket(note=form.note.data, user_create=current_user.id, group_work=current_user.group)
            db.session.add(ticket)
            db.session.commit()
            flash('Your ticket has been created.')
            return redirect(url_for('index'))
    return render_template('create_ticket.html', title='Create Ticket', form=form)


@app.route('/change_status/<int:ticket_id>', methods=['POST'])
@login_required
def change_status(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if ticket:
        new_status = request.form.get('status')
        if new_status in ['Pending', 'In review', 'Closed']:
            ticket.status = new_status
            db.session.commit()
            flash('Ticket status has been updated.')
        else:
            flash('Invalid status.')
    else:
        flash('Ticket not found.')
    return redirect(url_for('view_tickets'))



@app.route('/manage_ticket', methods=['GET', 'POST'])
@login_required
def manage_tickets():
    if current_user.role != 'Admin' and current_user.role != 'Manager':
        return redirect(url_for('index'))
    if current_user.role == 'Admin':
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(group_work=current_user.group).all()
    return render_template('manage_tickets.html', title='Manage Tickets', tickets=tickets)
