import gc
import time
from datetime import datetime

from Empire import run_empire
from reader import generate_tab_files
from scenario_random import generate_random_scenario

########
##USER##
########

USE_TEMP_DIR = True #True/False
temp_dir = './'
version = 'hydrogenAllCountries'
NoOfPeriods = 8
NoOfScenarios = 3
NoOfRegSeason = 4
lengthRegSeason = 168
regular_seasons = ["winter", "spring", "summer", "fall"]
NoOfPeakSeason = 2
lengthPeakSeason = 24
discountrate = 0.05
WACC = 0.05
LeapYearsInvestment = 5
solver = "Gurobi" #"Gurobi" #"CPLEX" #"Xpress"
scenariogeneration = True #True #False
EMISSION_CAP = True #False
WRITE_LP = False #True
PICKLE_INSTANCE = False #True 
OptimizingWithBinaries = False
hydrogen=True
hydrogenPercentages = [100] #Make it a whole number, this is divided by 100 later to make it a fraction between 0 and 1
otherMarketNodes = ['Germany', 'France', 'Spain','Austria','Italy','Greece']
h2priceOtherMarkets = 1
exactSolution = False
h2storage = False
TIME_LIMIT = 0
time_format = "%d/%m/%Y %H:%M"
north_sea = True
fix_sample = False


""" ### TEST-CONFIG ###
USE_TEMP_DIR = True #True/False
temp_dir = './'
version = 'hydrogenAllCountries' #two-period-test
NoOfPeriods = 8 #2
NoOfScenarios = 1
NoOfRegSeason = 4
lengthRegSeason = 24
regular_seasons = ["winter", "spring", "summer", "fall"]
NoOfPeakSeason = 2
lengthPeakSeason = 24
discountrate = 0.05
WACC = 0.05
LeapYearsInvestment = 5
solver = "Gurobi" #"Gurobi" #"CPLEX" #"Xpress"
scenariogeneration = True #True #False
EMISSION_CAP = False #False
WRITE_LP = False #True
PICKLE_INSTANCE = False #True 
OptimizingWithBinaries = False
hydrogen=True
hydrogenPercentages = [100] #Make it a whole number, this is divided by 100 later to make it a fraction between 0 and 1
otherMarketNodes = ['Germany', 'France', 'Spain','Austria','Italy','Greece']
h2priceOtherMarkets = 1
exactSolution = False
h2storage = False
TIME_LIMIT = 0
time_format = "%d/%m/%Y %H:%M"
north_sea = True
fix_sample = False """

#######
##RUN##
#######
# for i in range(1,13):
for hydrogenPercentage in hydrogenPercentages:
    name = version + '_H2Percentage' + str(hydrogenPercentage)
    if h2storage is True:
        name = name + '_withStorage'
    else:
        name = name + '_noStorage'
    if scenariogeneration:
        name = name + "_randomSGR" + '_scen' + str(NoOfScenarios)
    else:
        name = name + "_noSGR"
    # name = name + str(datetime.now().strftime("_%Y%m%d%H%M"))
    workbook_path = 'Data handler/' + version
    tab_file_path = 'Data handler/' + version + '/Tab_Files_' + name
    scenario_data_path = 'Data handler/' + version + '/ScenarioData'
    result_file_path = 'Results/' + version + '/' + name
    FirstHoursOfRegSeason = [lengthRegSeason*i + 1 for i in range(NoOfRegSeason)]
    FirstHoursOfPeakSeason = [lengthRegSeason*NoOfRegSeason + lengthPeakSeason*i + 1 for i in range(NoOfPeakSeason)]
    Period = [i + 1 for i in range(NoOfPeriods)]
    Scenario = ["scenario"+str(i + 1) for i in range(NoOfScenarios)]
    peak_seasons = ['peak'+str(i + 1) for i in range(NoOfPeakSeason)]
    Season = regular_seasons + peak_seasons
    Operationalhour = [i + 1 for i in range(FirstHoursOfPeakSeason[-1] + lengthPeakSeason - 1)]
    HoursOfRegSeason = [(s,h) for s in regular_seasons for h in Operationalhour \
                     if h in list(range(regular_seasons.index(s)*lengthRegSeason+1,
                                   regular_seasons.index(s)*lengthRegSeason+lengthRegSeason+1))]
    HoursOfPeakSeason = [(s,h) for s in peak_seasons for h in Operationalhour \
                         if h in list(range(lengthRegSeason*len(regular_seasons)+ \
                                            peak_seasons.index(s)*lengthPeakSeason+1,
                                            lengthRegSeason*len(regular_seasons)+ \
                                                peak_seasons.index(s)*lengthPeakSeason+ \
                                                    lengthPeakSeason+1))]
    HoursOfSeason = HoursOfRegSeason + HoursOfPeakSeason
    dict_countries = {"AT": "Austria", "BA": "BosniaH", "BE": "Belgium",
                      "BG": "Bulgaria", "CH": "Switzerland", "CZ": "CzechR",
                      "DE": "Germany", "DK": "Denmark", "EE": "Estonia",
                      "ES": "Spain", "FI": "Finland", "FR": "France",
                      "GB": "GreatBrit.", "GR": "Greece", "HR": "Croatia",
                      "HU": "Hungary", "IE": "Ireland", "IT": "Italy",
                      "LT": "Lithuania", "LU": "Luxemb.", "LV": "Latvia",
                      "MK": "Macedonia", "NL": "Netherlands", "NO": "Norway",
                      "PL": "Poland", "PT": "Portugal", "RO": "Romania",
                      "RS": "Serbia", "SE": "Sweden", "SI": "Slovenia",
                      "SK": "Slovakia", "MF": "MorayFirth", "FF": "FirthofForth",
                      "DB": "DoggerBank", "HS": "Hornsea", "OD": "OuterDowsing",
                      "NF": "Norfolk", "EA": "EastAnglia", "BS": "Borssele",
                      "HK": "HollandseeKust", "HB": "HelgoländerBucht", "NS": "Nordsøen",
                      "EHEU": "EnergyhubEU", 'NVEA': 'NordvestA', 'NVEC': 'NordvestC',
                      'VVA': 'VestavindA', 'SNVA': 'SønnavindA', 'SRVC': 'SørvestC',
                      'NVEB': 'NordvestB', 'VVF': 'VestavindF', 'SRVE': 'SørvestE',
                      'SRVA': 'SørvestA', 'VVB': 'VestavindB', 'VVC': 'VestavindC',
                      'VVD': 'VestavindD', 'SRVF': 'SørvestF', 'SRVB': 'SørvestB',
                      'NAVB': 'NordavindB', 'NAVA': 'NordavindA', 'NAVD': 'NordavindD', 
                      'NAVC': 'NordavindC', 'VVE': 'VestavindE', 'SRVD': 'SørvestD'}
    offshoreNodesList = ["Energyhub EU"]
    windfarmNodes = ["Moray Firth","Firth of Forth","Dogger Bank",
                     "Hornsea","Outer Dowsing","Norfolk","East Anglia",
                     "Borssele","Hollandsee Kust","Helgoländer Bucht",
                     "Nordsøen",'Nordvest A', 'Nordvest C', 'Vestavind A', 
                     'Sønnavind A', 'Sørvest C', 'Nordvest B', 'Vestavind F', 
                     'Sørvest E', 'Sørvest A', 'Vestavind B', 'Vestavind C',
                     'Vestavind D', 'Sørvest F', 'Sørvest B', 'Nordavind B', 
                     'Nordavind A', 'Nordavind D', 'Nordavind C', 'Vestavind E', 'Sørvest D']

    print('++++++++')
    print('+EMPIRE+')
    print('++++++++')
    print('Solver: ' + solver)
    print('Scenario Generation: ' + str(scenariogeneration))
    print('++++++++')
    print('ID: ' + name)
    print('++++++++')
    print('Hydrogen: ' + str(hydrogen))
    print('++++++++')


    if scenariogeneration:
        tick = time.time()
        generate_random_scenario(filepath = scenario_data_path,
                                 tab_file_path = tab_file_path,
                                 scenarios = NoOfScenarios,
                                 seasons = regular_seasons,
                                 Periods = NoOfPeriods,
                                 regularSeasonHours = lengthRegSeason,
                                 peakSeasonHours = lengthPeakSeason,
                                 dict_countries = dict_countries,
                                 time_format = time_format,
                                 fix_sample = fix_sample,
                                 north_sea = north_sea)
        tock = time.time()
        print("{hour}:{minute}:{second}: Scenario generation took [sec]:".format(
        hour=datetime.now().strftime("%H"), minute=datetime.now().strftime("%M"), second=datetime.now().strftime("%S")) + str(tock - tick))

    generate_tab_files(filepath = workbook_path, tab_file_path = tab_file_path,
                       scenariogeneration = scenariogeneration, hydrogen = hydrogen)

    run_empire(name = name,
               tab_file_path = tab_file_path,
               result_file_path = result_file_path,
               scenariogeneration = scenariogeneration,
               scenario_data_path = scenario_data_path,
               solver = solver,
               temp_dir = temp_dir,
               FirstHoursOfRegSeason = FirstHoursOfRegSeason,
               FirstHoursOfPeakSeason = FirstHoursOfPeakSeason,
               lengthRegSeason = lengthRegSeason,
               lengthPeakSeason = lengthPeakSeason,
               Period = Period,
               Operationalhour = Operationalhour,
               Scenario = Scenario,
               Season = Season,
               HoursOfSeason = HoursOfSeason,
               discountrate = discountrate,
               WACC = WACC,
               LeapYearsInvestment = LeapYearsInvestment,
               WRITE_LP = WRITE_LP,
               PICKLE_INSTANCE = PICKLE_INSTANCE,
               EMISSION_CAP = EMISSION_CAP,
               USE_TEMP_DIR = USE_TEMP_DIR,
               offshoreNodesList = offshoreNodesList,
               verboseResultWriting = False,
               optimizingWithBinaries = OptimizingWithBinaries,
               hydrogen = hydrogen,
               hydrogenPercentage = 100/100,
               exactSolution = exactSolution,
               TIME_LIMIT = TIME_LIMIT,
               h2storage = h2storage,
               h2priceOtherMarkets = h2priceOtherMarkets,
               otherMarketNodes = otherMarketNodes,
               windfarmNodes = windfarmNodes)
    gc.collect()