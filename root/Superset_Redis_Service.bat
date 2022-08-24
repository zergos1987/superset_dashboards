@echo off
set current_service_path=%~dp0
cmd.exe /K "%current_service_path%\Redis-x64-3.0.504\redis-server.exe --dbfilename dump.rdb --dir %current_service_path%\Redis-x64-3.0.504"
