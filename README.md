# 3e-timecard
A brief demonstration using Python to create timecards in Elite 3E.

## Getting started
Assuming a version of [Python 3.6.4 or higher is installed ](https://docs.python.org/3/)

### Create and activate a virtual environment
Create a folder on your local drive. For this example we'll use c:\dev\timecard3e
For more instructions see the [official documentation for virtual environments](https://docs.python.org/3/library/venv.html)
```
cd c:\dev\timecard3e
python3 -m venv venv
.\venv\Scripts\activate
```
### Check out a version of repository
Use the clone or download button above and save to your project folder (c:\dev\timecard3e).
### Install the requirements
Ensuring the virtual environment is active (your prompt should look like `(venv) C:\dev\timecard3e>`), install the requirements.
```
pip install -r requirements.txt
```
### Environment variables
The timecards.py file tries to read some environment variables. If on Windows, these can be set 
in the \venv\Scripts\activate.bat file by appending something like the following to the end of the file. It will be necessary 
to [deactivate and re-activate](https://www.codingforentrepreneurs.com/blog/activate-reactivate-deactivate-your-virtualenv/) the virtual environment after making changes to activate.bat.
```
SET "HTTP_NTLM_AUTH_USER=yourdomain\user.name"
SET "HTTP_NTLM_AUTH_PASS=seCretPassWord"
SET "ELITE_WAPI=elite1"
SET "ELITE_INSTANCE=TE_3E_UAT"
```
If not set in the environment, the defaults can be placed in line in the code as the second 
parameter to the os.environ.get calls to end up with something like:
```
    wapi = os.environ.get('ELITE_WAPI', 'elite1')
    instance = os.environ.get('ELITE_INSTANCE', 'TE_3E_UAT')
```
### Run the code
Hoping you've made it this far, now run the timecards.py file. You'll likely want to change the timekeeper and matter in
the timecard_attributes method.
```
python timecard.py
```
A bunch of output should display to the screen. In reality, I've used a custom process that takes the entry 
and posts/releases it immediately, but in this sample, we're using the TimeCardUpdate process which will put an entry onto 
the action list of the user specified in HTTP_NTLM_AUTH_USER.

### Zeep for Soap Calls
I've switched to [Zeep](http://docs.python-zeep.org/en/master/) over [Suds-Jurko](https://pypi.python.org/pypi/suds-jurko) as
it seems to be getting more love and doesn't require use of the Windows temp folder.
