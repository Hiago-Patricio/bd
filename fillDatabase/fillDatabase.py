import random

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy import create_engine, Column, ForeignKey, UniqueConstraint, Integer
from generateData import *

Base = automap_base()

class AutorMidia(Base):
    __tablename__ = 'autormidia'
    fkautorid = Column(Integer, ForeignKey('autor.autorid'), nullable=False, primary_key=True)
    fkmidiaid = Column(Integer, ForeignKey('midia.midiaid'), nullable=False, primary_key=True)


user = 'postgres'
password = '123'
engine = create_engine('postgresql://{}:{}@localhost:5432/livraria'.format(user, password))
Base.prepare(engine, reflect=True)

GeneroTable = Base.classes.genero
TipoMidiaTable = Base.classes.tipomidia
MidiaTable = Base.classes.midia
LivroTable = Base.classes.livro
MangaTable = Base.classes.manga
VolumeTable = Base.classes.volume
RevistaTable = Base.classes.revista
AutorTable = Base.classes.autor
AutorMidiaTable = AutorMidia
FuncionarioTable = Base.classes.funcionario
ClienteTable = Base.classes.cliente
CompraTable = Base.classes.compra
ProdutosCompradosTable = Base.classes.produtoscomprados


def insereGenero(quantidade=1):
    stmt = "INSERT INTO genero(nome, localizacao) VALUES('{}','{}');"
    session = Session(engine)
    for i in range(quantidade):
        while True:
            try:
                nome = randomName()
                localizacao = randomName()
                row = GeneroTable(
                    nome=nome,
                    localizacao=localizacao,
                )
                session.add(row)
                session.commit()
                print(stmt.format(nome, localizacao))
                break
            except:
                session.rollback()
                pass
    session.close()


def insereTipoMidia(quantidade=1):
    stmt = "INSERT INTO tipomidia(nome) VALUES('{}');"
    session = Session(engine)
    for i in range(quantidade):
        while True:
            try:
                nome = randomName()
                row = TipoMidiaTable(
                    nome=nome,
                )
                session.add(row)
                session.commit()
                print(stmt.format(nome))
                break
            except:
                session.rollback()
                pass
    session.close()


def insereMidia(quantidade=1, fkGeneroIdLista=[], fkTipoMidiaIdLista=[]):
    stmt = "INSERT INTO midia(fkgeneroid, fktipomidiaid, datapublicacao, editora, nome, idioma, localpublicacao, precomidia, quantidade) VALUES({}, {}, '{}', '{}', '{}', '{}', '{}', {}, {});"
    session = Session(engine)
    if fkGeneroIdLista == []:
        for class_instance in session.query(GeneroTable).all():
            fkGeneroIdLista.append(vars(class_instance)['generoid'])

    if fkTipoMidiaIdLista == []:
        for class_instance in session.query(TipoMidiaTable).all():
            fkTipoMidiaIdLista.append(vars(class_instance)['tipomidiaid'])

    for i in range(quantidade):
        while True:
            try:
                fkGeneroId = random.choice(fkGeneroIdLista)
                fkTipoMidiaId = random.choice(fkTipoMidiaIdLista)
                dataPublicacao = randomDate()
                editora = randomName()
                nome = randomName()
                idioma = randomName()
                localPublicacao = randomName()
                precoMidia = randomFloat(20, 100)
                quantidade = randomInteger(0, 100)
                row = MidiaTable(
                    fkgeneroid=fkGeneroId,
                    fktipomidiaid=fkTipoMidiaId,
                    datapublicacao=dataPublicacao,
                    editora=editora,
                    nome=nome,
                    idioma=idioma,
                    localpublicacao=localPublicacao,
                    precomidia=precoMidia,
                    quantidade=quantidade,
                )
                session.add(row)
                session.commit()
                print(stmt.format(fkGeneroId, fkTipoMidiaId, dataPublicacao, editora, nome, idioma, localPublicacao, precoMidia, quantidade))
                break
            except:
                session.rollback()
                pass
    session.close()


def insereLivro(quantidade=1, fkMidiaIdLista=[]):
    stmt="INSERT INTO livro(fkmidiaid, sinopse, edicao, paginas) VALUES({}, '{}', {}, {});"
    session = Session(engine)
    if fkMidiaIdLista == []:
        for class_instance in session.query(MidiaTable).all():
            fkMidiaIdLista.append(vars(class_instance)['midiaid'])

    for i in range(quantidade):
        while True:
            try:
                fkMidiaId = random.choice(fkMidiaIdLista)
                fkMidiaIdLista.remove(fkMidiaId)
                sinopse = randomText()
                edicao = randomInteger(1, 100)
                paginas = randomInteger(1, 500)
                row = LivroTable(
                    fkmidiaid=fkMidiaId,
                    sinopse=sinopse,
                    edicao=edicao,
                    paginas=paginas,
                )
                session.add(row)
                session.commit()
                print(stmt.format(fkMidiaId, sinopse, edicao, paginas))
                break
            except:
                session.rollback()
                pass
    session.close()


def insereManga(quantidade=1):
    stmt="INSERT INTO manga(nome, adaptacaoanime, finalizado) VALUES('{}',{}, {});"
    session = Session(engine)
    for i in range(quantidade):
        while True:
            try:
                nome = randomName()
                adaptacaoAnime = randomBoolean()
                finalizado = randomBoolean()
                row = MangaTable(
                    nome=nome,
                    adaptacaoanime=adaptacaoAnime,
                    finalizado=finalizado,
                )
                session.add(row)
                session.commit()
                print(stmt.format(nome, adaptacaoAnime, finalizado))
                break
            except:
                session.rollback()
                pass
    session.close()


def insereVolume(quantidade=1, fkMangaIdLista=[], fkMidiaIdLista=[]):
    stmt="INSERT INTO volume(fkmangaid, fkmidiaid, sinopse, numero, quantidadecapitulos) VALUES({}, {}, '{}', {}, {});"
    session = Session(engine)
    if fkMangaIdLista == []:
        for class_instance in session.query(MangaTable).all():
            fkMangaIdLista.append(vars(class_instance)['mangaid'])

    if fkMidiaIdLista == []:
        for class_instance in session.query(MidiaTable).all():
            fkMidiaIdLista.append(vars(class_instance)['midiaid'])

    for i in range(quantidade):
        while True:
            try:
                if fkMidiaIdLista == []:
                    break

                fkMangaId = random.choice(fkMangaIdLista)
                fkMidiaId = random.choice(fkMidiaIdLista)
                fkMidiaIdLista.remove(fkMidiaId)
                sinopse = randomText()
                numero = randomFloat(1, 100)
                quantidadeCapitulos = randomInteger(5, 120)
                row = VolumeTable(
                    fkmangaid=fkMangaId,
                    fkmidiaid=fkMidiaId,
                    sinopse=sinopse,
                    numero=numero,
                    quantidadecapitulos=quantidadeCapitulos,
                )
                session.add(row)
                session.commit()
                print(stmt.format(fkMangaId, fkMidiaId, sinopse, numero, quantidadeCapitulos))
                break
            except:
                session.rollback()
                pass
    session.close()


def insereRevista(quantidade=1, fkMidiaIdLista=[]):
    stmt="INSERT INTO revista(fkmidiaid, empresa, edicao) VALUES({}, '{}', {});"
    session = Session(engine)
    if fkMidiaIdLista == []:
        for class_instance in session.query(MidiaTable).all():
            fkMidiaIdLista.append(vars(class_instance)['midiaid'])

    for i in range(quantidade):
        while True:
            try:
                if fkMidiaIdLista == []:
                    break

                fkMidiaId = random.choice(fkMidiaIdLista)
                fkMidiaIdLista.remove(fkMidiaId)
                empresa = randomName()
                edicao = randomInteger(1, 100)
                row = RevistaTable(
                    fkmidiaid=fkMidiaId,
                    empresa=empresa,
                    edicao=edicao,
                )
                session.add(row)
                session.commit()
                print(stmt.format(fkMidiaId, empresa, edicao))
                break
            except:
                session.rollback()
                pass
    session.close()


def insereAutor(quantidade=1):
    stmt="INSERT INTO autor(nacionalidade, nome, datanascimento, datafalecimento) VALUES('{}', '{}', '{}', '{}');"
    session = Session(engine)
    for i in range(quantidade):
        while True:
            try:
                nacionalidade = randomName()
                nome = randomName()
                dataNascimento = randomDate()
                dataFalecimento = randomDate()
                row = AutorTable(
                    nacionalidade=nacionalidade,
                    nome=nome,
                    datanascimento=dataNascimento,
                    datafalecimento=dataFalecimento,
                )
                session.add(row)
                session.commit()
                print(stmt.format(nacionalidade, nome, dataNascimento, dataFalecimento))
                break
            except:
                session.rollback()
                pass
    session.close()


def insereAutorMidia(quantidade=1, fkAutorIdLista=[], fkMidiaIdLista=[]):
    stmt="INSERT INTO autormidia(fkautorid, fkmidiaid) VALUES({}, {});"
    session = Session(engine)
    if fkAutorIdLista == []:
        for class_instance in session.query(AutorTable).all():
            fkAutorIdLista.append(vars(class_instance)['autorid'])

    if fkMidiaIdLista == []:
        for class_instance in session.query(MidiaTable).all():
            fkMidiaIdLista.append(vars(class_instance)['midiaid'])

    for i in range(quantidade):
        while True:
            try:
                fkAutorId = random.choice(fkAutorIdLista)
                fkMidiaId = random.choice(fkMidiaIdLista)
                row = AutorMidiaTable(
                    fkautorid=fkAutorId,
                    fkmidiaid=fkMidiaId,
                )
                session.add(row)
                session.commit()
                print(stmt.format(fkAutorId, fkMidiaId))
                break
            except:
                session.rollback()
                pass
    session.close()


def insereFuncionario(quantidade=1):
    stmt="INSERT INTO funcionario(funcao, nome, salario, dataadmissao) VALUES('{}', '{}', {}, '{}');"
    session = Session(engine)
    for i in range(quantidade):
        while True:
            try:
                funcao = randomName()
                nome = randomName()
                salario = randomFloat(1000, 5000)
                dataAdmissao = randomDate()
                row = FuncionarioTable(
                    funcao=funcao,
                    nome=nome,
                    salario=salario,
                    dataadmissao=dataAdmissao,
                )
                session.add(row)
                session.commit()
                print(stmt.format(funcao, nome, salario, dataAdmissao))
                break
            except:
                session.rollback()
                pass
    session.close()


def insereCliente(quantidade=1):
    stmt="INSERT INTO cliente(endereco, sexo, nome, datanascimento) VALUES('{}', '{}', '{}', '{}');"
    session = Session(engine)
    for i in range(quantidade):
        while True:
            try:
                endereco = randomName()
                sexo = randomSex()
                nome = randomName()
                dataNascimento = randomDate()
                row = ClienteTable(
                    endereco=endereco,
                    sexo=sexo,
                    nome=nome,
                    datanascimento=dataNascimento,
                )
                session.add(row)
                session.commit()
                print(stmt.format(endereco, sexo, nome, dataNascimento))
                break
            except:
                session.rollback()
                pass
    session.close()


def insereCompra(quantidade=1, fkClienteIdLista=[], fkFuncionarioIdLista=[]):
    stmt="INSERT INTO compra(fkclienteid, fkfuncionarioid, data) VALUES ({}, {}, '{}');"
    session = Session(engine)
    if fkClienteIdLista == []:
        for class_instance in session.query(ClienteTable).all():
            fkClienteIdLista.append(vars(class_instance)['clienteid'])

    if fkFuncionarioIdLista == []:
        for class_instance in session.query(FuncionarioTable).all():
            fkFuncionarioIdLista.append(vars(class_instance)['funcionarioid'])

    for i in range(quantidade):
        while True:
            try:
                fkClienteId = random.choice(fkClienteIdLista)
                fkFuncionarioId = random.choice(fkFuncionarioIdLista)
                data = randomDate()
                row = CompraTable(
                    fkclienteid=fkClienteId,
                    fkfuncionarioid=fkFuncionarioId,
                    data=data,
                )
                session.add(row)
                session.commit()
                print(stmt.format(fkClienteId, fkFuncionarioId, data))
                break
            except:
                session.rollback()
                pass
    session.close()


def insereProdutosComprados(quantidade=1, fkCompraIdLista=[], fkMidiaIdLista=[]):
    stmt="INSERT INTO produtoscomprados(fkcompraid, fkmidiaid, quantidade) VALUES({}, {}, {});"
    session = Session(engine)
    if fkCompraIdLista == []:
        for class_instance in session.query(CompraTable).all():
            fkCompraIdLista.append(vars(class_instance)['compraid'])

    if fkMidiaIdLista == []:
        for class_instance in session.query(MidiaTable).all():
            fkMidiaIdLista.append(vars(class_instance)['midiaid'])

    for i in range(quantidade):
        while True:
            try:
                fkCompraId = random.choice(fkCompraIdLista)
                fkMidiaId = random.choice(fkMidiaIdLista)
                quantidade = randomInteger(1, 100)
                row = ProdutosCompradosTable(
                    fkcompraid=fkCompraId,
                    fkmidiaid=fkMidiaId,
                    quantidade=quantidade,
                )
                session.add(row)
                session.commit()
                print(stmt.format(fkCompraId, fkMidiaId, quantidade))
                break
            except:
                session.rollback()
                pass
    session.close()


insereGenero(quantidade=20)
insereTipoMidia(quantidade=3)
insereMidia(quantidade=130, fkGeneroIdLista=[], fkTipoMidiaIdLista=[])
insereLivro(quantidade=50, fkMidiaIdLista=[])
insereManga(quantidade=16)
insereVolume(quantidade=40, fkMangaIdLista=[], fkMidiaIdLista=[])
insereRevista(quantidade=40, fkMidiaIdLista=[])
insereAutor(quantidade=72)
insereAutorMidia(quantidade=130, fkAutorIdLista=[], fkMidiaIdLista=[])
insereFuncionario(quantidade=13)
insereCliente(quantidade=1200)

# Cria 50 vips
session = Session(engine)
fkClienteIdLista=[]
for class_instance in session.query(ClienteTable).all():
    fkClienteIdLista.append(vars(class_instance)['clienteid'])

for i in range(50):
    fkClienteId = random.choice(fkClienteIdLista)
    fkClienteIdLista.remove(fkClienteId)
    insereCompra(100, fkClienteIdLista=[fkClienteId], fkFuncionarioIdLista=[])
# Completa a inserção com Compras randoms
insereCompra(quantidade=54000 - 50 * 100, fkClienteIdLista=[], fkFuncionarioIdLista=[])

# Insere ao menos uma midia em cada produtosComprados
fkCompraIdLista=[]
for class_instance in session.query(CompraTable).all():
    fkCompraIdLista.append(vars(class_instance)['compraid'])

insereProdutosComprados(quantidade=54000, fkCompraIdLista=fkCompraIdLista, fkMidiaIdLista=[])
insereProdutosComprados(quantidade=126000 - 54000, fkCompraIdLista=[], fkMidiaIdLista=[])
session.close()