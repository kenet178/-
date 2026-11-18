from flask import Blueprint,current_app,render_template,request,redirect,url_for,flash,abort
from sqlalchemy import func,select
from app.models import Train,Station,Ticket
from app.repositories import TrainRepository
from app.services import TrainService,DomainError
bp=Blueprint('web',__name__)
def factory():return current_app.extensions['session_factory']
@bp.get('/')
def home():
    with factory()() as s:
        trains=s.scalar(select(func.count(Train.id)));tickets=s.scalar(select(func.count(Ticket.id)))
    return render_template('index.html',trains=trains,tickets=tickets)
@bp.get('/trains')
def trains():
    with factory()() as s:
        r=TrainRepository(s)
        data=r.list(request.args.get('q',''),request.args.get('origin_id',type=int),request.args.get('destination_id',type=int),
                    request.args.get('sort','departure'),request.args.get('direction','asc'))
        stations=r.stations()
        return render_template('list.html',trains=data,stations=stations)
@bp.get('/trains/<int:id>')
def detail(id):
    with factory()() as s:
        r=TrainRepository(s);obj=r.get(id)
        if obj is None:abort(404)
        return render_template('detail.html',train=obj,tickets=r.tickets(id))
@bp.route('/trains/create',methods=['GET','POST'])
def create():
    with factory()() as s:
        stations=TrainRepository(s).stations()
        if request.method=='POST':
            try:TrainService(s).save(request.form);flash('Поезд создан','success');return redirect(url_for('web.trains'))
            except DomainError as e:flash(str(e),'error')
        return render_template('create.html',train=None,stations=stations)
@bp.route('/trains/<int:id>/edit',methods=['GET','POST'])
def edit(id):
    with factory()() as s:
        r=TrainRepository(s);obj=r.get(id)
        if obj is None:abort(404)
        if request.method=='POST':
            try:TrainService(s).save(request.form,id);flash('Изменения сохранены','success');return redirect(url_for('web.detail',id=id))
            except DomainError as e:flash(str(e),'error')
        return render_template('edit.html',train=obj,stations=r.stations())
@bp.post('/trains/<int:id>/delete')
def delete(id):
    with factory()() as s:
        try:TrainService(s).remove(id);flash('Поезд удалён','success')
        except DomainError as e:flash(str(e),'error')
    return redirect(url_for('web.trains'))
@bp.post('/trains/<int:id>/buy')
def buy(id):
    with factory()() as s:
        try:TrainService(s).purchase(id,request.form.get('buyer',''),request.form.get('seat'));flash('Билет куплен','success')
        except DomainError as e:flash(str(e),'error')
    return redirect(url_for('web.detail',id=id))
