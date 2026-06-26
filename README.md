# NPTEL Statistics String Parser

## The Problem
It was that time of the semester when I had to choose an NPTEL course for my institute elective. I decided to analyze existing courses using the statistics available on the NPTEL site to find the best option for grading. 

However, copying the tabular data from the site strips away all formatting, resulting in a single, unbroken string of digits containing everything from total enrollment and certification levels to max/min marks, averages, and standard deviations. The objective of this project is to scrap data from NPTEL webpage and get statistics using api calls and analyse various parameters for multiple subjects of interests through a plot and make the ideal elective choice.

## Overview
This repository contains a Python script designed to automatically parse and reconstruct the original statistical columns from the NPTEL webpage and make suitable calculations to plot a graph to give a fair idea of subjects.

## Features
*   **Course id mapping:** Maps the input course with its respective course id obtained by scrapping the courses page of NPTEL website.
*   **Automated Data Extraction:** Get the statistical data of the inputed course from NPTEL database by employing api calls using the course id.
*   **Parameter calculation:** Various mathematical parameters (multiple ratios and a final score) are calculated from the hence obtained data.
*   **Graph plotting:** The calculated parameters are employed to plot a graph for better picture of all courses concerned

## How It Works


## Usage

## 0. Pre-Requisites
After forking the repo get a python virtual enviornment and install the pre requisites by running:
```bash
pip install -r requirements.txt
```

### 1. Execution

Run the script in your terminal environment. It will prompt you to enter the raw, unformatted string copied from the NPTEL statistics page:

```bash
python nptel_parser.py
```

### 2. Example Input

```text
Enter Subject: Principles Of Economics
```
After the script processes...
```text
Do you want to add another subject? (Y/n): 
Y -> for adding more subjects
n -> gives the final output
```

### 3. Output

The script maps the extracted variables and outputs an excel file.
It also calculates parameters for analyses and outputs a graph in png format.
