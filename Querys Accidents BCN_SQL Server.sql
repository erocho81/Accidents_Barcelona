---Fem una primera revisió de un dels datasets
---Hacemos una primera revisión de uno de los datasets
-- We make a first check of one of the datasets

SELECT TOP 100
	Descripcio_tipus_de_vehicle,
	Descripcio_marca, 
	Descripcio_model_simplificat

FROM dbo.vehicles



---Fem una Query simple amb Join, Where i Order, per conèixer el tipus de vehícle, marca i model d'expedients que tinguin més de 25 víctimes.
---Hacemos una Query senciclla con Join, Where i Order, para averiguar el tipo de vehículo, marca y modelo de expedientes con más de 25 víctimas.
---We create a simple Query using Join, Where and Order, to find the vehicle type, vehicle brand and model for expedients with more than 25 victims.

SELECT	Descripcio_tipus_de_vehicle,
		Descripcio_marca, 
		Descripcio_model_simplificat, 
		Numero_victimes

FROM dbo.Vehicles

INNER JOIN dbo.Quantitat_Persones
	ON Vehicles.Codi_expedient=Quantitat_Persones.Numero_expedient

WHERE Numero_victimes>25

ORDER BY Numero_victimes Desc



---Recompte de Marca i Model "Honda", "SH" a tots els expedients.
---Recuento de Marca y Modelo "Honda", "SH" en todos los expedientes.
---Count of Brand and Model "Honda", "SH" along all expedients.

SELECT 
	Descripcio_marca, 
	Descripcio_model_simplificat, 
	COUNT (Descripcio_model_simplificat) as Total_Modelo

FROM dbo.Vehicles

WHERE Descripcio_model_simplificat = 'SH'
	  AND Descripcio_marca = 'HONDA'

GROUP BY Descripcio_model_simplificat, 
		Descripcio_marca




---Recompte d'expedients on el tipus d'accident es "Abast" i la causa "Alcoholemia".
---Recuento de expedientes donde el tipo de accidente es "Abast" y la causa "Alcoholemia".
---Count of the expedients where the accident type is "Abast" and cause "Alcoholemia".

SELECT 
	COUNT (Tipus_Accidents.Numero_expedient) as Total_Abast_Alc

FROM dbo.Tipus_Accidents

INNER JOIN dbo.Causes
	ON Causes.Numero_expedient = Tipus_Accidents.Numero_expedient

WHERE
	Descripcio_Tipus_accident = 'Abast'
	AND Descripcio_causa_mediata = 'Alcohol?mia'




---Suma de víctimes per marca i models, per al tipus de vehícle "Motocicleta".
---Suma de víctimas por marca y modelo, para el tipo de vehículo "Motocicleta".
---Sum of the victims for each brand and model of the vehicle type "Motocicleta".

SELECT
		Descripcio_marca,
		Descripcio_model_simplificat, 
		SUM(Numero_victimes) as vic_tot

FROM dbo.Vehicles

INNER JOIN dbo.Quantitat_Persones
		ON Vehicles.Codi_expedient=Quantitat_Persones.Numero_expedient

WHERE Descripcio_tipus_de_vehicle = 'Motocicleta'

GROUP BY Descripcio_marca, 
         Descripcio_model_simplificat

ORDER BY vic_tot desc




---Mitjana d'Edat i Anys de carnet segons el tipus de vehícle i tipus de carnet.
---Media de Edad y Años de carnet según el tipo de vehículo y tipo de carnet.
---Average age and license years, according to the vehicle and license type.

SELECT
	Descripcio_Tipus_de_vehicle,
	Descripcio_carnet,
	AVG(Edat) as Ed,
	AVG(Antiguitat_carnet) as Car

FROM dbo.Vehicles


INNER JOIN dbo.Persones
	ON Persones.Numero_expedient= Vehicles.Codi_expedient

GROUP BY Descripcio_Tipus_de_vehicle,
		 Descripcio_carnet

ORDER BY Descripcio_tipus_de_vehicle


---Suma de victimes i els diferents tipus amb el nom del carrer i on la causa de l'expedient està relacionat amb l'alcohol.
---Suma victimas y sus tipos con nombre de calle i donde la causa del expediente está relacionada con el alcohol.
--- Sum of victims and its different types with the street names and where the cause of the expedient is related to alcohol use.



SELECT 
		Quantitat_Persones.Nom_Carrer,
		SUM (Numero_Victimes) as tot_vic,
		SUM (Numero_lesionats_lleus) as tot_lleu,
		SUM (Numero_lesionats_greus) as tot_greu,
		SUM (Numero_Morts) as tot_mort

FROM dbo.Quantitat_Persones

INNER JOIN dbo.Causes
	ON Causes.Numero_expedient=Quantitat_Persones.Numero_expedient 

WHERE Descripcio_causa_mediata = 'Alcohol?mia'

GROUP BY Quantitat_Persones.Nom_Carrer, 
		tot_vic,
		tot_lleu, 
		tot_greu,
		tot_mort

ORDER BY Numero_Victimes DESC



---Mitjana d'edat de les persones implicades, causa per any de la marca "Volkswagen" i model "Golf".
---Media de edad de las personas implicadas y causa por año de la marca  "Volkswagen" y modelo "Golf".
---Average age for involved people and cause for year, for brand "Volkswagen" and model "Golf".

SELECT
		Causes.NK_Any,
		AVG(Edat) as Media_Edad,
		Descripcio_causa_mediata,
		Descripcio_marca,
		Descripcio_model_simplificat

FROM dbo.Persones

INNER JOIN dbo.Causes
		on Causes.Numero_expedient= Persones.Numero_expedient

INNER JOIN dbo.Vehicles
		on Vehicles.Codi_expedient = Persones.Numero_expedient

WHERE Descripcio_marca = 'VOLKSWAGEN'
		AND Descripcio_model_simplificat = 'GOLF'

GROUP BY Causes.NK_Any, 
		Descripcio_causa_mediata, 
		Descripcio_marca,
		Descripcio_model_simplificat

ORDER BY Causes.NK_Any, 
Descripcio_causa_mediata



---Data amb més vehícles implicats en expedients d'accident (més de 100).
---Fecha con más vehículos implicados en expedientes de accidente (más de 100).
---Date with the most vehicles involved in accident expedients (more than 100).

SELECT
	Data_completa,
	max_vehic

FROM
		(SELECT 
			Data_completa,
			SUM (Numero_vehicles_implicats) as max_vehic

		FROM dbo.Quantitat_Persones

		GROUP BY Data_completa
		) AS total

WHERE max_vehic>100

GROUP BY Data_completa, 
		 max_vehic

ORDER BY max_vehic desc



---Left Join per revisar els expedients del fitxer "Tipus_Accident" per als que podem trobar marca en el fitxer "Vehicles".
---Left Join para revisar los expedientes del fichero "Tipus_Accident" para los que podemos encontrar marca en el fixhero "Vehicles".
---Left Join to check the expedients from the file "Tipus_Accident" for which we can find a brand in the file "Vehicles".

SELECT
		Numero_expedient,
		Tipus_Accidents.Data_completa,
		Descripcio_tipus_accident,
		Descripcio_marca

FROM dbo.Tipus_Accidents

LEFT JOIN dbo.Vehicles
		ON Tipus_Accidents.Numero_expedient = Vehicles.Codi_expedient

WHERE Tipus_accidents.Nom_mes = 'Novembre'
	  AND Tipus_accidents.Descripcio_dia_setmana = 'Diumenge'
	  AND Tipus_accidents.Dia_de_mes = 5



---Join de tots els fitxers de la BBDD amb columnes pertayents a tots els fitxers.
---Join de todos los ficheros de la BBDD con columnas pertenecientes a todos ellos.
---Join of all files of the DB with different selected columns for them.


SELECT TOP 10
		Codi_expedient,
		Vehicles.Data_Completa,
		Descripcio_tipus_de_vehicle,
		Descripcio_marca,
		Descripcio_causa_mediata,
		Descripcio_victimitzacio,
		SUM(Numero_victimes) AS Vic_total,
		SUM (Numero_vehicles_implicats) AS Vehic_total,
		Descripcio_tipus_accident

FROM dbo.Vehicles

INNER JOIN dbo.Causes
		ON Vehicles.Codi_expedient= Causes.Numero_expedient

INNER JOIN dbo.Persones
		ON Vehicles.Codi_expedient= Persones.Numero_expedient

INNER JOIN  dbo.Quantitat_Persones
		ON Vehicles.Codi_expedient= Quantitat_Persones.Numero_expedient

INNER JOIN  dbo.Tipus_Accidents
		ON Vehicles.Codi_expedient= Tipus_Accidents.Numero_expedient

WHERE Vehicles.NK_Any <2014
		AND Descripcio_color = 'Negre'

GROUP BY Codi_expedient,
		Vehicles.Data_Completa,
		Descripcio_tipus_de_vehicle,
		Descripcio_marca,
		Descripcio_causa_mediata,
		Descripcio_victimitzacio,
		Descripcio_tipus_accident



---CTE per mostrar la quantitat d'expedients amb victimes i sense elles.
---CTE para mostar la cantidad de expedientes con y sin victimas.
--- Using a CTE to show the quantity of expedients with and without victims.



WITH Sí_Victimas AS 

			(SELECT
				COUNT (Numero_expedient) as Total_Si
				
			FROM dbo.Quantitat_Persones
			
			WHERE Numero_victimes>0),

No_Victimas AS

			(SELECT 
				COUNT(Numero_expedient) as Total_No

			FROM dbo.Quantitat_Persones

			WHERE Numero_victimes=0)

SELECT   Total_Si,
		 Total_No

FROM Sí_Victimas, 
	 No_Victimas




---Víctimes per rang d'edat.
---Victimas por rango de edad
---victims per age range.

SELECT
	Rang_Edat,
	Count(*) AS Victimes_per_Rang

FROM(
		SELECT
			CASE
			WHEN Edat <= 10 then '<10'
			WHEN Edat > 10 and Edat <= 17 then '10-17'
			WHEN Edat >=18 and Edat <30 then '18-29'
			WHEN Edat >=30 and Edat <40 then '30-39'
			WHEN Edat>=40 and Edat <50 then '40-49'
			WHEN Edat>=50 and Edat<60 then '50-59'
			WHEN Edat >=60 and Edat<70 then '60-69'
			ELSE '>=70'
			END AS Rang_Edat,
			
			Numero_Victimes

		FROM dbo.Persones

		INNER JOIN dbo.Quantitat_Persones
			ON Persones.Numero_expedient = Quantitat_Persones.Numero_expedient

) AS total

GROUP BY Rang_edat

ORDER BY Rang_edat



--- Suma de víctimes per marca i model utilitzant window functions.
---Suma de víctimas por marca y modelo usando window functions.
---Sum of victims per brand and model using windows functions.

SELECT
		DISTINCT Descripcio_marca,
		Descripcio_model_simplificat,
		SUM(Numero_victimes) OVER (partition BY Descripcio_marca) as total_marca,
		SUM(Numero_victimes) OVER (partition BY Descripcio_model_simplificat) as total_model

FROM dbo.Vehicles

INNER JOIN dbo.Quantitat_Persones
		ON Vehicles.Codi_expedient=Quantitat_Persones.Numero_expedient

WHERE Descripcio_tipus_de_vehicle = 'Motocicleta'

ORDER BY total_marca desc, 
		total_model desc




