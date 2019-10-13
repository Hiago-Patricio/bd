	--TRIGGER DA REGRA 19 "Cliente vip tem 10% de desconto no valor inicial da compra"
CREATE OR REPLACE FUNCTION desconto_10_para_vip_FUNC()
RETURNS TRIGGER AS $BODY$
DECLARE bol_vip BOOLEAN;
BEGIN
	SELECT vip
	INTO bol_vip
	FROM Cliente
	WHERE ClienteId = NEW.ClientId;
	IF vip = t THEN
		UPDATE Compra
		SET desconto = desconto + 10
		WHERE fkClienteId = NEW.ClienteId
	END IF;
	RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER desconto_10_para_vip_TG
BEFORE INSERT ON COMPRA
FOR EACH ROW
EXECUTE PROCEDURE
desconto_10_para_vip_FUNC();
