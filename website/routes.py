from flask import Flask, Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Ticket, InventoryIn, InventoryOut, Assigned, Upcoming, Response
from . import db
import json
from datetime import datetime, timedelta


routes = Blueprint('routes', __name__)


@routes.route('/email', methods=['GET', 'POST'])
def send_email():
    return render_template("email.html", user=current_user)


@routes.route('/', methods=['GET', 'POST'])
@routes.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST' and current_user.department != 'MANAGER' and current_user.department != 'LEAD' and current_user.department != 'ITSC':
        # grab ticket text
        ticket = request.form.get('ticket')

        # checking if ticket is blank
        if len(ticket) < 1:
            flash('Blank Ticket', category='error')
        else:
            # create instance of ticket
            new_ticket = Ticket(data=ticket,
                                user_id=current_user.id,
                                date=datetime.utcnow()-timedelta(hours=5))
            # add new ticket to database
            db.session.add(new_ticket)
            # update & save database
            db.session.commit()
            flash('Ticket added!', category='success')

    elif (request.method == 'POST' and current_user.department == 'MANAGER') or (request.method == 'POST' and current_user.department == 'LEAD'):
        managerEmail = request.form.get('assign')
        ticketId = request.form.get('ticket_id')
        assigned_ticket = Assigned(assigned_to=managerEmail, ticket_id=ticketId)
        db.session.add(assigned_ticket)
        # update & save database
        db.session.commit()
        flash('Ticket Assigned!', category='success')

    # get all tickets
    tickets = Ticket.query.all()
    # get all users
    users = User.query.all()
    # get lead manager
    leads = User.query.filter_by(department='LEAD').all()
    # get managers
    managers = User.query.filter_by(department='MANAGER').all()
    # get assigned tickets
    assigned = Assigned.query.all()
    # get responses to tickets
    responses = Response.query.all()

    return render_template("home.html",
                           user=current_user,
                           tickets=tickets,
                           users=users,
                           leads=leads,
                           managers=managers,
                           assigned=assigned,
                           responses=responses)


@routes.route('/response/<id>', methods=['POST'])
@login_required
def respond(id):
    if current_user.department == 'MANAGER' or current_user.department == 'LEAD' or current_user.department == 'ITSC':
        response = request.form.get('response')
        if not response:
            flash('Response EMPTY!', category='error')
        else:
            ticket = Ticket.query.filter_by(id=int(id))
            if ticket:
                response = Response(data=response, ticket_id=id, user_id=current_user.id)
                db.session.add(response)
                db.session.commit()
            else:
                flash('Does not exist!', category='error')

    else:
        response = request.form.get('response')
        if not response:
            flash('Response EMPTY!', category='error')
        else:
            ticket = Ticket.query.filter_by(id=int(id))
            if ticket:
                response = Response(data=response, ticket_id=id, user_id=current_user.id)
                db.session.add(response)
                db.session.commit()
            else:
                flash('Does not exist!', category='error')

        tickets = Ticket.query.all()
        users = User.query.all()
        responses = Response.query.all()

        return render_template("my_history.html", user=current_user,
                               tickets=tickets, users=users, responses=responses)
    assigned = Assigned.query.order_by(Assigned.id.desc()).all()
    tickets = Ticket.query.all()
    users = User.query.all()
    responses = Response.query.all()

    return render_template("my_tickets.html", user=current_user, assigned=assigned,
                           tickets=tickets, users=users, responses=responses)


@routes.route('/delete-ticket', methods=['POST'])
def delete_ticket():
    ticket = json.loads(request.data)
    ticketId = ticket['ticketId']
    ticket = Ticket.query.get(ticketId)
    if ticket:
        if ticket.user_id == current_user.id or current_user.department == 'MANAGER' or current_user.department == 'LEAD':
            responses = Response.query.all()
            for re in responses:
                if re.ticket_id == ticketId:
                    db.session.delete(re) # delete the responses to help declutter database
            db.session.delete(ticket)
            db.session.commit()
            if ticket.user_id == current_user.id:
                flash('Ticket DELETED!', category='error')
            if current_user.department == 'MANAGER' or current_user.department == 'LEAD':
                flash('Ticket CLOSED!', category='success')

    return jsonify({})


@routes.route('/delete-event', methods=['POST'])
def delete_event():
    event = json.loads(request.data)
    eventId = event['eventId']
    event = Upcoming.query.get(eventId)
    if event:
        db.session.delete(event)
        db.session.commit()

    return jsonify({})


@routes.route('/tech/view_users/delete-user', methods=['GET', 'POST'])
def delete_user():
    user = json.loads(request.data)
    userId = user['userId']
    user = User.query.get(int(userId))
    if user:
        db.session.delete(user)
        db.session.commit()

    return jsonify({})


@routes.route('/tech/equipment_log/sign-out', methods=['POST'])
def sign_out():
    item = json.loads(request.data)
    itemId = item['itemId']
    item = InventoryIn.query.get(int(itemId))
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Item DELETED!', category='error')

    return jsonify({})


@routes.route('/tech/equipment_log/sign-in', methods=['POST'])
def sign_in():
    item = json.loads(request.data)
    itemId = item['itemId']
    item = InventoryOut.query.get(int(itemId))
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Item REMOVED!', category='success')
        new_item = InventoryIn(item_name=item.item_name,
                               item_type=item.item_type,
                               item_number=item.item_number,
                               dateIn=datetime.utcnow()-timedelta(hours=5))
        db.session.add(new_item)
        db.session.commit()

    return jsonify({})
