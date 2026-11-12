import logging 
import os

#Step1: create log directory
os.makedirs("logs",exist_ok = True)

#Step2: configure logging
logging.basicConfig(
    
    level = logging.INFO,
    format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    handlers = [
        logging.FileHandler("logs/app.log"),
        logging .StreamHandler()
    ]
)

#Step3: create logger
logger = logging.getLogger("EmployeePerformanceAPI")
