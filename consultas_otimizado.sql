
	--Seleciona clientes_compras_funcionario
CREATE VIEW compra_otimizada_view AS
SELECT c.nome as nomeCliente, co.compraId compraId, co.data, co.preco, f.nome nomeFuncionario
FROM Cliente c, Compra co, Funcionario f
WHERE c.clienteId = co.fkClienteId
AND co.fkFuncionarioId = f.funcionarioId
ORDER BY nomeCliente;

  --Seleciona midias_tipos_genero
CREATE VIEW midia_otimizada_view AS
SELECT m.nome as nomeMidia, m.midiaId midiaId, g.nome as nomeGenero, tm.nome nomeTipo
FROM Midia m, Genero g, TipoMidia tm
WHERE m.fkTipoMidiaId = tm.tipoMidiaId
AND g.generoId = m.fkGeneroId
ORDER BY nomeMidia;

  --Seleciona funcionarios e suas vendas
CREATE VIEW venda_funcionario_view AS
SELECT f.nome, co.data, pc.quantidade, pc.fkMidiaId
FROM Funcionario f, Compra co, ProdutosComprados pc
WHERE f.funcionarioId = co.fkFuncionarioId
AND co.compraId = pc.fkCompraId
ORDER BY f.nome;

  --Seleciona autores e suas midias e o tipo da midia
CREATE VIEW autor_midia_view AS
SELECT a.nome, mv.nomeMidia, mv.nomeTipo, mv.nomeGenero, mv.midiaId
FROM Autor a
INNER JOIN AutorMidia am ON a.autorId = am.fkAutorId
INNER JOIN midia_otimizada_view mv ON mv.midiaId = am.fkMidiaId
ORDER BY a.nome;


  --Relatorio dos produtos comprados pelos clientes
CREATE MATERIALIZED VIEW relatorio_view AS
SELECT cv.nomeCliente, cv.data, cv.preco, cv.nomeFuncionario, mv.nomeMidia,
mv.nomeGenero, mv.nomeTipo, pc.precoUnidade, pc.quantidade
FROM ProdutosComprados pc
LEFT OUTER JOIN compra_otimizada_view cv ON pc.fkCompraId = cv.compraId
LEFT OUTER JOIN midia_otimizada_view mv ON pc.fkMidiaId = mv.midiaId
ORDER BY cv.nomeCliente;

  --Relatorio de autores que tiveram suas midias vendidas e por quais funcionarios
CREATE MATERIALIZED VIEW relatorio2_view AS
SELECT amv.nome nomeAutor, amv.nomeMidia, amv.nomeTipo, amv.nomeGenero, 
vfv.nome nomeFuncionario, vfv.data, vfv.quantidade
FROM autor_midia_view amv
INNER JOIN venda_funcionario_view vfv ON amv.midiaId = vfv.fkMidiaId
ORDER BY nomeAutor;


