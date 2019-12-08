import datetime, random
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, Date, Float, Text, Boolean, \
    UniqueConstraint, Sequence, create_engine, select, func
from sqlalchemy.dialects import postgresql
from faker import Faker


def random_sex():
    sex = ['M', 'F']
    return sex[random.randrange(0,2)]


def randomDate():
    day = random.randrange(1, 32)
    mounth = random.randrange(1, 13)
    year = random.randrange(1900, 2019)
    while True:
        day = random.randrange(1, 32)
        mounth = random.randrange(1, 13)
        year = random.randrange(1900, 2019)
        try:
            datetime.date(year, mounth, day)
            break
        except:
            pass
    date = '{}-{}-{}'.format(year, mounth, day)
    return date


metadata = MetaData()
tableGenero = Table('genero', metadata,
    # Column('generoid', Integer, Sequence('generoid'), primary_key=True, nullable=False),
    Column('nome', String(255), unique=True, nullable=False),
    Column('localizacao', String(255), nullable=False),
)
insertGenero = tableGenero.insert()

tableTipoMidia = Table('tipomidia', metadata,
    # Column('tipomidiaid', Integer, Sequence('tipomidiaid'), primary_key=True, nullable=False),
    Column('nome', String(255), unique=True, nullable=False),
)
insertTipoMidia = tableTipoMidia.insert()

tableMidia = Table('midia', metadata,
    # Column('midiaid', Integer, Sequence('midiaid'), primary_key=True, nullable=False),
    Column('fkgeneroid', None, ForeignKey('genero.generoid'), nullable=False),
    Column('fktipomidiaid', None, ForeignKey('tipomidia.tipomidiaid'), nullable=False),
    Column('datapublicacao', Date, nullable=False),
    Column('editora', String(255), nullable=False),
    Column('nome', String(255), nullable=False),
    Column('idioma', String(255), nullable=False),
    Column('localpublicacao', String(255), nullable=False),
    Column('precomidia', Float, nullable=False),
    Column('quantidade', Integer, nullable=False),
)
insertMidia = tableMidia.insert()

tableLivro = Table('livro', metadata,
    # Column('livroid', Integer, Sequence('livroid'), primary_key=True, nullable=False),
    Column('fkmidiaid', None, ForeignKey('midia.midiaid'), unique=True, nullable=False),
    Column('sinopse', Text, nullable=False),
    Column('edicao', Integer, nullable=False),
    Column('paginas', Integer, nullable=False),
)
insertLivro = tableLivro.insert()

tableManga = Table('manga', metadata,
    # Column('mangaid', Integer, Sequence('mangaid'), primary_key=True, nullable=False),
    Column('nome', String(255), nullable=False),
    Column('adaptacaoanime', Boolean, nullable=False),
    Column('finalizado', Boolean, nullable=False),
)
insertManga = tableManga.insert()

tableVolume = Table('volume', metadata,
    # Column('volumeid', Integer, Sequence('volumeid'), primary_key=True, nullable=False),
    Column('fkmidiaid', None, ForeignKey('midia.midiaid'), unique=True, nullable=False),
    Column('fkmangaid', None, ForeignKey('manga.mangaid'), nullable=False),
    Column('sinopse', Text, nullable=False),
    Column('numero', Float, nullable=False),
    Column('quantidadecapitulos', Integer, nullable=False),
)
insertVolume = tableVolume.insert()

tableRevista = Table('revista', metadata,
    # Column('revistaid', Integer, Sequence('revistaid'), primary_key=True, nullable=False),
    Column('fkmidiaid', None, ForeignKey('midia.midiaid'), unique=True, nullable=False),
    Column('empresa', String(255), nullable=False),
    Column('edicao', Integer, nullable=False),
)
insertRevista = tableRevista.insert()

tableAutor = Table('autor', metadata,
    # Column('autorid', Integer, Sequence('autorid'), primary_key=True, nullable=False),
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
    # Column('funcionarioid', Integer, Sequence('funcionarioid'), primary_key=True, nullable=False),
    Column('funcao', String(255), nullable=False),
    Column('nome', String(255), nullable=False),
    Column('salario', Float, nullable=False),
    Column('dataadmissao', Date, nullable=False),
)
insertFuncionario = tableFuncionario.insert()

tableCliente = Table('cliente', metadata,
    # Column('clienteid', Integer, Sequence('clienteid'), primary_key=True, nullable=False),
    # Column('quantidadecompras', Integer, nullable=False),
    Column('endereco', String(255), nullable=False),
    Column('sexo', String(255), nullable=False),
    Column('nome', String(255), nullable=False),
    Column('datanascimento', Date, nullable=False),
    # Column('vip', Boolean, nullable=False),
)
insertCliente = tableCliente.insert()

tableCompra = Table('compra', metadata,
    # Column('compraid', Integer, Sequence('compraid'), primary_key=True, nullable=False),
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
        nome = fake.name()
        localizacao = fake.name()
        values = (nome, localizacao, )
        conn.execute(insertGenero.values(values))
        return True
    except:
        return False


def insereTipoMidia():
    try:
        nome = fake.name()
        values = (nome, )
        conn.execute(insertTipoMidia.values(values))
        return True
    except:
        return False


def insereMidia(quantidadeLinhasGenero = 0, quantidadeLinhasTipoMidia = 0,
    fkGeneroIdDesejada = 0, fkTipoMidiaIdDesejada = 0):
    try:
        if fkGeneroIdDesejada != 0:
            fkGeneroId = fkGeneroIdDesejada
        else:
            fkGeneroId = random.randrange(1,quantidadeLinhasGenero+1)
        
        if fkTipoMidiaIdDesejada != 0:
            fkTipoMidiaId = fkTipoMidiaIdDesejada
        else:
            fkTipoMidiaId = random.randrange(1,quantidadeLinhasTipoMidia+1)
        
        dataPublicacao = randomDate()
        editora = fake.name()
        nome = fake.name()
        idioma = fake.name()
        localPublicacao = fake.name()
        precoMidia = round(random.uniform(20, 100), 2)
        quantidade = random.randrange(0, 100)
        values = (fkGeneroId, fkTipoMidiaId, dataPublicacao, editora, nome, idioma, localPublicacao, precoMidia, quantidade)
        conn.execute(insertMidia.values(values))
        return True
    except:
        return False


def insereLivro(lastId):
    try:
        fkMidiaId = lastId
        sinopse = fake.text()
        edicao = random.randrange(1, 100)
        paginas = random.randrange(1, 500)
        values = (fkMidiaId, sinopse, edicao, paginas, )
        conn.execute(insertLivro.values(values))
        return True
    except:
        return False


def insereManga():
    try:
        nome = fake.name()
        adaptacaoAnime = bool(random.randrange(0, 2))
        finalizado = bool(random.randrange(0, 2))
        values = (nome, adaptacaoAnime, finalizado, )
        conn.execute(insertManga.values(values))
        return True
    except:
        return False


def insereVolume(lastId = 0, quantidadeLinhasManga = 0, fkMangaIdDesejada = 0):
    try:
        fkMidiaId = lastId
        if fkMangaIdDesejada != 0:
            fkMangaId = fkMangaIdDesejada
        else:
            fkMangaId = random.randrange(1, quantidadeLinhasManga + 1)

        sinopse = fake.text()
        numero = round(random.uniform(20, 100), 2)
        quantidadeCapitulos = random.randrange(1, 100)
        values = (fkMidiaId, fkMangaId, sinopse, numero, quantidadeCapitulos, )
        conn.execute(insertVolume.values(values))
        return True
    except:
        return False


def insereRevista(lastId):
    try:
        fkMidiaId = lastId
        empresa = fake.name()
        edicao = random.randrange(1, 100)
        values = (fkMidiaId, empresa, edicao, )
        conn.execute(insertRevista.values(values))
        return True
    except:
        return False


def insereAutor():
    try:
        nacionalidade = fake.name()
        nome = fake.name()
        dataNascimento = randomDate()
        dataFalecimento = randomDate()
        values = (nacionalidade, nome, dataNascimento, dataFalecimento, )
        conn.execute(insertAutor.values(values))
        return True
    except:
        return False


def insereAutorMidia(quantidadeLinhasAutor, quantidadeLinhasMidia):
    try:
        fkAutorId = random.randrange(1, quantidadeLinhasAutor + 1)
        fkMidiaId = random.randrange(1, quantidadeLinhasMidia + 1)
        values = (fkAutorId, fkMidiaId, )
        conn.execute(insertAutorMidia.values(values))
        return True
    except:
        return False


def insereFuncionario():
    try:
        funcao = fake.name()
        nome = fake.name()
        salario = round(random.uniform(1000, 5000), 2)
        dataAdmissao = randomDate()
        values = (funcao, nome, salario, dataAdmissao, )
        conn.execute(insertFuncionario.values(values))
        return True
    except:
        return False


def insereCliente():
    try:
        endereco = fake.name()
        sexo = random_sex()
        nome = fake.name()
        dataNascimento = randomDate()
        values = (endereco, sexo, nome, dataNascimento, )
        conn.execute(insertCliente.values(values))
        return True
    except:
        return False


def insereCompra(quantidadeLinhasCliente = 0, quantidadeLinhasFuncionario = 0,
    fkClienteIdDesejada = 0):
    try:
        if fkClienteIdDesejada != 0:
            fkClienteId = fkClienteIdDesejada
        else:
            fkClienteId = random.randrange(1, quantidadeLinhasCliente + 1)
        
        fkFuncionarioId = random.randrange(1, quantidadeLinhasFuncionario + 1)
        data = randomDate()
        values = (fkClienteId, fkFuncionarioId, data, )
        conn.execute(insertCompra.values(values))
        return True
    except:
        return False


def insereProdutosComprados(quantidadeLinhasCompra = 0, quantidadeLinhasMidia = 0,
    fkCompraIdDesejada = 0, fkMidiaIdDesejada = 0):
    try:
        if fkCompraIdDesejada != 0:
            fkCompraId = fkCompraIdDesejada
        else:
            fkCompraId = random.randrange(1, quantidadeLinhasCompra + 1)
        
        if fkMidiaIdDesejada != 0:
            fkMidiaId = fkMidiaIdDesejada
        else:
            fkMidiaId = random.randrange(1, quantidadeLinhasMidia + 1)

        quantidade = random.randrange(1, 100)
        values = (fkCompraId, fkMidiaId, quantidade, )
        conn.execute(insertProdutosComprados.values(values))
        return True
    except:
        return False


# postgresql://usuario:senha@host:port/database
engine = create_engine('postgresql://postgres:123@localhost:5432/postgres')
conn = engine.connect()


quantidadeGenero = 20
print('Genero')
quantidade = 0
while 20 > quantidade:
    quantidade += insereGenero()
print('Quantidade: ', quantidade)

quantidadeTipoMidia = 3
print('TipoMidia')
quantidade = 0
while 3 > quantidade:
    quantidade += insereTipoMidia()
print('Quantidade: ', quantidade)

quantidadeMidia = 130
print('Midia')
quantidade = 0
# Insere ao menos um em cada
for fkGeneroIdDesejada in range(1, quantidadeGenero + 1):
    for fkTipoMidiaIdDesejada in range(1, quantidadeTipoMidia + 1):
        quantidade += insereMidia( 
            fkGeneroIdDesejada = fkGeneroIdDesejada, 
            fkTipoMidiaIdDesejada = fkTipoMidiaIdDesejada)
# Complementa com randoms
while 130 > quantidade:
    quantidade += insereMidia(quantidadeLinhasGenero = quantidadeGenero, 
        quantidadeLinhasTipoMidia = quantidadeTipoMidia)
print('Quantidade: ', quantidade)

quantidadeLivro = 50
print('Livro')
quantidade = 0
lastId = 0
while 50 > quantidade:
    lastId += 1
    quantidade += insereLivro(lastId)
print('Quantidade: ', quantidade)

quantidadeManga = 16
print('Manga')
quantidade = 0
while 16 > quantidade:
    quantidade += insereManga()
print('Quantidade: ', quantidade)

################################################################################

quantidadeVolume = 40
print('Volume')
quantidade = 0
# Insere ao menos 1 de cada
for fkMangaIdDesejada in range(1, quantidadeManga + 1):
    lastId += 1
    quantidade += insereVolume(lastId = lastId, fkMangaIdDesejada = fkMangaIdDesejada)
# Complementa com randoms
while 40 > quantidade:
    lastId += 1
    quantidade += insereVolume(lastId, quantidadeManga)
print('Quantidade: ', quantidade)

# ################################################################################

quantidadeRevista = 40
print('Revista')
quantidade = 0
while 40 > quantidade:
    lastId += 1
    quantidade += insereRevista(lastId)
print('Quantidade: ', quantidade)

quantidadeAutor = 72
print('Autor')
quantidade = 0
while 72 > quantidade:
    quantidade += insereAutor()
print('Quantidade: ', quantidade)

quantidadeAutorMidia = 130
print('AutorMidia')
quantidade = 0
while 130 > quantidade:
    quantidade += insereAutorMidia(quantidadeAutor, quantidadeMidia)
print('Quantidade: ', quantidade)

quantidadeFuncionario = 13
print('Funcionario')
quantidade = 0
while 13 > quantidade:
    quantidade += insereFuncionario()
print('Quantidade: ', quantidade)

quantidadeCliente = 1200
print('Cliente')
quantidade = 0
while 1200 > quantidade:
    quantidade += insereCliente()
print('Quantidade: ', quantidade)

################################################################################

quantidadeCompra = 54000
print('Compra')
quantidade = 0

# Cria 50 vips
quantidadeVips = 0
vips = []
while 50 > quantidadeVips:
    fkClienteIdDesejada = random.randrange(1, quantidadeCliente + 1)
    if not(fkClienteIdDesejada in vips):
        vips.append(random.randrange(1, quantidadeCliente + 1))
        quantidadeVips += 1

# Insere os vips
for fkClienteIdDesejada in vips:
    for i in range(100):
        quantidade += insereCompra(fkClienteIdDesejada = fkClienteIdDesejada,
            quantidadeLinhasFuncionario = quantidadeFuncionario)
        if quantidade % 100 == 0:
            print(quantidade)
print(quantidade)

# Complementa o resto com randoms
while 54000 > quantidade:
    quantidade += insereCompra(quantidadeCliente, quantidadeFuncionario)
    if quantidade % 100 == 0:
        print('Compra ', quantidade)
print('Quantidade: ', quantidade)

################################################################################

quantidadeProdutosComprados = 126000
print('ProdutosComprados')
quantidade = 0
# Insere ao menos um em cada
for fkCompraIdDesejada in range(1, quantidadeCompra + 1):
    while True:
        if insereProdutosComprados(fkCompraIdDesejada=fkCompraIdDesejada,
            quantidadeLinhasMidia = quantidadeMidia):
            quantidade += 1
            break
    if quantidade % 100 == 0:
        print(quantidade)
# Complementa com randoms
while 126000 > quantidade:
    quantidade += insereProdutosComprados(quantidadeCompra, quantidadeMidia)
    if quantidade % 100 == 0:
        print('ProdutosComprados ', quantidade)
print('Quantidade: ', quantidade)
################################################################################