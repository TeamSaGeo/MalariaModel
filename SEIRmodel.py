import math
import fiona
from PyQt6 import QtCore

class SEIRModel:
    def __init__(self,filename,shp,rainCSVData,tempCSVData):
        self.filename = filename
        self.shp = shp
        self.rainCSVData = rainCSVData
        self.tempCSVData = tempCSVData
        self.shpExport = ""
        self.csvExport = ""
        self.kmlExport = ""

    def setShpExport(self,path):
        self.shpExport = path

    def setCsvExport(self,path):
        self.csvExport = path

    def setKmlExport(self,path):
        self.kmlExport = path

    def setFrequence_display(self,frequence_display):
        self.frequence_display = frequence_display

    def setBDateOutput(self, bdate_output, minimumDate):
        self.bdate_output = bdate_output
        self.bdate = self.bdate_output.addYears(-1)
        if self.bdate < minimumDate:
            self.bdate = minimumDate

    def initialisation(self, paramKL):
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
        self.shp["ahE"] = 0.0
        self.shp["ahI"] = 0.0
        self.shp["humS"] = self.shp[paramKL[6]]
        self.shp["humE"] = 0.0
        self.shp["humI"] = 0.0
        self.shp["humR"] = 0.0

    def getRainExtreme(self, df, paramMeteo, lieu):
        min =  df.loc[df[paramMeteo[0]] == lieu, paramMeteo[4]].min() 	# Précipitation minimum
        max =  df.loc[df[paramMeteo[0]] == lieu, paramMeteo[4]].max()	# 322.88 Précipitation maximum
        return min, max

    def getWeeklyParamValue(self, df, paramMeteo,lieu,year,w):
        try:
            val = df.loc[(df[paramMeteo[0]] == lieu) & (df[paramMeteo[1]] == year) & (df[paramMeteo[2]] == w) , paramMeteo[4]].values[0]
        except IndexError:
            val = float("nan")
        return val

    def getMonthlyParamValue(self, df, paramMeteo,lieu,now):
        try:
            val = df.loc[(df[paramMeteo[0]] == lieu) & (df[paramMeteo[1]] == now.year()) & (df[paramMeteo[2]] == now.month()) , paramMeteo[4]].values[0]
        except IndexError:
            val = float("nan")
        return val

    def getDailyParamValue(self, df, paramMeteo,lieu,now):
        try:
            val = df.loc[(df[paramMeteo[0]] == lieu) & (df[paramMeteo[1]] == now.year()) & (df[paramMeteo[2]] == now.month()) & (df[paramMeteo[3]] == now.day()) , paramMeteo[4]].values[0]
        except IndexError:
            val = float("nan")
        return val

    def getWeekNumber(self,w):
        if w < 10:
            return "s0" + str(w)
        else:
            return "s" + str(w)

    def simulation(self,now,freq_meteo,day,paramKL,paramMeteo,cas_infectes):
        test_display = math.remainder(day,self.frequence_display)	# pour l'export des donnees tous les frequencedisplay jours
        fin = now.addDays(self.frequence_display - 1)

        if freq_meteo == "week":
            w = self.getWeekNumber(now.weekNumber()[0]) # Obtenir la semaine courante de l'année (exemple "S1")
            # w7 = self.getWeekNumber(now.addDays(-7).weekNumber()[0]) # Obtenir la semaine précédent de l'année (exemple "S52")

        TE = 12.9
        TDDE = 28.55 # 26.6
        fegg = 0.0
        TAg = 9.9
        TDDAg = 36.5
        fao = 2.0 # fAo
        fme = 0.1 # Taux de mortalite des oeufs
        mur = 0.08 # taux de mortalité additionnelle du comportement de recherche (d'hôtes et de sites de ponte)
        # raincumul7min = 0.0	# Précipitation par semaine minimum
        # raincumul7max = 322.87	# 322.88 Précipitation par semaine maximum

        tempmin = 16	# Température minimale de survie des Plasmodium
        # dynpop
        # Les parametres du modele
        b1 = 65 # 72 nombre moyen d'oeufs des nullipares
        b2 = 93 # 96 nombre moyen d'oeufs des pares
        sexr = 0.72  # 0.7 sex ratio
        muPem = 0.1     # taux de mortalite à l'emergence (des P)
        devAh = 2 # taux de developpement des adultes en recherche d'hote
        devAem = 0.8 # taux de developement des adultes emergents
        mui = 0.08	# taux de mortalité Anopheles infectés (hypothèse ==> même que mur)

        om1 = 0.533	# taux d'infection chez les humains (omega 1)
        om2 = 0.09	# taux d'infection chez les Anopheles (omega 2)
        ph = 0.00136	# taux de perte de l'immunité (phi h)
        th = 0.0714 # 1/14	// taux d'incubation chez les humains (teta h)
        gh = 0.143 # 1/6.9(Wadjo, 2020) 0.005	// taux de guérison (gamma h) - a verifier
        DT = 0.1
        npastemps = int(1/DT)

        for index, row in self.shp.iterrows():
            lieu = row[paramKL[0]]

            ## Read Meteo
            rain_min, rain_max = self.getRainExtreme(self.rainCSVData,paramMeteo[0],lieu)
            # Get daily data meteo values from weekly value
            if freq_meteo == "week":
                temperature = self.getWeeklyParamValue(self.tempCSVData, paramMeteo[1],lieu,now.year(),w)
                rain = self.getWeeklyParamValue(self.rainCSVData,paramMeteo[0],lieu,now.year(),w)
                # # Cumul des pluies de la semaine précédente
                # if w == "s01" :
                #     if now != self.bdate:
                #         previous_rain = self.getWeeklyParamValue(self.rainCSVData,paramMeteo[0],lieu,now.year(),w)
                #     else:
                #         previous_rain = rain
                #     print(now, (now.year() - 1), w7, previous_rain)
                # else:
                #     previous_rain = self.getWeeklyParamValue(self.rainCSVData, paramMeteo[0],lieu,now,w7)

            # Get daily data meteo values from monthly value
            elif freq_meteo == "month":
                temperature = self.getMonthlyParamValue(self.tempCSVData, paramMeteo[1],lieu,now)
                # nbdays_in_month = monthrange(now.year(), now.month())[1]
                rain = self.getMonthlyParamValue(self.rainCSVData, paramMeteo[0],lieu,now)

            # Get daily data meteo values
            else:
                temperature = self.getDailyParamValue(self.tempCSVData, paramMeteo[1], lieu, now)
                rain = self.getDailyParamValue(self.rainCSVData, paramMeteo[0],lieu,now)

            # normalisation des précipitations
            pnorm = (rain - rain_min) / (rain_max - rain_min)

            # Updatefunction
            # Egg development
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
            if temperature > TAg :
                fag1= temperature - TAg
                fag = fag1 / TDDAg

            # Taux de mortalite des larves et des nymphes
            fml1 = math.exp(-temperature/2)
            fml = fml1 + 0.08

            # Taux de mortalite des nymphes
            # fmp = fml

            # Taux de mortalite des adultes
            fma1 = 0.000148 * temperature * temperature
            fma = 0.1-0.00667 *temperature + fma1
            if fma<0.033:
                fma=0.033

            # Taux de mortalite en recherche d'hote
            fmurma = fma + mur

            # capacite du milieu en larves
            m = now.month()

            surfEau = row[paramKL[1]]
            surfRiv = row[paramKL[2]]
            surfCult = row[paramKL[3]]
            surfRiz = row[paramKL[4]]
            surfTot = row[paramKL[5]]
            nbrepop= row[paramKL[6]]

            # Si les valeurs des gites larvaires sont nulles alors les valeurs des paramètres KL seront nulles
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

            # fkl = kl.doubleValue()

            klvar = klvarRiv + klvarCult + klvarEau + klvarRiz
            klfix = klfixRiv + klfixCult + klfixEau + klfixRiz

            fkl = klfix + min(klvar * pnorm, klvar) # Calcul capacité de charge

            # fkp = fkl
            # Taux d'incubation chez les Anopheles
            fia = (temperature + tempmin)/111

            # c = surfSettlement/surfTot
            c = 0.01 # example
            try:
                tp = self.shp.loc[index, "ah"]/self.shp.loc[index, "adultestot"]	# taux de piqûre
            except :
                tp = 0

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
            x11aE = row["ahE"]
            x11aI = row["ahI"]
            if  now.daysTo(cas_infectes["date_intro"]) == 0:
                x12I = cas_infectes["nb_pers"]
                x12S = row["humS"] - x12I
            else:
                x12I = row["humI"]
                x12S = row["humS"]
            x12E = row["humE"]
            x12R = row["humR"]

            k1 = l1 = m1 = n1 = o1 = p1 = q1 = r1 = s1 = t1 = u1 = u2 = v1 = v2 = v3 = v4 = 0.0

            # Resolution des equations
            for y in range(0,npastemps) :
                try:
                    k1 = fao *(b1*round(x7) + b2*round(x10)) - x1*(fme + fegg)
                except:
                    k1 = float("nan")
                l1b = fml*(1.0+x2/fkl) + flarvae
                l1 = fegg*x1 - x2*l1b
                m1 = flarvae*x2 - x3*(fml+ fpupae)
                n1a = math.exp(-muPem*(1+x3/fkl))
                n1 = fpupae * sexr * x3 * n1a - x4 * (fma + devAem)
                o1 = devAem*x4 - x5*(fmurma + devAh)
                p1 = devAh*x5 - x6*(fma + fag)
                q1 = fag*x6 - x7*(fmurma + fao)
                r1 = fao*(x7 + x10) - x8*(fmurma + devAh)
                s1 = devAh*x8 - x9*(fma + fag)
                t1 = fag*x9 - x10*(fmurma + fao)

                u1 = om2*x12I*(x5+x8)/nbrepop*0.2 - x11aE*(fma + fia)	# équation de aE // rq AT : pas besoin de tp
                u2 = fia*x11aE - x11aI*(fma + mui)	# résolution de a1
                v1 = ph*x12R - x12S*om1*tp*c*x11aI/nbrepop	# équation de humS // rq AT ici aussi ajout de devAh
                v2 = x12S*om1*tp*c*x11aI/nbrepop - th*x12E	# équation de humE
    			#v2 = ((om1*tp*x12S)/nbrepop) - th*x12E	# équation de humE // rq AT : il y avait une erreur dans cette equation
                v3 = (th*x12E) - (gh*x12I)	# équation de humI
                v4 = (gh*x12I) - (ph*x12R)	# équation de humR

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
                x11aE += DT * u1
                x11aI += DT * u2
                x12S += DT * v1
                x12E += DT * v2
                x12I += DT * v3
                x12R += DT * v4
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
            self.shp.loc[index, "ahE"] = x11aE
            self.shp.loc[index, "ahI"] = x11aI
            self.shp.loc[index, "humS"] = int(max(0,x12S))
            self.shp.loc[index, "humE"] = int(max(0,x12E))
            self.shp.loc[index, "humI"] = int(max(0,x12I))
            self.shp.loc[index, "humR"] = int(max(0,x12R))

            # CalculAh
            self.shp.loc[index, "ah"] = x5 + x8

            # calculAtot
            self.shp.loc[index, "adultestot"] = x4 + x5 + x6 + x7 + x8 + x9 + x10

            # Renseignement des dates de validite de prediction pour l'export
            self.shp.loc[index, "date_debut"] = now.toString("yyyy-MM-dd")	# for Shp export and use with time manager plugin	%Y-%m-%d
            self.shp.loc[index, "date_fin"] = fin.toString("yyyy-MM-dd")  # in QGIS
            if now.month() != fin.month() and now.daysTo(QtCore.QDate(fin.year(), fin.month(), 1)) > 5:
                self.shp.loc[index, "mois"] = now.toString("MMM")
                self.shp.loc[index, "année"] = now.toString("yyyy")
                self.shp.loc[index, "mois-année"] = now.toString("MMM-yy")
            else:
                self.shp.loc[index, "mois"] = fin.toString("MMM")
                self.shp.loc[index, "année"] = fin.toString("yyyy")
                self.shp.loc[index, "mois-année"] = fin.toString("MMM-yy")

            if self.kmlExport and now > self.bdate_output and test_display == 0 :
                d = self.shp.loc[index, "adultestot"] / self.shp.loc[index, paramKL[5]] * 10000
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
                _fin = now.addDays(self.frequence_display)

                # kml.addGeometry ("An. coustani",styleAtot, now, _fin, geom, styleAtot,0)
                self.shp.loc[index, "Name"] = "An. SEIR model"
                self.shp.loc[index, "description"] = styleAtot
                self.shp.loc[index, "begin"] = now.toString("YYYY-MM-dd")
                self.shp.loc[index, "end"] = _fin.toString("YYYY-MM-dd")

        return test_display

    def exportResult(self,shp_list,kml_list,multidate, checked_columns):
        fiona.supported_drivers['KML'] = 'rw'

        if self.kmlExport:
            if multidate:
                kml_list.to_file(self.kmlExport, driver='KML')
            else:
                self.shp.to_file(self.kmlExport, driver='KML')

        columnsName = ["geometry","mdg_com_co", "mdg_fkt_co", "fokontany","date_debut","date_fin","mois", "année", "mois-année"] + checked_columns

        # 6) Export SHP
        if self.shpExport:
            if multidate:
                shp_list = shp_list.loc[:,shp_list.columns.isin(columnsName)]
                shp_list.to_file(self.shpExport, driver='ESRI Shapefile')
            else:
                self.shp= self.shp.loc[:,self.shp.columns.isin(columnsName)]
                self.shp.to_file(self.shpExport, driver='ESRI Shapefile')

        # # 5) Export CSV
        if self.csvExport:
            if multidate:
                shp_list = shp_list.loc[:,shp_list.columns.isin(columnsName)]
                shp_list.drop('geometry',axis=1).to_csv(self.csvExport, sep=";", decimal=",", index=False, encoding="utf-8")
            else:
                self.shp= self.shp.loc[:,self.shp.columns.isin(columnsName)]
                self.shp.drop('geometry',axis=1).to_csv(self.csvExport, sep=";", decimal=",", index=False, encoding="utf-8")
