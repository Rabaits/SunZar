from peewee import *
import datetime
import os

db = SqliteDatabase(os.getenv("DB_USRL"))

class BaseModel(Model):
    class Meta:
        database = db


class Hour(BaseModel):
    id = CharField(primary_key=True, max_length=3)  
    time = IntegerField()
    temp = IntegerField()
    state = CharField(max_length=20)

def DB_inint():
    
    db.connect()
    db.create_tables([Hour])


def DB_creat():
    Hour.create(id='new', time = 0, temp=0, state="none")  
    for i in range(1, 24):
        Hour.create(id=str(i), time = 0, temp=0, state="none")  

def DB_update(data):
    def up(h, ti, te, st):
        h.time = ti
        h.temp = te
        h.state = st
        h.save()

    data = data['data']['weatherByPoint']
    data_now = data['now']
    data_for = data['forecast']['hours']['edges']
    
    for h in Hour.select():
        id_hour = h.id
        if h.id != "new":
            data_h = data_for[int(id_hour)-1]['node']
            ti = int(data_h['time'][11:13])
            te = data_h['temperature']
            st = data_h['condition'].lower()
            up(h, ti, te, st)
        else:
            ti = 0
            te = data_now['temperature']
            st = data_now['condition'].lower()
            up(h, ti, te, st)

def DB_select():
    s = []
    for h in Hour.select():
        id_hour = h.id
        if h.id != "new":
            s.append((h.time, h.temp, h.state))
    return s

def DB_select_new(): 
    hnow = Hour.get(Hour.id == 'new')    
    return hnow.temp, hnow.state

