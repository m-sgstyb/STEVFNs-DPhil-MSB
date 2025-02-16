#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 11:16:24 2021

@author: aniqahsan
"""

from .EL_Demand import EL_Demand_Asset
from .HTH_Demand import HTH_Demand_Asset
from .CG import CG_Asset
from .EL_to_HTH import EL_to_HTH_Asset
from .BESS import BESS_Asset
from .BESS_Existing import BESS_Existing_Asset
from .EL_to_NH3 import EL_to_NH3_Asset
from .NH3_to_EL import NH3_to_EL_Asset
from .NH3_Storage import NH3_Storage_Asset
from .NH3_to_HTH import NH3_to_HTH_Asset
from .EL_Transport import EL_Transport_Asset
from .NH3_Transport import NH3_Transport_Asset
from .EL_Demand_UM import EL_Demand_UM_Asset
from .CO2_Budget import CO2_Budget_Asset
from .PP_CO2 import PP_CO2_Asset
from .PP_CO2_Existing import PP_CO2_Existing_Asset
from .RE_PV_Openfield_Lim import RE_PV_Openfield_Lim_Asset
from .RE_PV_Existing import RE_PV_Existing_Asset
from .RE_WIND_Onshore_Lim import RE_WIND_Onshore_Lim_Asset
from .RE_WIND_Existing import RE_WIND_Existing_Asset
from .PP_NGS_CCGT_CO2 import PP_NGS_CCGT_CO2_Asset
from .PP_NGS_SCGT_CO2 import PP_NGS_SCGT_CO2_Asset
from .PP_COAL_CO2 import PP_COAL_CO2_Asset



ASSET_DICT = {EL_Demand_Asset.asset_name: EL_Demand_Asset,
              HTH_Demand_Asset.asset_name: HTH_Demand_Asset,
              CG_Asset.asset_name: CG_Asset,
              EL_to_HTH_Asset.asset_name: EL_to_HTH_Asset,
              BESS_Asset.asset_name: BESS_Asset,
              BESS_Existing_Asset.asset_name: BESS_Existing_Asset,
              EL_to_NH3_Asset.asset_name: EL_to_NH3_Asset,
              NH3_to_EL_Asset.asset_name: NH3_to_EL_Asset,
              NH3_Storage_Asset.asset_name: NH3_Storage_Asset,
              NH3_to_HTH_Asset.asset_name: NH3_to_HTH_Asset,
              EL_Transport_Asset.asset_name: EL_Transport_Asset,
              NH3_Transport_Asset.asset_name: NH3_Transport_Asset,
              EL_Demand_UM_Asset.asset_name: EL_Demand_UM_Asset,
              CO2_Budget_Asset.asset_name: CO2_Budget_Asset,
              PP_CO2_Asset.asset_name: PP_CO2_Asset,
              PP_CO2_Existing_Asset.asset_name: PP_CO2_Existing_Asset,
              RE_PV_Openfield_Lim_Asset.asset_name: RE_PV_Openfield_Lim_Asset,
              RE_PV_Existing_Asset().asset_name: RE_PV_Existing_Asset,
              RE_WIND_Onshore_Lim_Asset.asset_name: RE_WIND_Onshore_Lim_Asset,
              RE_WIND_Existing_Asset.asset_name: RE_WIND_Existing_Asset,
              PP_NGS_CCGT_CO2_Asset.asset_name: PP_NGS_CCGT_CO2_Asset,
              PP_NGS_SCGT_CO2_Asset.asset_name: PP_NGS_SCGT_CO2_Asset,
              PP_COAL_CO2_Asset.asset_name: PP_COAL_CO2_Asset,
              }
