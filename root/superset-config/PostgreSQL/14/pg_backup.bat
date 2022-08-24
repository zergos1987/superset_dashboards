@echo off
for /F "skip=1 delims=" %%F in ('
    wmic PATH Win32_LocalTime GET Day^,Month^,Year /FORMAT:TABLE
') do (
    for /F "tokens=1-3" %%L in ("%%F") do (
        set CurrDay=%%M
        set CurrMonth=%%L
        set CurrYear=%%N
    )
)
set datestr=%CurrMonth%_%CurrDay%_%CurrYear%
echo datestr is %datestr%

set BACKUP_FILE="path to ...\PostgreSQL\14\pg_backup\postgres_full_bk_%datestr%.backup"
echo backup file name is %BACKUP_FILE%
SET PGPASSWORD=some password
echo on
"path to...\PostgreSQL\14\bin\pg_dump.exe" -h localhost -p 5432 -U postgres -F c -b -v -f %BACKUP_FILE% postgres
