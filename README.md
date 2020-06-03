Scrape community input table from the National Academies site.

# Installation

1. Download appropriate chromedriver [here](https://chromedriver.chromium.org/downloads). Place this zip file in the root of this repository and unzip it. You should now see the chromedriver file in this directory.  

2. Set up a virtual environment in which to store your python dependencies. For example, using python [venv](https://docs.python.org/3/library/venv.html):  

    ```
    python -m venv venv  
    source venv/bin/activate
    ``` 

3. Install the requirements with pip:  

    ```
    pip install -r requirements.txt
    ```

# Running

Simply run the python script with your preferred output file name. For example:
```
python scrape_papers astro2020papers.csv
```

