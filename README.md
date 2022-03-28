# Test
This repository contains the scripts developed for the engineering test.
All required packages and their versions are listed in the `Pipfile`.

Following the structure of the test, this repository contains two directories: `Part_1` and `Part_2`.

## Part_1
`gcloud-trans-request.py` is a script to send a translation request using Google Cloud Translation Basic API for generic (untrained) Google Translate engine.

### Requirements:
In order to send a translation request to Google Cloud, it is necessary to first install Google Cloud SDK. 
#### Step 1:
Create a [Google Account](cloud.google.com).
#### Step 2:
Download the correct [GCloud SDK Package](https://cloud.google.com/sdk/docs/downloads-versioned-archives#installation_instructions) according to your system.
#### Step 3:
From your terminal, unpack the `tar` file in your applications directory and install GCloud SDK by running the `.\install.bat` (Windows) or `.\install.sh` (macOS/Linux) file.
#### Step 4:
Open a new terminal window and update the GCloud SDK components by running:

```bash
gcloud components update
```

#### Step 5:
Access your account using the following command and create your Google Cloud Project:
```bash
gcloud auth login
```


#### Step 6:
Obtain the credentials for the Service Account linked to your project in JSON format by following the instructions in the [Google Documentation](https://cloud.google.com/docs/authentication/getting-started).


### Usage:
Given a JSON key (in my use-case, the JSON file `testnlpdeploy-ac6f428e336d.json`), run the application from the terminal using:

```bash
py gcloud-trans-request.py [-h] --text SRC_TEXT --json KEY_PATH --src SRC_LANG --trg TRG_LANG
```

All other arguments are required and have the following behaviors:

`--text` The source text to be translated. This should be a string, i.e. `--text "Hello World"`

`--src` The source language, formatted following the [ISO-639-1](https://cloud.google.com/translate/docs/languages)

`--trg` The target language, formatted following the [ISO-639-1](https://cloud.google.com/translate/docs/languages)

## Part_2
`excel-data-parser.py` is a python script that, given a recursive folder structure with each subfolder being the `name of project_results`, processes the `Corpus` and `Corpus revision steps` tabs of each Excel file and generates a corresponding `Summary.xlsx` file containing all relevant information. Additionally, the program generates a `Summary.log` file.

By default, the script uses xlrd v1.2.0 to parse the `.xlsx` files, because v2.0.1 [only supports `.xls` files](https://xlrd.readthedocs.io/en/latest/).
Optionally, it is also possible to use the latest version of [openpyxl (v3.0.9)](https://openpyxl.readthedocs.io/en/stable/), although the import time is significantly slower.

### Usage:
Given a nested directory, run the application by calling it from the terminal using:

```bash
py corpus_parser.py [-h] --dir DIR_PATH [--save_to [SAVE_PATH]] [--afterLQA [AFTER_LQA [AFTER_LQA ...]]]
```

All other arguments are optional and have the following behaviors:

`--save_to` Path where the output files will be saved. These are either absolute or relative to the current directory. The default save directory is the current working directory.

`--afterLQA` (case insensitive) Determines the steps to be considered as "After LQA", while all other steps are considered as "Before LQA".  E.g. by setting this to `--afterLQA correct1 review1` all steps including `correct1` or `review1` will be considered as "After LQA". The default behavior sets `correct2` and `correct3` as "After LQA".

`--engine` Can be set to either `xlrd` or `openpyxl`. Default is `xlrd`.
  
