print('\n>>>>>>>>>>>>>>>>>>>>>>>>>> init start: superset_production_config <<<<<<<<<<<<<<<<<<<<<<<<<<<<\n')
import imp  # pylint: disable=deprecated-module
import importlib.util
import json
import logging
import os
import re
import sys
import random
import string
import shutil
import socket
import requests
from ldap3 import (
    Server, 
    Connection, 
    ALL, 
    SUBTREE, 
    LEVEL,
)
from decouple import AutoConfig
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.local import LocalProxy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
#from s3cache import S3Cache
#from werkzeug.contrib.cache import RedisCache
import redis
import cx_Oracle
import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy import create_engine, MetaData, Table, select, asc
from sqlalchemy import Column, Integer, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, close_all_sessions

from collections import OrderedDict
from datetime import datetime, timedelta
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Type,
    TYPE_CHECKING,
    Union,
)

from urllib.parse import urlparse, parse_qs, quote, unquote
import pkg_resources
from cachelib.base import BaseCache
from celery.schedules import crontab
from dateutil import tz
from flask import Blueprint, Flask, session, redirect, g, flash, request, render_template
from flask_babel import lazy_gettext as _
import jwt
from flask_jwt_extended import current_user as current_user_jwt
from flask_jwt_extended import JWTManager
from flask_login import current_user, LoginManager, login_user, logout_user
from flask_appbuilder import (
    expose, 
    IndexView,
)
from superset import app
from superset.security import SupersetSecurityManager
from flask_appbuilder.security.sqla.models import User
from flask_appbuilder.security.views import UserDBModelView, AuthView, AuthDBView, AuthRemoteUserView
from flask_appbuilder.security.views import expose
from flask_appbuilder.security.manager import (
    AUTH_DB,
    AUTH_LDAP,
    AUTH_OAUTH,
    AUTH_OID,
    AUTH_REMOTE_USER,
    LOGMSG_ERR_SEC_ADD_REGISTER_USER,
    LOGMSG_ERR_SEC_AUTH_LDAP,
    LOGMSG_ERR_SEC_AUTH_LDAP_TLS,
    LOGMSG_WAR_SEC_LOGIN_FAILED,
    LOGMSG_WAR_SEC_NO_USER,
    LOGMSG_WAR_SEC_NOLDAP_OBJ,
    PERMISSION_PREFIX,
)
from pandas._libs.parsers import STR_NA_VALUES  # pylint: disable=no-name-in-module
from superset.advanced_data_type.plugins.internet_address import internet_address
from superset.advanced_data_type.plugins.internet_port import internet_port
from superset.advanced_data_type.types import AdvancedDataType
from superset.constants import CHANGE_ME_SECRET_KEY
from superset.jinja_context import BaseTemplateProcessor
from superset.stats_logger import DummyStatsLogger
from superset.superset_typing import CacheConfig, FlaskResponse
from superset.security import SupersetSecurityManager
from superset.utils.core import is_test, parse_boolean_string
from superset.utils.encrypt import SQLAlchemyUtilsAdapter
from superset.utils.log import DBEventLogger
from superset.utils.logging_configurator import DefaultLoggingConfigurator
from superset.utils.urls import headless_url
from superset.utils.machine_auth import MachineAuthProvider

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from flask_appbuilder.security.sqla import models

    from superset.connectors.sqla.models import SqlaTable
    from superset.models.core import Database

from flask_appbuilder.security.manager import BaseSecurityManager

# Config file ROOT DIR
CONFIG_ROOT_DIR = os.path.dirname(__file__)
config = AutoConfig(search_path=CONFIG_ROOT_DIR)



# ----------------------------------------------------------------------------------
# Superset VARS
# ----------------------------------------------------------------------------------
os.environ["FLASK_APP"] = os.environ.get("FLASK_APP", config('FLASK_APP'))
os.environ["FLASK_ENV"] = os.environ.get("FLASK_ENV", config('FLASK_ENV'))


os.environ["SUPERSET_LAUNCH_MODE"] = os.environ.get("SUPERSET_LAUNCH_MODE", config('SUPERSET_LAUNCH_MODE'))
os.environ["SUPERSET_HOME"] = CONFIG_ROOT_DIR.replace('\\', '/') + '/' + os.environ.get("SUPERSET_HOME", config('SUPERSET_HOME'))
os.environ["SUPERSET_HOST"] = os.environ.get("SUPERSET_HOST", config('SUPERSET_HOST'))
os.environ["SUPERSET_PORT"] = os.environ.get("SUPERSET_PORT", config('SUPERSET_PORT'))
os.environ["SUPERSET_ADMIN_LOGIN"] = os.environ.get("SUPERSET_ADMIN_LOGIN", config('SUPERSET_ADMIN_LOGIN'))
os.environ["SUPERSET_ADMIN_PASSWORD"] = os.environ.get("SUPERSET_ADMIN_PASSWORD", config('SUPERSET_ADMIN_PASSWORD'))
os.environ["SUPERSET_HTTPS_CRT"] = os.environ.get("SUPERSET_HTTPS_CRT", config('SUPERSET_HTTPS_CRT'))
os.environ["SUPERSET_HTTPS_KEY"] = os.environ.get("SUPERSET_HTTPS_KEY", config('SUPERSET_HTTPS_KEY'))
os.environ["SUPERSET_AUTH_TOKEN_SECRET"] = os.environ.get("SUPERSET_AUTH_TOKEN_SECRET", config('SUPERSET_AUTH_TOKEN_SECRET'))

os.environ["LDAP_url"] = os.environ.get("LDAP_url", config('LDAP_url'))
os.environ["LDAP_domain"] = os.environ.get("LDAP_domain", config('LDAP_domain'))
os.environ["LDAP_dc1"] = os.environ.get("LDAP_dc1", config('LDAP_dc1'))
os.environ["LDAP_dc2"] = os.environ.get("LDAP_dc2", config('LDAP_dc2'))
os.environ["LDAP_dc3"] = os.environ.get("LDAP_dc3", config('LDAP_dc3'))
os.environ["LDAP_user"] = os.environ.get("LDAP_user", config('LDAP_user'))
os.environ["LDAP_password"] = os.environ.get("LDAP_password", config('LDAP_password'))

os.environ["PROD_DB_HOST"] = os.environ.get("PROD_DB_HOST", config('PROD_DB_HOST'))
os.environ["PROD_DB_PORT"] = os.environ.get("PROD_DB_PORT", config('PROD_DB_PORT'))
os.environ["PROD_DB_DBNAME"] = os.environ.get("PROD_DB_DBNAME", config('PROD_DB_DBNAME'))
os.environ["PROD_DB_SHEMA"] = os.environ.get("PROD_DB_SHEMA", config('PROD_DB_SHEMA'))
os.environ["PROD_DB_USER"] = os.environ.get("PROD_DB_USER", config('PROD_DB_USER'))
os.environ["PROD_DB_PASS"] = os.environ.get("PROD_DB_PASS", config('PROD_DB_PASS'))

os.environ["PROD_USERS_DASHBOARDS_DB_1_HOST"] = os.environ.get("PROD_USERS_DASHBOARDS_DB_1_HOST", config('PROD_USERS_DASHBOARDS_DB_1_HOST'))
os.environ["PROD_USERS_DASHBOARDS_DB_1_PORT"] = os.environ.get("PROD_USERS_DASHBOARDS_DB_1_PORT", config('PROD_USERS_DASHBOARDS_DB_1_PORT'))
os.environ["PROD_USERS_DASHBOARDS_DB_1_DBNAME"] = os.environ.get("PROD_USERS_DASHBOARDS_DB_1_DBNAME", config('PROD_USERS_DASHBOARDS_DB_1_DBNAME'))
os.environ["PROD_USERS_DASHBOARDS_DB_1_SHEMA"] = os.environ.get("PROD_USERS_DASHBOARDS_DB_1_SHEMA", config('PROD_USERS_DASHBOARDS_DB_1_SHEMA'))
os.environ["PROD_USERS_DASHBOARDS_DB_1_USER"] = os.environ.get("PROD_USERS_DASHBOARDS_DB_1_USER", config('PROD_USERS_DASHBOARDS_DB_1_USER'))
os.environ["PROD_USERS_DASHBOARDS_DB_1_PASS"] = os.environ.get("PROD_USERS_DASHBOARDS_DB_1_PASS", config('PROD_USERS_DASHBOARDS_DB_1_PASS'))

os.environ["PROD_USERS_DASHBOARDS_DB_3_HOST"] = os.environ.get("PROD_USERS_DASHBOARDS_DB_3_HOST", config('PROD_USERS_DASHBOARDS_DB_3_HOST'))
os.environ["PROD_USERS_DASHBOARDS_DB_3_PORT"] = os.environ.get("PROD_USERS_DASHBOARDS_DB_3_PORT", config('PROD_USERS_DASHBOARDS_DB_3_PORT'))
os.environ["PROD_USERS_DASHBOARDS_DB_3_DBNAME"] = os.environ.get("PROD_USERS_DASHBOARDS_DB_3_DBNAME", config('PROD_USERS_DASHBOARDS_DB_3_DBNAME'))
os.environ["PROD_USERS_DASHBOARDS_DB_3_USER"] = os.environ.get("PROD_USERS_DASHBOARDS_DB_3_USER", config('PROD_USERS_DASHBOARDS_DB_3_USER'))
os.environ["PROD_USERS_DASHBOARDS_DB_3_PASS"] = os.environ.get("PROD_USERS_DASHBOARDS_DB_3_PASS", config('PROD_USERS_DASHBOARDS_DB_3_PASS'))

os.environ["PATH"] += os.pathsep + os.path.join(CONFIG_ROOT_DIR, "selenium")

REDIS_HOST = "127.0.0.1"
REDIS_PORT = "6379"

# This host ip
host_name = socket.getfqdn()
host_ip = socket.gethostbyname_ex(host_name)[2][0]

# default log
logger = logging.getLogger(__name__)

# Initialize Oracle client databases connections
try:
    cx_Oracle.init_oracle_client(lib_dir=CONFIG_ROOT_DIR + '/instantclient_19_12')
except Exception as e:
    pass

# The Superset Host INIT
SUPERSET_WEBSERVER_DOMAINS = [os.getenv('SUPERSET_HOST')]
if os.environ.get("SUPERSET_LAUNCH_MODE") in ['APP', 'THUMBNAILS']:
    SUPERSET_WEBSERVER_PROTOCOL = "http" if os.environ.get("FLASK_ENV") == "development" else "https"
    SUPERSET_WEBSERVER_PORT = int(os.getenv('SUPERSET_PORT'))
else:
    SUPERSET_WEBSERVER_PROTOCOL = "http" if os.environ.get("FLASK_ENV") == "development" else "https"
    SUPERSET_WEBSERVER_PORT = 8088

SUPERSET_URL = "{protocol}://{domainName}:{port}".format(
    protocol=SUPERSET_WEBSERVER_PROTOCOL, 
    domainName=SUPERSET_WEBSERVER_DOMAINS[0], 
    port=str(SUPERSET_WEBSERVER_PORT)
)
)


# This is an important setting, and should be lower than your
# [load balancer / proxy / envoy / kong / ...] timeout settings.
# You should also make sure to configure your WSGI server
# (gunicorn, nginx, apache, ...) timeout setting to be <= to this setting
SUPERSET_WEBSERVER_TIMEOUT = int(timedelta(minutes=4).total_seconds())

# ----------------------------------------------------------------------------------
# Superset specific config
# ----------------------------------------------------------------------------------
# Superset default Home URL - Dashboards list
class SupersetDashboardIndexView(IndexView):
    # Set default URL
    @expose("/redirect_dashboard_1/")
    @expose("/superset/welcome/")
    @expose("/")
    def index(self) -> FlaskResponse:
        redirect_url = None
        if "/redirect_dashboard_1/" in request.path: 
            # print('Try redirect to DASHBOARD - redirect_dashboard_1 ===============================================')
            if requests.get(f'{SUPERSET_URL}/superset/dashboard/1/').status_code == 200:
                redirect_url = "/superset/dashboard/1/"
        if redirect_url is None: redirect_url = "/dashboard/list/"
        return redirect(redirect_url)

   
FAB_INDEX_VIEW = f"{SupersetDashboardIndexView.__module__}.{SupersetDashboardIndexView.__name__}"
