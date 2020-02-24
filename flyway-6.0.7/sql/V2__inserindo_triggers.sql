-- Copiar o valor atual da midia para o produtocomprado
-- Primeiro
CREATE OR REPLACE FUNCTION valor_atual_produto_comprado_FUNC()
RETURNS TRIGGER AS $BODY$
DECLARE
    preco_midia FLOAT;
BEGIN
    SELECT M.precoMidia
    INTO preco_midia
    FROM Midia M
    WHERE NEW.fkMidiaId = M.midiaId;

    NEW.precoUnidade = preco_midia;

    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER a_valor_atual_produto_comprado_TR
BEFORE INSERT ON ProdutosComprados
FOR EACH ROW
EXECUTE PROCEDURE valor_atual_produto_comprado_FUNC();

-- Cliente recebe 10% de desconto no valor inicial do produto na compra a partir de 5 unidades
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
	SELECT Cl.vip
	INTO bool_vip
	FROM Cliente Cl
    JOIN Compra C
    ON C.fkClienteId = Cl.clienteId
	WHERE NEW.fkCompraId = C.compraId;

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
BEGIN
    SELECT Cl.quantidadeCompras
    INTO quantidade_compras
    FROM Cliente Cl
    JOIN Compra C
    ON Cl.clienteId = C.fkClienteId
    WHERE NEW.fkCompraId = C.compraId;

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
    SELECT M.finalizado
    INTO finalizado
    FROM Manga M
    JOIN Volume V
    ON V.fkMangaId = M.mangaId
    WHERE NEW.fkMidiaId = V.fkMidiaId;

    IF finalizado = TRUE THEN
        SELECT M.mangaId
        INTO mangaId
        FROM Manga M
        JOIN Volume V
        ON V.fkMangaId = M.mangaId
        WHERE NEW.fkMidiaId = V.fkMidiaId;

        SELECT COUNT (DISTINCT V.volumeId)
        INTO quantidade_volumes_existentes
        FROM Volume V
        WHERE V.fkMangaId = mangaId;

        SELECT COUNT (DISTINCT PC.produtosCompradosId)
        INTO quantidade_volumes_comprados
        FROM ProdutosComprados PC
        JOIN Midia M
        ON PC.fkMidiaId = M.midiaID
        JOIN TipoMidia TP
        ON M.fkTipoMidiaId = TP.tipoMidiaId
        WHERE 
            NEW.fkCompraId = PC.fkCompraId
            AND TP.nome = 'Volume';
     

		IF quantidade_volumes_comprados = quantidade_volumes_existentes THEN
            UPDATE ProdutosComprados PC
            SET descontoUnidade = descontoUnidade + precoUnidade * 0.2
            FROM Volume V
            WHERE 
                -- Seleciona a compra
                NEW.fkCompraId = PC.fkCompraId AND
                -- Seleciona os volumes comprados
                PC.fkMidiaId = V.fkMidiaId;
		END IF;
    END IF;
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
    
    UPDATE Compra C
    SET preco = preco + valor_final_produtos
    WHERE C.compraId = NEW.fkCompraId;
    
    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER f_atualiza_compra_TR
AFTER INSERT ON ProdutosComprados
FOR EACH ROW
EXECUTE PROCEDURE atualiza_compra_FUNC();

-- Atualiza quantidade de compras
-- Sétimo
CREATE OR REPLACE FUNCTION atualiza_quantidade_de_compras_FUNC()
RETURNS TRIGGER AS $BODY$
BEGIN
    UPDATE Cliente Cl
    SET quantidadeCompras = quantidadeCompras + 1
    WHERE NEW.fkClienteId = Cl.clienteId;

    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER g_atualiza_quantidade_de_compras_TG
AFTER INSERT ON Compra
FOR EACH ROW 
EXECUTE PROCEDURE atualiza_quantidade_de_compras_FUNC();

-- Depois de 100 compras o cliente vira vip
-- Oitavo
CREATE OR REPLACE FUNCTION cliente_vira_vip_depois_de_100_compras_FUNC()
RETURNS TRIGGER AS $BODY$
DECLARE
    quantidade_compras INTEGER;
BEGIN
    SELECT Cl.quantidadeCompras
    INTO quantidade_compras
    FROM Cliente Cl
    WHERE Cl.clienteId = NEW.fkClienteId; 
    
    IF quantidade_compras = 100 THEN
        UPDATE Cliente Cl
        SET vip = TRUE
        WHERE Cl.clienteId = NEW.fkClienteId;
    END IF;
    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER h_cliente_vira_vip_depois_de_100_compras_TG
AFTER INSERT ON Compra
FOR EACH ROW 
EXECUTE PROCEDURE cliente_vira_vip_depois_de_100_compras_FUNC();

-- Uma mídia só pode ser referenciada por uma revista, livro ou volume
--nono
CREATE OR REPLACE FUNCTION limita_uso_da_chave_da_midia_FUNC()
RETURNS TRIGGER AS $BODY$
DECLARE
    quantidadeUsadaFkMidiaId INTEGER;
BEGIN
    quantidadeUsadaFkMidiaId = 0;

    SELECT COUNT(*)
    INTO quantidadeUsadaFkMidiaId
    FROM livro l
    FULL JOIN revista r
    ON l.fkmidiaid = r.fkmidiaid
    FULL JOIN volume v
    ON v.fkmidiaid = r.fkmidiaid
    WHERE l.fkmidiaid = NEW.fkmidiaid;

    IF(quantidadeUsadaFkMidiaId != 0) THEN
        RAISE EXCEPTION 'Chave já usada em outro produto';
    END IF;
    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER limita_uso_da_chave_da_midia_livro_TG
BEFORE INSERT ON livro
FOR EACH ROW
EXECUTE PROCEDURE limita_uso_da_chave_da_midia_FUNC();

CREATE TRIGGER limita_uso_da_chave_da_midia_revista_TG
BEFORE INSERT ON revista
FOR EACH ROW
EXECUTE PROCEDURE limita_uso_da_chave_da_midia_FUNC();

CREATE TRIGGER limita_uso_da_chave_da_midia_volume_TG
BEFORE INSERT ON volume
FOR EACH ROW
EXECUTE PROCEDURE limita_uso_da_chave_da_midia_FUNC();
