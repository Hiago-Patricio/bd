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

-- Atualiza valor da compra
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

-- Cliente vip tem 10% de desconto no valor inicial da compra
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
		UPDATE ProdutosComprados
		SET NEW.descontoUnidade = NEW.descontoUnidade + NEW.descontoUnidade * 0.1
		WHERE ProdutosComprados.fkClienteId = NEW.ClienteId;
	END IF;
	RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER desconto_10_para_vip_TG
BEFORE INSERT ON ProdutosComprados
FOR EACH ROW
EXECUTE PROCEDURE desconto_10_para_vip_FUNC();

-- A cada 10 compras o cliente ganha 25% de desconto
CREATE OR REPLACE FUNCTION desconto_25_a_cada_10_compras_FUNC()
RETURNS TRIGGER AS $BODY$
DECLARE 
	quantidade_compras INTEGER;
BEGIN
	SELECT COUNT(Compra.*)
	INTO quantidade_compras
	FROM Cliente, Compra
	WHERE 
        NEW.fkCompraId = Compra.compraId AND
        Compra.fkClienteId = Cliente.clienteId;

	IF quantidade_compras % 10 = 9 THEN
		UPDATE ProdutosComprados
		SET NEW.descontoUnidade = NEW.descontoUnidade + NEW.descontoUnidade * 0.25
		WHERE fkClienteId = NEW.ClienteId;
	END IF;
	RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER desconto_25_a_cada_10_compras_TG
BEFORE INSERT ON ProdutosComprados
FOR EACH ROW
EXECUTE PROCEDURE desconto_25_a_cada_10_compras_FUNC();

-- Se o mangá estiver finalizado o cliente recebe 20% de desconto na compra de todos os volumes do mangá
CREATE OR REPLACE FUNCTION desconto_de_20_porcento_na_colecao_completa_de_manga_FUNC()
RETURNS TRIGGER AS $BODY$
DECLARE 
	finalizado BOOLEAN;
    mangaId INTEGER;
    quantidade_volumes_comprados INTEGER;
    quantidade_volumes_existentes INTEGER;
BEGIN
    SELECT Manga.finalizado, Manga.mangaId
    INTO finalizado, mangaId
    FROM Manga, Midia, Volume
    WHERE 
        -- Pega o id do mangá e se foi finalizado
        NEW.fkMidiaId = Volume.fkMidiaId AND
        Volume.fkMangaId = Manga.mangaId;

    IF finalizado = TRUE THEN
        SELECT COUNT (DISTINCT Volume.volumeId)
        INTO quantidade_volumes_existentes
        FROM Volume
        WHERE Volume.fkMangaId = mangaId;
        
        SELECT COUNT (DISTINCT Volume.volumeId)
        INTO quantidade_volumes_comprados
        FROM ProdutosComprados, Volume
        WHERE 
            -- Seleciona a compra
            NEW.fkCompraId = ProdutosComprados.fkCompraId AND
            -- Seleciona os volumes comprados
            ProdutosComprados.fkMidiaId = Volume.fkMidiaId;
        
        IF quantidade_volumes_comprados = quantidade_volumes_existentes THEN
            UPDATE ProdutosComprados
            SET descontoUnidade = descontoUnidade + precoUnidade * 0.2
            FROM Volume
            WHERE 
                -- Seleciona a compra
                NEW.fkCompraId = ProdutosComprados.fkCompraId AND
                -- Seleciona os volumes comprados
                ProdutosComprados.fkMidiaId = Volume.fkMidiaId;
        END IF;
    END IF;

	RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER desconto_de_20_porcento_na_colecao_completa_de_manga_TG
BEFORE INSERT ON ProdutosComprados
FOR EACH ROW
EXECUTE PROCEDURE desconto_de_20_porcento_na_colecao_completa_de_manga_FUNC();