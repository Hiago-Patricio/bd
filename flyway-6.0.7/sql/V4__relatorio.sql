
---Relatorio dos produtos comprados pelos clientes arrumado

CREATE VIEW relatorio_view AS
SELECT c.nome as nomeCliente, co.data, co.preco, f.nome as nomeFuncionario, m.nome as nomeMidia,
g.nome as nomeGenero, tm.nome as nomeTipo, pc.precoUnidade, pc.quantidade
FROM CLiente c
LEFT OUTER JOIN Compra co ON c.clienteId = co.fkClienteId
LEFT OUTER JOIN Funcionario f ON co.fkFuncionarioId = f.funcionarioId
LEFT OUTER JOIN ProdutosComprados pc ON co.compraId = pc.fkCompraId
LEFT OUTER JOIN Midia m ON pc.fkMidiaId = m.midiaId
LEFT OUTER JOIN TipoMidia tm ON m.fkTipoMidiaId = tm.tipoMidiaId
LEFT OUTER JOIN Genero g ON m.fkGeneroId = g.generoId
ORDER BY nomeCLiente;




---Relatorio de autores que tiveram suas midias vendidas e por quais funcionarios arrumado

CREATE VIEW relatorio2_view AS
SELECT a.nome as nomeAutor, m.nome as nomeMidia, tm.nome as nomeTipo, g.nome as nomeGenero,
f.nome as nomeFuncionario, co.data, pc.quantidade
FROM Autor a
LEFT OUTER JOIN AutorMidia am ON a.autorId = am.fkAutorId
LEFT OUTER JOIN Midia m ON am.fkMidiaId = m.MidiaId
LEFT OUTER JOIN Genero g ON m.fkGeneroId = g.generoId
LEFT OUTER JOIN TipoMidia tm ON m.fkTipoMidiaId = tm.tipoMidiaId
LEFT OUTER JOIN ProdutosComprados pc ON m.midiaId = pc.fkMidiaId
LEFT OUTER JOIN Compra co ON pc.fkCompraId = co.compraId
LEFT OUTER JOIN Funcionario f ON co.fkFuncionarioId = f.funcionarioId
ORDER BY nomeAutor;
