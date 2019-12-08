import datetime
import random
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, Date, Float, Text, Boolean, \
    UniqueConstraint, Sequence, create_engine, select, func
from sqlalchemy.dialects import postgresql
from faker import Faker


metadata = MetaData()
tableMidia = Table('midia', metadata,
                   Column('quantidade', Integer, nullable=False)
                   )
insertMidia = tableMidia.insert()
fake = Faker()


def insereQuantidadeEmMidia(quantidadeLinhas):
    stmt = 'UPDATE midia SET quantidade = {} WHERE midiaid = {}'
    for i in range(1, quantidadeLinhas + 1):
        quantidade = random.randrange(0, 100)
        aux = stmt.format(quantidade, i)
        conn.execute(aux)


# postgresql://usuario:senha@host:port/database
engine = create_engine('postgresql://postgres:123@localhost:5432/postgres')
conn = engine.connect()


insereQuantidadeEmMidia(130)
