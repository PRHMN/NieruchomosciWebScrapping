CREATE TABLE [dbo].[nieruchomosci_mieszkania](
	[url] [nvarchar](4000) NULL,
	[miejsce] [nvarchar](4000) NULL,
	[dzielnica] [nvarchar](500) NULL,
	[pietro] [nvarchar](10) NULL,
	[liczba_pokoi] [nvarchar](10) NULL,
	[rok_budowy] [nvarchar](50) NULL,
	[miejsce_parkingowe] [nvarchar](255) NULL,
	[czynsz] [nvarchar](50) NULL,
	[wyposazenie] [nvarchar](4000) NULL,
	[rynek] [nvarchar](50) NULL,
	[cena] [nvarchar](50) NULL,
	[powierzchnia] [nvarchar](50) NULL,
	[cena_za_m2] [nvarchar](50) NULL,
	[data_wstawienia] [datetime] NULL,
	[agent] [nvarchar](255) NULL,
	[isActive] [bit] NULL
)