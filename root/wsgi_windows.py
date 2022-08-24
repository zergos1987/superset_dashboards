import os
import sys

# Config file ROOT DIR
CONFIG_ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

# init app venv
activate_this = CONFIG_ROOT_DIR.replace('\\', '/') + '/' +  'venv/Scripts/activate_this.py'
exec(open(activate_this).read(), dict(__file__=activate_this))

# Add the app's directory to the PYTHONPATH
sys.path.append(CONFIG_ROOT_DIR.replace('\\', '/') + '/' +  'app')
sys.path.append(CONFIG_ROOT_DIR.replace('\\', '/') + '/' +  'venv/Lib')
sys.path.append(CONFIG_ROOT_DIR.replace('\\', '/') + '/' +  'venv/Scripts')

# Add enviroment variables
os.environ["FLASK_ENV"] = "production"
os.environ["FLASK_APP"] = "superset"
os.environ["SUPERSET_LAUNCH_MODE"] = "APP"
os.environ["SUPERSET_CONFIG_PATH"] = CONFIG_ROOT_DIR.replace('\\', '/') + '/' +  'superset-config/superset_config.py'

from superset.app import create_app
application = create_app()
