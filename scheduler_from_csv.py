import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
import time
import subprocess
from datetime import datetime, timedelta

# Read the CSV file
df = pd.read_csv('export.csv')
interval_sum = float(df['interval'].sum())

def get_time_now(add=0.0) -> str:
    now = datetime.now()
    # Add the float value to the current time 
    new_time = now + timedelta(seconds=add)
    formatted_time = new_time.strftime("%H:%M:%S")
    return formatted_time

def execute_command(job_id, interval, interval_sum, command, value):
    print(f"{get_time_now():<10} > Executing: {command:<20}{value:<15}")
    scheduler.remove_job(job_id)

def schedule_commands(first_start=False):
    global scheduler
    time_in_cycle = 0
    if(first_start):
        print("==================== JOB LIST ========================")
        print(f"Starttime: {get_time_now()}")
    # Iterate over the DataFrame and add jobs
    for index, row in df.iterrows():
        interval = row['interval']
        command = row['command']
        value = row['value']
        time_in_cycle += interval
        if(first_start):
            print(f"Job: {command:<20}{value:<15} @time: {time_in_cycle:<10}")

        # Schedule the job to run only once 
        job_id = f"job_{index}"
        scheduler.add_job(execute_command, 'interval',id=job_id, seconds=time_in_cycle, args=[job_id, interval, interval_sum, command, value])
    if(first_start):
        print(f"Looping infinitely every {interval_sum} seconds")
        print(f"=====================================================")



def main_task(): 
    # This function runs the `for` loop on an interval
    print(f">> Next Projector Commands Loop Started (Repeating every {interval_sum}s)")
    schedule_commands()


# Create a scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(main_task, 'interval', seconds=(interval_sum+0.1))
# Start the scheduler
scheduler.start()
schedule_commands(first_start=True)


try:
    # Keep the script running
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
