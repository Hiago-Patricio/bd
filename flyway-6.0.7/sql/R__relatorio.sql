
	--Seleciona clientes
CREATE VIEW cliente_view AS
SELECT clienteId, nome, quantidadeCompras, vip, sexo, endereco, dataNascimento
FROM Cliente;

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


	--Seleciona cliente e suas compras - relatorio
CREATE MATERIALIZED VIEW relatorio_cliente_view AS
SELECT cv.nome, cov.data, cov.preco, fv.nome, mv.nomeMidia, gv.nome, mv.nomeTipo, pcv.precoUnidade, pcv.quantidade
FROM cliente_view cv
LEFT OUTER JOIN compra_view cov ON cv.clienteId = cov.fkClienteId
LEFT OUTER JOIN produtosComprados_view pcv ON cov.compraId = pcv.fkCompraId
LEFT OUTER JOIN funcionario_view fv ON cov.fkFuncionarioId = fv.funcionarioId
LEFT OUTER JOIN midia_view mv ON pcv.fkMidiaId = mv.midiaId
LEFT OUTER JOIN genero_view gv ON mv.fkGeneroId = gv.generoId
ORDER BY cv.nome;

	--Quais autores tiveram midias vendidos por quais funcionarios - relatorio 2
CREATE MATERIALIZED VIEW relatorio_funcionario_view AS
SELECT av.nome, mv.nomeMidia, mv.nomeTipo, fv.nome, cov.data, pcv.quantidade
FROM funcionario_view fv
INNER JOIN compra_view cov ON fv.funcionarioId = cov.fkFuncionarioId
INNER JOIN produtosComprados_view pcv ON pcv.fkCompraId = cov.compraId
INNER JOIN midia_view mv ON pcv.fkMidiaId = mv.midiaId
INNER JOIN autor_view av ON av.fkMidiaId = mv.midiaId
ORDER BY av.nome;
