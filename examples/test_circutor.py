import time
from pathlib import Path
import threading
import statistics
import json


from src.testing.test_framework import AmmeterTestFramework

from src.utils.logger import TestLogger

start_time = time.time()

def main():
    # יצירת מסגרת הבדיקות
    framework = AmmeterTestFramework()
                
    # הרצת בדיקות לכל סוגי האמפרמטרים
    #ammeter_types = ["greenlee", "entes", "circutor"]
    ammeter_type = "circutor"
    results = {}

    itterations = framework.itteration
    duration = framework.duration
    # Sample frequency in Hz:
    sample_freq = framework.sample_freq

    interval = 1.0 / sample_freq
    end_time = time.perf_counter() + duration
    itteration_count = 0
    
    current_list = []
        
    #logs = TestLogger(Path(__file__).stem)
    loggers = {ammeter_type: TestLogger(test_name=f"{Path(__file__).stem}")}

    #print(framework.config)

    framework.start_circutor()

    print(">>>>> Starting Server <<<<<<")

    ## Test will terminate upon duration or itteration, whichever will occur first
    print(f"Test started on {sample_freq}Hz for {duration}s with {itterations} itterations ")

    while time.perf_counter() < end_time and itteration_count < itterations:
        loop_start = time.perf_counter()
        itteration_count += 1    
        
        print(f"************** Ammeter Type {ammeter_type} ********************")                      
        print(f"Running iterration ----- {itteration_count} ------")
        results[ammeter_type] = framework.run_test(ammeter_type)
        cur = results[ammeter_type]
        # Convert the result to a dictionary
        json_ready_string = cur.replace("'", '"')
        res1 = json.loads(json_ready_string)

        # Set minimum, maximum values for current here:
        min_current = framework.min_current
        max_current = framework.max_current

        current = res1["current"]
        time_step = res1["time_step"]
        voltages = res1["voltages"]
        pretty_result = f"Current = {current}, Time Step = {time_step}, Voltages = {voltages}"
        
        # This is the logic for looging specific Ammeter types:
        logger = loggers[ammeter_type]

        current_list.append(current)       
        

        if current < min_current:
            logger.warning(pretty_result)
                    
        elif current > max_current:
            """
            In real scenario, this should be the error notification if server or DUT is not responding.
            A retry or re-connect method will be used here.

            For the available usecase an 'to high' current was the trigger for 'error' log level.
            """            
            logger.error(pretty_result)
        else:
            logger.debug(pretty_result)

        elapsed = time.perf_counter() - loop_start
        sleep_time = interval - elapsed

        if sleep_time > 0:
            time.sleep(sleep_time)        
    
    logger.info(f"Mean Current = {statistics.mean(current_list)}, Median = {statistics.median(current_list)}, Min = {min(current_list)}, Max = {max(current_list)}")                       
          
    
if __name__ == "__main__":
    main()