
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
SELECT




---Relatorio de autores que tiveram suas midias vendidas e por quais funcionarios arrumado

CREATE VIEW relatorio2_view AS
SELECT
