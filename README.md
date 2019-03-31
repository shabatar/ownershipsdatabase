# ownershipsdatabase
This repository contains utils aimed at retrieving necessary data from companies' public reports.

## Settings
* **ReportsCount**: count of reports to process

* **RegionSize**: count of lines of desired region

* **EndMargin**: add `EndMargin` lines after the end of found region

* **StartSkipPercent**: skip `file_size` * `StartSkipPercent` before search starts

* **ExtendUntilTable**: extend region until html table ends


## Usage
#### Download reports
`$ python3 src/get_reports.py`

Reports will be downloaded into `data` folder

#### Extract regions from reports
`$ python3 src/cut_reports.py`

Extracted regions will be saved into `dataCut`
