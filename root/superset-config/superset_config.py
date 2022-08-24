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

# Multiple favicons can be specified here. The "href" property
# is mandatory, but "sizes," "type," and "rel" are optional.
# For example:
# {
#     "href":path/to/image.png",
#     "sizes": "16x16",
#     "type": "image/png"
#     "rel": "icon"
# },
FAVICONS = [{"href": "/static/assets/images/logo_brand.ico"}]

SECRET_KEY = f"\2\{os.getenv('SUPERSET_APP_SECRET_KEY', 'ASfdsdge3323radfgasE@@54236TRFG')}\1\2\e\y\y\h"

# The SQLAlchemy connection string.
#SQLALCHEMY_DATABASE_URI = "sqlite:///path to ...www/superset/superset.db"
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{PROD_DB_USER}:{PROD_DB_PASS}@{PROD_DB_HOST}:{PROD_DB_PORT}/{PROD_DB_DBNAME}?options=-c search_path={PROD_DB_SHEMA}".format(
    PROD_DB_USER=os.getenv('PROD_DB_USER'),
    PROD_DB_PASS=os.getenv('PROD_DB_PASS'),
    PROD_DB_HOST=os.getenv('PROD_DB_HOST'),
    PROD_DB_PORT=os.getenv('PROD_DB_PORT'),
    PROD_DB_DBNAME=os.getenv('PROD_DB_DBNAME'),
    PROD_DB_SHEMA=os.getenv('PROD_DB_SHEMA')
    )

SQLALCHEMY_EXAMPLES_URI = "postgresql+psycopg2://{PROD_USERS_DASHBOARDS_DB_1_USER}:{PROD_USERS_DASHBOARDS_DB_1_PASS}@{PROD_USERS_DASHBOARDS_DB_1_HOST}:{PROD_USERS_DASHBOARDS_DB_1_PORT}/{PROD_USERS_DASHBOARDS_DB_1_DBNAME}?options=-c search_path={PROD_USERS_DASHBOARDS_DB_1_SHEMA}".format(
    PROD_USERS_DASHBOARDS_DB_1_USER=os.getenv('PROD_USERS_DASHBOARDS_DB_1_USER'),
    PROD_USERS_DASHBOARDS_DB_1_PASS=os.getenv('PROD_USERS_DASHBOARDS_DB_1_PASS'),
    PROD_USERS_DASHBOARDS_DB_1_HOST=os.getenv('PROD_USERS_DASHBOARDS_DB_1_HOST'),
    PROD_USERS_DASHBOARDS_DB_1_PORT=os.getenv('PROD_USERS_DASHBOARDS_DB_1_PORT'),
    PROD_USERS_DASHBOARDS_DB_1_DBNAME=os.getenv('PROD_USERS_DASHBOARDS_DB_1_DBNAME'),
    PROD_USERS_DASHBOARDS_DB_1_SHEMA=os.getenv('PROD_USERS_DASHBOARDS_DB_1_SHEMA')
)

# Enable profiling of Python calls. Turn this on and append ``?_instrument=1``
# to the page to see the call stack.
PROFILING = os.environ.get("FLASK_ENV") == "development"
# ----------------------------------------------------------------------------------
# GLOBALS FOR APP Builder
# ----------------------------------------------------------------------------------
# Uncomment to setup Your App name
APP_NAME = "Brand text"

# Specify the App icon
APP_ICON = "/static/assets/images/brand_icon.svg"


# Specify where clicking the logo would take the user
# e.g. setting it to '/' would take the user to '/superset/welcome/'
LOGO_TARGET_PATH = SUPERSET_URL + '/dashboard/list'

# Specify tooltip that should appear when hovering over the App Icon/Logo
LOGO_TOOLTIP = "Поддержка/информация: support@email.ru"

# Specify any text that should appear to the right of the logo
LOGO_RIGHT_TEXT: Union[Callable[[], str], str] = 'Main page brand name text' 

# ----------------------------------------------------------------------------------
# Modules, datasources and middleware to be registered
# ----------------------------------------------------------------------------------
class RemoteUserMiddleware(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        # REQUEST_REMOTE_USER = environ.pop('HTTP_PROXY_REMOTE_USER', None)
        # environ['REMOTE_USER'] = REQUEST_REMOTE_USER
        REQUEST_REMOTE_USER = environ.get('REMOTE_USER', None)
        # if REQUEST_REMOTE_USER is not None:
        #     os.system(f'echo REMOTE USER: +++ {str(REQUEST_REMOTE_USER)} > {CONFIG_ROOT_DIR}\\REQUEST_REMOTE_USER_1.txt')
        # else:
        #     os.system(f'echo REMOTE USER: --- {str(REQUEST_REMOTE_USER)} > {CONFIG_ROOT_DIR}\\REQUEST_REMOTE_USER_0.txt')

        # REQUEST_REMOTE_USER_MAIN_ROLE = environ.get('REQUEST_REMOTE_USER_MAIN_ROLE', None)
        return self.app(environ, start_response)

ADDITIONAL_MIDDLEWARE = [RemoteUserMiddleware, ]

# ----------------------------------------------------------------------------------
# AUTHENTICATION CONFIG
# ----------------------------------------------------------------------------------
# The authentication type
# AUTH_OID : Is for OpenID
# AUTH_DB : Is for database (username/password)
# AUTH_LDAP : Is for LDAP
# AUTH_REMOTE_USER : Is for using REQUEST_REMOTE_USER from web server
AUTH_TYPE = AUTH_DB
#AUTH_TYPE = AUTH_REMOTE_USER
#AUTH_TYPE = AUTH_LDAP

# Uncomment to setup Full admin role name
AUTH_ROLE_ADMIN = 'Admin'

# Uncomment to setup Public role name, no authentication needed
# AUTH_ROLE_PUBLIC = 'Public'

# Will allow user self registration
AUTH_USER_REGISTRATION = False

# The default user self registration role
AUTH_USER_REGISTRATION_ROLE = "Dashboards_Reader"

# When using LDAP Auth, setup the LDAP server
AUTH_LDAP_SERVER = f"ldap://{os.getenv('LDAP_url', '')}"
AUTH_LDAP_SEARCH = f"DC={os.getenv('LDAP_dc1', '')},DC={os.getenv('LDAP_dc2', '')},DC={os.getenv('LDAP_dc3', '')}"
AUTH_LDAP_APPEND_DOMAIN = os.getenv('LDAP_domain', '')

AUTH_LDAP_BIND_USER = os.getenv('LDAP_user')
AUTH_LDAP_BIND_PASSWORD = os.getenv('LDAP_password')

AUTH_LDAP_UID_FIELD = "sAMAccountName"
AUTH_LDAP_FIRSTNAME_FIELD = "givenName"
AUTH_LDAP_LASTNAME_FIELD = "sn"
AUTH_LDAP_EMAIL_FIELD = "mail"
AUTH_LDAP_USE_TLS = False
AUTH_LDAP_ALLOW_SELF_SIGNED = False

# Init db connetion before start init CustomSecurityManager
def init_db_connection():
    engine = conn = metadata = None
    if os.getenv('db_connection_exists', '0') == '0':
        os.environ["db_connection_exists"] = '1'
        dsnStr = cx_Oracle.makedsn(os.getenv('PROD_USERS_DASHBOARDS_DB_3_HOST'), os.getenv('PROD_USERS_DASHBOARDS_DB_3_PORT'), os.getenv('PROD_USERS_DASHBOARDS_DB_3_DBNAME'),)
        engine_str = ("oracle+cx_oracle://{user}:{pwd}@{dsnStr}".format(user=os.getenv('PROD_USERS_DASHBOARDS_DB_3_USER'), pwd=os.getenv('PROD_USERS_DASHBOARDS_DB_3_PASS'), dsnStr=dsnStr))
        engine = create_engine(engine_str, echo=False)
        conn = engine.connect()
        metadata = MetaData(bind=conn)
    #print(engine, conn, metadata)
    return engine, conn, metadata

# Custom Auth Perms - logging
def user_logging_actions(username, status='failed'):
    with open(f'{CONFIG_ROOT_DIR}\\logs\\superset_user_log_in.txt', 'a', encoding="utf-8") as logs:
        s = f"datetime: {str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))} // username: {username} // status: {status}\n"
        logs.write(s)

# Extra Auth JWT and Ldap_Ntlm Auth extension
class ExtraAuth_JWT_and_LDAP_NTLM_MOD_WSGI_View(AuthDBView):
    @expose('/login_admin/', methods=['GET', 'POST'])
    @expose('/login/', methods=['GET', 'POST'])
    def login(self):

        if g.user is not None and g.user.is_authenticated:
            return redirect(self.appbuilder.get_url_for_index)

        if request.remote_addr == host_ip and 'login_admin' not in request.path:
            # if host in login_page
            return redirect('/login_admin/')
        # else will check remote_user in login_page if supplied

        # if 'login_admin' in request.path:
        #     if g.user is not None and g.user.is_authenticated:
        #         logout_user()
        #         return redirect('/login_admin/')
        # else:
        #     # if host in login_page
        #     if request.remote_addr == host_ip:
        #         return redirect('/login_admin/')
        #     if g.user is not None and g.user.is_authenticated:
        #         return redirect(self.appbuilder.get_url_for_index)
        
        token_user = None
        remote_user = None
        auth_user = None

        REQUEST_REMOTE_USER = request.environ.get("REMOTE_USER", None)
        if REQUEST_REMOTE_USER: remote_user = self.appbuilder.sm.find_user(REQUEST_REMOTE_USER)

        # os.system(f'echo REMOTE USER: === {str(REQUEST_REMOTE_USER)} > {CONFIG_ROOT_DIR}\\REQUEST_REMOTE_USER_2.txt')

        # extract token from url query
        next_url = request.args.get('next', None)
        if '/login/?next=' in request.url:
            next_url = unquote(request.url.split('/login/?next=', 1)[1])
            token_auth_jwt = parse_qs(urlparse(next_url).query).get('token', None)
            if token_auth_jwt: 
                token_auth_jwt = token_auth_jwt[0]
        else:
            token_auth_jwt = request.args.get('token', None)
            
        def create_access_token(payload, secret):
            token_auth_jwt = jwt.encode(payload, secret, algorithm="HS256")
            return token_auth_jwt

        def validate_access_token(self, token_auth_jwt):
            if token_auth_jwt:
                try:
                    token_auth_jwt = jwt.decode(token_auth_jwt, os.environ.get("SUPERSET_AUTH_TOKEN_SECRET"), algorithms=["HS256"])
                except Exception as e:
                    token_auth_jwt = None
                    user_logging_actions('NonValidToken', 'failed [2.6]')
                
                if token_auth_jwt:
                    username = token_auth_jwt.get('username', None)
                    token_dt = token_auth_jwt.get('token_dt', None)
                    duration_minutes = token_auth_jwt.get('duration_minutes', None)
                    
                    token_user = self.appbuilder.sm.find_user(username)

                    if token_user:
                        if token_dt and duration_minutes:
                            token_dt = datetime.strptime(token_dt, '%Y-%m-%d %H:%M:%S')
                            datetiff = (token_dt-datetime.now()).total_seconds() / 60.0
                            if abs(datetiff) > int(duration_minutes):
                                user_logging_actions(f'ExpiredToken - {username}', 'failed [2.7]')
                                token_user = None
                else:
                    token_user = None
                    user_logging_actions('NonValidToken', 'failed [2.4]')
            else:
                token_user = None
                #user_logging_actions('NotExistsToken', 'failed [2.5]')
            return token_user

        if token_auth_jwt:
            token_user = validate_access_token(self, token_auth_jwt = token_auth_jwt)
            token_auth_init_jwt = create_access_token(
                payload={"username": "login", "token_dt": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), "duration_minutes": "5"},
                secret=os.environ.get("SUPERSET_AUTH_TOKEN_SECRET")
            )
            # print(token_user, "token_auth_init_jwt =============== ", token_auth_init_jwt)
            # print(token_user, "token_auth_jwt =============== ", token_auth_jwt)

        if remote_user:
            user_logging_actions(f'AccessViaRemoteUser - {remote_user.username}', 'success [2.4]')
            auth_user = remote_user
        elif token_user:
            user_logging_actions(f'AccessViaToken - {token_user.username}', 'success [2.4]')
            auth_user = token_user

        if auth_user:
            if auth_user.last_login is None:
                # update LDAP and DB user roles if user first login
                auth_user.changed_on = datetime.now()
                self.appbuilder.sm.update_user(auth_user)
                self.appbuilder.sm.auth_user_db(auth_user.username, os.getenv('SUPERSET_ADMIN_PASSWORD'))
            elif auth_user.changed_on is None:
                auth_user.changed_on = datetime.now()
                auth_user.changed_by_fk = 1
                self.appbuilder.sm.update_user(auth_user)
            elif auth_user.changed_on is not None and abs((auth_user.changed_on - datetime.now()).days) > 2:
                # update LDAP and DB user roles if user have old data more than 3 days
                auth_user.changed_on = datetime.now()
                auth_user.changed_by_fk = 1
                self.appbuilder.sm.update_user(auth_user)
                self.appbuilder.sm.auth_user_db(auth_user.username, os.getenv('SUPERSET_ADMIN_PASSWORD'))
            login_user(auth_user, remember=False)
            return redirect(request.args.get("next") or '/dashboard/list')
        else:
            # flash('Попытка авторизации не удалась.', 'warning')
            # return redirect('/401')
            return super(ExtraAuth_JWT_and_LDAP_NTLM_MOD_WSGI_View, self).login()



# Extra Ldap_Ntlm Auth extension
class ExtraAuth_LDAP_NTLM_View(AuthRemoteUserView):
    login_template = ""

    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
        REQUEST_REMOTE_USER = request.environ.get("REMOTE_USER", None)
        
        if g.user is not None and g.user.is_authenticated:
            return redirect(self.appbuilder.get_url_for_index)
        if username:
            user = self.appbuilder.sm.auth_user_remote_user(username)
            if user is None:
                flash(as_unicode(self.invalid_login_message), "warning")
            else:
                login_user(user)
        else:
            flash(as_unicode(self.invalid_login_message), "warning")
        return redirect(self.appbuilder.get_url_for_index)


# Custom Auth Perms
class CustomSecurityManager(SupersetSecurityManager):
    db_engine = db_conn = db_metadata = None
    authdbview = ExtraAuth_JWT_and_LDAP_NTLM_MOD_WSGI_View
    authremoteuserview = ExtraAuth_LDAP_NTLM_View
    
    def __init__(self, appbuilder):
        super(CustomSecurityManager, self).__init__(appbuilder)

    def auth_user_db(self, username, password):
        """
        Method for authenticating user, auth db style

        :param username:
            The username or registered email address
        :param password:
            The password, will be tested against hashed password on db
        """        
        # ldap_methods
        def valid_username(input_string=str):
            import re
            output = input_string, False
            if re.match("^[A-Za-z0-9_-]*$", input_string):
                output = input_string, True
            return output

        def ldap_open_connetion(LDAP_url, LDAP_domain, LDAP_user, LDAP_password):
            server = Server(f'ldap://{LDAP_url}', use_ssl=True, get_info=ALL)
            conn = Connection(server,
                check_names=False, 
                auto_bind=False,
                user=f"{LDAP_domain}\\{LDAP_user}",
                password=f"{LDAP_password}", 
                authentication="NTLM")
            conn.open()
            return conn

        def auth_ldap(Search_user, LDAP_user, LDAP_password, LDAP_url=os.getenv('LDAP_url'), LDAP_domain=os.getenv('LDAP_domain'), LDAP_dc1=os.getenv('LDAP_dc1'), LDAP_dc2=os.getenv('LDAP_dc2'), LDAP_dc3=os.getenv('LDAP_dc3')):
            ldap_user_data = {'username': Search_user, 'is_active': True, 'is_logged': False, 'details': {}}
            
            conn = ldap_open_connetion(LDAP_url=LDAP_url, LDAP_domain=LDAP_domain, LDAP_user=LDAP_user, LDAP_password=LDAP_password)
            conn.bind()
            if conn.bind():
                conn.search(
                    f"DC={LDAP_dc1},DC={LDAP_dc2},DC={LDAP_dc3}", 
                    f"(&(objectClass=user)(sAMAccountName={Search_user}))", 
                    SUBTREE, 
                    attributes=[
                        'sAMAccountName', 
                        'memberOF',
                    ]
                )
                user_details = {}
                for i in conn.entries:
                    ldap_user_data['details']['Groups'] = ['LDAP_'+i.split(',')[0][3:] for i in i.memberOF.values]
                    if i.userAccountControl.values[0] not in ['512']: # ['512', '544', '66048', '66080']:
                        ldap_user_data['is_active'] = False
                
                conn.unbind()
                #ldap_user_data['is_active'] = is_active
                ldap_user_data['is_logged'] = True
            else:
                ldap_user_data['is_logged'] = False

            return ldap_user_data



        # auth validate username
        if not isinstance(username, str):
            user_logging_actions('NonValidName', 'failed [1.1]')
            return None
        if not valid_username(input_string=username)[1]:
            user_logging_actions('NonValidName', 'failed [1.2]')
            return None
        if len(username) < 4:
            user_logging_actions('NonValidName', 'failed [1.3]')
            return None
        if username is None or username == "":
            user_logging_actions('NonValidName', 'failed [1.4]')
            return None
        
        # auth process username
        first_user = self.get_first_user()
        user = self.find_user(username=username)
        
        # for admin
        if username.lower() == 'admin':
            if password == os.getenv('SUPERSET_ADMIN_PASSWORD', f'AW{random.choice(string.ascii_letters)}qewf{random.randrange(100, 10000)}rsad*{random.randrange(1, 1000)}gsg{random.choice(string.ascii_letters)}bndvb*#{random.randrange(33, 55)}a{random.choice(string.ascii_letters)}'):
                self.update_user_auth_stat(user, True)
                user_logging_actions('admin', 'success [2.1]')
                return user
            else:
                user_logging_actions(username, 'failed [2.1]')
                return None
        else:
            # for LDAP users
            if password == os.getenv('SUPERSET_ADMIN_PASSWORD', f'AW{random.choice(string.ascii_letters)}qewf{random.randrange(100, 10000)}rsad*{random.randrange(1, 1000)}gsg{random.choice(string.ascii_letters)}bndvb*#{random.randrange(33, 55)}a{random.choice(string.ascii_letters)}'):
                ldap_user_data = auth_ldap(Search_user=username, LDAP_user=os.getenv('LDAP_user'), LDAP_password=os.getenv('LDAP_password'))
            else:
                ldap_user_data = auth_ldap(Search_user=username, LDAP_user=username, LDAP_password=password)
            if ldap_user_data.get('is_logged', False) == True:
                # create user if not exists
                if not user:
                    role_admin = self.appbuilder.sm.find_role('Dashboards_Reader')
                    user = self.add_user(
                        username=username,
                        first_name=username,
                        last_name=username,
                        email=f"{username}@{os.getenv('LDAP_dc2', 'superset')}.{os.getenv('LDAP_dc3', 'com')}",
                        role=self.appbuilder.sm.find_role('Dashboards_Reader'),
                    )
                    user.active = False
                    self.appbuilder.sm.update_user(user)
                    logger.debug("New user registered: {0}".format(user))
                    user_logging_actions(username, f'New user registered. is_active: {user.is_active}')
                    
                    #If user registration failed, go away
                    if not user:
                        logger.info(LOGMSG_ERR_SEC_ADD_REGISTER_USER.format(username))
                        return None
                # init db engine
                if not self.db_engine:
                    self.db_engine, self.db_conn, self.db_metadata = init_db_connection()

                #If user disabled, go away 
                if not user.is_active:
                    user_logging_actions(username, 'failed [1.5]')
                    return None

                # enrich roles of LDAP by db
                if self.db_engine:
                    Session = sessionmaker(self.db_engine)
                    session_1 = Session()

                    results = 0
                    try:
                        sql = "select 1 from dual"
                        results = self.db_conn.execute(sql)
                    except Exception as e:
                        user_logging_actions(username, f'db - test connection error. {str(e)}')
                    else:
                        try:
                            if results.scalar() > 0:
                                results = 0
                                sql = f"""select 1 as col1 from dual"""
                                results = self.db_conn.execute(sql)
                        except Exception as e:
                            user_logging_actions(username, f'db - cannot get user roles. {str(e)}')
                        else:
                            #if results.scalar() > 0:
                            user_db_data = [{column: value for column, value in rowproxy.items()} for rowproxy in results]
                            if len(user_db_data) > 0: 
                                user_db_data_clean = [i.get("role") for i in user_db_data]
                                ldap_user_data['details']['Groups'] = ldap_user_data.get('details').get('Groups') + user_db_data_clean
                    finally: 
                        session_1.close()
                
                # set LDAP and DB superset roles
                for role_name in ldap_user_data.get('details').get('Groups'):
                    role_object = self.appbuilder.sm.find_role(role_name)
                    if not role_object: self.appbuilder.sm.add_role(role_name)

                # set LDAP and DB user roles
                current_user_role_names = [r.name for r in user.roles]
                for role_name in ldap_user_data.get('details').get('Groups'):
                    if role_name not in current_user_role_names:
                        role_object = self.appbuilder.sm.find_role(role_name)
                        try:
                            user.roles.append(role_object)
                        except Exception as e:
                            pass
                # remove non-exists LDAP and DB user roles
                for role_name in current_user_role_names:
                    if ('LDAP_' in role_name or 'DB_' in role_name) and role_name not in ldap_user_data.get('details').get('Groups'):
                        user.roles.remove(self.appbuilder.sm.find_role(role_name))
                
                # Update user attributes
                user.first_name = ldap_user_data.get('details').get('FirstName')
                user.last_name = ldap_user_data.get('details').get('LastName')
                user.email = ldap_user_data.get('details').get('Email')
                self.appbuilder.sm.update_user(user)
                self.update_user_auth_stat(user, True)
                user_logging_actions(username, 'success [2.2]')
                return user          
            # for DB users
            #elif check_password_hash(user.password, password):
            #    self.update_user_auth_stat(user, True)
            #    user_logging_actions(username, 'success [2.3]')
            #    return user
            else:
                #if auth failed
                logger.info(LOGMSG_WAR_SEC_LOGIN_FAILED.format(username))
                user_logging_actions(username, 'failed [2.3]')
                return None
                #self.update_user_auth_stat(user, False)
                #logger.info(LOGMSG_WAR_SEC_LOGIN_FAILED.format(username))
                #user_logging_actions(username, 'failed [2.3]')
                #return None

CUSTOM_SECURITY_MANAGER = CustomSecurityManager
# ----------------------------------------------------------------------------------
# Roles config
# ----------------------------------------------------------------------------------
# Setup default language
BABEL_DEFAULT_LOCALE = "ru"
# Your application default translation path
BABEL_DEFAULT_FOLDER = "superset/translations"
# The allowed translation for you app
LANGUAGES = {
    "ru": {"flag": "ru", "name": "Russian"},
    "en": {"flag": "us", "name": "English"},
    "es": {"flag": "es", "name": "Spanish"},
    "it": {"flag": "it", "name": "Italian"},
    "fr": {"flag": "fr", "name": "French"},
    "zh": {"flag": "cn", "name": "Chinese"},
    "ja": {"flag": "jp", "name": "Japanese"},
    "de": {"flag": "de", "name": "German"},
    "pt": {"flag": "pt", "name": "Portuguese"},
    "pt_BR": {"flag": "br", "name": "Brazilian Portuguese"},
    "ko": {"flag": "kr", "name": "Korean"},
    "sk": {"flag": "sk", "name": "Slovak"},
    "sl": {"flag": "si", "name": "Slovenian"},
    "nl": {"flag": "nl", "name": "Dutch"},
}

# ---------------------------------------------------
# Feature flags
# ---------------------------------------------------
# Feature flags that are set by default go here. Their values can be
# overwritten by those specified under FEATURE_FLAGS in superset_config.py
# For example, DEFAULT_FEATURE_FLAGS = { 'FOO': True, 'BAR': False } here
# and FEATURE_FLAGS = { 'BAR': True, 'BAZ': True } in superset_config.py
# will result in combined feature flags of { 'FOO': True, 'BAR': True, 'BAZ': True }

DEFAULT_FEATURE_FLAGS: Dict[str, bool] = {
    # allow dashboard to use sub-domains to send chart request
    # you also need ENABLE_CORS and
    # SUPERSET_WEBSERVER_DOMAINS for list of domains
    "ALLOW_DASHBOARD_DOMAIN_SHARDING": True,
    # Experimental feature introducing a client (browser) cache
    "CLIENT_CACHE": False,
    "DISABLE_DATASET_SOURCE_EDIT": False,
    # When using a recent version of Druid that supports JOINs turn this on
    "DRUID_JOINS": False,
    "DYNAMIC_PLUGINS": False,
    # With Superset 2.0, we are updating the default so that the legacy datasource
    # editor no longer shows. Currently this is set to false so that the editor
    # option does show, but we will be depreciating it.
    "DISABLE_LEGACY_DATASOURCE_EDITOR": True,
    # For some security concerns, you may need to enforce CSRF protection on
    # all query request to explore_json endpoint. In Superset, we use
    # `flask-csrf <https://sjl.bitbucket.io/flask-csrf/>`_ add csrf protection
    # for all POST requests, but this protection doesn't apply to GET method.
    # When ENABLE_EXPLORE_JSON_CSRF_PROTECTION is set to true, your users cannot
    # make GET request to explore_json. explore_json accepts both GET and POST request.
    # See `PR 7935 <https://github.com/apache/superset/pull/7935>`_ for more details.
    "ENABLE_EXPLORE_JSON_CSRF_PROTECTION": False,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "ENABLE_TEMPLATE_REMOVE_FILTERS": False,
    # Allow for javascript controls components
    # this enables programmers to customize certain charts (like the
    # geospatial ones) by inputing javascript in controls. This exposes
    # an XSS security vulnerability
    "ENABLE_JAVASCRIPT_CONTROLS": True,
    "KV_STORE": False,
    # When this feature is enabled, nested types in Presto will be
    # expanded into extra columns and/or arrays. This is experimental,
    # and doesn't work with all nested types.
    "PRESTO_EXPAND_DATA": False,
    # Exposes API endpoint to compute thumbnails
    "THUMBNAILS": True,
    "DASHBOARD_CACHE": False,
    "REMOVE_SLICE_LEVEL_LABEL_COLORS": False,
    "SHARE_QUERIES_VIA_KV_STORE": False,
    "TAGGING_SYSTEM": False,
    "SQLLAB_BACKEND_PERSISTENCE": True,
    "LISTVIEWS_DEFAULT_CARD_VIEW": True,
    # When True, this flag allows display of HTML tags in Markdown components
    "DISPLAY_MARKDOWN_HTML": True,
    # When True, this escapes HTML (rather than rendering it) in Markdown components
    "ESCAPE_MARKDOWN_HTML": False,
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CROSS_FILTERS": True,
    # Feature is under active development and breaking changes are expected
    "DASHBOARD_NATIVE_FILTERS_SET": True,
    "DASHBOARD_FILTERS_EXPERIMENTAL": True,
    "GLOBAL_ASYNC_QUERIES": False,
    "VERSIONED_EXPORT": True,
    "EMBEDDED_SUPERSET": False,
    # Enables Alerts and reports new implementation
    "ALERT_REPORTS": True,
    "DASHBOARD_RBAC": True,
    "ENABLE_EXPLORE_DRAG_AND_DROP": False,
    "ENABLE_FILTER_BOX_MIGRATION": False,
    "ENABLE_ADVANCED_DATA_TYPES": False,
    "ENABLE_DND_WITH_CLICK_UX": False,
    # Enabling ALERTS_ATTACH_REPORTS, the system sends email and slack message
    # with screenshot and link
    # Disables ALERTS_ATTACH_REPORTS, the system DOES NOT generate screenshot
    # for report with type 'alert' and sends email and slack message with only link;
    # for report with type 'report' still send with email and slack message with
    # screenshot and link
    "ALERTS_ATTACH_REPORTS": True,
    # FORCE_DATABASE_CONNECTIONS_SSL is depreciated.
    "FORCE_DATABASE_CONNECTIONS_SSL": False,
    # Enabling ENFORCE_DB_ENCRYPTION_UI forces all database connections to be
    # encrypted before being saved into superset metastore.
    "ENFORCE_DB_ENCRYPTION_UI": False,
    # Allow users to export full CSV of table viz type.
    # This could cause the server to run out of memory or compute.
    "ALLOW_FULL_CSV_EXPORT": False,
    "UX_BETA": False,
    "GENERIC_CHART_AXES": False,
    "ALLOW_ADHOC_SUBQUERY": False,
    # Apply RLS rules to SQL Lab queries. This requires parsing and manipulating the
    # query, and might break queries and/or allow users to bypass RLS. Use with care!
    "RLS_IN_SQLLAB": False,
}

# EXTRA_CATEGORICAL_COLOR_SCHEMES is used for adding custom categorical color schemes
# example code for "My custom warm to hot" color scheme
EXTRA_CATEGORICAL_COLOR_SCHEMES = [
    {
        "id": 'Test_VisualizationColors_1',
        "description": '',
        "label": 'Test Visualization Colors 1',
        "isDefault": True,
        "colors": [
            '#006699', '#009DD9', '#5AAA46', '#44AAAA', '#DDAA77', '#7799BB', '#88AA77',
            '#552288', '#5AAA46', '#CC7788', '#EEDD55', '#9977BB', '#BBAA44', '#DDCCDD'
        ]
    }]

# This is merely a default.
FEATURE_FLAGS = {"ALERT_REPORTS": True}
# ----------------------------------------------------------------------------------
# Thumbnail config (behind feature flag)
# Also used by Alerts & Reports
# ----------------------------------------------------------------------------------
THUMBNAIL_SELENIUM_USER = "admin"
THUMBNAIL_CACHE_CONFIG: CacheConfig = {
    "CACHE_TYPE": "NullCache",
    "CACHE_NO_NULL_WARNING": True,
}

# Time before selenium times out after trying to locate an element on the page and wait
# for that element to load for a screenshot.
SCREENSHOT_LOCATE_WAIT = int(timedelta(seconds=10).total_seconds())
# Time before selenium times out after waiting for all DOM class elements named
# "loading" are gone.
SCREENSHOT_LOAD_WAIT = int(timedelta(minutes=1).total_seconds())
# Selenium destroy retries
SCREENSHOT_SELENIUM_RETRIES = 5
# Give selenium an headstart, in seconds
SCREENSHOT_SELENIUM_HEADSTART = 3
# Wait for the chart animation, in seconds
SCREENSHOT_SELENIUM_ANIMATION_WAIT = 5


# ----------------------------------------------------------------------------------
# Image and file configuration
# ----------------------------------------------------------------------------------
# The file upload folder, when using models with files
#UPLOAD_FOLDER = "path to ...www/superset/superset_config/uploads"
UPLOAD_FOLDER = CONFIG_ROOT_DIR + "/uploads"
UPLOAD_CHUNK_SIZE = 4096

# The image upload folder, when using models with images
#IMG_UPLOAD_FOLDER = "path to .../www/superset/superset_config/uploads"
IMG_UPLOAD_FOLDER = CONFIG_ROOT_DIR + "/uploads"

# Setup image size default is (300, 200, True)
# IMG_SIZE = (300, 200, True)

#Metadata Caching
CACHE_CONFIG: CacheConfig = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 900, #900 sec #24*60*60, # 1 day
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_URL': 'redis://%s:%s/1' % (REDIS_HOST, REDIS_PORT)
}

#Caching the Data from the Database shown in the Dashboards
DATA_CACHE_CONFIG: CacheConfig = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 900, #900 sec #24*60*60, # 1 day
    'CACHE_KEY_PREFIX': 'data_',
    'CACHE_REDIS_URL': 'redis://%s:%s/1' % (REDIS_HOST, REDIS_PORT)
}

#Cache for filters state
FILTER_STATE_CACHE_CONFIG: CacheConfig = {
    "CACHE_TYPE": "redis",
    'CACHE_DEFAULT_TIMEOUT': 900, #900 sec #24*60*60, # 1 day
    'CACHE_KEY_PREFIX': 'filter_',
    "CACHE_THRESHOLD": 0,
    "REFRESH_TIMEOUT_ON_RETRIEVAL": True,
    'CACHE_REDIS_URL': 'redis://%s:%s/1' % (REDIS_HOST, REDIS_PORT)

}

#Cache for chart form data
EXPLORE_FORM_DATA_CACHE_CONFIG: CacheConfig = {
    "CACHE_TYPE": "redis",
    'CACHE_DEFAULT_TIMEOUT': 900, #900 sec #24*60*60, # 1 day
    'CACHE_KEY_PREFIX': 'Chart_',
    "CACHE_THRESHOLD": 0,
    "REFRESH_TIMEOUT_ON_RETRIEVAL": True,
    'CACHE_REDIS_URL': 'redis://%s:%s/1' % (REDIS_HOST, REDIS_PORT)

}

#Cache for thumbnail
THUMBNAIL_CACHE_CONFIG: CacheConfig = {
    "CACHE_TYPE": "redis",
    'CACHE_DEFAULT_TIMEOUT': 24*60*60, # 1 day
    'CACHE_KEY_PREFIX': 'thumbnail_',
    'CACHE_NO_NULL_WARNING': True,
    'CACHE_REDIS_URL': 'redis://%s:%s/1' % (REDIS_HOST, REDIS_PORT)
}

#Caches the top 5 Dashboards at 6:30 am
CELERYBEAT_SCHEDULE = {
    'cache-warmup-hourly': {
        'task': 'cache-warmup',
        'schedule': crontab(minute=30, hour='6'),  
        'kwargs': {
            'strategy_name': 'top_n_dashboards',
            'top_n': 5,
            'since': '7 days ago',
        },
    },
}

# Allowed format types for upload on Database view
EXCEL_EXTENSIONS = {"xlsx", "xls"}
CSV_EXTENSIONS = {"csv", "tsv", "txt"}
COLUMNAR_EXTENSIONS = {"parquet", "zip"}
ALLOWED_EXTENSIONS = {*EXCEL_EXTENSIONS}

# CSV Options: key/value pairs that will be passed as argument to DataFrame.to_csv
# method.
# note: index option should not be overridden
CSV_EXPORT = {
    #"encoding": "utf-8"
    "encoding": "utf_8_sig"
}


# ----------------------------------------------------------------------------------
# Time grain configurations
# ----------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
# List of viz_types not allowed in your environment
# For example: Disable pivot table and treemap:
#  VIZ_TYPE_DENYLIST = ['pivot_table', 'treemap']
# ----------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
# List of data sources not to be refreshed in druid cluster
# ----------------------------------------------------------------------------------


# Console Log Settings

LOG_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
LOG_LEVEL = "DEBUG"

# ---------------------------------------------------
# Enable Time Rotate Log Handler
# ---------------------------------------------------
# LOG_LEVEL = DEBUG, INFO, WARNING, ERROR, CRITICAL
if os.environ.get("SUPERSET_LAUNCH_MODE") == "THUMBNAILS":
    ENABLE_TIME_ROTATE = True
    FILENAME = (os.path.join(CONFIG_ROOT_DIR, "logs/superset_thumbnails.log")).replace('\\', '/')
    ROLLOVER = "midnight"
    INTERVAL = 1
    BACKUP_COUNT = 7
else:
    ENABLE_TIME_ROTATE = True
    FILENAME = (os.path.join(CONFIG_ROOT_DIR, "logs/superset.log")).replace('\\', '/')
    ROLLOVER = "midnight"
    INTERVAL = 1
    BACKUP_COUNT = 7

# Maximum number of rows returned for any analytical database query
SQL_MAX_ROW = 100000

# Maximum number of rows displayed in SQL Lab UI
# Is set to avoid out of memory/localstorage issues in browsers. Does not affect
# exported CSVs
DISPLAY_MAX_ROW = 5000

# Default row limit for SQL Lab queries. Is overridden by setting a new limit in
# the SQL Lab UI
#DEFAULT_SQLLAB_LIMIT = 100 # SOMEWHERE ONE ADD LIMIT TO SQL QUERY !!!!

# Maximum number of tables/views displayed in the dropdown window in SQL Lab.
MAX_TABLE_NAMES = 50

# Data and Metadata Caching uses a REDIS in memory server (needs to be installed and run on the machine)

# Default celery config is to use SQLA as a broker, in a production setting
# you'll want to use a proper broker as specified here:
# http://docs.celeryproject.org/en/latest/getting-started/brokers/index.html

class CeleryConfig:
    broker_url = 'redis://%s:%s/0' % (REDIS_HOST, REDIS_PORT)
    imports = ('superset.sql_lab', "superset.tasks", "superset.tasks.thumbnails", )
    result_backend = 'redis://%s:%s/0' % (REDIS_HOST, REDIS_PORT)
    worker_log_level = 'DEBUG'
    worker_prefetch_multiplier = 3
    task_acks_late = False
    task_annotations = {
        'sql_lab.get_sql_results': {
            'rate_limit': '100/s',
        },
        'email_reports.send': {
            'rate_limit': '1/s',
            'time_limit': int(timedelta(seconds=120).total_seconds()),
            #'soft_time_limit': 150,
            'ignore_result': True,
        },
    }
    beat_schedule = {
        'email_reports.schedule_hourly': {
            'task': 'email_reports.schedule_hourly',
            'schedule': crontab(minute=1, hour='*'),
        },
        'reports.scheduler': {
            'task': 'reports.scheduler',
            'schedule': crontab(minute='*', hour='*'),
        },
        'reports.prune_log': {
            'task': 'reports.prune_log',
            'schedule': crontab(minute=0, hour=0),
        },
    }

CELERY_CONFIG = CeleryConfig  # pylint: disable=invalid-name

# Set celery config to None to disable all the above configuration
# CELERY_CONFIG = None

# Additional static HTTP headers to be served by your Superset server. Note
# Flask-Talisman applies the relevant security HTTP headers.
#
# DEFAULT_HTTP_HEADERS: sets default values for HTTP headers. These may be overridden
# within the app
# OVERRIDE_HTTP_HEADERS: sets override values for HTTP headers. These values will
# override anything set within the app
HTTP_HEADERS = {'X-Frame-Options': f'ALLOW-FROM {SUPERSET_URL}'}

# Timeout duration for SQL Lab synchronous queries
SQLLAB_TIMEOUT = int(timedelta(seconds=300).total_seconds())

# The MAX duration a query can run for before being killed by celery.
SQLLAB_ASYNC_TIME_LIMIT_SEC = int(timedelta(minutes=7).total_seconds())

# Flag that controls if limit should be enforced on the CTA (create table as queries).
SQLLAB_CTAS_NO_LIMIT = True

# Session life time limit
def make_session_permanent():
    # print('RRRRRRRRRRRRRRRRRRRRRRRRRRR', session, os.environ.get('REQUEST_URI'))
    '''
    Enable maxAge for the cookie 'session'
    '''
    session.permanent = True

# Set up max age of session to 1 hours
PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

# If a callable is specified, it will be called at app startup while passing
# a reference to the Flask app. This can be used to alter the Flask app
# in whatever way.
# example: FLASK_APP_MUTATOR = lambda x: x.before_request = f
def FLASK_APP_MUTATOR(app: Flask) -> None:
    app.before_request_funcs.setdefault(None, []).append(make_session_permanent)

    from flask import redirect, url_for
    from flask_login import login_user, current_user, logout_user, login_required

    #@app.login_manager.user_loader # Here your app is already created and configured with login manager
    #def load_user(id):
    #    #Get your user from the database or where ever you are storing your user information and construct the user object to return
    #    print(id, 'RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR')
    
    @app.before_request
    def beforerequest():
        #print("before_request!", current_user.is_anonymous)
        #print("before_request!", dir(current_user))

        if ('/chart/list/' in request.path or '/superset/explore/' in request.path) and SUPERSET_URL[:-1] in request.root_url:
            if current_user.is_active == True:
                # print(request, 'QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ', dir(current_user))
                for i in current_user.roles:
                    if i.name == 'Dashboards_Reader':
                        # print(i.name, type(i), i.name == 'Dashboards_Reader')
                        # print('Dashboards_Reader' in current_user.roles)
                        # print(request.path)
                        # print(request.root_path)
                        # print(request.root_url)
                        # print(request.full_path)
                        return redirect("/dashboard/list")
        if current_user.is_anonymous == False:
            if current_user.is_active == False:
                #print("before_request!", current_user.username, current_user.is_active)
                logout_user()
                return redirect("/login")
            
    
        #if not current_user.__class__.__name__ == "LocalProxy":
        #if current_user:
        #    if not current_user.is_active:
        #        print("before_request!", current_user.username, current_user.is_active)
        #print("before_request!", app.appbuilder.sm.get_all_users())
     
    @app.after_request
    def afterrequest(response):
        #print("after_request is running!")
        return response

# The link to a page containing common errors and their resolutions
# It will be appended at the bottom of sql_lab errors.
TROUBLESHOOTING_LINK = SUPERSET_URL + "/sql_lab/errors"

# CSRF token timeout, set to None for a token that never expires
WTF_CSRF_TIME_LIMIT = int(timedelta(hours=3).total_seconds())

# This link should lead to a page with instructions on how to gain access to a
# Datasource. It will be placed at the bottom of permissions errors.
PERMISSION_INSTRUCTIONS_LINK = 'https://superset_docs.ru/permissions_info'

# Blueprint views
page_401 = Blueprint('page_401', __name__, template_folder='/templates', static_folder='/static', static_url_path='/assets')
#@page_401.route('/', defaults={'page': '401'}, methods=['GET'])
@page_401.route('/401/', methods=['GET'])
def view_401():
    return render_template('superset/401.html')

page_403 = Blueprint('page_403', __name__, template_folder='/templates', static_folder='/static', static_url_path='/assets')
#@page_401.route('/', defaults={'page': '401'}, methods=['GET'])
@page_403.route('/403/', methods=['GET'])
def view_403():
    return render_template('superset/403.html')

BLUEPRINTS: List[Blueprint] = [page_401, page_403]

# The id of a template dashboard that should be copied to every new user
#DASHBOARD_TEMPLATE_ID = 3 # "Dashbord_template_main"

# Note that the returned uri and params are passed directly to sqlalchemy's
# as such `create_engine(url, **params)`
def DB_CONNECTION_MUTATOR(uri, params, username, security_manager, source):
    # user = security_manager.find_user(username=username)
    #print('DB_CONNECTION_MUTATOR: ', f'\n...user: {str(user)}', f'\n...username: {str(username)}', f'\n...uri: {str(uri)}', f'\n...params: {str(params)}', f'\n...security_manager: {str(security_manager)}')
    return uri, params

# A function that intercepts the SQL to be executed and can alter it.
# The use case is can be around adding some sort of comment header
# with information such as the username and worker node information
#
#    def SQL_QUERY_MUTATOR(sql, user_name, security_manager, database):
#        dttm = datetime.now().isoformat()
#        return f"-- [SQL LAB] {username} {dttm}\n{sql}"
def SQL_QUERY_MUTATOR(  # pylint: disable=invalid-name,unused-argument
    sql: str,
    user_name: Optional[str],
    security_manager: LocalProxy,
    database: "Database",
) -> str:
    sql_validated = sql
    #if user_name in ['admin']: return sql
     query_log_str = f"datetime: {str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))} // username: {user_name} // database: {database}"

    log_file = os.path.join(CONFIG_ROOT_DIR, "logs/superset_user_database_queries.log").replace('\\', '/')
    log_this_day_archive = log_file.replace('.log', '.'+str(datetime.now().strftime('%Y-%m-%d')+'.log'))
    
    with open(log_file, 'a', encoding="utf-8") as logs:
        logs.write(f'{query_log_str}\n{sql}\n' )
        
    if os.path.getsize(log_file) > 10000000: #10mb
        try:
            os.remove(log_this_day_archive)
        except Exception as e:
            pass
        os.rename(log_file, log_this_day_archive)
    
    return sql_validated


# ---------------------------------------------------
# Alerts & Reports
# ---------------------------------------------------
# Used for Alerts/Reports (Feature flask ALERT_REPORTS) to set the size for the
# sliding cron window size, should be synced with the celery beat config minus 1 second
ALERT_REPORTS_NOTIFICATION_DRY_RUN = True
# Any config options to be passed as-is to the webdriver
WEBDRIVER_TYPE = "chrome"#"firefox"

# Window size - this will impact the rendering of the data
WEBDRIVER_WINDOW = {
    "dashboard": (1600, 2000),
    "slice": (3000, 1200),
    "pixel_density": 1,
}

# An optional override to the default auth hook used to provide auth to the
# offline webdriver

def auth_driver(driver, user):
    # Setting cookies requires doing a request first, but /login is redirected to oauth provider, and stuck there.

    driver = webdriver.Chrome();
    driver.get(SUPERSET_URL)
    cookies = MachineAuthProvider.get_auth_cookies(user)

    for cookie_name, cookie_val in cookies.items():
        driver.add_cookie(dict(name=cookie_name, value=cookie_val))

    return driver
    
WEBDRIVER_AUTH_FUNC = auth_driver

WEBDRIVER_OPTION_ARGS = [
    "--force-device-scale-factor=2.0",
    "--high-dpi-support=2.0",
    "--headless",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-extensions",
]

WEBDRIVER_BASEURL = SUPERSET_URL
WEBDRIVER_CONFIGURATION: Dict[Any, Any] = {
    "service_log_path": (os.path.join(CONFIG_ROOT_DIR, "logs/superset_thumbnails_selenium.txt")).replace('\\', '/')
}
# they need a browser installed. Default config uses firefox
# the celery worker (asynch workers) is needed too and needs to be up and running




# Send user to a link where they can report bugs
BUG_REPORT_URL = 'https://superset_docs.ru/report_bug'# Send user to a link where they can read more about Superset
DOCUMENTATION_URL = 'https://superset_docs.ru/documentation'
DOCUMENTATION_TEXT = "Brand text documentation"
DOCUMENTATION_ICON = f'{SUPERSET_WEBSERVER_PROTOCOL}://site_name.ru:8080/doc.ico'

# A list of preferred databases, in order. These databases will be
# displayed prominently in the "Add Database" dialog. You should
# use the "engine_name" attribute of the corresponding DB engine spec
# in `superset/db_engine_specs/`.
PREFERRED_DATABASES: List[str] = [
    "PostgreSQL",
    "Oracle",
    "Microsoft SQL Server",
    # etc.
]

    
    
    
