	--TRIGGER DA REGRA 19 "Cliente vip tem 10% de desconto no valor inicial da compra"
CREATE OR REPLACE FUNCTION desconto_10_para_vip_FUNC()
RETURNS TRIGGER AS $BODY$
DECLARE bol_vip BOOLEAN;
BEGIN
	SELECT vip
	INTO bol_vip
	FROM Cliente
	WHERE ClienteId = NEW.ClienteId;
	IF vip = TRUE THEN
		UPDATE Compra
		SET desconto = desconto + 10
		WHERE fkClienteId = NEW.ClienteId
	END IF;
	RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER desconto_10_para_vip_TG
AFTER INSERT ON ProdutosComprados
FOR EACH ROW
EXECUTE PROCEDURE desconto_10_para_vip_FUNC();
