CREATE VIEW [dbo].[v_nieruchomosci_mieszkania] AS
SELECT  [url]
      ,[miejsce]
	  ,cast(replace(replace(cena, ' ',''),'zł','') as int) as cena
	  ,CAST(REPLACE(REPLACE(REPLACE([powierzchnia], 'm2', ''), ' ', ''), ',','.') AS DECIMAL(8,2)) as powierzchnia
      ,TRY_CAST(REPLACE(REPLACE(REPLACE([cena_za_m2], 'zł/m2', ''), ' ', ''),',','.') AS DECIMAL(8,2)) as cena_za_m2
	  ,agent
	  ,[data_wstawienia]
      ,[dzielnica]
      ,[pietro]
      ,[liczba_pokoi]
      ,[rok_budowy]
      ,[miejsce_parkingowe]
      ,[czynsz]
      ,[wyposazenie]
      ,[rynek]
  FROM [NieruchomosciScrapping].[dbo].nieruchomosci_mieszkania A
  WHERE TRY_CAST(REPLACE(REPLACE(REPLACE([cena_za_m2], 'zł/m2', ''), ' ', ''),',','.') AS DECIMAL(8,2)) IS NOT NULL
