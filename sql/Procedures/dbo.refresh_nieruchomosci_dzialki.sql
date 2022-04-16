CREATE PROCEDURE [dbo].[refresh_nieruchomosci_dzialki]
AS

MERGE dbo.nieruchomosci_dzialki as tgt
using stg.nieruchomosci_dzialki as src
ON tgt.url=src.url
WHEN NOT MATCHED BY TARGET THEN
INSERT ([url],[miejsce],[miejscowosc],[cena],[powierzchnia],[cena_za_m2],[data_wstawienia],[agent],isActive)
VALUES (src.[url],src.[miejsce],src.[miejscowosc],src.[cena],src.[powierzchnia],src.[cena_za_m2],src.[data_wstawienia],src.[agent],1)

WHEN NOT MATCHED BY SOURCE THEN
UPDATE SET tgt.isActive=0;