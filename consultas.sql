	--Mostra lista de clientes
SELECT clienteId, nome, quantidadeCompras, endereco, sexo, dataNascimento, vip
FROM Cliente
ORDER BY clienteId;

	--Seleciona clientes
CREATE VIEW cliente_view AS
SELECT clienteId, nome, quantidadeCompras, vip, sexo, endereco, dataNascimento
FROM cliente;

	--Seleciona Compra
CREATE VIEW compra_view AS
SELECT compraId, data, preco, fkClienteId, fkFuncionarioId
FROM Compra;

	--Seleciona ProdutosComprados
CREATE VIEW produtosComprados_view AS
SELECT produtosCompradosId, fkCompraId, fkMidiaId, quantidade, precoUnidade, descontoUnidade
FROM ProdutosComprados;

	--Seleciona Midias
CREATE VIEW midia_view AS
SELECT tm.nome nomeTipo, m.midiaId, fkGeneroId, m.nome nomeMidia, m.dataPublicacao, m.idioma, m.localPublicacao, m.editora, m.precoMidia
FROM Midia m, TipoMidia tm
WHERE m.fkTipoMidiaId = tm.tipoMidiaId
ORDER BY tm.nome;

	-- Livro
CREATE VIEW livro_view AS
SELECT livroId, fkMidiaId, sinopse, edicao, paginas
FROM Livro;

	--Revista
CREATE VIEW revista_view AS
SELECT revistaId, fkMidiaId, empresa, edicao
FROM Revista;
	
	--Manga
CREATE VIEW manga_view AS
SELECT mangaId, nome, adaptacaoAnime, finalizado
FROM Manga;

	--Volume do manga
CREATE VIEW volume_view AS
SELECT volumeId, fkMidiaId, fkMangaId, sinopse, numero, quantidadeCapitulos
FROM Volume;


	--Seleciona genero
CREATE VIEW genero_view AS
SELECT generoId, nome, localizacao
FROM Genero;

	--SelecionaAutores e suas obras disponiveis na livraria
CREATE VIEW autor_view AS
SELECT  a.autorId, a.nome, a.nacionalidade, a.dataNascimento, a.dataFalecimento, am.fkMidiaId
FROM Autor a, AutorMidia am
WHERE a.autorId = am.fkAutorId
ORDER BY a.nome;

	--Seleciona Funcionarios
CREATE VIEW funcionario_view AS
SELECT funcionarioId, nome, funcao, salario, dataAdmissao
FROM Funcionario;


	--Seleciona cliente e suas compras
SELECT cv.nome, cov.data, cov.preco, fv.nome, mv.nomeMidia, gv.nome, mv.nomeTipo, pcv.precoUnidade, pcv.quantidade
FROM cliente_view cv
LEFT OUTER JOIN compra_view cov ON cv.clienteId = cov.fkClienteId
LEFT OUTER JOIN produtosComprados_view pcv ON pcv.fkCompraId = cov.compraId
LEFT OUTER JOIN funcionario_view fv ON cov.fkFuncionarioId = fv.funcionarioId
LEFT OUTER JOIN midia_view mv ON mv.midiaId = pcv.fkMidiaId
LEFT OUTER JOIN genero_view gv ON gv.generoId = mv.fkGeneroId
ORDER BY cv.nome;

