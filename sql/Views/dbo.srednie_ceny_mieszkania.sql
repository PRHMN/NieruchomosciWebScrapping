CREATE VIEW [dbo].[srednie_ceny_mieszkania] AS 
SELECT * FROM (
SELECT 
	 AVG( CAST(REPLACE(REPLACE(cena,' ',''),'zł','') as  int))as cena
      ,AVG(TRY_CAST(REPLACE(REPLACE(REPLACE([cena_za_m2], 'zł/m2', ''), ' ', ''),',','.') AS DECIMAL(8,2))) as cena_za_m2
	  ,count(*) as cnt
	  ,dzielnica
  FROM [NieruchomosciScrapping].dbo.nieruchomosci_mieszkania A
  WHERE TRY_CAST(REPLACE(REPLACE(REPLACE([cena_za_m2], 'zł/m2', ''), ' ', ''),',','.') AS DECIMAL(8,2)) IS NOT NULL

  group by dzielnica) a