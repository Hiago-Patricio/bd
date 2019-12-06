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
    # Column('produtoscompradosid', Integer, Sequence('produtoscompradosid'), primary_key=True, nullable=False),
    Column('fkcompraid', None, ForeignKey('compra.compraid'), nullable=False),
    Column('fkmidiaid', None, ForeignKey('midia.midiaid'), nullable=False),
    Column('quantidade', Integer, nullable=False),
    # Column('precounidade', Float, nullable=False),
    # Column('descontounidade', Float, nullable=False),
    UniqueConstraint('fkcompraid', 'fkmidiaid'),
)
insertProdutosComprados = tableProdutosComprados.insert()

fake = Faker()
def insereGenero():
    try:
        stmt = "SELECT nextval('genero_generoid_seq')"
        generoId = conn.execute(stmt).fetchone()[0]
        nome = fake.name()
        localizacao = fake.name()
        values = (generoId, nome, localizacao, )
        conn.execute(insertGenero.values(values))
        return True
    except:
        return False


def insereTipoMidia():
    try:
        stmt = "SELECT nextval('tipoMidia_tipoMidiaId_seq')"
        tipoMidiaId = conn.execute(stmt).fetchone()[0]
        nome = fake.name()
        values = (tipoMidiaId, nome, )
        conn.execute(insertTipoMidia.values(values))
        return True
    except:
        return False


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
        return True
    except:
        return False


def insereLivro():
    try:
        stmt = "SELECT nextval('livro_livroId_seq')"
        livroId = conn.execute(stmt).fetchone()[0]
        stmt = select([tableMidia]).order_by(func.random())
        # fkMidiaId = conn.execute(stmt).fetchone()['midiaid']
        fkMidiaId = lastIdMidia
        sinopse = fake.text()
        edicao = random.randrange(1, 100)
        paginas = random.randrange(1, 500)
        values = (livroId, fkMidiaId, sinopse, edicao, paginas, )
        conn.execute(insertLivro.values(values))
        return True
    except:
        return False


def insereManga():
    try:
        stmt = "SELECT nextval('manga_mangaId_seq')"
        mangaId = conn.execute(stmt).fetchone()[0]
        nome = fake.name()
        adaptacaoAnime = bool(random.randrange(0, 2))
        finalizado = bool(random.randrange(0, 2))
        values = (mangaId, nome, adaptacaoAnime, finalizado, )
        conn.execute(insertManga.values(values))
        return True
    except:
        return False


def insereVolume():
    try:
        stmt = "SELECT nextval('volume_volumeId_seq')"
        volumeId = conn.execute(stmt).fetchone()[0]
        stmt = select([tableMidia]).order_by(func.random())
        # fkMidiaId = conn.execute(stmt).fetchone()['midiaid']
        fkMidiaId = lastIdMidia
        stmt = select([tableManga]).order_by(func.random())
        fkMangaId = conn.execute(stmt).fetchone()['mangaid']
        sinopse = fake.text()
        numero = round(random.uniform(20, 100), 2)
        quantidadeCapitulos = random.randrange(1, 100)
        values = (volumeId, fkMidiaId, fkMangaId, sinopse, numero, quantidadeCapitulos, )
        conn.execute(insertVolume.values(values))
        return True
    except:
        return False


def insereRevista():
    try:
        stmt = "SELECT nextval('revista_revistaId_seq')"
        revistaId = conn.execute(stmt).fetchone()[0]
        stmt = select([tableMidia]).order_by(func.random())
        # fkMidiaId = conn.execute(stmt).fetchone()['midiaid']
        fkMidiaId = lastIdMidia
        empresa = fake.name()
        edicao = random.randrange(0, 100)
        values = (revistaId, fkMidiaId, empresa, edicao, )
        conn.execute(insertRevista.values(values))
        return True
    except:
        return False


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
        return True
    except:
        return False


def insereAutorMidia():
    try:
        stmt = select([tableAutor]).order_by(func.random())
        fkAutorId = conn.execute(stmt).fetchone()['autorid']
        stmt = select([tableMidia]).order_by(func.random())
        fkMidiaId = conn.execute(stmt).fetchone()['midiaid']
        fkMidiaId = lastIdMidia
        values = (fkAutorId, fkMidiaId, )
        conn.execute(insertAutorMidia.values(values))
        return True
    except:
        return False


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
        return True
    except:
        return False


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
        return True
    except:
        return False


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
        return True
    except:
        return False


def insereProdutosComprados():
    try:
        fkCompraId = random.randrange(1, 54002)
        fkMidiaId = random.randrange(1, 131)
        quantidade = random.randrange(1, 130)
        values = (fkCompraId, fkMidiaId, quantidade, )
        conn.execute(insertProdutosComprados.values(fkcompraid=fkCompraId, fkmidiaid=fkMidiaId, quantidade=quantidade, ))
        return True
    except:
        return False


# postgresql://usuario:senha@host:port/database
engine = create_engine('postgresql://postgres:123@localhost:5432/postgres')
conn = engine.connect()

# print('Genero')
# quantidade = 0
# for i in range(20):
#     quantidade += insereGenero()
# print('Quantidade: ', quantidade)

# print('TipoMidia')
# quantidade = 0
# for i in range(3):
#     quantidade += insereTipoMidia()
# print('Quantidade: ', quantidade)

# print('Midia')
# quantidade = 0
# for i in range(130):
#     quantidade += insereMidia()
# print('Quantidade: ', quantidade)

# lastIdMidia = 0Client
# print('Livro')
# quantidade = 0
# for i in range(50):
#     lastIdMidia += 1
#     quantidade += insereLivro()
# print('Quantidade: ', quantidade)

# print('Manga')
# quantidade = 0
# for i in range(16):
#     quantidade += insereManga()
# print('Quantidade: ', quantidade)

# print('Volume')
# quantidade = 0
# lastIdMidia = 50
# for i in range(40):
#     lastIdMidia += 1
#     quantidade += insereVolume()
# print('Quantidade: ', quantidade)

# print('Revista')
# quantidade = 0
# lastIdMidia = 90
# for i in range(40):
#     lastIdMidia += 1
#     quantidade += insereRevista()
# print('Quantidade: ', quantidade)Client
# print('Autor')
# quantidade = 0
# for i in range(72):
#     quantidade += insereAutor()
# print('Quantidade: ', quantidade)

# print('AutorMidia')
# quantidade = 0
# lastIdMidia = 0
# for i in range(130):
#     lastIdMidia += 1
#     quantidade += insereAutorMidia()
# print('Quantidade: ', quantidade)

# print('Funcionario')
# quantidade = 0
# for i in range(13):
#     quantidade += insereFuncionario()
# print('Quantidade: ', quantidade)

# print('Cliente')
# quantidade = 0
# for i in range(1200):
#     quantidade += insereCliente()
# print('Quantidade: ', quantidade)

# print('Compra')
# quantidade = 0
# for i in range(54000):
#     quantidade += insereCompra()
#     if i % 100 == 0:
#         print(i)
# print('Quantidade: ', quantidade)

print('ProdutosComprados')
quantidade = 0
# for i in range(126000):
while(quantidade < 126000):
    quantidade += insereProdutosComprados()
    if quantidade % 100 == 0:
        print(quantidade)
print('Quantidade: ', quantidade)