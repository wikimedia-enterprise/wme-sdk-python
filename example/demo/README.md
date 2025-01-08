## Prerequisites:
1. **Wikimedia Enterprise Account** (Free)
   Sign up for a Wikimedia Enterprise account here:
   [https://dashboard.enterprise.wikimedia.com/signup/](https://dashboard.enterprise.wikimedia.com/signup/)

2. **Optional: OpenCage API Account** (Free)
   This is only needed if you run the "locations" demo.
   Sign up for an OpenCage API key here:
   [https://opencagedata.com/](https://opencagedata.com/)

## Environment Setup
Create a `.env` file in the project directory and save your Wikimedia Enterprise username, password, and OpenCage API key in it.

### Example `.env` file:
```bash
WME_USERNAME=your_wikimedia_username
WME_PASSWORD=your_wikimedia_password
OPENCAGE_API_KEY=your_opencage_api_key
```


## Step-by-Step Guide

### 1. Clone the Project:
First, clone this repository to your local machine.

```bash
git clone https://github.com/wikimedia-enterprise/wme-sdk-python.git
cd wme-sdk-python
# For this demo app:
cd wme-sdk-python/example/demo/locations
```

### 2. Create a Python Virtual Environment:
Set up a Python virtual environment named `geo` to isolate project dependencies.

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment:
Activate the virtual environment before installing the required dependencies.

- **On macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

- **On Windows:**
  ```bash
  venv\Scripts\activate
  ```

### 4. Install Project Dependencies:
Once the virtual environment is activated, install the required Python packages by running:

```bash
pip install -r requirements.txt
```
Check they all the dependencies install correctly, some may require you to install additional OS level packages.

Choose one of the three demos:
1. [word-cloud README](./word-cloud/README.md)
1. [elections README](./elections/README.md)
1. [locations README](./locations/README.md)
