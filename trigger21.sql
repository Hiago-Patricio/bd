	--TRIGGER DA REGRA 21 "A cada 10 compras o cliente ganha 25% de desconto"
CREATE OR REPLACE FUNCTION desconto_25_a_cada_10_compras_FUNC()
RETURNS TRIGGER AS $BODY$
DECLARE quantidade_compras INTEGER;
BEGIN
	SELECT COUNT(*)
	INTO quantidade_compras
	FROM Compra
	WHERE fkClienteId = NEW.fkClientId;
	IF quantidade_compras = 5 THEN
		UPDATE Compra
		SET desconto = desconto + 25
		WHERE clienteId = NEW.fkClienteId
	END IF;
	RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER desconto_25_a_cada_10_compras_TG
AFTER INSERT ON COMPRA
FOR EACH ROW
EXECUTE PROCEDURE
desconto_25_a_cada_10_compras_FUNC();
