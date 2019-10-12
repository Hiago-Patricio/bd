	--Mostra lista de clientes

SELECT clienteId, nome, quantidadeCompras, endereco, sexo, dataNascimento, vip
FROM Cliente
ORDER BY clienteId;

	--Seleciona vip's

SELECT clienteid, nome, vip FROM cliente
WHERE vip = TRUE;

	--Histórico de gasto do cliente

SELECT c.clienteId, c.nome, co.data, co.precoTotal, co.desconto, co.precoFinal
FROM Cliente c, Compra co
WHERE c.clienteId = co.fkClienteId
ORDER BY c.clienteId;

	--Histórico de compra do cliente

SELECT c.clienteId, c.nome, co.compraId, pc.quantidade, m.nome, m.tipo
FROM Cliente c, Compra co, ProdutosComprados pc, Midia m
WHERE c.clienteId = co.fkClienteId
AND co.compraId = pc.fkCompraId
AND pc.fkMidiaId = m.midiaId
ORDER BY c.clienteId;

	--Midias Disponiveis na livraria por tipo

SELECT m.tipo, m.midiaId, m.nome, m.dataPublicacao, m.idioma, m.localPublicacao, m.editora, m.precoMidia
FROM Midia m
ORDER BY m.tipo;

	--Midias disponiveis na livraria por genero

SELECT g.nome, m.midiaId, m.nome, m.dataPublicacao, m.tipo, m.idioma, m.localPublicacao, m.editora, m.precoMidia
FROM Midia m, Genero g
WHERE g.generoId = m.fkGeneroId
ORDER BY g.nome;

	--Autores e suas obras disponiveis na livraria

SELECT  a.nome, a.autorId, a.nacionalidade, a.dataNascimento, a.dataFalecimento, m.tipo, m.nome, m.dataPublicacao, m.precoMidia
FROM Autor a, AutorMidia am, Midia m
WHERE a.autorId = am.fkAutorId
AND am.fkMidiaId = m.midiaId
ORDER BY a.nome;

	--Funcionarios e suas vendas
SELECT f.funcionarioId, f.nome, f.funcao, co.fkClienteId, c.nome, co.compraId, co.data, co.compraId
FROM Funcionario f, Compra co, Cliente c
WHERE f.funcionarioId = co.fkFuncionarioId
AND co.fkClienteId = c.clienteId
ORDER BY f.funcionarioId;


