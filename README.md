# DC 311 Service Requests Analysis (2025)

**Author:** Moses Baridone, Information Science, University of Maryland

## What this project does
Washington, DC residents use 311 to report problems like missed trash pickup, potholes, and broken streetlights. I took the city's public 2025 dataset of **[TOTAL] requests**, cleaned it with Python, loaded it into a SQLite database, and wrote SQL queries to find out:

1. Which problems get reported most
2. Which wards report the most problems
3. How long the city takes to resolve each type of request
4. How request volume changes across the year
5. The top problem in each of DC's 8 wards

## Key findings
*(Fill these in after running analysis.py on the real data.)*
- The most common request type was **[TYPE]**, with **[NUMBER]** requests.
- **Ward [X]** submitted the most requests; **Ward [Y]** submitted the fewest.
- **[TYPE]** requests took the longest to resolve, averaging **[N] days**.
- Requests peaked in **[MONTH]**, likely because **[your guess why]**.

## Charts
![Top request types](charts/top_request_types.png)
![Requests by ward](charts/requests_by_ward.png)
![Requests per month](charts/requests_per_month.png)

## Tools used
Python (pandas, matplotlib), SQL (SQLite), including GROUP BY, HAVING, subqueries, window functions (RANK), and date math.

## How to run it
1. Download the CSV from [DC Open Data](https://opendata.dc.gov/datasets/DCGIS::311-city-service-requests-in-2025) and save it as `dc_311_2025.csv` in this folder.
2. Install the libraries: `pip install pandas matplotlib`
3. Run `python load_data.py` to build the database.
4. Run `python analysis.py` to print the results and save the charts.

## Data source
[311 City Service Requests in 2025](https://opendata.dc.gov/datasets/DCGIS::311-city-service-requests-in-2025), Office of Unified Communications, DC Open Data.
