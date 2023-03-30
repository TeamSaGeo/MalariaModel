import os
import datetime
import pandas as pd
import geopandas as gpd
import math
import fiona
import ntpath

class ModelCoustani:
    def __init__(self, iface):
        fiona.supported_drivers['KML'] = 'rw'
        self.iface = iface

        # 1) Instanciation des datafacers : inputs
        # Donnees meteo
        self.rainCSVData = pd.read_csv(self.iface.rainFileName.text(),delimiter=";")# le fichier texte (csv) avec les donnees Meteo : pluies
        self.tempCSVData = pd.read_csv(self.iface.tempFileName.text(),delimiter=";") # le fichier texte (csv) avec les donnees Meteo : temperatures
        # # Parcelles
        self.shp = gpd.read_file(self.iface.parcelFileName.text()) # le shapefile avec les parcelles

    def getOutputPath (self, bdate_output, format, oneDate):
        filename =  ntpath.basename(self.iface.parcelFileName.text()).split('.')[0]
        extension = self.iface.edate.date().toString("yyyyMMdd") + format
        if oneDate:
            filename += extension
        else:
            filename += bdate_output.toString("yyyyMMdd_") + extension
        return os.path.join(self.iface.pathOutput.text(),filename)

    def getWeeklyRainValue(self,codeCommune,now,w):
        return self.rainCSVData.loc[(self.rainCSVData['CodeCommune'] == codeCommune) & (self.rainCSVData['numero_annee'] == now.year()) , w].values[0]

    def initialisation(self, bdate_output):
        # 2) Instanciation des datafacers : outputs
        # SHP 1 date
        self.shpout1 = self.getOutputPath(bdate_output, ".shp", True)
        # SHP multidates
        self.shpout = self.getOutputPath(bdate_output, ".shp", False) 	# le fichier ShapeFile en sortie : toutes les dates
        # KML 1 date
        self.kmlExport1 = self.getOutputPath(bdate_output, ".kml", True)
        # KML multidates
        self.kmlExport = self.getOutputPath(bdate_output, ".kml", False)
        # CSV 1 date
        self.csvExport1 = self.getOutputPath(bdate_output, ".csv", True)
        # CSV multidates
        self.csvExport = self.getOutputPath(bdate_output, ".csv", False)

        # # 4) Initialisation
        self.shp["oeufs"] = 10000000.0
        self.shp["larves"] = 0.0
        self.shp["nymphes"] = 0.0
        self.shp["aem"] = 0.0
        self.shp["a1h"] = 0.0
        self.shp["a1g"] = 0.0
        self.shp["a1o"] = 0.0
        self.shp["a2h"] = 0.0
        self.shp["a2g"] = 0.0
        self.shp["a2o"] = 0.0
        self.shp["rain7"] = 0.0
        self.shp["raincumul7"] = 0.0
        self.shp["rainday7"] = 0.0

    def simulation(self,now,w,w7,day,bdate_output,frequence_display):
        test_display = math.remainder(day,frequence_display)	# pour l'export des donnees tous les frequencedisplay jours
        fin = now.addDays(frequence_display - 1)

        # Boucle sur les parcelles
        for index, row in self.shp.iterrows():
            # Read Meteo
            codeCommune = row["mdg_com_co"]
            rain = self.getWeeklyRainValue(codeCommune,now,w) / 7
            temperature = self.tempCSVData.loc[(self.tempCSVData['CodeCommune'] == codeCommune) & (self.tempCSVData['numero_annee'] == now.year()) , w].values[0]
            # w7 = self.getWeekNumber(now.addDays(-7).weekNumber()[0])
            # if w7 == "s53" :
            #     # try :
            #     #     rain7 = rainCSVData.loc[(rainCSVData['CodeCommune'] == codeCommune) & (rainCSVData['numero_annee'] == (now.year - 1)) , "s52"].values[0]
            #     #     raincumul7 = rainCSVData.loc[(rainCSVData['CodeCommune'] == codeCommune) & (rainCSVData['numero_annee'] == (now.year - 1)) , "s52"].values[0]
            #     # except IndexError:
            #     rain7 = self.getWeeklyRainValue(codeCommune,now,"s52") / 7
            #     raincumul7 = self.getWeeklyRainValue(codeCommune,now,"s52")
            # else:
            rain7 = self.getWeeklyRainValue(codeCommune,now,w7) / 7
            raincumul7 =  self.getWeeklyRainValue(codeCommune,now,w7)

            # Updatefunction
            # Egg development
            TE = 12.9
            TDDE = 26.6
            fegg = 0.0
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
            m = now.month()
            # surfRiv = row["RivieresM2"] if not math.isnan(row["RivieresM2"]) else 0
            # surfCult = row["CultAgriM2"] if not math.isnan(row["CultAgriM2"]) else 0
            # surfEau = row["PlanDeauM2"] if not math.isnan(row["PlanDeauM2"]) else 0
            # surfRiz = row["RizieresM2"] if not math.isnan(row["RizieresM2"]) else 0
            surfRiv = row["RivieresM2"]
            surfCult = row["CultAgriM2"]
            surfEau = row["PlanDeauM2"]
            surfRiz = row["RizieresM2"]

            klvarRiv = int(surfRiv * 1914 * 0.9)  if not math.isnan(surfRiv) else surfRiv # 1914 larves/m2 ==> nombre de larves d'Anopheles max par m2
            klfixRiv = int(surfRiv * 1914 * 0.1) if not math.isnan(surfRiv) else surfRiv
            klvarCult = int(surfCult * 1914 * 0.9) if not math.isnan(surfCult) else surfCult
            klfixCult = int(surfCult * 1914 * 0.1) if not math.isnan(surfCult) else surfCult
            klvarEau = int(surfEau * 1914 * 0.9) if not math.isnan(surfEau) else surfEau
            klfixEau = int(surfEau * 1914 * 0.1) if not math.isnan(surfEau) else surfEau

            if (((m >= 1) and (m <= 7)) or ((m >= 10) and (m <= 12))) :
                klvarRiz = int(surfRiz * 1914 * 0.9) if not math.isnan(surfRiz) else surfRiz
                klfixRiz = int(surfRiz * 1914 * 0.1) if not math.isnan(surfRiz) else surfRiz
            else :
            	klfixRiz = int(surfRiz * 1914.0) if not math.isnan(surfRiz) else surfRiz
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

            DT = 0.1
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
                try:
                    k1 = fao *(b1*round(x7) + b2*round(x10)) - x1*(fme + fegg)
                except:
                    k1 = float("nan")
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

            # Fin boucle for

            self.shp.loc[index, "oeufs"] = x1
            self.shp.loc[index, "larves"] = x2
            self.shp.loc[index, "nymphes"] = x3
            self.shp.loc[index, "aem"] = x4
            self.shp.loc[index, "a1h"] = x5
            self.shp.loc[index, "a1g"] = x6
            self.shp.loc[index, "a1o"] = x7
            self.shp.loc[index, "a2h"] = x8
            self.shp.loc[index, "a2g"] = x9
            self.shp.loc[index, "a2o"] = x10

            # CalculAh
            self.shp.loc[index, "ah"] = self.shp.loc[index, "a1h"] + self.shp.loc[index, "a2h"]
            # calculAtot
            self.shp.loc[index, "adultestot"] = x4 + x5 + x6 + x7 + x8 + x9 + x10
            # Renseignement des dates de validite de prediction pour l'export
            self.shp.loc[index, "date_debut"] = now.toString("yyyy-MM-dd")	# for Shp export and use with time manager plugin	%Y-%m-%d
            self.shp.loc[index, "date_fin"] = fin.toString("yyyy-MM-dd")  # in QGIS

            if self.iface.outputKML.isChecked() and now > bdate_output and test_display == 0 :
                # println("output KML")
        		# classifyAtot()
                d = self.shp.loc[index, "adultestot"] / self.shp.loc[index, "SurfFktM2"] * 10000
                self.shp.loc[index, "Class"] = 1
                if d >= 10 and d < 20:
                    self.shp.loc[index, "Class"] = 2
                elif d >= 20 and d < 50:
                    self.shp.loc[index, "Class"] = 3
                elif d >= 50 and d < 100 :
                    self.shp.loc[index, "Class"] = 4
                elif d >= 100 and d < 200:
                    self.shp.loc[index, "Class"] = 5
                elif d >= 200 and d < 500:
                    shp.loc[index, "Class"] = 6
                elif d >= 500 and d < 1000 :
                    self.shp.loc[index, "Class"] = 7
                elif d >= 1000 and d < 2000:
                    self.shp.loc[index, "Class"] = 8
                elif d >= 2000 and d < 5000:
                    self.shp.loc[index, "Class"] = 9
                elif d >= 5000 :
                    self.shp.loc[index, "Class"] = 10

                # # outputKml (now, frequencedisplay, kmlExport)
                styleAtot= "Atot_" + str(self.shp.loc[index, "Class"])
                _fin = now +  datetime.timedelta(days = frequence_display)

                # kml.addGeometry ("An. coustani",styleAtot, now, _fin, geom, styleAtot,0)
                self.shp.loc[index, "Name"] = "An. coustani"
                self.shp.loc[index, "description"] = styleAtot
                self.shp.loc[index, "begin"] = now.strftime("%Y-%m-%d")
                self.shp.loc[index, "end"] = _fin.strftime("%Y-%m-%d")

        # Fin de la boucle sur les parcelles
        return test_display

    def exportResult(self,shp_list,kml_list):
        # # 5) Export KML
        if self.iface.outputKML.isChecked():
            if self.iface.multidate.isChecked():
                kml_list.to_file(self.kmlExport, driver='KML')
            else:
                self.shp.to_file(self.kmlExport1, driver='KML')

        # 6) Export SHP
        if self.iface.outputSHP.isChecked():
            if self.iface.multidate.isChecked():
                shp_list = shp_list.loc[:,shp_list.columns.isin(["geometry","mdg_com_co", "mdg_fkt_co", "fokontany","date_debut","date_fin","oeufs","larves","nymphes","ah","adultestot"])]
                shp_list.to_file(self.shpout, driver='ESRI Shapefile')
            else:
                self.shp= self.shp.loc[:,self.shp.columns.isin(["geometry","mdg_com_co", "mdg_fkt_co", "fokontany","date_debut","date_fin","oeufs","larves","nymphes","ah","adultestot"])]
                self.shp.to_file(self.shpout1, driver='ESRI Shapefile')

        # # 5) Export CSV
        if self.iface.outputCSV.isChecked():
            if self.iface.multidate.isChecked():
                shp_list = shp_list.loc[:,shp_list.columns.isin(["geometry","mdg_com_co", "mdg_fkt_co", "fokontany","date_debut","date_fin","oeufs","larves","nymphes","ah","adultestot"])]
                shp_list.drop('geometry',axis=1).to_csv(self.csvExport)
            else:
                self.shp= self.shp.loc[:,self.shp.columns.isin(["geometry","mdg_com_co", "mdg_fkt_co", "fokontany","date_debut","date_fin","oeufs","larves","nymphes","ah","adultestot"])]
                self.shp.drop('geometry',axis=1).to_csv(self.csvExport1)
