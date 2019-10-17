Insurance
=============================

A tool for comparing health insurance plans 

## Getting started

1. Make sure the information about the health insurance plans you would like to compare in *rates.json* is correct. 
2. Make sure the required Python packages are installed. Currently these are:
    * *json*
    * *numpy*
    * *matplotlib*
3. Run the Python script *analysis.py*.

## Output

The following output is currently produced by *analysis.py*:

* */<plan name/>.png*: Shows the total out-of-pocket cost for every level of services received under plan \<plan name\>, and shows how much of this cost is spent towards premiums, deductible, and co-insurance.
* *totals.png*: Shows the total out-of-pocket cost for every level of services under every plan specified in *rates.json*.
