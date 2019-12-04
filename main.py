import datetime, random
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, Date, Float, Text, Boolean, \
    UniqueConstraint, Sequence, create_engine, select, func
from sqlalchemy.dialects import postgresql
from faker import Faker


file_name = 'popular_banco.sql'
def write_in_file(content: str):
	with open(file_name, 'a') as file:
		file.write(content + '\n')
		file.close()


def random_sex():
    sex = ['M', 'F']
    return sex[random.randrange(0,2)]


def validate_date(day: int, mounth: int, year: int):
    try:
        datetime.date(year, mounth, day)
        return True
    except:
        return False


def random_date():
    day = random.randrange(1, 32)
    mounth = random.randrange(1, 13)
    year = random.randrange(1900, 2019)
    while (not (validate_date(day, mounth, year))):
        day = random.randrange(1, 32)
        mounth = random.randrange(1, 13)
        year = random.randrange(1900, 2019)
    date = '{}-{}-{}'.format(year, mounth, day)
    return date


metadata = MetaData()
tableGenero = Table('genero', metadata,
    Column('generoid', Integer, Sequence('generoid'), primary_key=True, nullable=False),
    Column('nome', String(255), unique=True, nullable=False),
    Column('localizacao', String(255), nullable=False),
)
insertGenero = tableGenero.insert()

tableTipoMidia = Table('tipomidia', metadata,
    Column('tipomidiaid', Integer, Sequence('tipomidiaid'), primary_key=True, nullable=False),
    Column('nome', String(255), unique=True, nullable=False),
)
insertTipoMidia = tableTipoMidia.insert()

tableMidia = Table('midia', metadata,
    Column('midiaid', Integer, Sequence('midiaid'), primary_key=True, nullable=False),
    Column('fkgeneroid', None, ForeignKey('genero.generoid'), nullable=False),
    Column('fktipomidiaid', None, ForeignKey('tipomidia.tipomidiaid'), nullable=False),
    Column('datapublicacao', Date, nullable=False),
    Column('editora', String(255), nullable=False),
    Column('nome', String(255), nullable=False),
    Column('idioma', String(255), nullable=False),
    Column('localpublicacao', String(255), nullable=False),
    Column('precomidia', Float, nullable=False),
)
insertMidia = tableMidia.insert()

tableLivro = Table('livro', metadata,
    Column('livroid', Integer, Sequence('livroid'), primary_key=True, nullable=False),
    Column('fkmidiaid', None, ForeignKey('midia.midiaid'), unique=True, nullable=False),
    Column('sinopse', Text, nullable=False),
    Column('edicao', Integer, nullable=False),
    Column('paginas', Integer, nullable=False),
)
insertLivro = tableLivro.insert()

tableManga = Table('manga', metadata,
    Column('mangaid', Integer, Sequence('mangaid'), primary_key=True, nullable=False),
    Column('nome', String(255), nullable=False),
    Column('adaptacaoanime', Boolean, nullable=False),
    Column('finalizado', Boolean, nullable=False),
)
insertManga = tableManga.insert()

tableVolume = Table('volume', metadata,
    Column('volumeid', Integer, Sequence('volumeid'), primary_key=True, nullable=False),
    Column('fkmidiaid', None, ForeignKey('midia.midiaid'), unique=True, nullable=False),
    Column('fkmangaid', None, ForeignKey('manga.mangaid'), nullable=False),
    Column('sinopse', Text, nullable=False),
    Column('numero', Float, nullable=False),
    Column('quantidadecapitulos', Integer, nullable=False),
)
insertVolume = tableVolume.insert()

tableRevista = Table('revista', metadata,
    Column('revistaid', Integer, Sequence('revistaid'), primary_key=True, nullable=False),
    Column('fkmidiaid', None, ForeignKey('midia.midiaid'), unique=True, nullable=False),
    Column('empresa', String(255), nullable=False),
    Column('edicao', Integer, nullable=False),
)
insertRevista = tableRevista.insert()

tableAutor = Table('autor', metadata,
    Column('autorid', Integer, Sequence('autorid'), primary_key=True, nullable=False),
    Column('nacionalidade', String(255), nullable=False),
    Column('nome', String(255), nullable=False),
    Column('datanascimento', Date, nullable=False),
    Column('datafalecimento', Date, nullable=False),
)
insertAutor = tableAutor.insert()

tableAutorMidia = Table('autormidia', metadata,
    Column('fkautorid', None, ForeignKey('autor.autorid'), nullable=False),
    Column('fkmidiaid', None, ForeignKey('midia.midiaid'), nullable=False),
    UniqueConstraint('fkautorid', 'fkmidiaid'),
)
insertAutorMidia = tableAutorMidia.insert()

tableFuncionario = Table('funcionario', metadata,
    Column('funcionarioid', Integer, Sequence('funcionarioid'), primary_key=True, nullable=False),
    Column('funcao', String(255), nullable=False),
    Column('nome', String(255), nullable=False),
    Column('salario', Float, nullable=False),
    Column('dataadmissao', Date, nullable=False),
)
insertFuncionario = tableFuncionario.insert()

tableCliente = Table('cliente', metadata,
    Column('clienteid', Integer, Sequence('clienteid'), primary_key=True, nullable=False),
    Column('quantidadecompras', Integer, nullable=False),
    Column('endereco', String(255), nullable=False),
    Column('sexo', String(255), nullable=False),
    Column('nome', String(255), nullable=False),
    Column('datanascimento', Date, nullable=False),
    # Column('vip', Boolean, nullable=False),
)
insertCliente = tableCliente.insert()

tableCompra = Table('compra', metadata,
    Column('compraid', Integer, Sequence('compraid'), primary_key=True, nullable=False),
    Column('fkclienteid', None, ForeignKey('cliente.clienteid'), nullable=False),
    Column('fkfuncionarioid', None, ForeignKey('funcionario.funcionarioid'), nullable=False),
    Column('data', Date, nullable=False),
)
insertCompra = tableCompra.insert()

tableProdutosComprados = Table('produtoscomprados', metadata,
    Column('produtoscompradosid', Integer, Sequence('produtoscompradosid'), primary_key=True, nullable=False),
    Column('fkcompraid', None, ForeignKey('compra.compraid'), nullable=False),
    Column('fkmidiaid', None, ForeignKey('midia.midiaid'), nullable=False),
    Column('quantidade', Integer, nullable=False),
    # Column('precounidade', Float, nullable=False),
    # Column('descontounidade', Float, nullable=False),
    UniqueConstraint('fkcompraid', 'fkmidiaid'),
)
insertProdutosComprados = tableProdutosComprados.insert()


def insereGenero():
    try:
        stmt = "SELECT nextval('genero_generoid_seq')"
        generoId = conn.execute(stmt).fetchone()[0]
        nome = fake.name()
        localizacao = fake.name()
        values = (generoId, nome, localizacao, )
        conn.execute(insertGenero.values(values))
        query = str(insertGenero.compile(dialect=postgresql.dialect()))
        query = query % {'generoid': generoId, 'nome': nome, 'localizacao': localizacao}
        write_in_file(query)
    except:
        pass


def insereTipoMidia():
    try:
        stmt = "SELECT nextval('tipoMidia_tipoMidiaId_seq')"
        tipoMidiaId = conn.execute(stmt).fetchone()[0]
        nome = fake.name()
        values = (tipoMidiaId, nome, )
        conn.execute(insertTipoMidia.values(values))
        query = str(insertTipoMidia.compile(dialect=postgresql.dialect()))
        query = query % {'tipomidiaid':tipoMidiaId, 'nome':nome, }
        write_in_file(query)
    except:
        pass


def insereMidia():
    try:
        stmt = "SELECT nextval('midia_midiaId_seq')"
        midiaId = conn.execute(stmt).fetchone()[0]
        stmt = select([tableGenero]).order_by(func.random())
        fkGeneroId = conn.execute(stmt).fetchone()['generoid']
        stmt = select([tableTipoMidia]).order_by(func.random())
        fkTipoMidiaId = conn.execute(stmt).fetchone()['tipomidiaid']
        dataPublicacao = random_date()
        editora = fake.name()
        nome = fake.name()
        idioma = fake.name()
        localPublicacao = fake.name()
        precoMidia = round(random.uniform(20, 100), 2)
        values = (midiaId, fkGeneroId, fkTipoMidiaId, dataPublicacao, editora, nome, idioma, localPublicacao, precoMidia, )
        conn.execute(insertMidia.values(values))
        query = str(insertMidia.compile(dialect=postgresql.dialect()))
        query = query % {'midiaid':midiaId, 'fkgeneroid':fkGeneroId, 'fktipomidiaid':fkTipoMidiaId,
                         'datapublicacao':dataPublicacao, 'editora':editora, 'nome':nome, 'idioma':idioma,
                         'localpublicacao':localPublicacao, 'precomidia':precoMidia, }
        write_in_file(query)
    except:
        pass


def insereLivro():
    try:
        stmt = "SELECT nextval('livro_livroId_seq')"
        livroId = conn.execute(stmt).fetchone()[0]
        stmt = select([tableMidia]).order_by(func.random())
        fkMidiaId = conn.execute(stmt).fetchone()['midiaid']
        sinopse = fake.text()
        edicao = random.randrange(1, 100)
        paginas = random.randrange(1, 500)
        values = (livroId, fkMidiaId, sinopse, edicao, paginas, )
        conn.execute(insertLivro.values(values))
        query = str(insertLivro.compile(dialect=postgresql.dialect()))
        query = query % {'livroid': livroId, 'fkmidiaid': fkMidiaId, 'sinopse': sinopse, 'edicao': edicao,
                         'paginas': paginas, }
        write_in_file(query)
    except:
        pass


def insereManga():
    try:
        stmt = "SELECT nextval('manga_mangaId_seq')"
        mangaId = conn.execute(stmt).fetchone()[0]
        nome = fake.name()
        adaptacaoAnime = bool(random.randrange(0, 2))
        finalizado = bool(random.randrange(0, 2))
        values = (mangaId, nome, adaptacaoAnime, finalizado, )
        conn.execute(insertManga.values(values))
        query = str(insertManga.compile(dialect=postgresql.dialect()))
        query = query % {'mangaid': mangaId, 'nome': nome, 'adaptacaoanime': adaptacaoAnime, 'finalizado': finalizado, }
        write_in_file(query)
    except:
        pass


def insereVolume():
    try:
        stmt = "SELECT nextval('volume_volumeId_seq')"
        volumeId = conn.execute(stmt).fetchone()[0]
        stmt = select([tableMidia]).order_by(func.random())
        fkMidiaId = conn.execute(stmt).fetchone()['midiaid']
        stmt = select([tableManga]).order_by(func.random())
        fkMangaId = conn.execute(stmt).fetchone()['mangaid']
        sinopse = fake.text()
        numero = round(random.uniform(20, 100), 2)
        quantidadeCapitulos = random.randrange(1, 100)
        values = (volumeId, fkMidiaId, fkMangaId, sinopse, numero, quantidadeCapitulos, )
        conn.execute(insertVolume.values(values))
        query = str(insertVolume.compile(dialect=postgresql.dialect()))
        query = query % {'volumeid': volumeId, 'fkmidiaid': fkMidiaId, 'fkmangaid': fkMangaId, 'sinopse': sinopse,
                         'numero': numero, 'quantidadecapitulos': quantidadeCapitulos, }
        write_in_file(query)
    except:
        pass


def insereRevista():
    try:
        stmt = "SELECT nextval('revista_revistaId_seq')"
        revistaId = conn.execute(stmt).fetchone()[0]
        stmt = select([tableMidia]).order_by(func.random())
        fkMidiaId = conn.execute(stmt).fetchone()['midiaid']
        empresa = fake.name()
        edicao = random.randrange(0, 100)
        values = (revistaId, fkMidiaId, empresa, edicao, )
        conn.execute(insertRevista.values(values))
        query = str(insertRevista.compile(dialect=postgresql.dialect()))
        query = query % {'revistaid': revistaId, 'fkmidiaid': fkMidiaId, 'empresa': empresa, 'edicao': edicao, }
        write_in_file(query)
    except:
        pass


def insereAutor():
    try:
        stmt = "SELECT nextval('autor_autorId_seq')"
        autorId = conn.execute(stmt).fetchone()[0]
        nacionalidade = fake.name()
        nome = fake.name()
        dataNascimento = random_date()
        dataFalecimento = random_date()
        values = (autorId, nacionalidade, nome, dataNascimento, dataFalecimento, )
        conn.execute(insertAutor.values(values))
        query = str(insertAutor.compile(dialect=postgresql.dialect()))
        query = query % {'autorid': autorId, 'nacionalidade': nacionalidade, 'nome': nome,
                         'datanascimento': dataNascimento, 'datafalecimento': dataFalecimento, }
        write_in_file(query)
    except:
        pass


def insereAutorMidia():
    try:
        stmt = select([tableAutor]).order_by(func.random())
        fkAutorId = conn.execute(stmt).fetchone()['autorid']
        stmt = select([tableMidia]).order_by(func.random())
        fkMidiaId = conn.execute(stmt).fetchone()['midiaid']
        values = (fkAutorId, fkMidiaId, )
        conn.execute(insertAutorMidia.values(values))
        query = str(insertAutorMidia.compile(dialect=postgresql.dialect()))
        query = query % {'fkautorid': fkAutorId, 'fkmidiaid': fkMidiaId, }
        write_in_file(query)
    except:
        pass


def insereFuncionario():
    try:
        stmt = "SELECT nextval('funcionario_funcionarioId_seq')"
        funcionarioId = conn.execute(stmt).fetchone()[0]
        funcao = fake.name()
        nome = fake.name()
        salario = round(random.uniform(20, 100), 2)
        dataAdmissao = random_date()
        values = (funcionarioId, funcao, nome, salario, dataAdmissao, )
        conn.execute(insertFuncionario.values(values))
        query = str(insertFuncionario.compile(dialect=postgresql.dialect()))
        query = query % {'funcionarioid': funcionarioId, 'funcao': funcao, 'nome': nome, 'salario': salario,
                         'dataadmissao': dataAdmissao, }
        write_in_file(query)
    except:
        pass


def insereCliente():
    try:
        stmt = "SELECT nextval('cliente_clienteId_seq')"
        clienteId = conn.execute(stmt).fetchone()[0]
        quantidadeCompras = 0
        endereco = fake.name()
        sexo = random_sex()
        nome = fake.name()
        dataNascimento = random_date()
        values = (clienteId, quantidadeCompras, endereco, sexo, nome, dataNascimento, )
        conn.execute(insertCliente.values(values))
        query = str(insertCliente.compile(dialect=postgresql.dialect()))
        query = query % {'clienteid': clienteId, 'quantidadecompras': quantidadeCompras, 'endereco': endereco,
                         'sexo': sexo, 'nome': nome, 'datanascimento': dataNascimento, }
        write_in_file(query)
    except:
        pass


def insereCompra():
    try:
        stmt = "SELECT nextval('compra_compraId_seq')"
        compraId = conn.execute(stmt).fetchone()[0]
        stmt = select([tableCliente]).order_by(func.random())
        fkClienteId = conn.execute(stmt).fetchone()['clienteid']
        stmt = select([tableFuncionario]).order_by(func.random())
        fkFuncionarioId = conn.execute(stmt).fetchone()['funcionarioid']
        data = random_date()
        values = (compraId, fkClienteId, fkFuncionarioId, data, )
        conn.execute(insertCompra.values(values))
        query = str(insertCompra.compile(dialect=postgresql.dialect()))
        query = query % {'compraid': compraId, 'fkclienteid': fkClienteId, 'fkfuncionarioid': fkFuncionarioId,
                         'data': data, }
        write_in_file(query)
    except:
        pass


def insereProdutosComprados():
    try:
        stmt = "SELECT nextval('produtosComprados_produtosCompradosId_seq')"
        produtosCompradosId = conn.execute(stmt).fetchone()[0]
        stmt = select([tableCompra]).order_by(func.random())
        fkCompraId = conn.execute(stmt).fetchone()['compraid']
        stmt = select([tableMidia]).order_by(func.random())
        fkMidiaId = conn.execute(stmt).fetchone()['midiaid']
        quantidade = random.randrange(1, 200)
        values = (produtosCompradosId, fkCompraId, fkMidiaId, quantidade, )
        conn.execute(insertProdutosComprados.values(values))
        query = str(insertProdutosComprados.compile(dialect=postgresql.dialect()))
        query = query % {'produtoscompradosid': produtosCompradosId, 'fkcompraid': fkCompraId, 'fkmidiaid': fkMidiaId,
                         'quantidade': quantidade, }
        write_in_file(query)
    except:
        pass


# postgresql://usuario:senha@host:port/database
engine = create_engine('postgresql://postgres:123@localhost:5432/postgres')
conn = engine.connect()

quantidadeInsercoesCadaTabela = 5000
fake = Faker()
# for i in range(quantidadeInsercoesCadaTabela):
#     insereGenero()
#     insereTipoMidia()
#     insereMidia()
#     insereLivro()
#     insereManga()
#     insereVolume()
#     insereRevista()
#     insereAutor()
#     insereAutorMidia()
#     insereFuncionario()
#     insereCliente()
#     insereCompra()
#     insereProdutosComprados()
#     if i % 100 == 0:
#         print(i)

quantidadeGenero = 20
quantidadeTipoMidia = 3
quantidadeLivro = 50
quantidadeManga = 16
quantidadeVolume = 40
quantidadeRevista = 40
quantidadeMidia = quantidadeLivro + quantidadeVolume + quantidadeRevista
quantidadeAutor = 72
quantidadeAutorMidia = quantidadeMidia
quantidadeFuncionario = 13
quantidadeCliente = 1200
quantidadeCompra = 54000
quantidadeProdutosComprados = 126000

for i in range(20):
    insereGenero()
    print(i)
for i in range(3):
    insereTipoMidia()
    print(i)
for i in range(130):
    insereMidia()
    print(i)
for i in range(50):
    insereLivro()
    print(i)
for i in range(16):
    insereManga()
    print(i)
for i in range(40):
    insereVolume()
    print(i)
for i in range(40):
    insereRevista()
    print(i)
for i in range(72):
    insereAutor()
    print(i)
for i in range(130):
    insereAutorMidia()
    print(i)
for i in range(13):
    insereFuncionario()
    print(i)
for i in range(1200):
    insereCliente()
    print(i)
for i in range(54000):
    insereCompra()
    print(i)
for i in range(126000):
    insereProdutosComprados()
    print(i)