# Book Search Engine 

This project comprises several components including a Scrapy crawler, a Solr server setup and UI. It is designed to crawl, index, and search book data efficiently.

[Overview video](TODO)


## Project Structure

```
Root/
├── project3Book/  # Scrapy for crawling
│   └── data/
│       └── bookData3.json # Crawled data
├── bookSearchUI/         # User Interface
└── Solr-8.11.0/          # Solr server

```

## Components

### Scrapy - Web Crawling

#### To run Scrapy:
1. Navigate to the spiders directory:
   ```bash
   cd project3Book/project3Book/spiders
   ```
2. Execute the spider:
   ```bash
   scrapy runspider bookSpider.py -o out.json
   ```

The scraper is designed to extract data from sources:
- https://www.doabooks.org
- https://market.feedbooks.com
- www.bookdepository.com (closed)


### Solr - Search Platform
This platform uses **Sorl-8.11.0** as a search engine. 

#### To start Solr:
1. Navigate to the Solr directory:
   ```bash
   cd Solr-8.11.0
   ```
2. Start Solr in cloud mode on the default port (8983):
   ```bash
   bin/solr start -e cloud
   ```
3. When prompted to create a new collection:
   - Provide the collection name as `bookTest2` to avoid creating a new one.

### UI - User Interface (Quasar\Vue)

The UI is hosted on GitLab Pages to avoid local dependency setup (need to run the application on localhost 8983):

🔗 [Book Search UI](https://joyalbertini.github.io/bookSearchUI/#/)

#### To run locally:
1. Navigate to the UI directory:
   ```bash
   cd bookSearchUI/quasar-demo
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the application in development mode:
   ```bash
   quasar dev
   ```
4. To build the application:
   ```bash
   quasar build
   ```
   Note: Running the build locally requires setting up a server or using GitLab Pages as demonstrated.

## Guide/Report
[Guide PDF](gitData/report%20project%203%20book%20Search%20Joy%20Albertini.pdf)





Strcuture: 
Root:
  project3Book : Scrapy (crawling)
     Crawled data in project3Book/project3Book/data/bookData3.json
  bookSearchUI : UI and 
  Solr-8.11.0 : solr
  Report (report and slides)


Scrapy  -----------------------------------------------------------
To run scrapy:
Cd to project3Book/project3Book/spiders

scrapy runspider bookSpider.py -o out.json

Solr --------------------------------------------------------------
To run solrL
Cd to solr-8.11.0 

bin/solr start -e cloud important should be started on default port 
8983

On question: now let's create a new collection for indexing documents 
in your 1-node cluster.
Please provide a name for your new collection: [gettingstarted] 
You can answer with bookTest2 so that you don't have to create 
a new collection


UI ----------------------------------------------------------------
I posted the UI on gitlab pages so that you don't have to download 
all dependencies needed to run the the UI, works perfectly with solr

https://joyalbertini.github.io/bookSearchUI/#/

If you want to run it you should go to in bookSearchUI/quasar-demo

$npm install : to install all dependencies 
$quasar dev : run the application in dev mode, work correctly

If you want the build 
$quasar build
But to run it you need to set up a server or use gitlab Pages as I did. 

 


