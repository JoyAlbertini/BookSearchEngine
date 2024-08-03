# Book Search Engine
<img src="gitData/BookSearch.png" alt="Book Search Logo" width="300" height="300">
This project comprises several components including a Scrapy crawler, a Solr server setup, and a UI. It is designed to crawl, index, and search book data efficiently.

[Overview video](TODO)

## Features
- **Multiple languages**: Supports searching in multiple languages, applying Solr pipeline to remove stop words, stemming, etc.
- **Operators**: Supports complex queries through UI elements called operators, which are essentially a reskin of Solr's querying language.
- **Fast querying and retrieval**
- **Scraping data** from various sources

## Project Structure

```
Root/
├── project3Book/         # Scrapy for crawling
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

The scraper extracts data from the following sources:
- [DOABooks](https://directory.doabooks.org/recent-submissions?offset=0)
- [Feedbooks](https://market.feedbooks.com/recent)
- [Book Depository](https://www.bookdepository.com/bestsellers?searchLang=123&page=0) (closed)

### Solr - Search Platform
This project uses **Solr 8.11.0** as the search engine. Use the distributed code as some settings have been modified (refer to the guide for details).

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
   - Provide the collection name as `bookTest2` to use the example scraped data.

### UI - User Interface (Quasar/Vue/Vuex)

The UI is hosted on GitLab Pages to avoid local dependency setup (needs to run the application on localhost:8983):

🔗 [Book Search UI](https://joyalbertini.github.io/bookSearchUI/#/)

- Quasar 2.0.0 
- Vue 3.2 
- Vuex 4

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
   Note: Running the build locally requires setting up a server or using GitLab Pages.

## Guide/Report
For more detailed information, refer to the [Guide PDF](gitData/report%20project%203%20book%20Search%20Joy%20Albertini.pdf).

---

### Additional Information

#### Solr Customizations
- **CORS**: Disabled CORS protection for direct queries.
- **URI Size**: Increased `maxRequestHeaderSize` in `jetty.xml` to handle long queries.

#### Query Strategy
- **Base Query**: Defined in `bookSearchUI/quasar-demo/src/store/solr.js`.
- **ORed Words**: Increases recall by ORing all words split by space in the query.
- **Field Boosts**: Important fields like `subjects` and `title` have higher boosts.

#### Multiple Languages
- **Dynamic Fields**: Uses Solr dynamic fields with language-specific suffixes (`_txt_en`, `_txt_it`).
- **Querying**: Evaluates queries across all supported languages, leading to long queries.

