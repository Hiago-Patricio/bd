DROP TABLE IF EXISTS ProdutosComprados;
DROP TABLE IF EXISTS Compra;
DROP TABLE IF EXISTS Cliente;
DROP TABLE IF EXISTS Funcionario;
DROP TABLE IF EXISTS AutorMidia;
DROP TABLE IF EXISTS Autor;
DROP TABLE IF EXISTS Revista;
DROP TABLE IF EXISTS Volume;
DROP TABLE IF EXISTS Manga;
DROP TABLE IF EXISTS Livro;
DROP TABLE IF EXISTS Midia;
DROP TABLE IF EXISTS TipoMidia;
DROP TABLE IF EXISTS Genero;

CREATE TABLE Genero (
    generoId SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    localizacao VARCHAR(255) NOT NULL
);

CREATE TABLE TipoMidia(
    tipoMidiaId SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    UNIQUE (nome)
);

CREATE TABLE Midia (
    midiaId SERIAL PRIMARY KEY,
    fkGeneroId INTEGER REFERENCES Genero(generoId) NOT NULL,
    fkTipoMidiaId INTEGER NOT NULL REFERENCES TipoMidia(tipoMidiaId),
    dataPublicacao date NOT NULL,
    editora VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    idioma VARCHAR(255) NOT NULL,
    localPublicacao VARCHAR(255) NOT NULL,
    precoMidia FLOAT NOT NULL CHECK(precoMidia >= 0)
);


CREATE TABLE Livro (
    livroId SERIAL PRIMARY KEY,
    fkMidiaId INTEGER REFERENCES Midia(midiaId) NOT NULL,
    sinopse VARCHAR(255) NOT NULL,
    edicao INTEGER NOT NULL CHECK(edicao > 0),
    paginas INTEGER NOT NULL CHECK(paginas > 0),
    UNIQUE(fkMidiaId)
);

CREATE TABLE Manga (
    mangaId SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    adaptacaoAnime BOOLEAN NOT NULL,
    finalizado BOOLEAN NOT NULL
);

CREATE TABLE Volume (
    volumeId SERIAL PRIMARY KEY,
    fkMidiaId INTEGER REFERENCES Midia(midiaId) NOT NULL,
    fkMangaId INTEGER REFERENCES Manga(mangaId) NOT NULL,
    sinopse VARCHAR(255) NOT NULL,
    numero FLOAT NOT NULL CHECK(numero >= 0),
    quantidadeCapitulos INTEGER NOT NULL CHECK(quantidadeCapitulos > 0),
    UNIQUE(fkMidiaId)
);

CREATE TABLE Revista (
    revistaId SERIAL PRIMARY KEY,
    fkMidiaId INTEGER REFERENCES Midia(midiaId) NOT NULL,
    empresa VARCHAR(255) NOT NULL,
    edicao INTEGER NOT NULL CHECK(edicao > 0),
    UNIQUE(fkMidiaId)
);

CREATE TABLE Autor (
    autorId SERIAL PRIMARY KEY,
    nacionalidade VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    dataNascimento DATE NOT NULL,
    dataFalecimento DATE NOT NULL
);

CREATE TABLE AutorMidia (
    fkAutorId INTEGER REFERENCES Autor(autorId),
    fkMidiaId INTEGER REFERENCES Midia(midiaId),
    UNIQUE(fkAutorId, fkMidiaId)
);

CREATE TABLE Funcionario (
    funcionarioId SERIAL PRIMARY KEY,
    funcao VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    salario FLOAT NOT NULL CHECK(salario > 0),
    dataAdmissao DATE NOT NULL
);

CREATE TABLE Cliente (
    clienteId SERIAL PRIMARY KEY,
    quantidadeCompras INTEGER NOT NULL DEFAULT 0,
    endereco VARCHAR(255) NOT NULL,
    sexo VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    dataNascimento DATE NOT NULL,
    vip BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE Compra (
    compraId SERIAL PRIMARY KEY,
    fkCLienteId INTEGER REFERENCES Cliente(clienteId) NOT NULL,
    fkFuncionarioId INTEGER REFERENCES Funcionario(funcionarioId) NOT NULL,
    data DATE NOT NULL,
    preco FLOAT NOT NULL CHECK(preco >= 0) DEFAULT 0
);

CREATE TABLE ProdutosComprados (
    produtosCompradosId SERIAL PRIMARY KEY,
    fkCompraId INTEGER REFERENCES Compra(compraId) NOT NULL,
    fkMidiaId INTEGER REFERENCES Midia(midiaId) NOT NULL,
    quantidade INTEGER NOT NULL CHECK(quantidade > 0),
    precoUnidade FLOAT CHECK(precoUnidade >= 0),
    descontoUnidade FLOAT NOT NULL CHECK(descontoUnidade >= 0) DEFAULT 0,
    CHECK (precoUnidade >= descontoUnidade),
    UNIQUE(fkCompraId, fkMidiaId)
);