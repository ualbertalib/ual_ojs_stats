# 1. Overview

The objective of this project is to periodically generate statistical reports of OJS journals hosted the University of Alberta Library.

To achieve the above goal, we leverage the Application Programming Interface (API) offered by OJS and take advantage of
the programming power offered by the Python program language. 


# 2. List of Journals

There are many journals hosted by the University of Alberta Library. They are
compiled and presented below.

| Journal Title | Abbreviated Journal Title |
|:---|:---|
|Phenomenology and Practice| pandpr |

# 3. API Key for Each Journal

For each login account to each journal, one can generate an API key, which is needed to
access securely the API endpoints. 

To generate the API key, we use the journal "Phenomenology and Practice" as an example, and
illustrate the basic step.

![API Key](images/api_key.png)

# 4. Input Format

The input is in csv format, for example, journals.csv:

```
jabbr,base_url,token
pandpr,https://journals.library.ualberta.ca/,******************************************

```

- ***jabbr*** stands for the journal title abbreviation
- ***base_url*** the base part of the host URL
- ***token*** this is the api key that is used to access the API endpoints

# 5. Execution of the Python Program

```
python3 stats.py journals.csv
```

- ***stats.py*** can be found [here](scripts/stats.py)
- ***journals.csv*** can be found [here](files/journals.csv)

# 6. Output Format

```
[
    {
        "journal abbreviation": "pandpr",
        "published submissions": 214,
        "published issues": 25,
        "abstract views": 2271,
        "galley views": 4660
    }
]

```
