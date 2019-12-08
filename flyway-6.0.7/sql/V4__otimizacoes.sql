
--SET work_mem = '16MB';

CREATE INDEX idx_compra_data ON Compra (data);
CREATE INDEX idx_cliente_vip ON Cliente (vip);
