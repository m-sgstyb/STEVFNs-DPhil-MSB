#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 10:19:15 2021

@author: aniqahsan
"""

### Import Packages ###

import os
import pandas as pd
import cvxpy as cp
from . import Node_STEVFNs
from ..Assets.Assets_Dictionary import ASSET_DICT
from ..Plotting import bar_chart_artist

class Network_STEVFNs:
    """This is the NETWORK class of STEVFNs"""
    def __init__(self):
        self.lat_lon_df = pd.DataFrame(columns = ["lat", "lon"])
        self.assets = []
        self.costs = []
        self.constraints = []
        self.nodes_df = pd.Series([], index = pd.MultiIndex.from_tuples([], names = ["location", "type", "time"]))
        self.base_folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return
    
    def set_usage_factor(self, discount_rate, timesteps):
        discount_factor = 1 / (1+discount_rate)
        NPV_factor = (1-discount_factor**30)/(1-discount_factor)#Assume the asset will be used for 30 years
        yearly_factor = 365.0*24 / timesteps
        self.usage_factor = NPV_factor * yearly_factor
        return
    
    def generate_node(self, node_location, node_type, node_time):
        new_node = Node_STEVFNs()
        node_df = pd.Series([new_node], 
                            index = pd.MultiIndex.from_tuples([(node_location, node_type, node_time)], 
                                    names = ["location", "type", "time"]))
        self.nodes_df = self.nodes_df.append(node_df)
        return
    
    def extract_node(self, node_location, node_type, node_time):
        if not((node_location, node_type, node_time) in self.nodes_df.index):
            self.generate_node(node_location, node_type, node_time)
        return self.nodes_df[node_location, node_type, node_time]
    
    def add_asset(self, asset):
        asset.network = self
        self.assets += [asset]
        return
    
    def build_assets(self):
        self.costs = []
        for counter1 in range(len(self.assets)):
            self.assets[counter1].build()
            self.costs += [self.assets[counter1].cost]
    
    def build_constraints(self):
        self.constraints = []
        for counter1 in range(self.nodes_df.size):
            node = self.nodes_df.iloc[counter1]
            node.build_constraints()
            self.constraints += node.constraints
        return
    
    def build_cost(self):
        self.cost = cp.sum(self.costs)
        return
    
    def build_problem(self):
        self.build_assets()
        self.build_cost()
        self.build_constraints()
        self.objective = cp.Minimize(self.cost)
        self.problem = cp.Problem(self.objective, self.constraints)
        return
    
    def solve_problem(self):
        # self.problem.solve()
        # self.problem.solve(warm_start=True)# This can sometimes use OSQP solver that sometimes gives errors.
        self.problem.solve(solver = cp.ECOS, warm_start=True)
        # self.problem.solve(solver = cp.OSQP, warm_start=True)
        # self.problem.solve(solver = cp.CVXOPT, warm_start=True)
        # self.problem.solve(solver = cp.SCS, warm_start=True)
        return
    
    def satisfy_net_loads(self):
        for counter1 in range(len(self.assets)):
            asset = self.assets[counter1]
            if type(asset).__name__ == "Conventional_Generator":
                asset.satisfy_net_load()
        return
    
    def generate_asset(self, asset_structure):
        asset_class_name = asset_structure["Asset_Class"]
        my_asset = ASSET_DICT[asset_class_name]()
        self.add_asset(my_asset)
        my_asset.define_structure(asset_structure)
        return
    
    def build(self, network_structure_df):
        #Set System Structure#
        self.system_structure_df = network_structure_df[["Asset_Number", "Asset_Class", "Location_1", "Location_2"]]
        #Generate Assets#
        for counter1 in range(len(network_structure_df)):
            self.generate_asset(network_structure_df.iloc[counter1])
        self.set_usage_factor(discount_rate = 0.05, timesteps = network_structure_df["End_Time"].max())
        #Build Problem#
        self.build_problem()
        return
    
    def update(self, location_parameters_df, asset_parameters_df):
        #Update Location lat,lon#
        for counter1 in range(len(location_parameters_df)):
            location = location_parameters_df.iloc[counter1]["Location"]
            self.lat_lon_df.loc[location, "lat"] = location_parameters_df.iloc[counter1]["lat"]
            self.lat_lon_df.loc[location, "lon"] = location_parameters_df.iloc[counter1]["lon"]
        #update Assets#
        for counter1 in range(len(asset_parameters_df)):
            asset_number = asset_parameters_df.iloc[counter1]["Asset_Number"]
            asset_type = asset_parameters_df.iloc[counter1]["Asset_Type"]
            self.assets[asset_number].update(asset_type)
        return
    
    def print_asset_sizes(self):
        #Plot some stuff#
        print("")
        for counter1 in range(len(self.assets)):
            asset = self.assets[counter1]
            print("Size of ", asset.asset_name, ":")
            print(asset.size())
        print("")
        return
    
    def get_asset_sizes(self):
        # Returns dictionary of asset sizes #
        asset_sizes_dict = dict()
        for counter1 in range(len(self.assets)):
            asset = self.assets[counter1]
            asset_sizes_dict.update(asset.get_asset_sizes())
        return asset_sizes_dict
    
    def plot_asset_sizes(self):
        # Make Bar Chart of Asset Sizes #
        my_artist = bar_chart_artist()
        my_artist.add_group("Base")
        for counter1 in range(len(self.assets)):
            asset = self.assets[counter1]
            asset_name = str(counter1) + r"_" + asset.asset_name
            my_artist.add_asset(asset_name, asset)
        my_artist.plot()
        return
    
    def plot_asset_usage(self):
        # Plot the flows in each asset #
        for counter1 in range(len(self.assets)):
            asset = self.assets[counter1]
            asset.plot_asset_usage()
        return
    
    def get_asset_number_by_locations(self, loc_1, loc_2):
        # Returns list of Asset_Number of assets at the specific loc_1 and loc_2 #
        con_1 = self.system_structure_df["Location_1"] == loc_1
        con_2 = self.system_structure_df["Location_2"] == loc_2
        t_con = con_1 & con_2
        return list(self.system_structure_df[t_con]["Asset_Number"])
