CREATE PROCEDURE [dbo].[refresh_nieruchomosci_mieszkania]
AS

MERGE dbo.nieruchomosci_mieszkania as tgt
using stg.nieruchomosci_mieszkania as src
ON tgt.url=src.url
WHEN NOT MATCHED BY TARGET THEN
INSERT ([url],[miejsce],[dzielnica],[pietro],[liczba_pokoi],[rok_budowy],[miejsce_parkingowe],[czynsz],[wyposazenie],[rynek],[cena],[powierzchnia],[cena_za_m2],[data_wstawienia],[agent],[isActive])
VALUES (src.[url],src.[miejsce],src.[dzielnica],src.[pietro],src.[liczba_pokoi],src.[rok_budowy],src.[miejsce_parkingowe],src.[czynsz],src.[wyposazenie],src.[rynek],src.[cena],src.[powierzchnia],src.[cena_za_m2],src.[data_wstawienia],src.[agent],1)

WHEN NOT MATCHED BY SOURCE THEN
UPDATE SET tgt.isActive=0;