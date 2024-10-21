## Demo of WME Structured Contents API

US Presidential Electorial College Votes over Time from 1980 to 2020.  We take a Data Science approach to collecting the data, tidying the data they way we need it, and then charting it

Final chart of running the code in this repository:
![US Presidential Electorial College Votes over Time from 1980 to 2020](image.png)

You must have Python installed.

## Setup and Run

Termainal commands:
```
#setup the virtual environment
python3 -m venv sdk
source sdk/bin/activate

#install the dependencies
pip install -r requirements.txt

# Run the on-demand example
python -m example.demo.get
python -m example.demo.parse
python -m example.demo.chart
```
To close the chart click the close button on the Window, or on the keyboard press Ctrl-C to stop the command in the terminal.
