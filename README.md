# DC 311 Service Requests Analysis (2025)

**Author:** Moses Baridone, Information Science, University of Maryland

## What this project does
Washington, DC residents use 311 to report problems like missed trash pickup, potholes, and broken streetlights. I took the city's public 2025 dataset of **440,562 requests**, cleaned it with Python, loaded it into a SQLite database, and wrote SQL queries to find out:

1. Which problems get reported most
2. Which wards report the most problems
3. How long the city takes to resolve each type of request
4. How request volume changes across the year
5. The top problem in each of DC's 8 wards

## Key findings
- **Bulk Collection** (large-item trash pickup) was the most common request, with **67,408 requests**, about 15% of everything DC residents reported. Parking Enforcement was second with 58,138.
- **Ward 5** submitted the most requests (**66,937**) and **Ward 3** the fewest (**41,816**). Ward 5 filed about 60% more requests than Ward 3.
- What residents report depends on where they live. Parking Enforcement was the #1 request in Wards 1, 2 and 6, which are dense neighborhoods closer to downtown. Bulk Collection was #1 in Wards 3, 4, 5 and 7, and Ward 8's top request was DC Government Information.
- Infrastructure repairs take the longest to resolve. **Roadway Repair** averaged **141 days** and **Sidewalk Repair 122 days**, compared to weeks for most other request types.
- Requests peaked in **July (45,137)** and bottomed out in **December (26,378)**, a 71% swing. Seasonal services like yard waste pickup and more outdoor activity in summer likely explain the difference.



## Tools used
Python (pandas, matplotlib), SQL (SQLite), including GROUP BY, HAVING, subqueries, window functions (RANK), and date math.

## How to run it
1. Download the CSV from [DC Open Data](https://opendata.dc.gov/datasets/DCGIS::311-city-service-requests-in-2025) and save it as `dc_311_2025.csv` in this folder.
2. Install the libraries: `pip install pandas matplotlib`
3. Run `python load_data.py` to build the database.
4. Run `python analysis.py` to print the results and save the charts.

## Data source
[311 City Service Requests in 2025](https://opendata.dc.gov/datasets/DCGIS::311-city-service-requests-in-2025), Office of Unified Communications, DC Open Data.
