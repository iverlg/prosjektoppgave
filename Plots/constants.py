# Definition of offshore areas/nodes
WIND_FARM_NODES = ['HelgoländerBucht', 'NordvestA', 'MorayFirth', 'DoggerBank', 'Hornsea', 'Nordsøen', 'FirthofForth', 'VestavindA', 'Norfolk', 'SønnavindA', 'EastAnglia', 'HollandseeKust', 'SørvestA', 'VestavindB', 'OuterDowsing', 'Borssele', 'VestavindC', 'NordvestB', 'SørvestE', 'NordavindC', 'SørvestF', 'NordvestC', 'NordavindB', 'SørvestC', 'VestavindE', 'SørvestD', 'SørvestB', 'VestavindF', 'NordavindD', 'VestavindD', 'NordavindA']
NO_NODES = ['Nordvest A', 'Nordvest C', 'Vestavind A', 
                     'Sønnavind A', 'Sørvest C', 'Nordvest B', 'Vestavind F', 
                     'Sørvest E', 'Sørvest A', 'Vestavind B', 'Vestavind C',
                     'Vestavind D', 'Sørvest F', 'Sørvest B', 'Nordavind B', 
                     'Nordavind A', 'Nordavind D', 'Nordavind C', 'Vestavind E', 'Sørvest D']
NO_NODES = [node.replace(" ", "") for node in NO_NODES]
ENERGY_HUBS = ["Energyhub EU", "Energyhub North", "Energyhub Central"]
NORDIC_NODES = ['NO1', 'NO2', 'NO3', 'NO4', 'NO5', 'Denmark', 'Sweden', 'Finland']
OFFSHORE_AREAS = WIND_FARM_NODES + [hub.replace(" ", "") for hub in ENERGY_HUBS]

# Consistent color mapping on graphs
TECH_TO_COLOR = {'Solar': '#ffe119', 'Windonshore': '#4363d8', 'Bio': '#3cb44b', 'Nuclear': '#e6194B', 'Windoffshoregrounded': '#f58231', 'GasOCGT': '#911eb4', 'Hydrorun-of-the-river': '#42d4f4', 'Hydroregulated': '#f032e6', 'GasCCGT': '#bfef45', 'Windoffshorefloating': '#fabed4', 'Lignite': '#469990', 'Waste': '#dcbeff', 'Bio10cofiring': '#9A6324', 'Wave': '#fffac8', 'Geo': '#800000', 'Coal': '#aaffc3', 'Bioexisting': '#808000', 'Oilexisting': '#ffd8b1', 'GasCCSadv': '#000075', 'Gasexisting': '#a9a9a9', 'CoalCCSadv': [0.188235, 0.635294, 0.854902], 'Bio10cofiringCCS': [0.988235, 0.309804, 0.188235], 'LigniteCCSsup': [0.898039, 0.682353, 0.219608], 'CoalCCS': [0.427451, 0.564706, 0.309804], 'GasCCS': [0.545098, 0.545098, 0.545098], 'Coalexisting': [0.090196, 0.745098, 0.811765], 'LigniteCCSadv': [0.580392, 0.403922, 0.741176], 'Liginiteexisting': [0.839216, 0.152941, 0.156863]}
WIND_FARM_NODES_TO_COLOR = {'HelgoländerBucht': [0.121569, 0.466667, 0.705882], 'NordvestA': [1.0, 0.498039, 0.054902], 'MorayFirth': [0.172549, 0.627451, 0.172549], 'DoggerBank': [0.839216, 0.152941, 0.156863], 'Hornsea': [0.580392, 0.403922, 0.741176], 'Nordsøen': [0.54902, 0.337255, 0.294118], 'FirthofForth': [0.890196, 0.466667, 0.760784], 'VestavindA': [0.498039, 0.498039, 0.498039], 'Norfolk': [0.737255, 0.741176, 0.133333], 'SønnavindA': [0.090196, 0.745098, 0.811765], 'EastAnglia': [0.227451, 0.003922, 0.513725], 'HollandseeKust': [0.0, 0.262745, 0.003922], 'SørvestA': [0.058824, 1.0, 0.662745], 'VestavindB': [0.368627, 0.0, 0.25098], 'OuterDowsing': [0.737255, 0.737255, 1.0], 'Borssele': [0.847059, 0.686275, 0.635294], 'VestavindC': [0.721569, 0.0, 0.501961], 'NordvestB': [0.0, 0.305882, 0.32549], 'SørvestE': [0.419608, 0.396078, 0.0], 'NordavindC': [0.490196, 0.007843, 0.0], 'SørvestF': [0.380392, 0.14902, 1.0], 'NordvestC': [1.0, 1.0, 0.603922], 'NordavindB': [0.341176, 0.286275, 0.392157], 'SørvestC': [0.54902, 0.721569, 0.580392], 'VestavindE': [0.580392, 0.988235, 1.0], 'SørvestD': [0.007843, 0.509804, 0.407843], 'SørvestB': [0.568627, 1.0, 0.0], 'VestavindF': [0.513725, 0.0, 0.627451], 'NordavindD': [0.678431, 0.537255, 0.266667], 'VestavindD': [0.356863, 0.203922, 0.0], 'NordavindA': [1.0, 0.752941, 0.952941]}
HUB_TO_COLOR = {'EnergyhubEU': '#4363d8', 'EnergyhubNorth': '#e6194B', 'EnergyhubCentral': '#3cb44b'}

# Technology types
HYDROGEN_TYPES = ["HydrogenCCGT", "HydrogenOCGT"]
OW_TYPES = ["Windoffshoregrounded", "Windoffshorefloating"]
