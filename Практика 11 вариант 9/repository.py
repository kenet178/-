import sqlite3
class FlightRepository:
    def __init__(self, conn: sqlite3.Connection): self.conn=conn
    def all(self, destination: str | None=None):
        sql='''SELECT f.id,f.number,a.city AS origin,d.city AS destination,
                      f.departure,f.price,f.free_seats
               FROM flights f JOIN airports a ON a.id=f.origin_id
               JOIN airports d ON d.id=f.destination_id'''
        params=[]
        if destination:
            sql+=' WHERE d.city LIKE ?';params=[f'%{destination}%']
        return [dict(row) for row in self.conn.execute(sql+' ORDER BY f.departure',params)]
    def get(self, id: int):
        row=self.conn.execute('SELECT * FROM flights WHERE id=?',(id,)).fetchone()
        return dict(row) if row else None
    def create(self, number: str, origin_id: int, destination_id: int, aircraft_id: int,
               departure: str, price: float, free_seats: int):
        cur=self.conn.execute('''INSERT INTO flights(number,origin_id,destination_id,aircraft_id,departure,price,free_seats)
                  VALUES(?,?,?,?,?,?,?)''',(number,origin_id,destination_id,aircraft_id,departure,price,free_seats))
        return self.get(cur.lastrowid)
    def update_price(self,id: int,price: float) -> bool:
        return self.conn.execute('UPDATE flights SET price=? WHERE id=?',(price,id)).rowcount>0
    def delete(self,id: int) -> bool:
        return self.conn.execute('DELETE FROM flights WHERE id=?',(id,)).rowcount>0
    def stats(self):
        return [dict(x) for x in self.conn.execute('''SELECT a.city AS origin,COUNT(*) AS flights,
              ROUND(AVG(f.price),2) AS avg_price FROM airports a LEFT JOIN flights f
              ON a.id=f.origin_id GROUP BY a.id HAVING COUNT(f.id)>0 ORDER BY flights DESC''')]
