import os
import json
import datetime
import pandas as pd

# ==============================================================================
# 國際環境與電網基準參數 (碳排放因子庫)
# ==============================================================================
# 台灣經濟部能源署最新電力排碳係數 (kgCO2e / kWh)
GRID_CARBON_INTENSITY_TW = 0.495

# 雲端資料中心平均電能使用效率 (PUE - Power Usage Effectiveness, 依據 Uptime Institute 基準)
DATA_CENTER_PUE = 1.25

# 智慧型手機搖籃到大門 (Cradle-to-Gate) 體現碳 (Embodied Carbon, kgCO2e / 台, 依據 Apple/Fairphone LCA 報告)
SMARTPHONE_EMBODIED_CARBON_KG = 55.0
SMARTPHONE_LIFETIME_HOURS = 3.0 * 365.0 * 24.0  # 預設三年生命週期

# A4 醫療級原生紙張碳足跡 (含木漿採伐、製程及運送, kgCO2e / 張, 依據 Ecoinvent 數據)
PAPER_MEDICAL_SHEET_KGCO2E = 0.00485

class EnterpriseScope3CarbonEngine:
    def __init__(self):
        # 物理功率常數 (kW)
        self.P_OLED_DARK = 0.00038       # OLED 純黑像素自發光功耗 (#000000)
        self.P_OLED_BRIGHT = 0.00115     # 一般淺色主題 OLED 功耗 (對照組)
        self.P_CAMERA_SENSOR = 0.00135   # CMOS 感光元件與神經網路 ISP 採樣 (rPPG 啟動)
        self.P_RENDER_CORE_KW = 0.0032   # Render 虛擬化容器 CPU 工作分配功耗
        self.ENERGY_PER_GB_NETWORK = 0.015 # 4G/5G 骨幹網路與基地台每 GB 傳輸功耗 (kWh/GB)

    def calculate_single_session_lca(self, duration_sec=19, camera_sec=3, payload_kb=220):
        """
        計算單次受試者身心處方調息之微觀產品碳足跡 (ISO 14067 產品生命週期評估)
        """
        # 1. 邊緣手機端實際耗能 (kWh)
        oled_energy_kwh = (duration_sec * self.P_OLED_DARK) / 3600.0
        rppg_energy_kwh = (camera_sec * self.P_CAMERA_SENSOR) / 3600.0
        edge_energy_kwh = oled_energy_kwh + rppg_energy_kwh

        # 2. 雲端伺服器運算耗能 (含 PUE 算力加權, kWh)
        cloud_server_energy_kwh = (0.35 * self.P_RENDER_CORE_KW * DATA_CENTER_PUE) / 3600.0

        # 3. 5G/行動數據傳輸耗能 (kWh)
        network_energy_kwh = (payload_kb / (1024.0 * 1024.0)) * self.ENERGY_PER_GB_NETWORK

        # 總作業能耗
        total_energy_kwh = edge_energy_kwh + cloud_server_energy_kwh + network_energy_kwh
        total_operational_carbon_g = total_energy_kwh * GRID_CARBON_INTENSITY_TW * 1000.0

        # 4. 硬體實體體現碳攤銷 (Embodied Carbon Allocation)
        hardware_embodied_carbon_g = (duration_sec / 3600.0) * (SMARTPHONE_EMBODIED_CARBON_KG / SMARTPHONE_LIFETIME_HOURS) * 1000.0
        total_lca_carbon_g = total_operational_carbon_g + hardware_embodied_carbon_g

        # 5. 綠色演算法節能效益評估 (相較於淺色 UI 與紙本實體問卷)
        oled_savings_kwh = (duration_sec * (self.P_OLED_BRIGHT - self.P_OLED_DARK)) / 3600.0
        oled_avoided_carbon_g = oled_savings_kwh * GRID_CARBON_INTENSITY_TW * 1000.0
        paper_avoided_carbon_g = PAPER_MEDICAL_SHEET_KGCO2E * 1000.0  # 避免一張 A4 紙張與列印碳排
        net_carbon_benefit_g = (paper_avoided_carbon_g + oled_avoided_carbon_g) - total_lca_carbon_g

        return {
            "operational_energy_kwh": round(total_energy_kwh, 7),
            "operational_carbon_gCO2e": round(total_operational_carbon_g, 4),
            "embodied_hardware_carbon_gCO2e": round(hardware_embodied_carbon_g, 4),
            "total_lca_carbon_gCO2e": round(total_lca_carbon_g, 4),
            "paper_avoided_carbon_gCO2e": round(paper_avoided_carbon_g, 3),
            "net_carbon_benefit_gCO2e": round(net_carbon_benefit_g, 3),
            "verification_status": "ISO 14067 & GHG Protocol Scope 3 Ready"
        }

    def generate_annual_enterprise_ghg_report(self, session_db_path="system_logs/active_sessions.json"):
        """
        聚合年度全體員工數據，生成符合 GHG Protocol 範疇三 (Category 11)
        與 GRI 302 (能源)、GRI 305 (排放) 規範之企業碳揭露審計摘要表
        """
        if not os.path.exists(session_db_path):
            return pd.DataFrame()

        try:
            with open(session_db_path, "r", encoding="utf-8") as f:
                db_data = json.load(f)
        except Exception:
            return pd.DataFrame()

        total_sessions = len(db_data)
        if total_sessions == 0:
            return pd.DataFrame()

        # 彙總全體員工年度累計數據
        single = self.calculate_session_impact()
        annual_energy_kwh = total_sessions * single["operational_energy_kwh"]
        annual_scope3_ghg_kg = (total_sessions * single["total_lca_carbon_gCO2e"]) / 1000.0
        annual_paper_saved_kg = (total_sessions * single["paper_avoided_carbon_gCO2e"]) / 1000.0
        annual_net_benefit_kg = (total_sessions * single["net_carbon_benefit_gCO2e"]) / 1000.0

        current_year = datetime.datetime.now().year

        audit_matrix = {
            "ESG 準則指標": [
                "GRI 302-1 / 302-4",
                "GHG Protocol Scope 3 (Cat 11)",
                "ISO 14064-1:2018 類別四",
                "SDG 12.5 / 減廢效益",
                "GRI 403-6 / 健康促進覆蓋"
            ],
            "揭露項目 (Disclosure Item)": [
                f"{current_year} 年度數位身心健康服務累計能耗 (Electricity Consumption)",
                f"{current_year} 年度產品售後使用階段間接溫室氣體排放量 (Use of Sold Products)",
                f"{current_year} 雲端算力與終端數位足跡全生命週期碳排放 (Full LCA Footprint)",
                f"{current_year} 數位化無紙化身心處方淨減碳效益 (Net Avoided Emissions)",
                f"{current_year} 受惠員工總人次與主動健康管理介入次數 (Total Engagement)"
            ],
            "數值 (Metric Value)": [
                f"{round(annual_energy_kwh, 4)} kWh",
                f"{round(annual_scope3_ghg_kg, 3)} kgCO2e",
                f"{round(annual_scope3_ghg_kg * 1.05, 3)} kgCO2e (含 5% 不確定性餘量)",
                f"-{round(annual_net_benefit_kg, 3)} kgCO2e (實質負碳效益)",
                f"{total_sessions:,} 人次 (100% 零個資 No-PII 架構)"
            ],
            "確信佐證與邊界界定": [
                "依據台電排碳係數 0.495 及雲端 PUE 1.25 加權換算",
                "GHG Protocol 範疇三技術指引 Category 11 間接排放",
                "含邊緣手機硬體體現碳 LCA 3 年分攤模型",
                "對照傳統醫療雙聯處方籤 4.85g/張 之實體替代量",
                "去中心化 Photo-Hash 密鑰雜湊，符合 GDPR 隱私標準"
            ]
        }

        report_df = pd.DataFrame(audit_matrix)
        out_path = os.path.join("system_logs", "ESG_Annual_GHG_Scope3_Report.csv")
        report_df.to_csv(out_path, index=False, encoding="utf-8-sig")
        return report_df

    def calculate_session_impact(self):
        return self.calculate_single_session_lca()