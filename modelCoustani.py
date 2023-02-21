import os
import datetime
import pandas as pd
import geopandas as gpd
import math
import fiona

fiona.supported_drivers['KML'] = 'rw'

print("Model ModeleCoustani ready to run")

# Noms des fichiers d'entree
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
DATA_DIR = os.path.join(ROOT_DIR, 'data')

pathCSV = os.path.join(DATA_DIR, 'METEO')
pathSHP = os.path.join(DATA_DIR, 'SHP')
pathOutput = os.path.join(ROOT_DIR, 'output')

rainFileName = os.path.join(pathCSV,"PrecipitationMrd.csv")
tempFileName = os.path.join(pathCSV,"TemperatureMrd.csv")
parcelFileName = os.path.join(pathSHP,"FktSurfGitesLarvDistMorondava.shp")

# Parametres
DT = 0.1
FREQUENCE_DISPLAY = 7 # frequence d'affichage pour l'export multidates - ici tous les 7 jours
bdate = datetime.date(2013, 1, 1) # date debut simulation = debut des donnees meteo
bdate_output = datetime.date(2014, 1, 1) # date debut des sorties (> 1 annee d'initialisation)
edate = datetime.date(2014, 1, 31) # date fin simulation
outputSHPAllDates = False # Boolean : sortie Shapefile multidates
outputSHPLastDate = False # Boolean : sortie Shapefile pour la derniere date
outputKMLAllDates = False # Boolean : sortie KML multidates
outputKMLLastDate = True # Boolean : sortie KML pour la derniere date

# 1) Instanciation des datafacers : inputs
# Donnees meteo
rainCSVData = pd.read_csv(rainFileName,delimiter=";")# le fichier texte (csv) avec les donnees Meteo : pluies
tempCSVData = pd.read_csv(tempFileName,delimiter=";") # le fichier texte (csv) avec les donnees Meteo : temperatures

# Parcelles
shp = gpd.read_file(parcelFileName) # le shapefile avec les parcelles

# 2) Instanciation des datafacers : outputs
def add_years(d):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year = d.year + 1)
    except ValueError:
        return d + (date(d.year + 1, 1, 1) - date(d.year, 1, 1))

d = add_years(bdate)
if d > bdate_output:
    bdate_output = d # (test : il faut au moins 1 annee d'initialisation)

# SHP 1 date
nomDeFichierShp1Date = edate.strftime("%Y%m%d") +".shp"
shpout1 = os.path.join(pathOutput,nomDeFichierShp1Date)

# SHP multidates
nomDeFichierShpAll = bdate_output.strftime("%Y%m%d_")+ edate.strftime("%Y%m%d")  +".shp" # Definition des parametres : date de debut et duree de la simulation
shpout = os.path.join(pathOutput,nomDeFichierShpAll) 	# le fichier ShapeFile en sortie : toutes les dates

# KML 1 date
kmlFileName1 = edate.strftime("%Y%m%d") +".kml"
kmlExport1 = os.path.join(pathOutput,kmlFileName1)

# KML multidates
kmlFileName = bdate_output.strftime("%Y%m%d_") + edate.strftime("%Y%m%d")  +".kml"
kmlExport = os.path.join(pathOutput,kmlFileName)

# Definition des styles de sorties
# plt = colorRange(10,"gyr")        # get list of colors from predefined pate "gyr"
# kmlExport.defStyleRange("Atot_",1.0,plt,-0.2) # prefix, line thickness, list of colors , darken line color a little
# kmlExport1.defStyleRange("Atot_",1.0,plt,-0.2) # prefix, line thickness, list of colors , darken line color a little
bdate_output = datetime.date(bdate_output.year, 1, 1) # pour commencer les sorties au 1er janvier

# 3) Lecture des donnees
print("Reading data ... ")
## Parcelles
# List of Parcels obtained from the Shapefile datafacer ShpParcelle
print("found "+ str(shp.shape[0]) +" parcels" )

## Donnees meteo
print("Size of rain data file: " + str(len(rainCSVData)))
print("Size of temperature data file: " + str(len(tempCSVData)))

# construction des keymaps meteo
# kmrain =  # Keymap <codecommmune_year_week, rain>
# kmtemp =  # Keymap <codecommmune_year_week, temperature>
# constructionKeyMap(kmrain,datarain)
# constructionKeyMap(kmtemp,datatemp)

# 4) Initialisation
print("Initialization ... ")
now = bdate
fin = now
test_display =0.0

shp["oeufs"] = 10000000.0
shp["larves"] = 0.0
shp["nymphes"] = 0.0
shp["aem"] = 0.0
shp["a1h"] = 0.0
shp["a1g"] = 0.0
shp["a1o"] = 0.0
shp["a2h"] = 0.0
shp["a2g"] = 0.0
shp["a2o"] = 0.0
shp["rain7"] = 0.0
shp["raincumul7"] = 0.0
shp["rainday7"] = 0.0

# 5) Simulation
print("Simulation start: "+ bdate.strftime("%d/%m/%Y"))
day = 0
shp_list = gpd.GeoDataFrame()
kml_list = gpd.GeoDataFrame()

# Boucle sur les jours
while now < edate:
    w = (now + datetime.timedelta(weeks=1)).strftime("s%W")
    if w == "s00":
        w = "s52"
    print(now.strftime("%d/%m/%Y") + "; week " + w)
    test_display = math.remainder(day,FREQUENCE_DISPLAY)	# pour l'export des donnees tous les frequencedisplay jours
    fin = now + datetime.timedelta(days = FREQUENCE_DISPLAY -1)

    # Boucle sur les parcelles
    for index, row in shp.iterrows():
        # Read Meteo
        codeCommune = row["mdg_com_co"]
        rain = rainCSVData.loc[(rainCSVData['CodeCommune'] == codeCommune) & (rainCSVData['numero_annee'] == now.year) , w].values[0] / 7
        temperature = tempCSVData.loc[(tempCSVData['CodeCommune'] == codeCommune) & (tempCSVData['numero_annee'] == now.year) , w].values[0]
        w7 = now.strftime("s%W")
        if w7 == "s00" :
            # try :
            #     rain7 = rainCSVData.loc[(rainCSVData['CodeCommune'] == codeCommune) & (rainCSVData['numero_annee'] == (now.year - 1)) , "s52"].values[0]
            #     raincumul7 = rainCSVData.loc[(rainCSVData['CodeCommune'] == codeCommune) & (rainCSVData['numero_annee'] == (now.year - 1)) , "s52"].values[0]
            # except IndexError:
            rain7 = rainCSVData.loc[(rainCSVData['CodeCommune'] == codeCommune) & (rainCSVData['numero_annee'] == now.year) , "s52"].values[0] / 7
            raincumul7 = rainCSVData.loc[(rainCSVData['CodeCommune'] == codeCommune) & (rainCSVData['numero_annee'] == now.year) , "s52"].values[0]
        else:
            rain7 = rainCSVData.loc[(rainCSVData['CodeCommune'] == codeCommune) & (rainCSVData['numero_annee'] == now.year) , w7].values[0] / 7
            raincumul7 = rainCSVData.loc[(rainCSVData['CodeCommune'] == codeCommune) & (rainCSVData['numero_annee'] == now.year) , w7].values[0]

        # Updatefunction
        # Egg development
        TE = 12.9
        TDDE = 26.6
        if temperature > TE :
            fegg1 = (temperature - TE)
            fegg = fegg1 / TDDE
        if fegg < 0 :
            fegg = 0.0

        # Pupae development
        fpupae1 = math.exp(0.162*(temperature-10))
        fpupae2 = math.exp(0.162*25-35+temperature)
        fpupae = 0.021*(fpupae1 - fpupae2)/5.007
        if fpupae < 0 :
            fpupae = 0.0

        # Larvae development
        flarvae = fpupae/4

        # fAg
        TAg = 9.9
        TDDAg = 36.5
        if temperature > TAg :
            fag1= temperature - TAg
            fag = fag1 / TDDAg

        # fAo
        fao = 2.0

        # Taux de mortalite des oeufs
        fme = 0.1

        # Taux de mortalite des larves
        fml1 = math.exp(-temperature/2)
        fml = fml1 + 0.08

        # Taux de mortalite des nymphes
        fmp = fml

        # Taux de mortalite des adultes
        fma1 = 0.000148 * temperature * temperature
        fma = 0.1-0.00667 *temperature + fma1
        if fma<0.033:
            fma=0.033

        # Taux de mortalite en recherche d'hote
        mur = 0.08         # taux de mortalité additionnelle du comportement de recherche (d'hôtes et de sites de ponte)
        fmurma = fma + mur

        # capacite du milieu en larves
        m = now.month
        surfRiv = row["RivieresM2"] if not math.isnan(row["RivieresM2"]) else 0
        surfCult = row["CultAgriM2"] if not math.isnan(row["CultAgriM2"]) else 0
        surfEau = row["PlanDeauM2"] if not math.isnan(row["PlanDeauM2"]) else 0
        surfRiz = row["RizieresM2"] if not math.isnan(row["RizieresM2"]) else 0

        klvarRiv = int(surfRiv * 1914 * 0.9)   # 1914 larves/m2 ==> nombre de larves d'Anopheles max par m2
        klfixRiv = int(surfRiv * 1914 * 0.1)
        klvarCult = int(surfCult * 1914 * 0.9)
        klfixCult = int(surfCult * 1914 * 0.1)
        klvarEau = int(surfEau * 1914 * 0.9)
        klfixEau = int(surfEau * 1914 * 0.1)

        if (((m >= 1) and (m <= 7)) or ((m >= 10) and (m <= 12))) :
            klvarRiz = int(surfRiz * 1914 * 0.9)
            klfixRiz = int(surfRiz * 1914 * 0.1)
        else :
        	klfixRiz = int(surfRiz * 1914.0)
        	klvarRiz = 0.0

        raincumul7min = 0.0	# Précipitation par semaine minimum
        raincumul7max = 322.88	# Précipitation par semaine maximum
        pnorm = (raincumul7 - raincumul7min) / (raincumul7max - raincumul7min)	# normalisation des précipitations par semaine
        # fkl = kl.doubleValue()

        klvar = klvarRiv + klvarCult + klvarEau + klvarRiz
        klfix = klfixRiv + klfixCult + klfixEau + klfixRiz

        fkl = klfix + min(klvar * pnorm, klvar) # Calcul capacité de charge

        fkp = fkl

        # dynpop
        # Les parametres du modele
        b1 = 72 # nombre moyen d'oeufs des nullipares
        b2 = 96 # nombre moyen d'oeufs des pares
        sexr = 0.7  # sex ratio
        muPem = 0.1     # taux de mortalite à l'emergence (des P)
        devAh = 2 # taux de developpement des adultes en recherche d'hote
        devAem = 0.8 # taux de developement des adultes emergents

        npastemps = int(1/DT)

        # initialisation
        x1 = row["oeufs"]
        x2 = row["larves"]
        x3 = row["nymphes"]
        x4 = row["aem"]
        x5 = row["a1h"]
        x6 = row["a1g"]
        x7 = row["a1o"]
        x8 = row["a2h"]
        x9 = row["a2g"]
        x10 = row["a2o"]

        k1 = 0.0
        l1 = 0.0
        m1 = 0.0
        n1 = 0.0
        o1 = 0.0
        p1 = 0.0
        q1 = 0.0
        r1 = 0.0
        s1 = 0.0
        t1 = 0.0

        # Resolution des equations
        for y in range(0,npastemps) :
            k1 = fao *(b1*round(x7) + b2*round(x10)) - x1*(fme + fegg)
            l1b = fml*(1.0+x2/fkl) + flarvae
            l1 = fegg*x1 - x2*l1b
            m1 = flarvae*x2 - x3*(fmp+ fpupae)
            n1a = math.exp(-muPem*(1+x3/fkp))
            n1 = fpupae * sexr * x3 * n1a - x4 * (fma + devAem)
            o1 = devAem*x4 - x5*(fmurma + devAh)
            p1 = devAh*x5 - x6*(fma + fag)
            q1 = fag*x6 - x7*(fmurma + fao)
            r1 = fao*(x7 + x10) - x8*(fmurma + devAh)
            s1 = devAh*x8 - x9*(fma + fag)
            t1 = fag*x9 - x10*(fmurma + fao)

            x1 += DT * k1
            x2 += DT * l1
            x3 += DT * m1
            x4 += DT * n1
            x5 += DT * o1
            x6 += DT * p1
            x7 += DT * q1
            x8 += DT * r1
            x9 += DT * s1
            x10 += DT * t1

            # if shp.loc[index, "fokontany"] == "Ambahivahibe" :
            #     print(str(y+1)+ ";" + str(x1) + ";"+str(x2) + ";"+str(x3)
            #                     + ";"+str(x4) + ";"+str(x5)+ ";"+str(x6)
            #                     + ";"+str(x7) + ";"+str(x8)+ ";"+str(x9)
            #                     + ";"+str(x10)
            #                     )

        # Fin boucle for
        shp.loc[index, "oeufs"] = x1
        shp.loc[index, "larves"] = x2
        shp.loc[index, "nymphes"] = x3
        shp.loc[index, "aem"] = x4
        shp.loc[index, "a1h"] = x5
        shp.loc[index, "a1g"] = x6
        shp.loc[index, "a1o"] = x7
        shp.loc[index, "a2h"] = x8
        shp.loc[index, "a2g"] = x9
        shp.loc[index, "a2o"] = x10
        # if shp.loc[index, "fokontany"] == "Ambahivahibe" :
        #     print("oeufs =" + str(x1))

        # CalculAh
        shp.loc[index, "ah"] = shp.loc[index, "a1h"] + shp.loc[index, "a2h"]

        # calculAtot
        shp.loc[index, "adultestot"] = x4 + x5 + x6 + x7 + x8 + x9 + x10


        # Renseignement des dates de validite de prediction pour l'export
        shp.loc[index, "date_debut"] = now.strftime("%Y-%m-%d")	# for Shp export and use with time manager plugin	%Y-%m-%d
        shp.loc[index, "date_fin"] = fin.strftime("%Y-%m-%d")  # in QGIS

        # if shp.loc[index, "fokontany"] == "Ambahivahibe" and w == "s01":
        #     print(str(shp.loc[index, "date_debut"] )+ ";" + str(x1))
        if outputKMLAllDates or outputKMLLastDate and now > bdate_output and test_display == 0 :
                # println("output KML")
        		# classifyAtot()
                d = shp.loc[index, "adultestot"] / shp.loc[index, "SurfFktM2"] * 10000
                shp.loc[index, "Class"] = 1
                if d >= 10 and d < 20:
                    shp.loc[index, "Class"] = 2
                elif d >= 20 and d < 50:
                    shp.loc[index, "Class"] = 3
                elif d >= 50 and d < 100 :
                    shp.loc[index, "Class"] = 4
                elif d >= 100 and d < 200:
                    shp.loc[index, "Class"] = 5
                elif d >= 200 and d < 500:
                    shp.loc[index, "Class"] = 6
                elif d >= 500 and d < 1000 :
                    shp.loc[index, "Class"] = 7
                elif d >= 1000 and d < 2000:
                    shp.loc[index, "Class"] = 8
                elif d >= 2000 and d < 5000:
                    shp.loc[index, "Class"] = 9
                elif d >= 5000 :
                    shp.loc[index, "Class"] = 10

                # # outputKml (now, frequencedisplay, kmlExport)
                styleAtot= "Atot_" + str(shp.loc[index, "Class"])
                _fin = now +  datetime.timedelta(days = FREQUENCE_DISPLAY)

                # kml.addGeometry ("An. coustani",styleAtot, now, _fin, geom, styleAtot,0)
                shp.loc[index, "Name"] = "An. coustani"
                shp.loc[index, "description"] = styleAtot
                shp.loc[index, "begin"] = now.strftime("%Y-%m-%d")
                shp.loc[index, "end"] = _fin.strftime("%Y-%m-%d")
        # Fin de la boucle sur les parcelles

    # Write values in shapefile - a partir de l'annee 2
    if now > bdate_output and test_display == 0 :
        if outputKMLAllDates :
            kml_list = pd.concat([kml_list,shp],ignore_index = True)
        if outputSHPAllDates:
            shp_list = pd.concat([shp_list,shp], ignore_index = True)

    day += 1
    now = now + datetime.timedelta(days = 1)
    # Fin de la boucle sur les jours

# 5) Export KML
if outputKMLAllDates:
    kml_list.to_file(kmlExport, driver='KML')

if outputKMLLastDate :
    shp.to_file(kmlExport1, driver='KML')

# 6) Export SHP
if outputSHPAllDates:
    shp_list = shp_list.loc[:,shp_list.columns.isin(["geometry","mdg_com_co", "mdg_fkt_co", "fokontany","date_debut","date_fin","oeufs","larves","nymphes","ah","adultestot"])]
    shp_list.to_file(shpout, driver='ESRI Shapefile')

if outputSHPLastDate :
    shp= shp.loc[:,shp.columns.isin(["geometry","mdg_com_co", "mdg_fkt_co", "fokontany","date_debut","date_fin","oeufs","larves","nymphes","ah","adultestot"])]
    shp.to_file(shpout1, driver='ESRI Shapefile')

print("Simulation terminee !")
