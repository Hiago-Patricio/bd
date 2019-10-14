-- Copiar o valor atual da midia para o produtocomprado
-- OK
CREATE OR REPLACE FUNCTION valor_atual_produto_comprado_FUNC()
RETURNS TRIGGER AS $BODY$
DECLARE
    preco_midia FLOAT;
BEGIN
    SELECT Midia.precoMidia
    INTO preco_midia
    FROM Midia
    WHERE NEW.fkMidiaId = Midia.midiaId;

    NEW.precoUnidade = preco_midia;

    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER a_valor_atual_produto_comprado_TR
BEFORE INSERT ON ProdutosComprados
FOR EACH ROW
EXECUTE PROCEDURE valor_atual_produto_comprado_FUNC();

-- Atualiza valor da compra
-- OK
CREATE OR REPLACE FUNCTION atualiza_compra_FUNC()
RETURNS TRIGGER AS $BODY$
DECLARE
    valor_final_produtos FLOAT;
BEGIN
    valor_final_produtos = (NEW.precoUnidade - NEW.descontoUnidade) * NEW.quantidade;
    
    UPDATE Compra
    SET preco = preco + valor_final_produtos
    WHERE compraId = NEW.fkCompraId;
    
    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER atualiza_compra_TR
AFTER INSERT ON ProdutosComprados
FOR EACH ROW
EXECUTE PROCEDURE atualiza_compra_FUNC();

-- Depois de 100 compras o cliente vira vip
-- OK
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

CREATE TRIGGER a_cliente_vira_vip_depois_de_100_compras_TG
AFTER INSERT ON Compra
FOR EACH ROW 
EXECUTE PROCEDURE cliente_vira_vip_depois_de_100_compras_FUNC();

-- Cliente recebe 10% de desconto no valor inicial da compra a partir de 5 unidades
-- OK
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

-- Cliente vip tem 10% de desconto no valor inicial da compra
-- OK
CREATE OR REPLACE FUNCTION desconto_10_para_vip_FUNC()
RETURNS TRIGGER AS $BODY$
DECLARE 
	bool_vip BOOLEAN;
BEGIN
	SELECT Cliente.vip
	INTO bool_vip
	FROM Cliente, Compra
	WHERE 
        NEW.fkCompraId = Compra.compraId AND
        Compra.fkClienteId = Cliente.clienteID;

	IF bool_vip = TRUE THEN
        NEW.descontoUnidade = NEW.descontoUnidade + NEW.precoUnidade * 0.1;
	END IF;
	RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER desconto_10_para_vip_TG
BEFORE INSERT ON ProdutosComprados
FOR EACH ROW
EXECUTE PROCEDURE desconto_10_para_vip_FUNC();

-- Se o mangá estiver finalizado o cliente recebe 20% de desconto na compra de todos os volumes do mangá
CREATE OR REPLACE FUNCTION desconto_de_20_porcento_na_colecao_completa_de_manga_FUNC()
RETURNS TRIGGER AS $BODY$
DECLARE 
	finalizado BOOLEAN;
    mangaId INTEGER;
    quantidade_volumes_comprados INTEGER;
    quantidade_volumes_existentes INTEGER;
BEGIN
    SELECT Manga.finalizado
    INTO finalizado
    FROM Manga, Midia, Volume
    WHERE 
        NEW.fkMidiaId = Volume.fkMidiaId AND
        Volume.fkMangaId = Manga.mangaId;

    SELECT Manga.mangaId
    INTO mangaId
    FROM Manga, Midia, Volume
    WHERE 
        NEW.fkMidiaId = Volume.fkMidiaId AND
        Volume.fkMangaId = Manga.mangaId;

    IF finalizado = TRUE THEN
        SELECT COUNT (DISTINCT Volume.volumeId)
        INTO quantidade_volumes_existentes
        FROM Volume
        WHERE Volume.fkMangaId = mangaId;
        
        SELECT COUNT (DISTINCT ProdutosComprados.fkMidiaId)
        INTO quantidade_volumes_comprados
        FROM ProdutosComprados, Midia
        WHERE 
            -- Seleciona a compra
            NEW.fkCompraId = ProdutosComprados.fkCompraId AND
            -- Seleciona as mídias comprados
            ProdutosComprados.fkMidiaId = Midia.MidiaId AND
			-- Seleciona os volumes
			Midia.tipo = 'Volume';
        
		quantidade_volumes_comprados = quantidade_volumes_comprados + 1; 
        IF quantidade_volumes_comprados = quantidade_volumes_existentes THEN
             UPDATE ProdutosComprados
             SET descontoUnidade = descontoUnidade + precoUnidade * 0.2
             FROM Volume
             WHERE 
                 -- Seleciona a compra
                 NEW.fkCompraId = ProdutosComprados.fkCompraId AND
                 -- Seleciona os volumes comprados
                 ProdutosComprados.fkMidiaId = Volume.fkMidiaId;
			NEW.descontoUnidade = NEW.descontoUnidade + NEW.precoUnidade * 0.2;
		END IF;
    END IF;

	RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER desconto_de_20_porcento_na_colecao_completa_de_manga_TG
BEFORE INSERT ON ProdutosComprados
FOR EACH ROW
EXECUTE PROCEDURE desconto_de_20_porcento_na_colecao_completa_de_manga_FUNC();

-- A cada 10 compras o cliente ganha 25% de desconto
CREATE OR REPLACE FUNCTION desconto_25_a_cada_10_compras_FUNC()
RETURNS TRIGGER AS $BODY$
DECLARE 
	quantidade_compras INTEGER;
    id_cliente INTEGER;
BEGIN
    SELECT Cliente.clienteid
    INTO id_cliente
    FROM Cliente, Compra
    WHERE
        NEW.fkCompraId = Compra.compraId AND
        Compra.fkClienteId = Cliente.clienteId; 

	SELECT COUNT(*)
	INTO quantidade_compras
	FROM Compra
    WHERE id_cliente = Compra.fkClienteId;   
        
	IF quantidade_compras % 10 = 9 THEN
		UPDATE ProdutosComprados AS PC
		SET descontoUnidade = descontoUnidade + precoUnidade * 0.25
		WHERE PC.fkCompraId = NEW.fkcompraId;
	END IF;
	RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER desconto_25_a_cada_10_compras_TG
AFTER INSERT ON ProdutosComprados
FOR EACH ROW
EXECUTE PROCEDURE desconto_25_a_cada_10_compras_FUNC();