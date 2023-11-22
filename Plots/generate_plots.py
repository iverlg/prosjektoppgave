### Pipeline for generating plots for given case(s)
### Plots generated: EnergyMix, HubCapacity, Transmission (Europe/NS) and OWCapacity (NO/NS)

### Legends can be generated in 'legends.ipynb'
### Sensitivities on OW capacity in 'ow_sensitivity.ipynb'
### Rotational mass study in 'rotational_mass.ipynb'

import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
from constants import (ENERGY_HUBS, HUB_TO_COLOR, HYDROGEN_TYPES, NO_NODES,
                       TECH_TO_COLOR, WIND_FARM_NODES,
                       WIND_FARM_NODES_TO_COLOR)
from cycler import cycler
from matplotlib.lines import Line2D

### DEFINE CASES HERE ###
CASES = ["Base", "NOgrid", "NoHubs", "NoHubsNOgrid", "OnlyCentral", "OnlyEU", "OnlyNorth"]

# Import lat/lon of all nodes to be used for transmission grid plots
LATLON = pd.read_csv("EMPIRE_extension/Output/nodes.csv").drop(columns=["geometry"])
LATLON["Node"] = LATLON["Node"].apply(lambda s: s.replace(" ", ""))

ENERGY_HUBS = [hub.replace(" ", "") for hub in ENERGY_HUBS]

# Plot of total generation / energy mix
def plot_gen_by_source(case, _df):
    print(f"Generation by source for case: {case}")
    
    df_gen_source = _df.copy()
    df_gen_source = df_gen_source[~df_gen_source["GeneratorType"].isin(HYDROGEN_TYPES)]

    NS_OW_prod_2050 = df_gen_source[(df_gen_source["Node"].isin(WIND_FARM_NODES)) & (df_gen_source["Period"] == "2045-2050")]\
                    ["genInstalledCap_MW"].sum() / 1000 # in GW

    df_gen_source["genInstalledCap_MW"] = df_gen_source.groupby(['GeneratorType', 'Period'])['genInstalledCap_MW'].transform('sum')
    df_gen_source = df_gen_source.drop_duplicates(("GeneratorType", "Period"), ignore_index=True)[["GeneratorType", "Period", "genInstalledCap_MW"]]

    periods = list(df_gen_source["Period"].unique())

    gen_source_sorted_by_cap = list(df_gen_source[df_gen_source["Period"] == "2055-2060"]\
                              .sort_values(by="genInstalledCap_MW", ascending=False)["GeneratorType"].values)
        
    gen_source_displayed = gen_source_sorted_by_cap

    installed_caps_gen = []
    for gen_source in gen_source_displayed:
        cap_by_period = []
        for period in periods:
            cap_by_period.append(df_gen_source[(df_gen_source["GeneratorType"] == gen_source) & (df_gen_source["Period"] == period)]["genInstalledCap_MW"].values[0])

        # Remove gen_source that have no capacity (1 MW since some threshold)
        if all(c < 1 for c in cap_by_period):
            gen_source_displayed.remove(gen_source)
        else:
            installed_caps_gen.append(cap_by_period)

    installed_caps_gen_TW = [[cap/1000000 for cap in sublist] for sublist in installed_caps_gen]
    period_displayed_gen = [period.split("-")[1] for period in periods]

    plt.rcParams.update({'font.size': 14})
    default_cycler = cycler(color=[TECH_TO_COLOR[tech] for tech in gen_source_displayed])
    plt.figure(figsize=(10,6))
    plt.rc('axes', axisbelow=True, prop_cycle=default_cycler)
    plt.grid(linewidth=0.3)
    plt.stackplot(period_displayed_gen, installed_caps_gen_TW, labels=gen_source_displayed, edgecolor='white', lw=0.7)
    plt.ylabel('Generator capacity [TW]')
    #plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=5, fontsize=10)
    plt.margins(x=0)

    y_max = 6
    plt.ylim(0, y_max)
    
    # Plot capacity 2050 
    prod_2050 = sum([gen_cap[5] for gen_cap in installed_caps_gen_TW]) # Total gen in TW

    plt.axvline(x = 5, color = 'black', ls="--")
    plt.text(x=1.9, y=y_max*0.95, s=f"Total capacity in 2050: {round(prod_2050, 1)} TW", verticalalignment='top', fontsize=14)
    plt.text(x=1.9, y=y_max*0.88, s=f"OW capacity in NS 2050: {round(NS_OW_prod_2050)} GW", verticalalignment='top', fontsize=14)
    plt.savefig(f"Plots/SavedFigs/EnergyMix/{case}", bbox_inches='tight')

# Plot of wind farm capacity in North Sea
def plot_wind_prod(case, _df):
    print(f"Wind production (floating + grounded) by area for case: {case}")

    df_wind_farm_nodes = _df[_df['Node'].isin(WIND_FARM_NODES)]

    # Sum floating + grounded cap
    df_wind_farm_nodes["genInstalledCap_MW"] = df_wind_farm_nodes.groupby(['Node', 'Period'])['genInstalledCap_MW'].transform('sum')
    df_wind_farm_nodes = df_wind_farm_nodes.drop_duplicates(("Node", "Period"), ignore_index=True)[["Node", "Period", "genInstalledCap_MW"]]
    
    df_NO_nodes = df_wind_farm_nodes[df_wind_farm_nodes["Node"].isin(NO_NODES)]
    prod_NO_2050 = df_NO_nodes[df_NO_nodes["Period"] == "2045-2050"]["genInstalledCap_MW"].sum()

    print(f"NO prod in 2050: {round(prod_NO_2050/1000, 1)} GW")

    periods = list(df_wind_farm_nodes["Period"].unique())
    nodes_sorted_by_cap = list(df_wind_farm_nodes[df_wind_farm_nodes["Period"] == "2055-2060"].sort_values(by="genInstalledCap_MW", ascending=False)["Node"].values)
    
    nodes_displayed = nodes_sorted_by_cap

    installed_caps = []
    for node in nodes_displayed:
        cap_by_period = []
        for period in periods:
            cap_by_period.append(df_wind_farm_nodes[(df_wind_farm_nodes["Node"] == node) & (df_wind_farm_nodes["Period"] == period)]["genInstalledCap_MW"].values[0])

        # Remove nodes that have no capacity (1 MW since some threshold)
        if all(c < 1 for c in cap_by_period):
            nodes_displayed.remove(node)
        else:
            installed_caps.append(cap_by_period)

    installed_caps_GW = [[cap/1000 for cap in sublist] for sublist in installed_caps]
    period_displayed = [period.split("-")[1] for period in periods]

    plt.rcParams.update({'font.size': 14})
    plt.figure(figsize=(10,6))
    default_cycler = cycler(color=[WIND_FARM_NODES_TO_COLOR[node] for node in nodes_displayed])
    plt.rc('axes', axisbelow=True, prop_cycle=default_cycler)
    plt.grid(lw=0.3)
    plt.stackplot(period_displayed, installed_caps_GW, labels=nodes_displayed, edgecolor="white", lw=0.7)
    plt.ylabel('Wind power capacity [GW]')
    #plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.4), ncol=5, fontsize=10)
    plt.margins(x=0)

    y_max = 300
    plt.ylim(0, y_max)

    # Plot capacity 2050 
    prod_2050 = sum([cap[5] for cap in installed_caps_GW]) # Total cap in GW

    plt.axvline(x = 5, color = 'black', ls="--")
    plt.text(x=2.4, y=y_max*0.9, s=f"Capacity in 2050: {round(prod_2050, 1)} GW", verticalalignment='top', fontsize=14)
    plt.savefig(f"Plots/SavedFigs/OWCapacity-NS/{case}", bbox_inches='tight')

# Plot wind farm capacity by NO wind farms
def plot_wind_prod_NO(case, _df):
    print(f"Wind production (floating + grounded) for NO areas for case: {case}")
    df_wind_farm_nodes = _df[_df['Node'].isin(NO_NODES)]

    # Sum floating + grounded cap
    df_wind_farm_nodes["genInstalledCap_MW"] = df_wind_farm_nodes.groupby(['Node', 'Period'])['genInstalledCap_MW'].transform('sum')
    df_wind_farm_nodes = df_wind_farm_nodes.drop_duplicates(("Node", "Period"), ignore_index=True)[["Node", "Period", "genInstalledCap_MW"]]
    
    prod_NO_2050 = df_wind_farm_nodes[df_wind_farm_nodes["Period"] == "2045-2050"]["genInstalledCap_MW"].sum()

    print(f"NO prod in 2050: {round(prod_NO_2050/1000, 1)} GW")

    periods = list(df_wind_farm_nodes["Period"].unique())
    nodes_sorted_by_cap = list(df_wind_farm_nodes[df_wind_farm_nodes["Period"] == "2055-2060"].sort_values(by="genInstalledCap_MW", ascending=False)["Node"].values)
    
    nodes_displayed = nodes_sorted_by_cap

    installed_caps = []
    for node in nodes_displayed:
        cap_by_period = []
        for period in periods:
            cap_by_period.append(df_wind_farm_nodes[(df_wind_farm_nodes["Node"] == node) & (df_wind_farm_nodes["Period"] == period)]["genInstalledCap_MW"].values[0])

        # Remove nodes that have no capacity (1 MW since some threshold)
        if all(c < 1 for c in cap_by_period):
            nodes_displayed.remove(node)
        else:
            installed_caps.append(cap_by_period)

    installed_caps_GW = [[cap/1000 for cap in sublist] for sublist in installed_caps]
    period_displayed = [period.split("-")[1] for period in periods]

    plt.rcParams.update({'font.size': 14})
    default_cycler = cycler(color=[WIND_FARM_NODES_TO_COLOR[node] for node in nodes_displayed])
    plt.figure(figsize=(10,6))
    plt.rc('axes', axisbelow=True, prop_cycle=default_cycler)
    plt.grid(lw=0.3)
    plt.stackplot(period_displayed, installed_caps_GW, labels=nodes_displayed, edgecolor="white", lw=0.7)
    plt.ylabel('Wind power capacity [GW]')
    #plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=5, fontsize=10)
    plt.margins(x=0)

    y_max = 120
    plt.ylim(0, y_max)

    # Plot capacity 2050 
    cap_2050 = sum([cap[5] for cap in installed_caps_GW]) # Total cap in GW
    
    plt.axvline(x = 5, color = 'black', ls="--")
    plt.text(x=2.5, y=y_max*0.9, s=f"Capacity in 2050: {round(cap_2050, 1)} GW", verticalalignment='top', fontsize=14)
    plt.savefig(f"Plots/SavedFigs/OWCapacity-NO/{case}", bbox_inches='tight')

# Plot offshore converter (hub) capacity 
def plot_offshore_converter_cap(case, _df):
    print(f"Offshore converter capacity for case: {case}")

    df = _df[["Node", "Period", "Converter total capacity [MW]"]]

    prod_converter_2050 = df[df["Period"] == "2045-2050"]["Converter total capacity [MW]"].sum()
    print(f"Offshore converter total capacity 2050 for case {case}: {round(prod_converter_2050/1000, 2)} GW\n")

    # Skip plots that have no capacity (1 MW since some threshold)
    if prod_converter_2050 < 1: 
        return

    periods = list(df["Period"].unique())
    nodes_sorted_by_cap = list(df[df["Period"] == "2055-2060"]\
                              .sort_values(by="Converter total capacity [MW]", ascending=False)["Node"].values)

    nodes_displayed = nodes_sorted_by_cap
    
    installed_caps = []
    for node in nodes_displayed:
        cap_by_period = []
        for period in periods:
            cap_by_period.append(df[(df["Node"] == node) & (df["Period"] == period)]["Converter total capacity [MW]"].values[0])

        # Remove nodes that have no capacity (1 MW since some threshold)
        if all(c < 1 for c in cap_by_period):
            nodes_displayed.remove(node)
            continue
        else:
            installed_caps.append(cap_by_period)
    
    installed_caps_GW = [[cap/1000 for cap in sublist] for sublist in installed_caps]
    period_displayed = [period.split("-")[1] for period in periods]

    plt.rcParams.update({'font.size': 14})
    default_cycler = cycler(color=[HUB_TO_COLOR[node] for node in nodes_displayed])
    plt.figure(figsize=(10,6))
    plt.rc('axes', axisbelow=True, prop_cycle=default_cycler)
    plt.grid(lw=0.3)
    plt.stackplot(period_displayed, installed_caps_GW, labels=nodes_displayed, edgecolor="white", lw=0.7)
    plt.ylabel('Offshore converter capacity [GW]')
    #plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=5, fontsize=10)
    plt.margins(x=0)

    y_max = 220
    plt.ylim(0, y_max)
    
    # Plot capacity 2050 
    cap_2050 = sum([cap[5] for cap in installed_caps_GW]) # Total trans cap in GW

    plt.axvline(x = 5, color = 'black', ls="--")
    plt.text(x=2.5, y=y_max*0.95, s=f"Capacity in 2050: {round(cap_2050, 1)} GW", verticalalignment='top', fontsize=14)
    plt.savefig(f"Plots/SavedFigs/HubCapacity/{case}", bbox_inches='tight')

# Plot transmission lines Europe
def plot_transmission_lines_Europe(case, _df):
    print(f'Transmission capacity Europe for case: {case}')
    # Set 2050 
    df = _df[_df["Period"] == "2045-2050"]

    # Remove 0-connections
    df = df[df["transmissionInstalledCap_MW"] > 1].reset_index(drop=True)
    
    custom_lines = [Line2D([0], [0], color='black', linewidth=1/3),
                Line2D([0], [0], color='black', linewidth=5/3),
                Line2D([0], [0], color='black', linewidth=10/3),
                Line2D([0], [0], color='black', linewidth=20/3),
                Line2D([0], [0], color='black', linewidth=30/3)]
    fig = plt.figure(figsize=(20,20))
    ax = plt.axes(projection=ccrs.Orthographic())
    ax.add_feature(cartopy.feature.BORDERS.with_scale('50m'), alpha=.5)
    ax.add_feature(cartopy.feature.LAND.with_scale('50m'), facecolor="white")
    ax.add_feature(cartopy.feature.OCEAN.with_scale('50m'))

    # Keep track of used nodes 
    used_nodes = set([])

    # Plot connections
    for _, df_row in df.iterrows():
        used_nodes.add(df_row["BetweenNode"])
        used_nodes.add(df_row["AndNode"])

        plt.plot([LATLON[LATLON["Node"] == df_row["BetweenNode"]]["Longitude"].values[0], LATLON[LATLON["Node"] == df_row["AndNode"]]["Longitude"].values[0]],\
                [LATLON[LATLON["Node"] == df_row["BetweenNode"]]["Latitude"].values[0], LATLON[LATLON["Node"] == df_row["AndNode"]]["Latitude"].values[0]],
                    color = 'black',
                    linewidth = df_row["transmissionInstalledCap_MW"]/3000,
                    transform=ccrs.Geodetic())
        
    # Plot nodes (only those in use/with transmission capacity)
    for _, latlon_row in LATLON.iterrows():
        if latlon_row["Node"] not in used_nodes:
            continue
        plt.plot(latlon_row["Longitude"], latlon_row["Latitude"],
            marker = 's' if latlon_row["Node"] in ENERGY_HUBS else 'o',
            color = 'blue' if latlon_row["Node"] in ENERGY_HUBS else 'black',
            markersize=10,
            transform=ccrs.Geodetic()
        )

    ax.set_extent([-7, 17, 43, 72], crs=ccrs.PlateCarree())
    ax.legend(custom_lines, ['  1 GW', '  5 GW', '  10 GW','  20 GW','  30 GW'], borderpad=1, labelspacing=1, handlelength=7, loc="upper left", fontsize=20)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlines = False
    gl.ylines = False
    gl.xlocator = mticker.FixedLocator([-5, 0, 5, 10, 15, 20])
    gl.ylocator = mticker.FixedLocator([45, 50, 55, 60, 65, 70, 75])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 20}
    gl.ylabel_style = {'size': 20}
    plt.savefig(f"Plots/SavedFigs/Transmission-Europe/{case}", bbox_inches='tight')

# Plot transmission capacity in North Sea
def plot_transmission_lines_NS(case, _df):
    print(f'Transmission capacity North Sea in 2050 for case: {case}')
    # Set 2050 
    df = _df[_df["Period"] == "2045-2050"]

    # Remove 0-connections
    df = df[df["transmissionInstalledCap_MW"] > 1].reset_index(drop=True)
    
    custom_lines = [Line2D([0], [0], color='black', linewidth=1/3),
                Line2D([0], [0], color='black', linewidth=5/3),
                Line2D([0], [0], color='black', linewidth=10/3),
                Line2D([0], [0], color='black', linewidth=20/3),
                Line2D([0], [0], color='black', linewidth=30/3)]
    fig = plt.figure(figsize=(20,20))
    ax = plt.axes(projection=ccrs.Orthographic())
    ax.add_feature(cartopy.feature.BORDERS.with_scale('50m'), alpha=.5)
    ax.add_feature(cartopy.feature.LAND.with_scale('50m'), facecolor="white")
    ax.add_feature(cartopy.feature.OCEAN.with_scale('50m'))

    # Keep track of used nodes 
    used_nodes = set([])

    # Plot connections
    for _, df_row in df.iterrows():
        used_nodes.add(df_row["BetweenNode"])
        used_nodes.add(df_row["AndNode"])

        plt.plot([LATLON[LATLON["Node"] == df_row["BetweenNode"]]["Longitude"].values[0], LATLON[LATLON["Node"] == df_row["AndNode"]]["Longitude"].values[0]],\
                [LATLON[LATLON["Node"] == df_row["BetweenNode"]]["Latitude"].values[0], LATLON[LATLON["Node"] == df_row["AndNode"]]["Latitude"].values[0]],
                    color = 'black',
                    linewidth = df_row["transmissionInstalledCap_MW"]/3000,
                    transform=ccrs.Geodetic())
        
    # Plot nodes (only those in use/with transmission capacity)
    for _, latlon_row in LATLON.iterrows():
        if latlon_row["Node"] not in used_nodes:
            continue
        plt.plot(latlon_row["Longitude"], latlon_row["Latitude"],
            marker = 's' if latlon_row["Node"] in ENERGY_HUBS else 'o',
            color = 'blue' if latlon_row["Node"] in ENERGY_HUBS else 'black',
            markersize=10,
            transform=ccrs.Geodetic()
        )
        
    ax.set_extent([-5, 17, 50, 73], crs=ccrs.PlateCarree())
    ax.legend(custom_lines, ['  1 GW', '  5 GW', '  10 GW','  20 GW','  30 GW'], borderpad=1, labelspacing=1, handlelength=7, loc="upper left", fontsize=20)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlines = False
    gl.ylines = False
    gl.xlocator = mticker.FixedLocator([-5, 0, 5, 10, 15, 20])
    gl.ylocator = mticker.FixedLocator([45, 50, 55, 60, 65, 70, 75])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 20}
    gl.ylabel_style = {'size': 20}
    plt.savefig(f"Plots/SavedFigs/Transmission-NS/{case}", bbox_inches='tight')

PLOT_TO_FILE = {
    plot_gen_by_source: 'results_output_gen.csv',
    plot_wind_prod: 'results_output_gen.csv',
    plot_wind_prod_NO: 'results_output_gen.csv',
    plot_offshore_converter_cap: 'results_output_offshoreConverter.csv',
    plot_transmission_lines_Europe: 'results_output_transmission.csv',
    plot_transmission_lines_NS: 'results_output_transmission.csv'
}

def main():
    for func, file in PLOT_TO_FILE.items():
        DF_BY_CASES = dict({})
        for case in CASES:
            _df = pd.read_csv(f'Plots/Results/{case}/{file}')
            DF_BY_CASES[case] = _df
        for case, _df in DF_BY_CASES.items():
            func(case, _df)

if __name__ == "__main__":
    main()