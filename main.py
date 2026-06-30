import threading
import time

from Ammeters.Circutor_Ammeter import CircutorAmmeter
from Ammeters.Entes_Ammeter import EntesAmmeter
from Ammeters.Greenlee_Ammeter import GreenleeAmmeter
from Ammeters.client import request_current_from_ammeter

iterrations = 15
sleep_time = 1


def run_greenlee_emulator():
    greenlee = GreenleeAmmeter(5001)
    greenlee.start_server()

def run_entes_emulator():
    entes = EntesAmmeter(5002)
    entes.start_server()

def run_circutor_emulator():
    circutor = CircutorAmmeter(5003)
    circutor.start_server()

if __name__ == "__main__":
    # Start each ammeter in a separate thread
    threading.Thread(target=run_greenlee_emulator, daemon=True).start()
    threading.Thread(target=run_entes_emulator, daemon=True).start()
    threading.Thread(target=run_circutor_emulator, daemon=True).start()

    # This section is commented out because it shouldn't work.
    # Read the README.md file as well as the source code if you need, and fix the problem.

    # Wait for the servers to start, if you have problem restarting the servers between runs try increasing sleep time.
    time.sleep(7)
    for x in range(iterrations):
        print(f"\n***************** Iterration {x + 1} *******************\n")
        print("+++++ Ammeter Greenlee ++++++\n")
        request_current_from_ammeter(5001, b'MEASURE_GREENLEE -get_measurement')  # Request from Greenlee Ammeter
        print("\n+++++ Ammeter Entes ++++++\n")
        request_current_from_ammeter(5002, b'MEASURE_ENTES -get_data')  # Request from ENTES Ammeter
        print("\n+++++ Ammeter Circutor ++++++\n")
        request_current_from_ammeter(5003, b'MEASURE_CIRCUTOR -get_measurement -current')  # Request from CIRCUTOR Ammeter
        time.sleep(sleep_time)

    pass
