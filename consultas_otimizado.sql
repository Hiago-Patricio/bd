
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
FROM Midia m, Genero g
WHERE m.fkTipoMidiaId = tm.tipoMidiaId
AND g.generoId = m.fkGeneroId
ORDER BY nomeMidia;


  --Relatorio dos produtos comprados pelos clientes
CREATE VIEW relatorio_view AS
SELECT cv.nomeCliente, cv.data, cv.preco, cv.nomeFuncionario, mv.nomeMidia,
mv.nomeGenero, mv.nomeTipo, pc.precoUnidade, pc.quantidade
FROM ProdutosComprados pc
LEFT OUTER JOIN compra_otimizada_view cv ON pc.fkCompraId = cv.compraId
LEFT OUTER JOIN midia_otimizada_view mv ON pc.fkMidiaId = mv.midiaId
ORDER BY cv.nomeCliente;

