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
DROP TABLE IF EXISTS Genero;

CREATE TABLE Genero (
    generoId SERIAL PRIMARY KEY,
    nome VARCHAR NOT NULL,
    localizacao VARCHAR NOT NULL
);

CREATE TABLE Midia (
    midiaId SERIAL PRIMARY KEY,
    fkGeneroId INTEGER REFERENCES Genero(generoId) NOT NULL,
    tipo VARCHAR NOT NULL,
    dataPublicacao date NOT NULL,
    editora VARCHAR NOT NULL,
    nome VARCHAR NOT NULL,
    idioma VARCHAR NOT NULL,
    localPublicacao VARCHAR NOT NULL,
    precoMidia FLOAT NOT NULL CHECK(precoMidia >= 0)
);


CREATE TABLE Livro (
    livroId SERIAL PRIMARY KEY,
    fkMidiaId INTEGER REFERENCES Midia(midiaId) NOT NULL,
    sinopse VARCHAR NOT NULL,
    edicao INTEGER NOT NULL CHECK(edicao > 0),
    paginas INTEGER NOT NULL CHECK(paginas > 0)
);

CREATE TABLE Manga (
    mangaId SERIAL PRIMARY KEY,
    nome VARCHAR NOT NULL,
    adaptacaoAnime BOOLEAN NOT NULL,
    finalizado BOOLEAN NOT NULL
);

CREATE TABLE Volume (
    volumeId SERIAL PRIMARY KEY,
    fkMidiaId INTEGER REFERENCES Midia(midiaId) NOT NULL,
    fkMangaId INTEGER REFERENCES Manga(mangaId) NOT NULL,
    sinopse VARCHAR NOT NULL,
    numero FLOAT NOT NULL CHECK(numero >= 0),
    quantidadeCapitulos INTEGER NOT NULL CHECK(quantidadeCapitulos > 0)
);

CREATE TABLE Revista (
    revistaId SERIAL PRIMARY KEY,
    fkMidiaId INTEGER REFERENCES Midia(midiaId) NOT NULL,
    empresa VARCHAR NOT NULL,
    edicao INTEGER NOT NULL CHECK(edicao > 0)
);

CREATE TABLE Autor (
    autorId SERIAL PRIMARY KEY,
    nacionalidade VARCHAR NOT NULL,
    nome VARCHAR NOT NULL,
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
    funcao VARCHAR NOT NULL,
    nome VARCHAR NOT NULL,
    salario FLOAT NOT NULL CHECK(salario > 0),
    dataAdmissao DATE NOT NULL
);

CREATE TABLE Cliente (
    clienteId SERIAL PRIMARY KEY,
    quantidadeCompras INTEGER NOT NULL,
    endereco VARCHAR NOT NULL,
    sexo VARCHAR NOT NULL,
    nome VARCHAR NOT NULL,
    dataNascimento DATE NOT NULL,
    vip BOOLEAN NOT NULL
);

CREATE TABLE Compra (
    compraId SERIAL PRIMARY KEY,
    fkCLienteId INTEGER REFERENCES Cliente(clienteId) NOT NULL,
    fkFuncionarioId INTEGER REFERENCES Funcionario(funcionarioId) NOT NULL,
    data DATE NOT NULL,
    precoTotal FLOAT NOT NULL CHECK(precoTotal >= 0),
    desconto FLOAT NOT NULL CHECK(desconto >= 0),
    precoFinal FLOAT NOT NULL CHECK(precoFinal >= 0)
);

CREATE TABLE ProdutosComprados (
    produtosCompradosId SERIAL PRIMARY KEY,
    fkCompraId INTEGER REFERENCES Compra(compraId) NOT NULL,
    fkMidiaId INTEGER REFERENCES Midia(midiaId) NOT NULL,
    quantidade INTEGER NOT NULL CHECK(quantidade > 0),
    descontoUnidade FLOAT NOT NULL CHECK(descontoUnidade >= 0),
    precoUnidade FLOAT NOT NULL CHECK(precoUnidade >= 0)
);