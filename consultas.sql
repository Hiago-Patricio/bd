	--Mostra lista de clientes
SELECT clienteId, nome, quantidadeCompras, endereco, sexo, dataNascimento, vip
FROM Cliente
ORDER BY clienteId;

	--Seleciona clientes
CREATE VIEW cliente_view AS
SELECT clienteid, nome, quantidadeCompras, vip, sexo, endereco, dataNascimento
FROM cliente

	--Seleciona Compra
CREATE VIEW compra_view AS
SELECT compraId, data, preco, fkClienteId, fkFuncionarioId
FROM Compra

	--Seleciona ProdutosComprados
CREATE VIEW produtosComprados_view AS
SELECT produtosCompradosId, fkCompraId, fkMidiaId, quantidade, precoUnidade, descontoUnidade
FROM ProdutosComprados

	--Seleciona Midias
CREATE VIEW midia_view AS
SELECT tm.nome, m.midiaId, fkGeneroId, m.nome, m.dataPublicacao, m.idioma, m.localPublicacao, m.editora, m.precoMidia
FROM Midia m, TipoMidia tm
WHERE m.fkTipoMidiaId = tm.tipoMidiaId
ORDER BY m.tipo;

	-- Midia com tipo ARRUMAR ARRUMAR ARRUMAR ARRUMAR ARRUMAR
CREATE VIEW tipo_view AS
SELECT 


	--Seleciona genero
CREATE VIEW genero_view AS
SELECT generoId, nome, localizacao
FROM Genero 

	--SelecionaAutores e suas obras disponiveis na livraria
CREATE VIEW autor_view AS
SELECT  a.autorId, a.nome, a.nacionalidade, a.dataNascimento, a.dataFalecimento, am.fkMidiaId
FROM Autor a, AutorMidia am
WHERE a.autorId = am.fkAutorId
ORDER BY a.nome;

	--Seleciona Funcionarios
CREATE VIEW funcionario_view AS
SELECT funcionarioId, nome, funcao, salario, dataAdmissao
FROM Funcionario


