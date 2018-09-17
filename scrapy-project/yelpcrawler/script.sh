# execute crawler yelp
scrapy crawl yelp 

# execute crawl yelp and output to json file
scrapy crawl yelp -o output.json -t json

# use job dir to save the job info to disk, so that we can resume the job
scrapy crawl yelp -s JOBDIR=yelpJob