# NPTEL Statistics String Parser

## The Problem
It was that time of the semester when I had to choose an NPTEL course for my institute elective. I decided to analyze existing courses using the statistics available on the NPTEL site to find the best option for grading. 

However, copying the tabular data from the site strips away all formatting, resulting in a single, unbroken string of digits containing everything from total enrollment and certification levels to max/min marks, averages, and standard deviations. The objective of this project is to map the mathematical relationships within that data and extract it into a usable format.

## Overview
This repository contains a Python script designed to automatically parse and reconstruct the original statistical columns from the raw, unformatted NPTEL data string using constraint satisfaction and backtracking.

## Features
*   **Automated Data Extraction:** Converts a continuous numerical string into a structured, readable Python dictionary.
*   **Constraint Satisfaction:** Uses recursive backtracking to identify correct numerical boundaries without explicit delimiters.
*   **Mathematical Validation:** Tests generated permutations against real-world NPTEL grading constraints to guarantee data accuracy.

## How It Works
The script first isolates the decimal points at the end of the string to extract the `Average` and `Standard Deviation`. It then blindly chunks the remaining integer string into segments and validates them against the following hardcoded logic:
1.  `Certified == Gold + Silver + Elite + Success`
2.  `Enrolled >= Registered >= Certified`
3.  `Maximum Mark <= 100`

If a specific sequence of chunks mathematically satisfies all of these constraints simultaneously, it is finalized and mapped to the respective statistical headers.
