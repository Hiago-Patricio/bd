CREATE INDEX idx_cliente ON Cliente (clienteId);
CREATE INDEX idx_compra_cliente ON Compra (fkClienteId);
CREATE INDEX idx_fkcompra_funcionario ON Compra (fkFuncionarioId);
CREATE INDEX idx_produtosComprados_compra ON ProdutosComprados (fkCompraId);
CREATE INDEX idx_produtosComprados_midia ON ProdutosComprados (fkMidiaId);
CREATE INDEX idx_funcionario ON Funcionario (funcionarioId);
CREATE INDEX idx_midia ON Midia (midiaId);
CREATE INDEX idx_autor_midia ON AutorMidia (fkMidiaId);
SET work_mem = '16MB';
