# src/turkey_twin/reporter.py
import os
import datetime
from turkey_twin.utils import load_data_pure, calculate_kpis_pure

# Configuration
HISTORY_FILE = "data/last_kpis.txt"
LOG_DIR = "logs"

def generate_report():
    print("--- Starting Automated Report Generation ---")
    
    # 1. Load Data & Calculate Current KPIs
    df = load_data_pure()
    if df.empty:
        print("No data found. Aborting report.")
        return

    kpis = calculate_kpis_pure(df)
    current_battery = kpis['avg_battery']
    
    print(f"Current Avg Battery: {current_battery:.2f}%")

    # 2. Load Previous State (Change Detection)
    last_battery = 0.0
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try:
                last_battery = float(f.read().strip())
            except ValueError:
                last_battery = 0.0
    
    # 3. Calculate Delta
    delta = current_battery - last_battery
    
    # 4. Determine Alert Status
    alert_triggered = False
    # If battery dropped by more than 5% since last report
    if delta < -5.0: 
        alert_triggered = True
        print(f"!!! ALERT: Battery dropped significantly ({delta:.2f}%)")

    # 5. Generate Markdown Content
    report_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_filename = f"{LOG_DIR}/report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    md_content = f"""# 🦃 TurkeyTwin Fleet Daily Report
**Generated:** {report_date}

## 📊 Executive Summary
| Metric | Value |
| :--- | :--- |
| **Fleet Health (Avg Battery)** | {current_battery:.2f}% |
| **Total Distance Traveled** | {kpis['total_distance']:.2f} units |
| **Utilization Ratio** | {kpis['utilization_ratio']:.2f}% |

## 📉 Change Detection
* **Previous Battery Level:** {last_battery:.2f}%
* **Change (Delta):** {delta:+.2f}%
"""

    if alert_triggered:
        md_content += f"\n> 🚨 **CRITICAL ALERT:** Significant performance drop detected! Battery efficiency has declined by {abs(delta):.2f}% since the last report."

    # 6. Save Report
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    with open(report_filename, 'w') as f:
        f.write(md_content)
    
    print(f"Report saved to: {report_filename}")

    # 7. Update History File (Persistence)
    with open(HISTORY_FILE, 'w') as f:
        f.write(str(current_battery))

if __name__ == "__main__":
    generate_report()