-- Depois de 100 compras o cliente vira vip
CREATE OR REPLACE FUNCTION cliente_vira_vip_depois_de_100_compras_FUNC()
RETURNS TRIGGER AS $BODY$
DECLARE 
    quantidade_compras INTEGER;
BEGIN
    SELECT COUNT(*) 
    INTO quantidade_compras 
    FROM Compra 
    WHERE fkClienteId = NEW.fkClienteId; 
    
    IF quantidade_compras = 100 THEN
        UPDATE Cliente
        SET vip = TRUE
        WHERE clienteId = NEW.fkClienteId;
    END IF;
    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER cliente_vira_vip_depois_de_100_compras_TG
AFTER INSERT ON Compra
FOR EACH ROW 
EXECUTE PROCEDURE cliente_vira_vip_depois_de_100_compras_FUNC();


-- Cliente recebe 10% de desconto no valor inicial da compra a partir de 5 unidades
CREATE OR REPLACE FUNCTION desconto_de_10_porcento_a_partir_de_5_unidades_FUNC()
RETURNS TRIGGER AS $BODY$
BEGIN
    IF NEW.quantidade >= 5 THEN
        NEW.descontoUnidade = NEW.descontoUnidade + NEW.precoUnidade * 0.1;
    END IF;
    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER desconto_de_10_porcento_a_partir_de_5_unidades_TG
BEFORE INSERT ON ProdutosComprados
FOR EACH ROW 
EXECUTE PROCEDURE desconto_de_10_porcento_a_partir_de_5_unidades_FUNC();