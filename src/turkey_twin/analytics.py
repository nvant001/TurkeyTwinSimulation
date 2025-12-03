# src/turkey_twin/analytics.py
import sqlite3
import os

from turkey_twin.config import DATABASE_PATH

def run_analytics():

    if not os.path.exists(DATABASE_PATH):
        print(f"ERROR: Database file not found at {DATABASE_PATH}.")
        print("Please run the main simulation first to generate data.")
        return

    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        print("TURKEYTWIN SIMULATION ANALYTICS REPORT")

        
 
        query_1_fleet_efficiency(cursor)
        query_2_fleet_utilization(cursor)
        query_3_time_to_discharge(cursor)
        query_4_most_active_region(cursor)

    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        if conn:
            conn.close()


def query_1_fleet_efficiency(cursor):

    print("1. Fleet Battery Performance (Total Loss)")

    
    sql_query = """
    WITH InitialState AS (
        SELECT vehicle_id, battery AS initial_battery
        FROM simulation_records
        WHERE tick = 0
    ),
    FinalState AS (
        SELECT vehicle_id, battery AS final_battery
        FROM simulation_records
        WHERE tick = (SELECT MAX(tick) FROM simulation_records)
    )
    SELECT 
        I.vehicle_id,
        I.initial_battery,
        F.final_battery,
        (I.initial_battery - F.final_battery) AS total_loss
    FROM InitialState I
    JOIN FinalState F ON I.vehicle_id = F.vehicle_id;
    """
    
    cursor.execute(sql_query)
    results = cursor.fetchall()

    print(f"{'Vehicle ID':<15}{'Initial Bat.':<15}{'Final Bat.':<15}{'Total Loss':<15}")
    for row in results:
        print(f"{row[0]:<15}{row[1]:<15.2f}{row[2]:<15.2f}{row[3]:<15.2f}")



def query_2_fleet_utilization(cursor):
    print("2. Fleet Utilization (Time Spent per Status)")
    
    sql_query = """
    SELECT
        status,
        COUNT(status) AS total_ticks
    FROM
        simulation_records
    GROUP BY
        status
    ORDER BY
        total_ticks DESC;
    """
    
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    print(f"{'Status':<15}{'Total Ticks':<15}")
    for row in results:
        print(f"{row[0]:<15}{row[1]:<15}")


def query_3_time_to_discharge(cursor):
    print("3. Maximum Discharge Point")
    

    sql_query = """
    SELECT 
        vehicle_id, 
        tick, 
        battery
    FROM
        simulation_records
    WHERE
        battery = (SELECT MIN(battery) FROM simulation_records)
    ORDER BY
        tick ASC
    LIMIT 1;
    """
    
    cursor.execute(sql_query)
    result = cursor.fetchone()

    if result:
        print(f"Vehicle: {result[0]} achieved minimum battery of {result[2]:.2f} at Tick: {result[1]}")
    else:
        print("No records found.")



def query_4_most_active_region(cursor):

    print("4. Most Active Region (Quadrant Analysis)")
    
    sql_query = """
    SELECT
        CASE
            WHEN x >= 0 AND y >= 0 THEN 'North-East (NE)'
            WHEN x < 0 AND y >= 0 THEN 'North-West (NW)'
            WHEN x < 0 AND y < 0  THEN 'South-West (SW)'
            WHEN x >= 0 AND y < 0 THEN 'South-East (SE)'
            ELSE 'Center/Origin'
        END AS Quadrant,
        COUNT(*) AS Ticks_Count
    FROM
        simulation_records
    GROUP BY
        Quadrant
    ORDER BY
        Ticks_Count DESC;
    """

    cursor.execute(sql_query)
    results = cursor.fetchall()

    print(f"{'Quadrant':<20}{'Ticks Count':<15}")
    for row in results:
        print(f"{row[0]:<20}{row[1]:<15}")


if __name__ == '__main__':
    run_analytics()