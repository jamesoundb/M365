## MS365 Health Checker
* #### A python script to run health checks on MS365 services, log the status codes of the endpoints, and display on a Raspberry Pi Sense Hat if the endpoint health checks passed or failed. Use the ms.py script if you have a Sense hat and want those functions, otherwise use the ms_no_hat.py file.
* #### Use the requirements.txt file to install the neccessary modules with:
```bash
pip install -r requirements.txt
```
* #### If using with no Sense Hat then use:
```bash
pip install -r requirements_nohat.txt
```
* #### To execute the script in a virtual environment:
```bash
python -m venv myenv
```
* #### Activate for macOS and Linux with:
```bash
source myenv/bin/activate
```
* #### Activate for Windows:
```bash
myenv\Scripts\activate.ps1
```
* #### Finally, execute your desired requirements.txt pip install and then execute the script. After executing deactivate the virtual environment with:
`deactive`
