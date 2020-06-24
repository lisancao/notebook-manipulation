# This is a link checker for notebooks 

## DECOMPOSITION: Broken links are present in notebooks, too burdensome to check manually

## SOLUTION: parse url links from notebooks and check for HTTP status code errors


## ABSTRACTION / ALGORITHM DESIGN

## GAMEPLAN 
# 1) parse links from json file into array 
	- use David's code to scrape cell sourcecode

# 2) iterate through array and feed elements to linkchecker 
	- urllib (HTTP client, pretty overboard?) 
	- scrapy [too heavy]
	- pylinkvalidator [Best contender but also requires beautifulsoup to run on py3] ** DOES NOT WORK ON 3.8 
	- ** issue: only validate given url and not all urls under host

# 3) return dataframe with pass/fail validity checks OR standard error message (possible to return line #?) 



## PSEUDOCODE STEP

## CONVERT PSEUDOCODE TO PYTHON CODE


## EVALUATE
-case testing
