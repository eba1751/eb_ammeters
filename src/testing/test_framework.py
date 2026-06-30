import time
import threading

from ..utils.config import load_config

from Ammeters.Greenlee_Ammeter import GreenleeAmmeter
from Ammeters.Entes_Ammeter import EntesAmmeter
from Ammeters.Circutor_Ammeter import CircutorAmmeter
from Ammeters.client import request_current_from_ammeter

greenl = GreenleeAmmeter(5001)
ents = EntesAmmeter(5002)
circt = CircutorAmmeter(5003)

yaml_path = "config/config.yaml"


class AmmeterTestFramework:
    def __init__(self, config_path: str = yaml_path):
        self.config = load_config(config_path)
        # Get parameters from yaml file:
        self.itteration = self.config["testing"]["sampling"]["measurements_count"]
        self.duration = self.config["testing"]["sampling"]["total_duration_seconds"]
        self.sample_freq = self.config["testing"]["sampling"]["sampling_frequency_hz"]

        # Ammeter parameters:
        self.ammeters = self.config["ammeters"]
                
    # ENTES Ammeter block:
    def run_entes_emulator(self):
        self.port = self.ammeters["entes"]["port"]
        entes = EntesAmmeter(self.port)
        entes.start_server()

    def start_entes(self):
        threading.Thread(target=self.run_entes_emulator, daemon=True).start()
        # Wait for server to start...
        time.sleep(3)

    def stop_entes(self):
        # Stop the server if for some reason the server needs to be stopped
        pass

    # GREENLEE Ammeter block:
    def run_greenle_emulator(self):
        self.port = self.ammeters["greenlee"]["port"]
        entes = GreenleeAmmeter(self.port)
        entes.start_server()

    def start_greenlee(self):
        threading.Thread(target=self.run_greenle_emulator, daemon=True).start()
        # Wait for server to start...
        time.sleep(3)

    def stop_greenlee(self):
        # Stop the server if for some reason the server needs to be stopped
        pass

    # CIRCUTOR Ammeter block:
    def run_circutor_emulator(self):
        self.port = self.ammeters["circutor"]["port"]
        entes = CircutorAmmeter(self.port)
        entes.start_server()

    def start_circutor(self):
        threading.Thread(target=self.run_circutor_emulator, daemon=True).start()
        # Wait for server to start...
        time.sleep(3)

    def stop_circutor(self):
        # Stop the server if for some reason the server needs to be stopped
        pass
    
    def run_test(self, ammeter_type: str) -> dict:
        self.result1 = None
        self.ammeter = self.ammeters[ammeter_type]
        self.port = self.ammeter["port"]
        self.command = self.ammeter["command"]
        self.min_current = float(self.ammeters[ammeter_type]["min_current"])
        self.max_current = float(self.ammeters[ammeter_type]["max_current"])

        self.result1 = request_current_from_ammeter(self.port, self.command.encode('utf-8'))           
            
        return self.result1