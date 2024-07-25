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

 


