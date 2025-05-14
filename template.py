import os
from pathlib import Path
import logging
import sys
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: [%(message)s]:')
project_name = "RAGwithSagemaker"

list_of_files = [".github/workflows/.gitkeep",
                 f"{project_name}/__init__.py",
                 f"{project_name}/components/__init__.py",
                 f"{project_name}/utils/__init__.py", 
                 f"{project_name}/utils/common.py", 
                 f"{project_name}/config/__init__.py", 
                 f"{project_name}/config/configuration.py",
                 f"{project_name}/pipeline/__init__.py",
                 f"{project_name}/entity/__init__.py",
                 f"{project_name}/entity/config_entity.py",
                 f"{project_name}/constants/__init__.py",
                 f"{project_name}/cloud/__init__.py",
                 f"{project_name}/exception/__init__.py",
                 f"{project_name}/logging/__init__.py",
                 f"Data/__init__.py",
                 "main.py",
                 "params.yaml",
                 "schema.yaml",
                 "config/config.yaml",
                 "Dockerfile",
                 "requirements.txt",
                 "setup.py",
                 "research/research.ipynb",
                 ]

for file_path in list_of_files:
    file_path = Path(file_path)
    filedir,filename = os.path.split(file_path)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory {filedir} for the file {filename}")
    
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, "w") as file:
            pass
        logging.info(f"{file_path} created")
    else:
        logging.info(f"{file_path} already exists")
# os.system("mv logger.py RAGwithSagemaker/logging ")

with open(f"{project_name}/logging/logging.py", "w") as f:
    f.write("""
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
            

            """)