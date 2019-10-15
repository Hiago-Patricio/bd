-- Copiar o valor atual da midia para o produtocomprado
-- Primeiro
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

-- Cliente recebe 10% de desconto no valor inicial da compra a partir de 5 unidades
-- Segundo
CREATE OR REPLACE FUNCTION desconto_de_10_porcento_a_partir_de_5_unidades_FUNC()
RETURNS TRIGGER AS $BODY$
BEGIN
    IF NEW.quantidade >= 5 THEN
        NEW.descontoUnidade = NEW.descontoUnidade + NEW.precoUnidade * 0.1;
    END IF;
    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER b_desconto_de_10_porcento_a_partir_de_5_unidades_TG
BEFORE INSERT ON ProdutosComprados
FOR EACH ROW 
EXECUTE PROCEDURE desconto_de_10_porcento_a_partir_de_5_unidades_FUNC();

-- Cliente vip tem 10% de desconto no valor inicial da compra
-- Terceiro
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

CREATE TRIGGER c_desconto_10_para_vip_TG
BEFORE INSERT ON ProdutosComprados
FOR EACH ROW
EXECUTE PROCEDURE desconto_10_para_vip_FUNC();

-- A cada 10 compras o cliente ganha 25% de desconto
-- Quarto
CREATE OR REPLACE FUNCTION desconto_25_a_cada_10_compras_FUNC()
RETURNS TRIGGER AS $BODY$
DECLARE 
	quantidade_compras INTEGER;
    clienteID INTEGER;
BEGIN
    SELECT Cliente.clienteid
    INTO clienteID
    FROM Cliente, Compra
    WHERE
        NEW.fkCompraId = Compra.compraId AND
        Compra.fkClienteId = Cliente.clienteId; 

	SELECT COUNT(*)
	INTO quantidade_compras
	FROM Compra
    WHERE clienteID = Compra.fkClienteId;   
        
	IF quantidade_compras > 0 AND quantidade_compras % 10 = 0 THEN
        NEW.descontoUnidade = NEW.descontoUnidade + NEW.precoUnidade * 0.25;
    END IF;
	RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER d_desconto_25_a_cada_10_compras_TG
BEFORE INSERT ON ProdutosComprados
FOR EACH ROW
EXECUTE PROCEDURE desconto_25_a_cada_10_compras_FUNC();

-- Se o mangá estiver finalizado o cliente recebe 20% de desconto na compra de todos os volumes do mangá
-- Quinto
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

    IF finalizado = TRUE THEN
        SELECT M.mangaId
        INTO mangaId
        FROM Manga M, Volume V
        WHERE 
            NEW.fkMidiaId = V.fkMidiaId AND
            V.fkMangaId = M.mangaId;

        SELECT COUNT (DISTINCT V.volumeId)
        INTO quantidade_volumes_existentes
        FROM Volume V
        WHERE V.fkMangaId = mangaId;

        SELECT COUNT (DISTINCT PC.produtosCompradosId)
        INTO quantidade_volumes_comprados
        FROM ProdutosComprados PC, Midia M, TipoMidia TP
        WHERE 
            NEW.fkCompraId = PC.fkCompraId
            AND PC.fkMidiaId = M.midiaID
            AND M.fkTipoMidiaId = TP.tipoMidiaId
            AND TP.nome = 'Volume';
     

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
    INSERT INTO Debug(finalizado, existente, comprado, is_volume)
    VALUES (finalizado, quantidade_volumes_existentes, quantidade_volumes_comprados, 0);
	RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER e_desconto_de_20_porcento_na_colecao_completa_de_manga_TG
AFTER INSERT ON ProdutosComprados
FOR EACH ROW
EXECUTE PROCEDURE desconto_de_20_porcento_na_colecao_completa_de_manga_FUNC();

-- Atualiza valor da compra
-- Sexto
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

CREATE TRIGGER f_atualiza_compra_TR
AFTER INSERT ON ProdutosComprados
FOR EACH ROW
EXECUTE PROCEDURE atualiza_compra_FUNC();

-- Depois de 100 compras o cliente vira vip
-- Sétimo
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

CREATE TRIGGER g_cliente_vira_vip_depois_de_100_compras_TG
AFTER INSERT ON Compra
FOR EACH ROW 
EXECUTE PROCEDURE cliente_vira_vip_depois_de_100_compras_FUNC();