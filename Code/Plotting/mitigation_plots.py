#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 18:00:38 2024

@author: Mónica Sagastuy-Breña

Plotting script for DPhil case study results as mitigation curve
"""

import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle

def mitigation_curve(total_data_filename, plot_filename, case_study_name, countries):
    '''
    Parameters
    ----------
    total_data_filename : path
        Path to the file with total data to be plotted.
    plot_filename : path
        Path and figure filename to save the final figure.
    case_study_name : string
        case study folder name to generate plots for
    countries: list
        list of countries in the case study, two-letter ISO abbreviation in all caps

    Returns
    -------
    png image
        Saves a png of matplotlib plot only for the costs mitigation curve, 
        (annualised costs vs collaboration emissions)

    '''
    
    total_data = pd.read_csv(total_data_filename)
    total_data = total_data.sort_values(by=['technology_name'])
    
    df = pd.DataFrame()
    row = pd.DataFrame()
    
    while not total_data.empty:
        counter = 0
        checker = total_data["technology_name"].iloc[0]
        name = total_data["technology_name"].iloc[counter]
        # Conditional to drop rows matching certain names
        if any(name == f'EL_Demand_[{country}]' or name == f'HTH_Demand_[{country}]' for country in countries):
            total_data = total_data[total_data["technology_name"] != name]
            # Restart the loop after modifying the DataFrame
            continue
        
        rows = pd.DataFrame()
        num_rows = len(total_data)
        while name == checker and counter < num_rows:
           row = total_data.iloc[counter:counter+1]
           rows = pd.concat([rows, row], ignore_index=True)
           counter += 1
           
           if counter < num_rows:
               name = total_data["technology_name"].iloc[counter]
           else:
               name = ""
       
        if not rows.empty:
            rows = rows.sort_values(by=["collaboration_emissions"])
            rows = rows.set_index("collaboration_emissions")
            col_name = rows["technology_name"].iloc[0]
            df[col_name] = rows["technology_cost"]
            df.index = rows.index
       
        total_data.drop(index=total_data.index[:counter], axis=0, inplace=True)
        
    
    # df.to_csv({case_study}_collab_plot_data.csv")
    
    
    ##### Save figure in case study folder
    fig, ax = plt.subplots()
    df.plot.area(ax=ax)
    ax.set_title(f"{case_study_name}")
    ax.set_xlabel("Collaboration Emissions (MtCO2e)")
    ax.set_ylabel("Costs (Billion USD)")
    ax.set_xlim(left=0)
    ax.legend(bbox_to_anchor=(0.5, -1.35), loc='lower center', borderaxespad=0, ncol=4)
    fig.savefig(plot_filename, dpi=300, bbox_inches="tight")
    return
    

def dpacc_subplots(total_data_filename, capacities_data_filename, plot_filename,
                case_study_name, countries):
    '''
    Parameters
    ----------
    total_data_filename : path
        Path to the file with total data to be plotted.
    capacities_data_filename: path
        Path to the file with capacities data to be plotted.
    plot_filename : path
        Path and figure filename to save the final figure.
    case_study_name: string
        folder name that contains data to be plotted
    countries: list
        list of countries in the case study, two-letter ISO abbreviation in all caps

    Returns
    -------
    png image
        Saves a png of matplotlib plot wiht subplots, one for system costs vs emissions by asset
        annualised investment, and the other for emissions vs Asset capacity,
        given extracted GMPA results in total_data_unrounded and capacities_total_data file formats.

    '''
    df = pd.DataFrame()
    row = pd.DataFrame()
    
    total_data = pd.read_csv(total_data_filename)
    total_data = total_data.sort_values(by=['technology_name'])
    
    while not total_data.empty:
        counter = 0
        checker = total_data["technology_name"].iloc[0]
        name = total_data["technology_name"].iloc[counter]
        # Conditional to drop rows matching certain names
        if any(name == f'EL_Demand_[{country}]' or name == f'HTH_Demand_[{country}]' for country in countries):
            total_data = total_data[total_data["technology_name"] != name]
            # Restart the loop after modifying the DataFrame
            continue
        rows = pd.DataFrame()
        num_rows = len(total_data)
        
        while name == checker and counter < num_rows:
           row = total_data.iloc[counter:counter+1]
           rows = pd.concat([rows, row], ignore_index=True)
           counter += 1
           
           if counter < num_rows:
               name = total_data["technology_name"].iloc[counter]
           else:
               name = ""
       
        if not rows.empty:
            rows = rows.sort_values(by=["collaboration_emissions_MtCO2e/y"])
            rows = rows.set_index("collaboration_emissions_MtCO2e/y")
            col_name = rows["technology_name"].iloc[0]
            df[col_name] = rows["technology_cost_G$/y"]
            df.index = rows.index
       
        total_data.drop(index=total_data.index[:counter], axis=0, inplace=True)
    
    
    cap_df = pd.DataFrame()
    cap_data = pd.read_csv(capacities_data_filename)
    cap_data = cap_data.sort_values(by=['technology_name'])
    
    while not cap_data.empty:
        counter = 0
        checker = cap_data["technology_name"].iloc[0]
        name = cap_data["technology_name"].iloc[counter]
        
        # Conditional to drop rows matching certain names
        if any(name == f'EL_Demand_[{country}]' or name == f'HTH_Demand_[{country}]' for country in countries):
            cap_data = cap_data[cap_data["technology_name"] != name]
            # Restart the loop after modifying the DataFrame
            continue
        
        cap_rows = pd.DataFrame()
        num_rows = len(cap_data)
        
        while name == checker and counter < num_rows:
            cap_row = cap_data.iloc[counter:counter+1]
            cap_rows = pd.concat([cap_rows, cap_row], ignore_index=True)
            counter += 1
            
            if counter < num_rows:
                name = cap_data["technology_name"].iloc[counter]
            else:
                name = ""
        
        if not cap_rows.empty:
            cap_rows = cap_rows.sort_values(by=["collaboration_emissions_MtCO2e/y"])
            cap_rows = cap_rows.set_index("collaboration_emissions_MtCO2e/y")
            col_name = cap_rows["technology_name"].iloc[0]
            cap_df[col_name] = cap_rows["technology_size"]
            cap_df.index = cap_rows.index
        
        cap_data.drop(index=cap_data.index[:counter], axis=0, inplace=True)
    # df.to_csv({case_study}_collab_plot_data.csv")
    
    
   # Plotting side-by-side subplots
    color_cycle = cycle(plt.cm.tab20.colors)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot total_data on the first subplot
    df.plot.area(ax=axes[0], color=[next(color_cycle) for _ in df.columns])
    axes[0].set_title(f"{case_study_name} - D-PACC for Costs")
    axes[0].set_xlabel("Collaboration Emissions (MtCO2e)")
    axes[0].set_ylabel("Costs (Billion USD)")
    axes[0].set_xlim(left=0)
    axes[0].legend().set_visible(False)
    # Reset color cycle
    color_cycle = cycle(plt.cm.tab20.colors)
    
    # Plot cap_data on the second subplot
    cap_df.plot.area(ax=axes[1], color=[next(color_cycle) for _ in cap_df.columns])
    axes[1].set_title(f"{case_study_name} - D-PACC for Installed Capacity")
    axes[1].set_xlabel("Collaboration Emissions (MtCO2e)")
    axes[1].set_ylabel("Capacity (GWp)")
    axes[1].set_xlim(left=0)
    axes[1].legend().set_visible(False)
    
    # Create a shared legend with labels from axes[0] only
    handles, labels = axes[0].get_legend_handles_labels()
    # Autarky 1 country legend location for plot
    # fig.legend(handles, labels, bbox_to_anchor=(0.5, -0.1), loc='lower center', borderaxespad=0, ncol=6)
    # Collabs 2-country legend location
    fig.legend(handles, labels, bbox_to_anchor=(0.5, -0.17), loc='lower center', borderaxespad=0, ncol=6)
    # Collabs 3-country legend location
    # fig.legend(handles, labels, bbox_to_anchor=(0.5, -0.25), loc='lower center', borderaxespad=0, ncol=6)
    
    # Save the figure
    fig.tight_layout()
    fig.savefig(plot_filename, dpi=300, bbox_inches="tight")
    return

