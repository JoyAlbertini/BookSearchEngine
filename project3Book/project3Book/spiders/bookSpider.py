# Joy albertini

import scrapy

#           0     1      2      3       4      5      6    7
ACTIVE = [True, True, True, True, True, True, True, True, True]


class bookSpider(scrapy.Spider):
    name = 'bookSpider'

    # start urls are offset urls
    start_urls = ['https://directory.doabooks.org/recent-submissions?offset=',

                  'https://www.feedbooks.com/recent?locale=it&page=',
                  'https://www.feedbooks.com/recent?locale=fr&page=',
                  'https://www.feedbooks.com/recent?locale=es&page=',
                  'https://www.feedbooks.com/recent?locale=en&page=',

                  'https://www.bookdepository.com/bestsellers?searchLang=123&page=',
                  'https://www.bookdepository.com/bestsellers?searchLang=150&page=',
                  'https://www.bookdepository.com/bestsellers?searchLang=404&page=',
                  ]

    def parse(self, response):
        # ------ doaBooks [multiple language] ------ (20 per page)
        if response.url == self.start_urls[0] and ACTIVE[0]:
            return self.offsetLinkGenerator(self.start_urls[0], 5000, 0, 20, self.parseDoaBooksLinks, 'english')

        # ------ feedBooks [Italian] ------ (50 per page)
        elif response.url == self.start_urls[1] and ACTIVE[1]:
            return self.offsetLinkGenerator(self.start_urls[1], 50, 0, 1, self.parseFeedBooksLinks, 'italian')

        # ------ feedBooks [French] ------ (50 per page)
        elif response.url == self.start_urls[2] and ACTIVE[2]:
            return self.offsetLinkGenerator(self.start_urls[2], 50, 0, 1, self.parseFeedBooksLinks, 'french')

        # ------ feedBooks [Spanish] ------ (50 per page)
        elif response.url == self.start_urls[3] and ACTIVE[3]:
            return self.offsetLinkGenerator(self.start_urls[3], 50, 0, 1, self.parseFeedBooksLinks, 'spanish')

        # ------ feedBooks [English] ------ (50 per page)
        elif response.url == self.start_urls[4] and ACTIVE[4]:
            return self.offsetLinkGenerator(self.start_urls[4], 70, 0, 1, self.parseFeedBooksLinks, 'english')

        # ------ bookDepository [english]------ (30 per page)
        elif response.url == self.start_urls[5] and ACTIVE[5]:
            return self.offsetLinkGenerator(self.start_urls[5], 70, 0, 1,
                                            self.parseBookRepositoryLinks, 'english')

        # ------ bookDepository [German]------ (30 per page)
        elif response.url == self.start_urls[6] and ACTIVE[6]:
            return self.offsetLinkGenerator(self.start_urls[6], 50, 0, 1,
                                            self.parseBookRepositoryLinks, 'german')

        # ------ bookDepository [spanish]------ (30 per page)
        elif response.url == self.start_urls[7] and ACTIVE[7]:
            return self.offsetLinkGenerator(self.start_urls[7], 50, 0, 1,
                                            self.parseBookRepositoryLinks, 'spanish')

    # generate next link by augmenting an offset in the url, basically it takes an offsetUrl
    # which is an url that can be indexed by an integer, this function will start at an index
    # defined by (pageStartOffset)and will increase by a defined offset (offsetAddition) the
    # index url until reaching a max page  number bound (pageMaxOffset).

    # This function is reused by all the 3 domains so i pass the callback function that scrapy
    # should call for each domain (parse function).

    # The language is passed to the callback function using meta, needed because some url are
    # specified by a language (so has books only in that language)

    def offsetLinkGenerator(self, offsetUrl, pageMaxOffset, pageStartOffset,
                            offsetAddition, parseFunction, language):
        while pageStartOffset <= pageMaxOffset:
            yield scrapy.Request(offsetUrl + str(pageStartOffset), parseFunction, meta={'language': language})
            pageStartOffset += offsetAddition

    # DoaBooks ------------------- DoaBooks ------------------- DoaBooks ------------------- DoaBooks -----------------

    # get the links of each book entity in a page (defined by the link generator):
    # it extracts the link by taking the the images of the book covers and iterating over it.

    # this function will pass the book Link to the parse function
    def parseDoaBooksLinks(self, response):
        sourceUrl = "https://directory.doabooks.org"

        for bookLinkRelative in response.css('.image-link::attr("href")').getall():
            bookLinkFull = sourceUrl + bookLinkRelative
            # not possible to crawl this page --> full link is possible
            yield response.follow(bookLinkFull + "?show=full", self.parseDoaBooksData)

    # parse function will get the data inside the page regarding the book
    def parseDoaBooksData(self, response):
        book = bookObject()
        book.clearObjects()
        book.setBookLink(response.url)

        # structure ['dc.date.issued, 2021, 'dc.contributor.author' , J.K. Rowling ....]
        table = response.css('td::text').getall()

        parsedTable = []

        # some entity will have en_US, must be removed or the structure will
        # not have the above structure
        for x in range(len(table)):
            if (table[x].strip()) != "en_US":
                parsedTable.append(table[x])

        language = 'None'
        for i in range(1, len(parsedTable) - 1, 2):
            # dc.date.issued
            key = parsedTable[i - 1].strip()
            # 2021
            value = parsedTable[i].strip()

            if key == 'dc.date.issued':
                book.setYearOfPublication(value)
            elif key == 'dc.contributor.editor':
                if ',' in value:
                    # on site last name, name --> make it name, last name
                    dataAuthor = (value.strip()).split(',')
                    nameAuthor = dataAuthor[1].strip()
                    lastNameAuthor = dataAuthor[0].strip()
                    book.addAuthor(nameAuthor + ' ' + lastNameAuthor)
                else:
                    book.addAuthor(replaceChar(value, ',', ''))

            elif key == 'dc.contributor.author':
                if ',' in value:
                    # on site last name, name --> make it name, last name
                    dataAuthor = (value.strip()).split(',')
                    nameAuthor = dataAuthor[1].strip()
                    lastNameAuthor = dataAuthor[0].strip()
                    book.addAuthor(nameAuthor + ' ' + lastNameAuthor)
                else:
                    book.addAuthor(replaceChar(value, ',', ''))

            elif key == 'dc.description.abstract':
                book.setDescription(value),

                # description of book in the language specified
                # always below dc.description.abstract if present
            elif key == 'oapen.abstract.otherlanguage':
                # there is some inconsistent data
                if language != 'english' and language != 'None':
                    book.setDescription(value),
            elif key == 'dc.language':
                book.setLanguage(value),
                language = value.strip()
            elif key == 'dc.subject.classification':
                value = replaceChar(value, ':', ' ')
                book.setSubjects(value),
            elif key == 'dc.subject.other':
                book.setSubjects(value),
            elif key == 'dc.title':
                book.setTitle(value),
            else:
                book.addOtherData(value)

        # output the data out
        yield book.outputBook()

        del book

    # feedbooks --------- feedbooks --------- feedbooks --------- feedbooks --------- feedbooks --------- feedbooks ----

    # get the links of each book entity in a page (defined by the link generator):
    # it extracts the link by taking the book title
    # needs to pass the language to parse function, in order to save the language

    def parseFeedBooksLinks(self, response):
        sourceUrl = "https://www.feedbooks.com"
        for bookLinkRelative in response.css('.block__item-title::attr("href")').getall():
            bookLinkFull = sourceUrl + bookLinkRelative
            yield scrapy.Request(bookLinkFull, self.parseFeedBooksData,
                                 meta={'language': response.meta.get('language')})

    # parse function will get the data inside the page regarding the book
    def parseFeedBooksData(self, response):

        language = response.meta.get('language')
        book = bookObject()
        book.clearObjects()
        book.setBookLink(response.url)
        book.setTitle(response.css('.item__title::text').get().strip())
        book.setAuthors(cleanArraydata(response.css('.item__subtitles').css('.link::text').getall()))
        book.setDescription(' '.join(cleanArraydata(response.css('p::text').getall())))
        book.setSubjects(' '.join(cleanArraydata(response.css('.item__chips').css('a::text').getall())))
        book.setLanguage(language)
        data = response.css('.item-details__value::text').getall()
        yearOfPublication = ""

        if len(data) >= 3 and language != 'spanish':
            yearOfPublication = getYearFromDate(data[2])
        else:
            # spanish date parser
            dateFull = (data[2].strip()).split(" ")
            if len(dateFull) >= 5:
                yearOfPublication = (dateFull[4].strip())
        book.addOtherData(' '.join(cleanArraydata(data)))
        book.setYearOfPublication(yearOfPublication)
        yield book.outputBook()
        del book

    # bookDepository ------- bookDepository ------- bookDepository ------- bookDepository ------- bookDepository -------

    # Get the links of each book entity in a page (defined by the link generator):
    # it extracts the link by taking the book title
    # needs to pass the language to parse function, in order to save the language

    def parseBookRepositoryLinks(self, response):
        sourceUrl = 'https://www.bookdepository.com'
        for bookLinkRelative in response.css('.title').css('a::attr("href")').getall():
            bookLinkFull = sourceUrl + bookLinkRelative
            yield scrapy.Request(bookLinkFull, self.parseBookRepositoryData,
                                 meta={'language': response.meta.get('language')})

    # parse function will get the data inside the page regarding the book
    def parseBookRepositoryData(self, response):
        language = response.meta.get('language')
        book = bookObject()
        book.clearObjects()
        book.setBookLink(response.url)
        book.setTitle(response.css('h1::text').get())
        book.setDescription(' '.join(cleanArraydata(response.css('.item-excerpt::text').getall())))
        authors = cleanArraydata(response.css('.author-info').css('span::text').getall())
        for x in authors:
            x = replaceChar(x, ',', '')
            book.addAuthor(x)
        book.setYearOfPublication(getYearFromDate(response.xpath('//span[@itemprop="datePublished"]/text()').get()))
        book.setSubjects(' '.join(cleanArraydata(response.css('.breadcrumb')[0].css('a::text').getall())))

        book.setLanguage(language)
        book.addOtherData(' '.join(cleanArraydata((response.css('.biblio-info span::text').getall()))))
        yield book.outputBook()
        del book


# remove empty data in array, and trim the data
def cleanArraydata(data):
    cleanData = []
    for x in data:
        x = x.strip()
        if x != '':
            cleanData.append(x)
    return cleanData


# get the year from a date 19 11 2021
def getYearFromDate(date):
    yearOfPublication = "None"
    if date is not None:
        arr = date.strip().split()
        if len(arr) == 3:
            yearOfPublication = arr[2].strip()
    return yearOfPublication


# replace a character
def replaceChar(value, charToRemove, charToAdd):
    parsedValue = value
    # check if char is in the string
    if charToRemove in parsedValue:
        parsedValue = parsedValue.replace(charToRemove, charToAdd)
    return parsedValue


# create a book object to hold the data scraped.
class bookObject:
    bookLink = ''
    bookTitle = ''
    authors = []
    yearOfPublication = ''
    description = ''
    language = ''
    subjects = ""
    otherData = ''

    def setBookLink(self, book):
        self.bookLink = book

    def addAuthor(self, author):
        self.authors.append(author)

    def setAuthors(self, authors):
        self.authors = authors

    def setYearOfPublication(self, date):
        self.yearOfPublication = date

    def setDescription(self, desc):
        self.description = desc
        # remove multiple spaces
        self.description = ' '.join(self.description.split())

    def setLanguage(self, language):
        self.language = language.lower()

    def setSubjects(self, subject):
        self.subjects += ' ' + subject
        # remove multiple spaces
        self.subjects = ' '.join(self.subjects.split())

    def setTitle(self, title):
        self.bookTitle = title
        self.bookTitle = self.bookTitle.strip()

    def addOtherData(self, data):
        self.otherData += ' ' + data

    def clearObjects(self):
        self.bookLink = ''
        self.bookTitle = ''
        self.authors.clear()
        self.yearOfPublication = ''
        self.description = ''
        self.language = ''
        self.subjects = ''
        # check if a book date is between 2017 -2021

    def checkYearOfPublication(self):
        date = self.yearOfPublication
        return date == "2021" or date == "2020" or date == "2019" or date == "2018" or date == "2017"

    # output data that have at least Title, authors, year of publication between 2017-2021 and Title

    def checkOutputBook(self):
        # title authors and year must be defined and language
        if (self.bookTitle == '') or (len(self.authors) == 0) or \
                (not self.checkYearOfPublication() or (self.description == '') or (self.subjects == '')):
            return False
        else:
            return True

    # check if the language of the book is present in solr amd return the
    # appropriate suffix
    def computeSuffix(self, language):
        langToSuffix = {'arabic': '_txt_ar',
                        'armenien': '_txt_hy',
                        'bulgarian': '_txt_bg',
                        'catalan': '_txt_ca',
                        'czech': '_txt_cz',
                        'danish': '_txt_da',
                        'english': '_txt_en',
                        'german': '_txt_de',
                        'greek': '_txt_el',
                        'spanish': '_txt_es',
                        'estonian': '_txt_et',
                        'basque': '_txt_eu',
                        'persian': '_txt_fa',
                        'finnish': '_txt_fi',
                        'french': '_txt_fr',
                        'irish': '_txt_ga',
                        'galician': '_txt_gl',
                        'hindi': '_txt_hi',
                        'indonesian': '_txt_id',
                        'italian': '_txt_it',
                        'dutch': '_txt_nl',
                        'norwegian': '_txt_no',
                        'portuguese': '_txt_pt',
                        'russian': '_txt_ru',
                        'swedish': '_txt_sv',
                        'turkish': '_txt_tr'
                        }
        if language in langToSuffix.keys():
            return langToSuffix[language]
        else:
            return ''

    def outputBook(self):
        #  title authors and year must be present
        if self.checkOutputBook():
            # language must be present, and be to the selected one
            suffix_lang = self.computeSuffix(self.language)
            if suffix_lang != '':
                return {
                    'link': self.bookLink,
                    'language': self.language,
                    'yearOfPublication': self.yearOfPublication,
                    'authors': self.authors,
                    'title' + suffix_lang: self.bookTitle,
                    'allOtherData': self.yearOfPublication + ' ' + self.language + ' '
                                    + ' '.join(self.authors) + ' ' + self.otherData,
                    'subjects' + suffix_lang: self.subjects,
                    'description' + suffix_lang: self.description
                }
