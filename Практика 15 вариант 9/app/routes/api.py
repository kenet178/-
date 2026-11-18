from flask import Blueprint,current_app,jsonify,request
from app.repositories import TrainRepository
from app.services import TrainService,DomainError
bp=Blueprint('api',__name__,url_prefix='/api')
def session():return current_app.extensions['session_factory']()
def serialize(t):return {'id':t.id,'number':t.number,'origin_id':t.origin_id,'destination_id':t.destination_id,
                          'departure':t.departure.isoformat(),'fare':t.fare,'seats':t.seats,'status':t.status}
def fail(message,status):return jsonify({'error':message}),status
@bp.get('/trains')
def list_api():
    with session() as s:
        data=TrainRepository(s).list(request.args.get('q',''),request.args.get('origin_id',type=int),request.args.get('destination_id',type=int),request.args.get('sort','departure'),request.args.get('direction','asc'))
        return jsonify([serialize(t) for t in data])
@bp.get('/trains/<int:id>')
def get_api(id):
    with session() as s:
        t=TrainRepository(s).get(id)
        return jsonify(serialize(t)) if t else fail('Поезд не найден',404)
@bp.post('/trains')
def add_api():
    with session() as s:
        try:return jsonify(serialize(TrainService(s).save(request.get_json(silent=True) or {}))),201
        except DomainError as e:return fail(str(e),409 if 'занят' in str(e) else 400)
@bp.route('/trains/<int:id>',methods=['PUT','PATCH'])
def change_api(id):
    with session() as s:
        service=TrainService(s)
        old=service.repo.get(id)
        if old is None:return fail('Поезд не найден',404)
        incoming=request.get_json(silent=True) or {}
        if request.method=='PATCH':incoming={**serialize(old),**incoming}
        try:return jsonify(serialize(service.save(incoming,id)))
        except DomainError as e:return fail(str(e),400)
@bp.delete('/trains/<int:id>')
def delete_api(id):
    with session() as s:
        try:TrainService(s).remove(id);return '',204
        except DomainError as e:return fail(str(e),404 if 'не найден' in str(e) else 409)
@bp.post('/tickets')
def ticket_api():
    data=request.get_json(silent=True) or {}
    with session() as s:
        try:
            t=TrainService(s).purchase(int(data.get('train_id',0)),data.get('buyer',''),data.get('seat'))
            return jsonify({'id':t.id,'train_id':t.train_id,'seat':t.seat,'buyer':t.buyer}),201
        except (DomainError,ValueError,TypeError) as e:return fail(str(e),409 if 'занято' in str(e) else 400)
