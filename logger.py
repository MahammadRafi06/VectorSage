import logging.config
import os
import sys
import logging
from datetime import datetime
# logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
# logging_dir = "logs"
# logging_filepath = os.path.join(logging_dir, "logging.log")
# os.makedirs(logging_dir, exist_ok=True)

# logging.basicConfig(level=logging.INFO, 
#                     format=logging_str,
#                     handlers=[logging.FileHandler(logging_filepath), 
#                               logging.StreamHandler(sys.stdout)]
#                     )

# logger = logging.getLogger("datasciencelogger")





LOG_DIR = os.getenv('LOG_DIR', './logs/')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

def get_logger(name, log_dir = LOG_DIR, log_level = LOG_LEVEL):

    '''
    Set up a logger with the given name and log level.
    '''
    _logs = logging.getLogger(name)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    f_handler = logging.FileHandler(os.path.join(log_dir, f'{ datetime.now().strftime("%Y%m%d_%H%M%S") }.log'))
    f_format = logging.Formatter('%(asctime)s, %(name)s, %(filename)s, %(lineno)d, %(funcName)s, %(levelname)s, %(message)s')
    f_handler.setFormatter(f_format)
    _logs.addHandler(f_handler)
    
    s_handler = logging.StreamHandler()
    s_format = logging.Formatter('%(asctime)s, %(filename)s, %(lineno)d, %(levelname)s, %(message)s')
    s_handler.setFormatter(s_format)
    _logs.addHandler(s_handler)
    
    _logs.setLevel(log_level)
    return _logs
logger = get_logger("networksecurity", log_dir = LOG_DIR, log_level = LOG_LEVEL)