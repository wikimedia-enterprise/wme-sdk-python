## Prerequisites:
1. **Wikimedia Enterprise Account** (Free)
   Sign up for a Wikimedia Enterprise account here:
   [https://dashboard.enterprise.wikimedia.com/signup/](https://dashboard.enterprise.wikimedia.com/signup/)

2. **Optional: OpenCage API Account** (Free)
   This is only needed if you run the "locations" demo.
   Sign up for an OpenCage API key here:
   [https://opencagedata.com/](https://opencagedata.com/)



## Step-by-Step Guide

### 1. Clone the Project and set Python to version 3.12:
First, clone this repository to your local machine. Switch Python to use 3.12

```bash
git clone https://github.com/wikimedia-enterprise/wme-sdk-python.git
cd wme-sdk-python/example/demo

Switch Python to use Python 3.12
# Mac OSX with Brew:
brew install python@3.12

# Or Mac without Brew:
pyenv install 3.12
pyenv local 3.12

# Windows:
py -3.12 --version
```

### 2. Create a `.env` file
Save it into directory `wme-sdk-python/example/demo`. Save your Wikimedia Enterprise username, password, and OpenCage API key in it.

#### Example `.env` file:
```bash
WME_USERNAME=your_wikimedia_username
WME_PASSWORD=your_wikimedia_password
OPENCAGE_API_KEY=your_opencage_api_key   #This one is optional, needed for the Location maps demo
```

Aside, there are rules for escaping special characters in environment varaibles in `.env` files
* Escape special characters using a backslash (\):
    * \# to include # in the value.
    * \= to include = in the value.
    * \ to include spaces at the beginning or end.
* Quote the value if it contains spaces or special characters:
    *Use double quotes (") or single quotes ('):
    ```
    WME_PASSWORD="pa$$word#1"
    API_SECRET='pa$$ word' # has a space
    ```
* Avoid unnecessary escaping within quotes:
* Within double quotes, only " and \ need escaping.
* Within single quotes, nothing needs escaping except for the closing single quote.

### 3. Create a Python Virtual Environment:
Set up a Python virtual environment named `geo` to isolate project dependencies.

```bash
python3 -m venv venv
```

### 4. Activate the Virtual Environment:
Activate the virtual environment before installing the required dependencies.

- **On macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

- **On Windows:**
  ```bash
  venv\Scripts\activate
  ```

### 5. Install Project Dependencies:
Once the virtual environment is activated, install the required Python packages by running:

```bash
pip install -r requirements.txt
```
Check they all the dependencies install correctly, some may require you to install additional OS level packages.

### 6. Choose one of the three demos:
1. [word-cloud README](./word-cloud/README.md)
1. [elections README](./elections/README.md)
1. [locations README](./locations/README.md)
