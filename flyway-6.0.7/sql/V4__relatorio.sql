
  --Relatorio dos produtos comprados pelos clientes
CREATE VIEW relatorio_view AS
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


---Relatorio dos produtos comprados pelos clientes arrumado

CREATE VIEW relatorio_view AS
SELECT c.nome as nomeCliente, co.data, co.preco, f.nome as nomeFuncionario, m.nome as nomeMidia,
g.nome as nomeGenero, tm.nome as nomeTipo, pc.precoUnidade, pc.quantidade
FROM CLiente c
LEFT OUTER JOIN Compra co ON c.clienteId = co.fkClienteId
LEFT OUTER JOIN Funcionario f ON co.fkFuncionarioId = f.fkFuncionarioId
LEFT OUTER JOIN ProdutosComprados pc ON co.compraId = pc.fkCompraId
LEFT OUTER JOIN Midia m ON pc.fkMidiaId = m.midiaId
LEFT OUTER JOIN TipoMidiaId tm ON m.TipoMidiaId = tm.tipoMidiaId
LEFT OUTER JOIN Genero g ON m.fkGeneroId = g.generoId
ORDER BY nomeCLiente;




---Relatorio de autores que tiveram suas midias vendidas e por quais funcionarios arrumado

CREATE VIEW relatorio2_view AS
SELECT a.nome as nomeAutor, m.nome as nomeMidia, tm.nome as nomeTipo, g.nome as nomeGenero,
f.nome as nomeFuncionario, co.data, pc.quantidade
FROM Autor a
LEFT OUTER JOIN AutorMidia am ON a.autorId = am.fkAutorId
LEFT OUTER JOIN Midia m ON am.fkMidiaId = m.fkMidiaId
LEFT OUTER JOIN Genero g ON m.fkGeneroId = g.generoId
LEFT OUTER JOIN TipoMidia tm ON m.fkTipoMidiaId = tm.tipoMidiaId
LEFT OUTER JOIN ProdutosComprados pc ON m.midiaId = pc.fkMidiaId
LEFT OUTER JOIN Compra co ON pc.fkCompraId = co.compraId
LEFT OUTER JOIN Funcionario f ON co.fkFuncionarioId = f.funcionarioId
GROUP BY nomeAutor;
