def main(init_steps=[], init_steps_skip=[]):
    import os
    import shutil
    import platform
    from datetime import datetime

    global CONFIG_ROOT_DIR, \
        PYTHON_VENV_VER, \
        set_install_dir, \
        set_config_thumbnails_file_path, \
        venv_install, \
        venv_activate, \
        venv_install_requirements, \
        venv_install_superset, \
        npm_install_node_modules, \
        superset_init_db_upgrade, \
        superset_init_fab_create_admin, \
        superset_init, \
        service_names_list, \
        superset_init_install_win_services, \
        superset_init_load_examples, \
        superset_launch, \
        superset_thumbnails_launch

    CONFIG_ROOT_DIR = os.path.abspath(os.getcwd())
    PYTHON_VENV_VER = "3.8.0 - 3.8.9"

    try:
        from decouple import AutoConfig
    except:
        print("No module: from decouple import config. Installing ..")
        print(f"CMD execute: install {CONFIG_ROOT_DIR}/superset-config/superset_requirements/backend/python_decouple-3.4-py3-none-any.whl")
        os.system(f"pip install {CONFIG_ROOT_DIR}/superset-config/superset_requirements/backend/python_decouple-3.4-py3-none-any.whl")
        os.system(f"pip install --upgrade {CONFIG_ROOT_DIR}/superset-config/superset_requirements/backend/pip-22.0.4-py3-none-any.whl")
        os.system(f"pip install --upgrade {CONFIG_ROOT_DIR}/superset-config/superset_requirements/backend/setuptools-57.0.0-py3-none-any.whl")
        os.system(f"pip install --upgrade {CONFIG_ROOT_DIR}/superset-config/superset_requirements/backend/psutil-5.9.1-cp38-cp38-win_amd64.whl")

    config = AutoConfig(search_path=CONFIG_ROOT_DIR + '/superset-config')

    # util functions
    def cmd_execute(step, result, console_log, cmd):
        import os
        import shutil
        import platform

        if result == "OK":
            try:
                step += 1
                eval(console_log)
                if len(cmd) > 1:
                    if 'win_services_manager' in console_log:
                        _operation = None
                        _service_names_list = 'service_names_list'
                        if 'service_install' in console_log: _operation = 'service_install'
                        if 'service_start' in console_log: _operation = 'service_start'
                        if 'service_stop' in console_log: _operation = 'service_stop'
                        if 'service_remove' in console_log: _operation = 'service_remove'
                        if 'service_names_list[0:1]' in console_log: _service_names_list = 'service_names_list[0:1]'
                        if 'service_names_list[1:2]' in console_log: _service_names_list = 'service_names_list[1:2]'
                        if 'service_names_list[2:3]' in console_log: _service_names_list = 'service_names_list[2:3]'
                        if 'service_names_list[3:4]' in console_log: _service_names_list = 'service_names_list[3:4]'
                        if 'service_names_list[4:5]' in console_log: _service_names_list = 'service_names_list[4:5]'
                        [win_services_manager(operation=_operation, name=s.get('name'), args=s.get('args'), re_install=True) for s in eval(_service_names_list)]
                    else:
                        exec(cmd)
            except Exception as e:
                result = "Fail"
                print(str(e))
            finally:
                print(f".. result: {result}")
        return step, result

    # Enviroments & constants
    step = 0
    result = "OK"

    # Win services
    def win_services_manager(operation, name, args=None, re_install=False) -> int:
        import os
        import psutil

        def check_if_service_installed(name):
            try:
                service = psutil.win_service_get(name)
                service_display_name = service.as_dict().get("display_name")
            except psutil.NoSuchProcess as e:
                service_display_name = None

            return service_display_name

        def install_service(name, args=None, re_install=False):
            if check_if_service_installed(name) and re_install:
                init_service(name, "stop")
                cmd_nssm = f"{CONFIG_ROOT_DIR}\\superset-config\\nssm-2.24\\win64\\nssm.exe remove {name} confirm"
                os.system(cmd_nssm)

            if not check_if_service_installed(name):
                cmd_nssm = f"{CONFIG_ROOT_DIR}\\superset-config\\nssm-2.24\\win64\\nssm.exe install {name} {CONFIG_ROOT_DIR}\\superset-config\\{name}.bat"
                os.system(cmd_nssm)

                if len(args) > 0:
                    for arg in args:
                        for k, v in arg.items():
                            if k in ["AppStdout", "AppStderr"]:
                                args_name = f"{k} {CONFIG_ROOT_DIR}\\superset-config\\logs\\{name}{v}"
                            else:
                                args_name = f"{k} {v}"

                            cmd_nssm = f"{CONFIG_ROOT_DIR}\\superset-config\\nssm-2.24\\win64\\nssm.exe set {name} {args_name}"
                            print(cmd_nssm)
                            os.system(cmd_nssm)

        def init_service(name, command):
            if check_if_service_installed(name):
                cmd_nssm = f"{CONFIG_ROOT_DIR}\\superset-config\\nssm-2.24\\win64\\nssm.exe {command} {name}"
                os.system(cmd_nssm)

        if operation == "service_install":
            install_service(name, args=args, re_install=re_install)
        elif operation == "service_start":
            init_service(name, "start")
        elif operation == "service_stop":
            init_service(name, "stop")
        elif operation == "service_remove":
            init_service(name, "remove")

        if check_if_service_installed(name):
            status = 1
        else:
            status = 0

        return status

    args_template = [
        {"AppStdout": ".log"},
        {"AppStderr": ".log"},
        {"AppRotateFiles": "1"},
        {"AppRotateOnline": "0"},
        {"AppRotateSeconds": "86400"},
        {"AppRotateBytes": "5140000"}
    ]

    service_names_list = [
        {
            "name": "Superset_Redis_Service",
            "args": [
                    ] + args_template
        }, {
            "name": "Superset_Service",
            "args": [
                        {"DependOnService": "Superset_Redis_Service"},
                    ] + args_template
        }, {
            "name": "Superset_Thumbnails_Service",
            "args": [
                        {"DependOnService": "Superset_Service"},
                    ] + args_template
        }
    ]

    # win_services_manager [ commands: service_install, service_start, service_stop, service_remove ]
    # for service in service_names_list:
    #     print(win_services_manager(operation="service_install", name=service.get("name"), args=service.get("args"), re_install=True))
    #     #print(win_services_manager(operation="service_start", name=service.get("name"), args=service.get("args")))

    # CMD & Python commands
    set_config_file_path = f"SET FLASK_APP=superset&SET SUPERSET_LAUNCH_MODE=APP&SET SUPERSET_CONFIG_PATH={CONFIG_ROOT_DIR}\\superset-config\\superset_config.py"
    set_config_thumbnails_file_path = set_config_file_path.replace('SUPERSET_LAUNCH_MODE=APP', 'SUPERSET_LAUNCH_MODE=THUMBNAILS')
    set_install_dir = f"cd /d {CONFIG_ROOT_DIR}"
    venv_install = f"{set_install_dir} & py -3.8 -m venv venv"
    venv_activate = f"{CONFIG_ROOT_DIR}\\venv\\Scripts\\activate.bat"
    venv_install_requirements = f"{set_install_dir} & {venv_activate} & pip install -r ./superset-config/superset_requirements/requirements.txt --no-index --find-links ./superset-config/superset_requirements/backend & pip list --format=freeze > ./app/requirements.txt"
    venv_install_superset = f"{set_install_dir} & {venv_activate} & cd /d ./app & pip install -e . & flask fab babel-compile --target ./superset/translations"
    npm_install_node_modules = f"{CONFIG_ROOT_DIR}\\app\\superset-frontend & npm ci & npm run build"
    superset_init_db_upgrade = f"{set_install_dir} & cd app & {venv_activate} & {set_config_file_path} & superset db upgrade"
    superset_init_fab_create_admin = f"{set_install_dir} & cd app & {venv_activate} & {set_config_file_path} & superset fab create-admin --username {config('SUPERSET_ADMIN_LOGIN')} --firstname Superset --lastname Admin --email admin@superset.com --password {config('SUPERSET_ADMIN_PASSWORD')}"
    superset_init = f"{set_install_dir} & cd app & {venv_activate} & {set_config_file_path} & superset init"
    superset_init_install_win_services = "[win_services_manager(operation='service_install', name=s.get('name'), args=s.get('args'), re_install=True) for s in service_names_list]"
    superset_init_load_examples = f"{set_install_dir} & cd app & {venv_activate} & {set_config_file_path} & superset load_examples --load-test-data"
    superset_launch = f"{set_install_dir} & {venv_activate} & {set_config_file_path} & cd /d app & superset run --cert {CONFIG_ROOT_DIR}\superset-config\ssl\{config('SUPERSET_HTTPS_CRT')} --key {CONFIG_ROOT_DIR}\superset-config\ssl\{config('SUPERSET_HTTPS_KEY')} -h {config('SUPERSET_HOST')} -p {config('SUPERSET_PORT')} --with-threads --debugger"
    superset_thumbnails_launch = f"{set_install_dir} & {venv_activate} & {set_config_thumbnails_file_path} & cd /d app & superset compute-thumbnails"

    # CMD execut
    print("\n################ Superset launcher - process start ################\n")

    install_tree = [
        {
            "#": 1,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. Must be installed | configured: \
            \\n Python ver. 3.8 - 3.89 \
            \\n Microsoft Visual C++ 14.0 with Build Tools for Visual Studio 2019 \
            \\n MSVC v142 - VS 2019 C++ x64/x86 build tools (v14.24) \
            \\n Windows 10 SDK (10.0.18362.0) \
            \\n node@v16.9.1 & npm@7.24.2 \
            \\n postgresql-14.1-1-windows-x64 \
            \\n Redis-x64-3.0.504 \
            \\n OpenJDK14U-jdk_x64_windows_hotspot_14.0.1_7 \
            \\n yarn-1.22.5 \
            \\n install {CONFIG_ROOT_DIR}/PostgreSQL/14/default_sql.sql and install backup script - pg_backup.bat \
            \\n create backup deily task in Task Scheduler - 'postgres_backup': \
            \\n   program/script: cmd \
            \\n   add arguments: /c 'path to ...//PostgreSQL/14/pg_backup.bat' \
            \\n   Put file [ superset-config/PostgreSQL/14/pg_backup.bat ] to [ path to .../PostgreSQL/14 ] & Change properties (PSW) in pg_backup.bat \
            \\n add to SYSTEM PATH - {CONFIG_ROOT_DIR}/superset-config/SybaseIQ-16/Bin64/ \
            \\n add to SYSTEM PATH - {CONFIG_ROOT_DIR}/superset-config/node-v16.14.2-win-x64 \
            \\n add to SYSTEM PATH - {CONFIG_ROOT_DIR}/superset-config/instantclient_19_12 \
            \\n  ")""",
            "cmd": """"""
        },
        {
            "#": 2,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. check python requirement version {PYTHON_VENV_VER}")""",
            "cmd": """if "3.8" not in platform.python_version(): raise ValueError('incorrect python version.') """
        },
        {
            "#": 3,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. remove {CONFIG_ROOT_DIR}\\\\superset-install.zip")""",
            "cmd": """if os.path.exists(f"{CONFIG_ROOT_DIR}\\\\superset-config\\\\logs"): shutil.rmtree(f"{CONFIG_ROOT_DIR}\\\\superset-config\\\\logs")"""
        },
        {
            "#": 4,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. add {CONFIG_ROOT_DIR}\\\\superset-config\\\\logs")""",
            "cmd": """if not os.path.exists(f"{CONFIG_ROOT_DIR}\\\\superset-config\\\\logs"): os.makedirs(f"{CONFIG_ROOT_DIR}\\\\superset-config\\\\logs")"""
        },
        {
            "#": 5,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. remove {CONFIG_ROOT_DIR}\\\\superset-install.zip")""",
            "cmd": """if os.path.exists(f"{CONFIG_ROOT_DIR}\\\\superset-install.zip"): os.remove(f"{CONFIG_ROOT_DIR}\\\\superset-install.zip")"""
        },
        {
            "#": 6,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. remove {CONFIG_ROOT_DIR}\\\\app")""",
            "cmd": """if os.path.exists(f"{CONFIG_ROOT_DIR}\\\\app"): shutil.rmtree(f"{CONFIG_ROOT_DIR}\\\\app")"""
        },
        {
            "#": 7,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. remove {CONFIG_ROOT_DIR}\\\\venv")""",
            "cmd": """if os.path.exists(f"{CONFIG_ROOT_DIR}\\\\venv"): shutil.rmtree(f"{CONFIG_ROOT_DIR}\\\\venv")"""
        },
        {
            "#": 8,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. remove {CONFIG_ROOT_DIR}\\\\dist")""",
            "cmd": """if os.path.exists(f"{CONFIG_ROOT_DIR}\\\\dist"): shutil.rmtree(f"{CONFIG_ROOT_DIR}\\\\dist")"""
        },
        {
            "#": 9,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. add {CONFIG_ROOT_DIR}\\\\app")""",
            "cmd": """if not os.path.exists(f"{CONFIG_ROOT_DIR}\\\\app"): os.makedirs(f"{CONFIG_ROOT_DIR}\\\\app")"""
        },
        {
            "#": 10,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. copy & replace from {CONFIG_ROOT_DIR}\\\\superset-config\\\\superset_requirements\\\\superset-master\\\\superset to {CONFIG_ROOT_DIR}\\\\app\\\\superset")""",
            "cmd": """if not os.path.exists(f"{CONFIG_ROOT_DIR}\\\\app\\\\superset"): shutil.copytree(f"{CONFIG_ROOT_DIR}\\\\superset-config\\\\superset_requirements\\\\superset-master\\\\superset", f"{CONFIG_ROOT_DIR}\\\\app\\\\superset", dirs_exist_ok=True)"""
        },
        {
            "#": 11,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. copy & replace from {CONFIG_ROOT_DIR}\\\\superset-config\\\\superset_requirements\\\\superset-master\\\\superset-frontend to {CONFIG_ROOT_DIR}\\\\app\\\\superset-frontend")""",
            "cmd": """if not os.path.exists(f"{CONFIG_ROOT_DIR}\\\\app\\\\superset-frontend"): shutil.copytree(f"{CONFIG_ROOT_DIR}\\\\superset-config\\\\superset_requirements\\\\superset-master\\\\superset-frontend", f"{CONFIG_ROOT_DIR}\\\\app\\\\superset-frontend", dirs_exist_ok=True)"""
        },
        {
            "#": 12,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. add {CONFIG_ROOT_DIR}\\\\app\\\\superset\\\\static")""",
            "cmd": """if not os.path.exists(f"{CONFIG_ROOT_DIR}\\\\app\\\\superset\\\\static"): os.makedirs(f"{CONFIG_ROOT_DIR}\\\\app\\\\superset\\\\static")"""
        },
        {
            "#": 13,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. print(13)""",
            "cmd": """print(13)"""
        },
        {
            "#": 14,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. copy from {CONFIG_ROOT_DIR}\\\\superset-config\\\\superset_requirements\\\\requirements.txt to {CONFIG_ROOT_DIR}\\\\app\\\\requirements.txt")""",
            "cmd": """shutil.copyfile(f"{CONFIG_ROOT_DIR}\\\\superset-config\\\\superset_requirements\\\\requirements.txt", f"{CONFIG_ROOT_DIR}\\\\app\\\\requirements.txt")"""
        },
        {
            "#": 17,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. copy from {CONFIG_ROOT_DIR}\\\\superset-config\\\\superset_requirements\\\\superset-master\\\\setup.py to {CONFIG_ROOT_DIR}\\\\app\\\\setup.py")""",
            "cmd": """if not os.path.isfile(f"{CONFIG_ROOT_DIR}\\\\app\\\\setup.py"): shutil.copyfile(f"{CONFIG_ROOT_DIR}\\\\superset-config\\\\superset_requirements\\\\superset-master\\\\setup.py", f"{CONFIG_ROOT_DIR}\\\\app\\\\setup.py")"""
        },
        {
            "#": 18,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. venv_install """ + venv_install.replace('\\', '\\\\') + """ ")""",
            "cmd": """if not os.path.exists(f"{CONFIG_ROOT_DIR}\\\\venv"): os.system(f"{venv_install}")"""
        },
        {
            "#": 19,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. venv_install_requirements """ + venv_install_requirements.replace('\\', '\\\\') + """ ")""",
            "cmd": """if os.path.exists(f"{CONFIG_ROOT_DIR}\\\\venv"): os.system(f"{venv_install_requirements}")"""
        },
        {
            "#": 20,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. venv_install_superset """ + venv_install_superset.replace('\\', '\\\\') + """ ")""",
            "cmd": """if os.path.exists(f"{CONFIG_ROOT_DIR}\\\\venv"): os.system(f"{venv_install_superset}")"""
        },
        {
            "#": 21,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. copy & replace from {CONFIG_ROOT_DIR}\\\\superset-config\\\\venv to {CONFIG_ROOT_DIR}\\\\venv")""",
            "cmd": """if os.path.exists(f"{CONFIG_ROOT_DIR}\\\\venv"): shutil.copytree(f"{CONFIG_ROOT_DIR}\\\\superset-config\\\\venv", f"{CONFIG_ROOT_DIR}\\\\venv", dirs_exist_ok=True)"""
        },
        {
            "#": 22,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. superset_init_db_upgrade """ + superset_init_db_upgrade.replace('\\', '\\\\') + """ ")""",
            "cmd": """if os.path.exists(f"{CONFIG_ROOT_DIR}\\\\venv"): os.system(f"{superset_init_db_upgrade}")"""
        },
        {
            "#": 23,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. superset_init_fab_create_admin """ + superset_init_fab_create_admin.replace('\\', '\\\\') + """ ")""",
            "cmd": """if os.path.exists(f"{CONFIG_ROOT_DIR}\\\\venv"): os.system(f"{superset_init_fab_create_admin}")"""
        },
        {
            "#": 24,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. superset_init """ + superset_init.replace('\\', '\\\\') + """ ")""",
            "cmd": """if os.path.exists(f"{CONFIG_ROOT_DIR}\\\\venv"): os.system(f"{superset_init}")"""
        },
        {
            "#": 25,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. superset_init_install_win_services """ + superset_init_install_win_services.replace('\\', '\\\\') + """ ")""",
            "cmd": """os.system(f"{superset_init_install_win_services}")"""
        },
        {
            "#": 26,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. copy & replace from {CONFIG_ROOT_DIR}\\\\superset-config\\\\app to {CONFIG_ROOT_DIR}\\\\app")""",
            "cmd": """if os.path.exists(f"{CONFIG_ROOT_DIR}\\\\app"): shutil.copytree(f"{CONFIG_ROOT_DIR}\\\\superset-config\\\\app", f"{CONFIG_ROOT_DIR}\\\\app", dirs_exist_ok=True)"""
        },
        {
            "#": 27,
            "console_log": """print('install npm')""",
            "cmd": """print('install npm')"""
        },
        # {
        #    "#": 27,
        #    "console_log": """print(f"CMD execute [step: #{step}]: \\n.. copy & replace from {CONFIG_ROOT_DIR}\\\\superset-config\\\\superset_requirements\\\\fronted\\\\npm\\\\static to {CONFIG_ROOT_DIR}\\\\app\\\\superset\\\\static")""",
        #    "cmd": """if os.path.exists(f"{CONFIG_ROOT_DIR}\\\\superset-config\\\\superset_requirements\\\\fronted\\\\npm\\\\static"): shutil.copytree(f"{CONFIG_ROOT_DIR}\\\\superset-config\\\\superset_requirements\\\\fronted\\\\npm\\\\static", f"{CONFIG_ROOT_DIR}\\\\app\\\\superset\\\\static", dirs_exist_ok=True)"""
        # },
        {
            "#": 28,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. start service RedisCashe """ + superset_init_install_win_services.replace('service_install', 'service_start').replace('service_names_list', 'service_names_list[0:1]').replace('\\', '\\\\') + """ ")""",
            "cmd": """os.system(f"{superset_init_install_win_services.replace('service_install', 'service_start').replace('service_names_list', 'service_names_list[0:1]')}")"""
        },
        {
            "#": 29,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. superset init """ + superset_init_load_examples.replace('\\', '\\\\') + """ ")""",
            "cmd": """if os.path.exists(f"{CONFIG_ROOT_DIR}\\\\venv"): os.system(f"{superset_init_load_examples}")"""
        },
        {
            "#": 30,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. stop service RedisCashe """ + superset_init_install_win_services.replace('service_install', 'service_stop').replace('service_names_list', 'service_names_list[0:1]').replace('\\', '\\\\') + """ ")""",
            "cmd": """os.system(f"{superset_init_install_win_services.replace('service_install', 'service_stop').replace('service_names_list', 'service_names_list[0:1]')}")"""
        },
        {
            "#": 31,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. launch superset as cmd """ + superset_launch.replace('\\', '\\\\') + """ ")""",
            "cmd": """os.system(f"{superset_launch}")"""
        },
        {
            "#": 32,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. create or update Superset_Service.bat """ + superset_launch.replace('\\', '\\\\') + """ ")""",
            "cmd": f"""with open(r'{CONFIG_ROOT_DIR}/superset-config/Superset_Service.bat', 'w', encoding='utf-8') as bat_file: bat_file.write(fr'{superset_launch}')"""
        },
        {
            "#": 33,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. create or update Superset_Thumbnails_Service.bat """ + superset_thumbnails_launch.replace(
                '\\', '\\\\') + """ ")""",
            "cmd": f"""with open(r'{CONFIG_ROOT_DIR}/superset-config/Superset_Thumbnails_Service.bat', 'w', encoding='utf-8') as bat_file: bat_file.write(fr'{superset_thumbnails_launch}')"""
        },
        {
            "#": 34,
            "console_log": """print(f"CMD execute [step: #{step}]: \\n.. stop service Superset_Service """ + superset_init_install_win_services.replace(
                'service_install', 'service_start').replace('service_names_list', 'service_names_list[1:2]').replace(
                '\\', '\\\\') + """ ")""",
            "cmd": """os.system(f"{superset_init_install_win_services.replace('service_install', 'service_start').replace('service_names_list', 'service_names_list[1:2]')}")"""
        }
    ]

    for run in install_tree:
        skip = False

        if len(init_steps) > 0:
            if run.get("#") not in init_steps:
                skip = True
        if len(init_steps_skip) > 0:
            if run.get("#") in init_steps_skip:
                skip = True
        if not skip:
            step, result = cmd_execute(step, result, run.get("console_log"), run.get("cmd"))
        if result == "Fail": break

    if result == "OK":
        print("\n################ Superset launcher - process DONE. ################\n")
    else:
        print("\n################ Superset launcher - process FAIL. ################\n")


if __name__ == "__main__":
    #import os
    #os.system(r"")
    # main(init_steps=[1], init_steps_skip=[])  # app-show-important-requirements-installed-before
    main(init_steps=[], init_steps_skip=[26, 31, 34])  # app-default-install
    # main(init_steps=[], init_steps_skip=[31, 34])  # app-full-install
    # main(init_steps=[26, 27], init_steps_skip=[31, 34])  # app-recompile-node_modules
    # main(init_steps=[31], init_steps_skip=[])  # app-run-console
    # main(init_steps=[34], init_steps_skip=[])  # app-run-service
