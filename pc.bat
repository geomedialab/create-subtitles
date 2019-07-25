@ECHO OFF
Rem This file runs the commands required for setting up the subtitle creation pipeline on your local machine.
Rem make sure that this .bat file is in the same top-level folder as the other files in this pipeline.

echo.
echo Verifying installation...
echo.
if exist "files\client_id.json" if exist "files\main.py" if exist "files\postprocess_and_fuse_subs.py" goto :run_python

:install

echo This program requires 100 Mb minimum available space on your hard drive.
pause
Rem upgrade pip, the python package installer, before continuing.
echo.
echo Installing files...
echo.
python -m pip install --upgrade pip

Rem install virtualenv (a package that will allow the creation of an isolated python 2 virtual environment)
pip install virtualenv

virtualenv -p python files

Rem move the the required files your new virtual environment folder
move main.py files/main.py
move postprocess_and_fuse_subs.py files/postprocess_and_fuse_subs.py
move requirements.txt files/requirements.txt
move client_id.json files/client_id.json

cd files
echo.
echo Activating virtual environment entitled 'files' and installing required python modules...
echo.
call "Scripts\activate.bat"
pip install -r requirements.txt
echo.
echo Before proceeding, make sure to place a folder containing your video and transcript inside the 'files' subfolder that was just created.
pause
call "Scripts\deactivate.bat"
goto :run_python2

:run_python

Rem run program
cd files
echo Activating virtual environment entitled 'files'...
:run_python2
echo.
call "Scripts\activate.bat"
echo Starting up program...
echo.
python main.py
call "Scripts\deactivate.bat"
cd ..