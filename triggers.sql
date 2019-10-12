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
CREATE OR REPLACE FUNCTION 10_porcento_desconto_a_partir_de_5_unidades_FUNC()
RETURNS TRIGGER AS $BODY$
DECLARE
    unidades INTEGER;
BEGIN
    SELECT SUM(quantidade)
    INTO unidades
    FROM ProdutosComprados
    WHERE fkCompraId = NEW.fkCompraId;

    IF unidades >= 5 THEN
        

END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER 10_porcento_desconto_a_partir_de_5_unidades_TG
AFTER INSERT ON ProdutosComprados
FOR EACH ROW 
EXECUTE PROCEDURE 10_porcento_desconto_a_partir_de_5_unidades_FUNC();