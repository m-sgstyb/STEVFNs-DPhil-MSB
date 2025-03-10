#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 13:06:03 2024

@authors: Aniq Ahsan & Mónica Sagastuy-Breña

This script creates/updates all Asset_Parameters.csv, Location_Parameters.csv,
and System_Parameters.csv files in all scenario folders of a case study
This is based upon the case_study_builder.py from GMPA project in the original
STEVFNs repository

The only lines to edit in this script are at the bottom.

Requirements before running:
    1. A Case_Study folder with:
        
        a) Network_Structure.csv
        b) BAU scenario folder with:
                Asset_Parameters.csv,
                System_Parameters.csv and
                Location_Prameters.csv
    
Running the script:
    
    1. For single-country case studies (Autarky_XX), rename "single_country_case_study"
    to the three letter ISO abbreviation. Run the script with the function update_scenarios_single_country
    
    2. For multiple countries, to create XXX_YYY_Autarky and XXX_YYY_Collab scenarios 
    parameters, rename the "multiple_country_case_study". Run the script with the 
    function update_scenarios_collab
    
    
    You may run both functions simultaneously if the required steps have been done for
    all case studies you want to update.
    
"""

import os
import pandas as pd
import numpy as np

# =============================================================================
# Definition of base folder to define specific file folders in functions
# =============================================================================
base_folder = os.path.dirname(__file__)


def update_scenarios_single_country(base_case_study):
    '''
    Function that pdates the case study folder, copying the content of Asset_Parameters.csv 
    in BAU to all emissions constraints scenario folders (0-90).

    Parameters
    ----------
    base_case_study : STRING
        String or assigned string variable name of the case study that will
        be created. For single-country scenarios, this should be a single, two-letter
        ISO abbreviation for the country to be modelled. e.g. "SG"

    Returns
    -------
    None.

    '''
    
    # Single country path definitions
    sc_case_study_folder = os.path.join(base_folder, single_country_case_study)
    sc_asset_filename = os.path.join(sc_case_study_folder, base_scenario_name, "Asset_Parameters.csv")
    sc_location_filename = os.path.join(sc_case_study_folder, base_scenario_name, "Location_Parameters.csv")
    sc_system_filename = os.path.join(sc_case_study_folder, base_scenario_name, "System_Parameters.csv")

    base_asset_df = pd.read_csv(sc_asset_filename)
    base_locs_df = pd.read_csv(sc_location_filename)
    base_sys_df = pd.read_csv(sc_system_filename)

    for counter1 in range(10):
        scenario_name = 'scenario_' + str((np.arange(10)*10)[-counter1-1])
        if not os.path.exists(os.path.join(sc_case_study_folder, scenario_name)):
            os.makedirs(os.path.join(sc_case_study_folder, scenario_name))
        
        
        new_asset_filename = os.path.join(sc_case_study_folder, scenario_name, "Asset_Parameters.csv")
        new_asset_df = base_asset_df.copy()
        asset_type_list = list(new_asset_df["Asset_Type"])
        asset_type_list[0] = new_asset_df["Asset_Type"][0] + counter1 + 1
        new_asset_df["Asset_Type"] = asset_type_list
        new_asset_df.to_csv(new_asset_filename, index=False)
        
        new_locations_filename = os.path.join(sc_case_study_folder, scenario_name, "Location_Parameters.csv")
        new_locs_df = base_locs_df.copy()
        new_locs_df.to_csv(new_locations_filename, index=False)
        
        new_sys_filename = os.path.join(sc_case_study_folder, scenario_name, "System_Parameters.csv")
        new_sys_df = base_sys_df.copy()
        new_sys_df.to_csv(new_sys_filename, index=False)
    
    

def update_scenarios_collab(base_case_study):
    '''
    Function that pdates the case study folder, copying the content of Asset_Parameters.csv 
    in BAU to all emissions constraints scenario folders (0-90).

    Parameters
    ----------
    base_case_study : STRING
        String or assigned string variable name of the case study that will
        be created. For collabe scenarios, this should be at least of two countries
        e.g. "ID-MY" or "SG-ID-MY"

    Returns
    -------
    None.

    '''
    
    # Multiple country path definitions
    case_study_folder_aut = os.path.join(base_folder, base_case_study + r"_Autarky")
    case_study_folder_col = os.path.join(base_folder, base_case_study + r"_Collab")
    asset_filename_aut = os.path.join(case_study_folder_aut, base_scenario_name, "Asset_Parameters.csv")
    asset_filename_col = os.path.join(case_study_folder_col, base_scenario_name, "Asset_Parameters.csv")

    location_filename_aut = os.path.join(case_study_folder_aut, base_scenario_name, "Location_Parameters.csv")
    location_filename_col = os.path.join(case_study_folder_col, base_scenario_name, "Location_Parameters.csv")
    
    system_filename_aut = os.path.join(case_study_folder_aut, base_scenario_name, "System_Parameters.csv")
    system_filename_col = os.path.join(case_study_folder_col, base_scenario_name, "System_Parameters.csv")
    
    # Updates the _Autarky case study scenarios
    base_asset_df = pd.read_csv(asset_filename_aut)
    base_locs_df = pd.read_csv(location_filename_aut)
    base_sys_df = pd.read_csv(system_filename_aut)

    for counter1 in range(10):
        scenario_name = str((np.arange(10)*10)[-counter1-1])
        if not os.path.exists(os.path.join(case_study_folder_aut, scenario_name)):
            os.makedirs(os.path.join(case_study_folder_aut, scenario_name))
        
        new_asset_filename = os.path.join(case_study_folder_aut, scenario_name, "Asset_Parameters.csv")
        new_asset_df = base_asset_df.copy()
        asset_type_list = list(new_asset_df["Asset_Type"])
        asset_type_list[0] = new_asset_df["Asset_Type"][0] + counter1 + 1
        new_asset_df["Asset_Type"] = asset_type_list
        new_asset_df.to_csv(new_asset_filename, index=False)
        
        new_locations_filename = os.path.join(case_study_folder_aut, scenario_name, "Location_Parameters.csv")
        new_locs_df = base_locs_df.copy()
        new_locs_df.to_csv(new_locations_filename, index=False)
        
        new_sys_filename = os.path.join(case_study_folder_aut, scenario_name, "System_Parameters.csv")
        new_sys_df = base_sys_df.copy()
        new_sys_df.to_csv(new_sys_filename, index=False)


    # Updates the _Collab case study scenarios
    base_asset_df = pd.read_csv(asset_filename_col)
    base_locs_df = pd.read_csv(location_filename_col)
    base_sys_df = pd.read_csv(system_filename_col)

    for counter1 in range(10):
        scenario_name = str((np.arange(10)*10)[-counter1-1])
        if not os.path.exists(os.path.join(case_study_folder_col, scenario_name)):
            os.makedirs(os.path.join(case_study_folder_col, scenario_name))
        
        new_asset_filename = os.path.join(case_study_folder_col, scenario_name, "Asset_Parameters.csv")
        new_asset_df = base_asset_df.copy()
        asset_type_list = list(new_asset_df["Asset_Type"])
        asset_type_list[0] = new_asset_df["Asset_Type"][0] + counter1 + 1
        new_asset_df["Asset_Type"] = asset_type_list
        new_asset_df.to_csv(new_asset_filename, index=False)
        
        new_locations_filename = os.path.join(case_study_folder_col, scenario_name, "Location_Parameters.csv")
        new_locs_df = base_locs_df.copy()
        new_locs_df.to_csv(new_locations_filename, index=False)
        
        new_sys_filename = os.path.join(case_study_folder_col, scenario_name, "System_Parameters.csv")
        new_sys_df = base_sys_df.copy()
        new_sys_df.to_csv(new_sys_filename, index=False)
        
    return


# =============================================================================
# TO-DO: Edit single and/or multiple country case study to the names required
# Leave base_scenario_name as "BAU"
# =============================================================================

single_country_case_study = "MEX"

base_scenario_name = "scenario_100"
# update_scenarios_collab(multiple_country_case_study)

update_scenarios_single_country(single_country_case_study)