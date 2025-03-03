# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 18:43:22 2024

@author: Mónica Sagastuy-Breña
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
from Code.Results import get_new_input_params

def logistic_curve(t, K, r, t0):
    '''
    

    Parameters
    ----------
    t : TYPE
        DESCRIPTION.
    K : TYPE
        DESCRIPTION.
    r : TYPE
        DESCRIPTION.
    t0 : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    return K / (1 + np.exp(-r * (t - t0)))

def logistic_curve_derivative(t, K, r, t0):
    '''
    

    Parameters
    ----------
    t : TYPE
        DESCRIPTION.
    K : TYPE
        DESCRIPTION.
    r : TYPE
        DESCRIPTION.
    t0 : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    return (r * K * np.exp(-r * (t - t0))) / ((1 + np.exp(-r * (t - t0)))**2)

def linear_approximation(t, m, b):
    '''
    

    Parameters
    ----------
    t : TYPE
        DESCRIPTION.
    m : TYPE
        DESCRIPTION.
    b : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    return m * t + b

def fit_s_curves(case_study_folder, tech_lim, assets_folder,
                  goal_capacity, goal_year, historical_data_file):
    '''
    

    Parameters
    ----------
    case_study_folder : TYPE
        DESCRIPTION.
    tech_lim : TYPE
        DESCRIPTION.
    assets_folder : TYPE
        DESCRIPTION.
    goal_capacity : TYPE
        DESCRIPTION.
    goal_year : TYPE
        DESCRIPTION.
    historical_data_file : TYPE
        DESCRIPTION.

    Returns
    -------
    K_fit : TYPE
        DESCRIPTION.
    r_fit : TYPE
        DESCRIPTION.
    t0_fit : TYPE
        DESCRIPTION.
    years : TYPE
        DESCRIPTION.
    capacities : TYPE
        DESCRIPTION.

    '''
    data = pd.read_csv(historical_data_file)
    goal_capacity = get_new_input_params.get_30y_opt_capacities(case_study_folder,
                                                                tech_lim,
                                                                assets_folder)
    years = data['year'].values
    # Identify limited technology for either wind or solar
    if tech_lim[0:5] == 'RE_PV':
        capacities = data['pv_installed_capacity_GW'].values
    elif tech_lim[0:5] == 'RE_WI':
        capacities = data['wind_installed_capacity_GW'].values
        
    # Append the goal data point to the historical data
    years_with_goal = np.append(years, goal_year)
    capacities_with_goal = np.append(capacities, goal_capacity)

    # Initial guesses and bounds to delay inflection
    initial_guess = [goal_capacity, 0.2, 2030]  # K, r, t0
    bounds = ([max(capacities), 0.01, 2030], [goal_capacity * 1.5, 1, 2055])

    # Fit the logistic curve with bounds using the augmented data
    params, _ = curve_fit(
        logistic_curve,
        years_with_goal,
        capacities_with_goal,
        p0=initial_guess,
        bounds=bounds
    )
    K_fit, r_fit, t0_fit = params

    return K_fit, r_fit, t0_fit, years, capacities

def approximate_scurve_derivative(case_study_folder, tech_lim, assets_folder,
                                  goal_capacity, goal_year, historical_data_file):
    '''
    

    Parameters
    ----------
    case_study_folder : TYPE
        DESCRIPTION.
    tech_lim : TYPE
        DESCRIPTION.
    assets_folder : TYPE
        DESCRIPTION.
    goal_capacity : TYPE
        DESCRIPTION.
    goal_year : TYPE
        DESCRIPTION.
    historical_data_file : TYPE
        DESCRIPTION.

    Returns
    -------
    derivative_years : TYPE
        DESCRIPTION.
    derivative_values : TYPE
        DESCRIPTION.

    '''
    K_fit, r_fit, t0_fit, years, capacities = fit_s_curves(case_study_folder, tech_lim, assets_folder,
                                        goal_capacity, goal_year, historical_data_file)
    # Calculate slope (m) at inflection point
    m = logistic_curve_derivative(t0_fit, K_fit, r_fit, t0_fit)
    b = logistic_curve(t0_fit, K_fit, r_fit, t0_fit) - m * t0_fit
    # Generate linear section (±5 years around t0)
    derivative_years = np.arange(int(t0_fit) - 5, int(t0_fit) + 6)
    derivative_values = linear_approximation(derivative_years, m, b)
    return derivative_years, derivative_values
    
    
def plot_scurves(case_study_folder, tech_lim, assets_folder,
                 goal_capacity, goal_year, historical_data_file):
    '''
    

    Parameters
    ----------
    case_study_folder : TYPE
        DESCRIPTION.
    tech_lim : TYPE
        DESCRIPTION.
    assets_folder : TYPE
        DESCRIPTION.
    goal_capacity : TYPE
        DESCRIPTION.
    goal_year : TYPE
        DESCRIPTION.
    historical_data_file : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    K_fit, r_fit, t0_fit, years, capacities = fit_s_curves(case_study_folder, tech_lim, assets_folder,
                                        goal_capacity, goal_year, historical_data_file)
    r_max = (r_fit * K_fit) / 4
    extended_years = np.arange(years[0], 2056)
    scurve_data = logistic_curve(extended_years, K_fit, r_fit, t0_fit)
    
    derivative_years, derivative_values = approximate_scurve_derivative(case_study_folder, tech_lim, assets_folder,
                                      goal_capacity, goal_year, historical_data_file)
    
    plt.figure(figsize=(12, 8))

    plt.plot(extended_years, scurve_data, color='blue', linestyle='--', label='Projected Logistic Curve')
    plt.scatter(years, capacities, color='red', marker='x', s=70, label='Actual Data')

    # Plot the linear section near the inflection point
    plt.plot(derivative_years, derivative_values, color='green', linestyle='-', label='Linear Approximation of derivative at $t_0$', linewidth=2)

    # Highlight the inflection point
    plt.scatter([t0_fit], [logistic_curve(t0_fit, K_fit, r_fit, t0_fit)], color='black', label='Inflection Point', zorder=5)
    plt.annotate(f"\nt = {t0_fit:.2f},\n$r_{{max}}$ = {r_max:.2f} GW / year", 
                 (t0_fit, logistic_curve(t0_fit, K_fit, r_fit, t0_fit)), 
                 textcoords="offset points", 
                 xytext=(-12, -60),
                 fontsize=12,
                 ha='left', color='black')

    plt.xlabel('Year', fontsize=14)
    plt.xticks(fontsize=12)
    plt.ylabel('Cumulative Installed Wind Capacity (GWp)', fontsize=14)
    plt.yticks(fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.show()
    return

def plot_asset_sizes_stacked(my_network, location_parameters_df, save_path=None):
    '''
    Manually hard-coded for specific assets in system for my thesis, needs to be
    generalised if more assets need to be plotted

    Parameters
    ----------
    my_network : STEVFNs network
        Full network after running a STEVFNs modelling iteration
    location_parameters_df : DataFrame
        Contains coordinates and labels to find the location name and plot
    save_path : PATH, optional
        Path to save the plot to if it needs to be saved. The default is None.

    Returns
    -------
    None.

    '''
    og_df = my_network.system_structure_df.copy()
    asset_sizes_array = np.array([my_network.assets[counter].asset_size() for counter in range(len(og_df))])
    og_df["Asset_Size"] = asset_sizes_array
    max_asset_size = np.max(asset_sizes_array)
    min_asset_size = max_asset_size * 1E-3

    og_df = og_df[og_df["Asset_Size"] >= min_asset_size]
    og_df = og_df[og_df['Asset_Class'] != 'CO2_Budget']
    asset_class_list = np.sort(og_df["Asset_Class"].unique())

    loc_1 = og_df["Location_1"].unique()
    loc_name = location_parameters_df.loc[loc_1[0]]['location_name']

    bars = []  # Collect all bars for the legend
    pv_colors = ['#f35b04', '#f18701']
    wind_colors = ['#126782', '#58B4D1']
    pp_colors = ['#8d99ae']
    bess_colors = ['#226f54', '#87c38f']
    hvdc_color = ['#5e548e']
    
    # PV Capacity
    if "RE_PV_Existing" in asset_class_list:
        existing_pv = float(og_df.query("Asset_Class == 'RE_PV_Existing'")['Asset_Size'].iloc[0])
        bars.append(plt.bar("Total PV", existing_pv, color=pv_colors[0], label="PV Existing", zorder=3))

        if "RE_PV_Openfield_Lim" in asset_class_list:
            new_pv = float(og_df.query("Asset_Class == 'RE_PV_Openfield_Lim'")['Asset_Size'].iloc[0])
            bars.append(plt.bar("Total PV", new_pv, bottom=existing_pv, color=pv_colors[1], label="PV New", zorder=3))

    # Wind Capacity
    if "RE_WIND_Existing" in asset_class_list:
        existing_wind = float(og_df.query("Asset_Class == 'RE_WIND_Existing'")['Asset_Size'].iloc[0])
        bars.append(plt.bar("Total Wind", existing_wind, color=wind_colors[0], label="Wind Existing", zorder=3))

        if "RE_WIND_Onshore_Lim" in asset_class_list:
            new_wind = float(og_df.query("Asset_Class == 'RE_WIND_Onshore_Lim'")['Asset_Size'].iloc[0])
            bars.append(plt.bar("Total Wind", new_wind, bottom=existing_wind, color=wind_colors[1], label="Wind New", zorder=3))

    # Fossil Generation
    if "PP_CO2_Existing" in asset_class_list:
        existing_fossil = float(og_df.query("Asset_Class == 'PP_CO2_Existing'")['Asset_Size'].iloc[0])
        bars.append(plt.bar("Fossil Gen.", existing_fossil, color=pp_colors[0], label="Fossil Existing", zorder=3))
        
    # BESS assets
    if "BESS_Existing" in asset_class_list:
        existing_bess = float(og_df.query("Asset_Class == 'BESS_Existing'")['Asset_Size'].iloc[0])
        bars.append(plt.bar("Total BESS", existing_bess, color=bess_colors[0], label="BESS Existing", zorder=3))
    else:
        existing_bess=0
        
    if "BESS" in asset_class_list:
        new_bess = float(og_df.query("Asset_Class == 'BESS'")['Asset_Size'].iloc[0])
        bars.append(plt.bar("Total BESS", new_bess, bottom=existing_bess, color=bess_colors[1], label="BESS New", zorder=3))
    
    if "EL_Transport" in asset_class_list:
        hvdc_cable = float(og_df.query("Asset_Class == 'EL_Transport'")['Asset_Size'].iloc[0])
        bars.append(plt.bar("EL_Transport", hvdc_cable, color=hvdc_color, label="HVDC Cable", zorder=3))
    
    
    plt.xlabel(loc_name)
    plt.ylabel("Asset Size (GWp)")
    plt.title("Asset Sizes " + my_network.scenario_name)

    # Use only unique labels in the legend to avoid duplicates
    handles, labels = plt.gca().get_legend_handles_labels()
    unique_labels = dict(zip(labels, handles))
    plt.grid(zorder=0)
    plt.legend(unique_labels.values(), unique_labels.keys())
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')

    plt.show()
    
    return 

