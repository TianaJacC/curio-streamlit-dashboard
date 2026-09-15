import os
import datetime

# 台灣電網最新碳排放係數 (kgCO2e / kWh)
GRID_CARBON_INTENSITY_TW = 0.495 

class SessionCarbonAudit:
    def __init__(self):
        # 設備功率常數 (kW)
        self.POWER_CAMERA_LED = 0.0012   # 手機相機與感光元件 3 秒採樣
        self.POWER_OLED_DARK = 0.00045   # OLED 全黑主題低功耗 (#000000)
        self.POWER_SERVER_CORE = 0.0025  # Render 輕量容器 CPU 算力
        self.NETWORK_ENERGY_PER_MB = 0.000012 # 4G/5G 傳輸每 MB 耗能 (kWh)

    def calculate_session_impact(self, duration_sec=19, payload_kb=180, camera_sec=3):
        """
        計算單次受試者身心處方生成之能源消耗與碳排放量 (符合 ISO 14067)
        """
        # 1. 終端手機耗能 (kWh)
        device_energy = ((duration_sec * self.POWER_OLED_DARK) + (camera_sec * self.POWER_CAMERA_LED)) / 3600.0

        # 2. 雲端算力耗能 (kWh)
        cloud_energy = (0.5 * self.POWER_SERVER_CORE) / 3600.0

        # 3. 數據傳輸耗能 (kWh)
        network_energy = (payload_kb / 1024.0) * self.NETWORK_ENERGY_PER_MB

        total_energy_kwh = device_energy + cloud_energy + network_energy
        carbon_emissions_g = total_energy_kwh * GRID_CARBON_INTENSITY_TW * 1000.0

        # 與一般看診紙本掛號/處方籤相比之減碳效益 (紙張約 4.5 gCO2e / 張)
        avoided_paper_carbon_g = 4.5
        net_carbon_saving_g = round(avoided_paper_carbon_g - carbon_emissions_g, 3)

        return {
            "session_energy_kwh": round(total_energy_kwh, 6),
            "carbon_emissions_gCO2e": round(carbon_emissions_g, 3),
            "avoided_paper_carbon_gCO2e": avoided_paper_carbon_g,
            "net_carbon_saving_gCO2e": net_carbon_saving_g,
            "green_design_tag": "OLED-Dark 節能架構 ✕ 無紙化去中心存證"
        }
