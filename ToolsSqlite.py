import os, sqlite3, re, config
from BiblesSqlite import BiblesSqlite
from BibleVerseParser import BibleVerseParser

class VerseData:

    def __init__(self, filename):
        # connect bibles.sqlite
        self.database = os.path.join("marvelData", "data", "{0}.data".format(filename))
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def getContent(self, bcvTuple):
        query = "SELECT Scripture FROM Bible WHERE Book=? AND Chapter=? AND Verse=?"
        self.cursor.execute(query, bcvTuple)
        content = self.cursor.fetchone()
        if not content:
            return "[not applicable]"
        else:
            return content[0]


class CrossReferenceSqlite:

    def __init__(self):
        # connect bibles.sqlite
        self.database = os.path.join("marvelData", "cross-reference.sqlite")
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def bcvToVerseReference(self, b, c, v):
        return BibleVerseParser(config.parserStandarisation).bcvToVerseReference(b, c, v)

    def scrollMapper(self, bcvTuple):
        query = "SELECT Information FROM ScrollMapper WHERE Book=? AND Chapter=? AND Verse=?"
        self.cursor.execute(query, bcvTuple)
        information = self.cursor.fetchone()
        if not information:
            return "[not applicable]"
        else:
            return information[0]

    def tske(self, bcvTuple):
        query = "SELECT Information FROM TSKe WHERE Book=? AND Chapter=? AND Verse=?"
        self.cursor.execute(query, bcvTuple)
        information = self.cursor.fetchone()
        if not information:
            return "[not applicable]"
        else:
            return information[0]


class ImageSqlite:

    def __init__(self):
        # connect images.sqlite
        self.database = os.path.join("marvelData", "images.sqlite")
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def exportImage(self, module, entry):
        query = "SELECT image FROM {0} WHERE path = ?".format(module)
        entry = "{0}_{1}".format(module, entry)
        self.cursor.execute(query, (entry,))
        information = self.cursor.fetchone()
        if information:
            htmlImageFolder = os.path.join("htmlResources", "images")
            if not os.path.isdir(htmlImageFolder):
                os.mkdir(htmlImageFolder)
            imageFolder = os.path.join(htmlImageFolder, module)
            if not os.path.isdir(imageFolder):
                os.mkdir(imageFolder)
            imageFilePath = os.path.join(imageFolder, entry)
            if not os.path.isfile(imageFilePath):
                imagefile = open(imageFilePath, "wb")
                imagefile.write(information[0])
                imagefile.close()


class IndexesSqlite:

    def __init__(self):
        # connect images.sqlite
        self.database = os.path.join("marvelData", "indexes.sqlite")
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.setResourceList()

    def __del__(self):
        self.connection.close()

    def setResourceList(self):
        self.topicList = [
            ("HIT", "Hitchcock's New and Complete Analysis of the Bible"),
            ("NAV", "Nave's Topical Bible"),
            ("TCR", "Thompson Chain References"),
            ("TNT", "Torrey's New Topical Textbook"),
            ("TOP", "Topical Bible"),
            ("EXLBT", "Search ALL Topical References")
        ]
        self.dictionaryList = [
            ("AMT", "American Tract Society Dictionary"),
            ("BBD", "Bridgeway Bible Dictionary"),
            ("BMC", "Freeman's Handbook of Bible Manners and Customs"),
            ("BUC", "Buck's A Theological Dictionary"),
            ("CBA", "Companion Bible Appendices"),
            ("DRE", "Dictionary Of Religion And Ethics"),
            ("EAS", "Easton's Illustrated Bible Dictionary"),
            ("FAU", "Fausset's Bible Dictionary"),
            ("FOS", "Bullinger's Figures of Speech"),
            ("HBN", "Hitchcock's Bible Names Dictionary"),
            ("MOR", "Morrish's Concise Bible Dictionary"),
            ("PMD", "Poor Man's Dictionary"),
            ("SBD", "Smith's Bible Dictionary"),
            ("USS", "Annals of the World"),
            ("VNT", "Vine's Expository Dictionary of New Testament Words")
        ]
        self.encyclopediaList = [
            ("DAC", "Hasting's Dictionary of the Apostolic Church"),
            ("DCG", "Hasting's Dictionary Of Christ And The Gospels"),
            ("HAS", "Hasting's Dictionary of the Bible"),
            ("ISB", "International Standard Bible Encyclopedia"),
            ("KIT", "Kitto's Cyclopedia of Biblical Literature"),
            ("MSC", "McClintock & Strong's Cyclopedia of Biblical Literature")
        ]

    def getAllIndexes(self, bcvTuple):
        indexList = ["exlbp", "exlbl", "exlbt", "dictionaries", "encyclopedia"]
        indexItems = [
            ("Characters", self.searchCharacters()),
            ("Locations", self.searchLocations()),
            ("Topics", self.searchTopics()),
            ("Dictionaries", self.searchDictionaries()),
            ("Encyclopedia", self.searchEncyclopedia())
        ]
        content = ""
        for counter, index in enumerate(indexList):
            content += "<h2>{0}</h2>".format(indexItems[counter][0])
            content += self.getContent(index, bcvTuple)
            content += "<p>{0}</p>".format(indexItems[counter][1])
        return content

    def searchCharacters(self):
        content = "<button class='feature' onclick='document.title={0}_command:::SEARCHTOOL:::EXLBP:::{0}'>search for a character</button>".format('"')
        content += "<br><button class='feature' onclick='document.title={0}_command:::SEARCHTOOL:::HBN:::{0}'>search for a name & its meaning</button>".format('"')
        return content

    def searchLocations(self):
        return "<button class='feature' onclick='document.title={0}_command:::SEARCHTOOL:::EXLBL:::{0}'>search for a location</button>".format('"')

    def searchTopics(self):
        action = "searchResource(this.value)"
        optionList = [("", "[search a topical reference]")] + self.topicList
        return self.formatSelectList(action, optionList)

    def searchDictionaries(self):
        action = "searchResource(this.value)"
        optionList = [("", "[search a dictionary]")] + self.dictionaryList
        return self.formatSelectList(action, optionList)

    def searchEncyclopedia(self):
        action = "searchResource(this.value)"
        optionList = [("", "[search an encyclopeida]")] + self.encyclopediaList
        return self.formatSelectList(action, optionList)

    def formatSelectList(self, action, optionList):
        selectForm = "<select onchange='{0}'>".format(action)
        for value, description in optionList:
            selectForm += "<option value='{0}'>{1}</option>".format(value, description)
        selectForm += "</select>"
        return selectForm

    def getContent(self, table, bcvTuple):
        query = "SELECT Information FROM {0} WHERE Book = ? AND Chapter = ? AND Verse = ?".format(table)
        self.cursor.execute(query, bcvTuple)
        content = self.cursor.fetchone()
        if not content:
            return "[not applicable]"
        else:
            if table == "dictionaries" or table == "encyclopedia":
                return "<table>{0}</table>".format(content[0])
            else:
                return content[0]


class SearchSqlite:

    def __init__(self):
        # connect images.sqlite
        self.database = os.path.join("marvelData", "search.sqlite")
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def getContent(self, module, entry):
        query = "SELECT link FROM {0} WHERE EntryID = ?".format(module)
        self.cursor.execute(query, (entry,))
        content = self.cursor.fetchone()
        if not content:
            return "[not found]"
        else:
            return content[0]

    def getSimilarContent(self, module, entry):
        query = "SELECT link FROM {0} WHERE EntryID LIKE ? AND EntryID != ?".format(module)
        self.cursor.execute(query, ("%{0}%".format(entry), entry))
        contentList = [m[0] for m in self.cursor.fetchall()]
        if not contentList:
            return "[not found]"
        else:
            return "<br>".join(contentList)


class LexiconData:

    def __init__(self):
        # connect lexicon.data
        self.database = os.path.join("marvelData", "data", "lexicon.data")
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def getLexiconList(self):
        t = ("table",)
        query = "SELECT name FROM sqlite_master WHERE type=? ORDER BY name"
        self.cursor.execute(query, t)
        versions = self.cursor.fetchall()
        exclude = ("Details")
        return [version[0] for version in versions if not version[0] in exclude]

    def getSelectForm(self, lexiconList, entry):
        lexiconName = {
            "SECE": "Strong's Exhaustive Concordance [Enhanced]",
            "BDB": "Brown-Driver-Briggs Hebrew-English Lexicon",
            "LSJ": "Liddell-Scott-Jones Greek-English Lexicon",
            "TBESH": "Tyndale Brief lexicon of Extended Strongs for Hebrew",
            "TBESG": "Tyndale Brief lexicon of Extended Strongs for Greek",
            "MGLNT": "Manual Greek Lexicon of the New Testament",
            "Mounce": "Mounce Concise Greek-English Dictionary",
            "Thayer": "Thayer's Greek-English Lexicon",
            "LXX": "LXX Lexicon",
            "LCT": "新舊約字典彙編",
            "Morphology": "Hebrew & Greek Analytical Lexicon",
            "ConcordanceBook": "Concordance (sorted by book)",
            "ConcordanceMorphology": "Concordance (sorted by morphology)",
            "BDAG": "BDAG (3rd ed.)",
            "LN": "Louw-Nida Greek Lexicon",
            "LGNTDF": "Levinsohn's Greek New Testament Discourse Features",
        }
        selectForm = '<p><form action=""><select id="{0}" name="{0}" onchange="lexicon(this.value, this.id)"><option value="">More lexicons HERE</option>'.format(entry)
        for lexicon in lexiconList:
            selectForm += '<option value="{0}">{1}</option>'.format(lexicon, lexiconName[lexicon])
        selectForm += '</select></form></p>'
        return selectForm

    def lexicon(self, module, entry):
        lexiconList = self.getLexiconList()
        if module in lexiconList:
            query = "SELECT Information FROM {0} WHERE EntryID = ?".format(module)
            self.cursor.execute(query, (entry,))
            information = self.cursor.fetchone()
            contentText = "<h2>{0} - {1}</h2>".format(module, entry)
            contentText += "<p>{0}</p>".format(self.getSelectForm([m for m in lexiconList if not m == module], entry))
            if not information:
                return contentText+"[not found]"
            else:
                contentText += information[0]
                # deal with images
                imageList = [m for m in re.findall('src="getImage\.php\?resource=([^"]*?)&id=([^"]*?)"', contentText)]
                if imageList:
                    imageSqlite = ImageSqlite()
                    for (imgModule, imgEntry) in imageList:
                        imageSqlite.exportImage(imgModule, imgEntry)
                    del imageSqlite
                contentText = re.sub('src="getImage\.php\?resource=([^"]*?)&id=([^"]*?)"', r'src="images/\1/\1_\2"', contentText)
                contentText = re.sub("src='getImage\.php\?resource=([^']*?)&id=([^']*?)'", r"src='images/\1/\1_\2'", contentText)
                return contentText
        else:
            return "INVALID_COMMAND_ENTERED"


class DictionaryData:

    def __init__(self):
        # connect images.sqlite
        self.database = os.path.join("marvelData", "data", "dictionary.data")
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def getContent(self, entry):
        query = "SELECT content FROM Dictionary WHERE path = ?"
        self.cursor.execute(query, (entry,))
        content = self.cursor.fetchone()
        if not content:
            return "[not found]"
        else:
            contentText = content[0]

            # deal with images
            imageList = [m for m in re.findall('src="getImage\.php\?resource=([^"]*?)&id=([^"]*?)"', contentText)]
            if imageList:
                imageSqlite = ImageSqlite()
                for (imgModule, imgEntry) in imageList:
                    imageSqlite.exportImage(imgModule, imgEntry)
                del imageSqlite
            contentText = re.sub('src="getImage\.php\?resource=([^"]*?)&id=([^"]*?)"', r'src="images/\1/\1_\2"', contentText)
            contentText = re.sub("src='getImage\.php\?resource=([^']*?)&id=([^']*?)'", r"src='images/\1/\1_\2'", contentText)

            abb = entry[:3]
            moduleName = dict(IndexesSqlite().dictionaryList)[abb]
            searchButton = "&ensp;<button class='feature' onclick='document.title=\"_command:::SEARCHTOOL:::{0}:::\"'>search</button>".format(abb)
            return "<p><b>{0}</b> {1}</p>{2}".format(moduleName, searchButton, contentText)


class EncyclopediaData:

    def __init__(self):
        # connect images.sqlite
        self.database = os.path.join("marvelData", "data", "encyclopedia.data")
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def getContent(self, module, entry):
        query = "SELECT content FROM {0} WHERE path = ?".format(module)
        self.cursor.execute(query, (entry,))
        content = self.cursor.fetchone()
        if not content:
            return "[not found]"
        else:
            contentText = content[0]

            # deal with images
            imageList = [m for m in re.findall('src="getImage\.php\?resource=([^"]*?)&id=([^"]*?)"', contentText)]
            if imageList:
                imageSqlite = ImageSqlite()
                for (imgModule, imgEntry) in imageList:
                    imageSqlite.exportImage(imgModule, imgEntry)
                del imageSqlite
            contentText = re.sub('src="getImage\.php\?resource=([^"]*?)&id=([^"]*?)"', r'src="images/\1/\1_\2"', contentText)
            contentText = re.sub("src='getImage\.php\?resource=([^']*?)&id=([^']*?)'", r"src='images/\1/\1_\2'", contentText)

            moduleName = dict(IndexesSqlite().encyclopediaList)[module]
            searchButton = "&ensp;<button class='feature' onclick='document.title=\"_command:::SEARCHTOOL:::{0}:::\"'>search</button>".format(module)
            return "<p><b>{0}</b> {1}</p>{2}".format(moduleName, searchButton, contentText)


class WordData:

    def __init__(self):
        # connect images.sqlite
        self.database = os.path.join("marvelData", "data", "word.data")
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def getContent(self, testament, entry):
        query = "SELECT Information FROM {0} WHERE EntryID = ?".format(testament)
        if testament == "NT":
            entryID = "{0:06d}".format(int(entry))
        else:
            entryID = entry
        self.cursor.execute(query, (entryID,))
        content = self.cursor.fetchone()
        if not content:
            return "[not found]"
        else:
            return content[0]


class ExlbData:

    def __init__(self):
        # connect images.sqlite
        self.database = os.path.join("marvelData", "data", "exlb.data")
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def getContent(self, module, entry):
        query = "SELECT content FROM {0} WHERE path = ?".format(module)
        self.cursor.execute(query, (entry,))
        content = self.cursor.fetchone()
        if not content:
            return "[not found]"
        else:
            if module == "exlbl":
                content = re.sub('href="getImage\.php\?resource=([^"]*?)&id=([^"]*?)"', r'href="javascript:void(0)" onclick="openImage({0}\1{0},{0}\2{0})"'.format("'"), content[0])
                return content.replace("[MYGOOGLEAPIKEY]", config.myGoogleApiKey)
            else:
                moduleName = {
                    "exlbp": "Exhaustive Library of Bible People",
                    "exlbl": "Exhaustive Library of Bible Locations",
                    "exlbt": "Exhaustive Library of Bible Topics",
                }
                searchButton = "&ensp;<button class='feature' onclick='document.title=\"_command:::SEARCHTOOL:::{0}:::\"'>search</button>".format(module)
                return "<p><b>{0}</b> {1}</p>{2}".format(moduleName[module], searchButton, content[0])


class Commentary:

    def __init__(self, text):
        self.text = text
        if self.text in self.getCommentaryList():
            self.database = os.path.join("marvelData", "commentaries", "c{0}.commentary".format(text))
            self.connection = sqlite3.connect(self.database)
            self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def bcvToVerseReference(self, b, c, v):
        return BibleVerseParser(config.parserStandarisation).bcvToVerseReference(b, c, v)

    def formCommentaryTag(self, commentary):
        return "<ref onclick='document.title=\"_commentary:::{0}\"' onmouseover='commentaryName(\"{0}\")'>".format(commentary)

    def formBookTag(self, b):
        bookAbb = self.bcvToVerseReference(b, 1, 1)[:-4]
        return "<ref onclick='document.title=\"_commentary:::{0}.{1}\"' onmouseover='bookName(\"{2}\")'>".format(self.text, b, bookAbb)

    def formChapterTag(self, b, c):
        return "<ref onclick='document.title=\"_commentary:::{0}.{1}.{2}\"' onmouseover='document.title=\"_info:::Chapter {2}\"'>".format(self.text, b, c)

    def formVerseTag(self, b, c, v):
        verseReference = self.bcvToVerseReference(b, c, v)
        return "<ref id='v{0}.{1}.{2}' onclick='document.title=\"COMMENTARY:::{3}:::{4}\"' onmouseover='document.title=\"_instantVerse:::{3}:::{0}.{1}.{2}\"' ondblclick='document.title=\"_commentary:::{3}.{0}.{1}.{2}\"'>".format(b, c, v, self.text, verseReference)

    def getCommentaryList(self):
        commentaryFolder = os.path.join("marvelData", "commentaries")
        commentaryList = [f[1:-11] for f in os.listdir(commentaryFolder) if os.path.isfile(os.path.join(commentaryFolder, f)) and f.endswith(".commentary")]
        return commentaryList

    def getCommentaries(self):
        commentaryList = self.getCommentaryList()
        commentaries = " ".join(["{0}<button class='feature'>{1}</button></ref>".format(self.formCommentaryTag(commentary), commentary) for commentary in commentaryList])
        return commentaries

    def getBookList(self):
        query = "SELECT DISTINCT Book FROM Commentary ORDER BY Book"
        self.cursor.execute(query)
        return [book[0] for book in self.cursor.fetchall()]

    def getBooks(self):
        bookList = self.getBookList()
        return " ".join(["{0}<button class='feature'>{1}</button></ref>".format(self.formBookTag(book), self.bcvToVerseReference(book, 1, 1)[:-4]) for book in bookList])

    def getChapterList(self, b=config.commentaryB):
        t = (b,)
        query = "SELECT DISTINCT Chapter FROM Commentary WHERE Book=? ORDER BY Chapter"
        self.cursor.execute(query, t)
        return [chapter[0] for chapter in self.cursor.fetchall()]

    def getChapters(self, b=config.commentaryB):
        chapterList = self.getChapterList(b)
        return " ".join(["{0}{1}</ref>".format(self.formChapterTag(b, chapter), chapter) for chapter in chapterList])

    def getVerseList(self, b, c):
        biblesSqlite = BiblesSqlite()
        verseList = biblesSqlite.getVerseList(b, c, "KJV")
        del biblesSqlite
        return verseList

    def getVerses(self, b=config.commentaryB, c=config.commentaryC):
        verseList = self.getVerseList(b, c)
        return " ".join(["{0}{1}</ref>".format(self.formVerseTag(b, c, verse), verse) for verse in verseList])

    def getMenu(self, command):
        if self.text in self.getCommentaryList():
            mainVerseReference = self.bcvToVerseReference(config.commentaryB, config.commentaryC, config.commentaryV)
            menu = "<ref onclick='document.title=\"COMMENTARY:::{0}:::{1}\"'>&lt;&lt;&lt; Go to {0} - {1}</ref>".format(config.commentaryText, mainVerseReference)
            menu += "<hr><b>Commentaries:</b> {0}".format(self.getCommentaries())
            items = command.split(".", 3)
            text = items[0]
            if not text == "":
                # i.e. text specified; add book menu
                menu += "<hr><b>Selected Commentary:</b> <span style='color: brown;' onmouseover='commentaryName(\"{0}\")'>{0}</span>  <button class='feature' onclick='document.title=\"COMMENTARY:::{0}:::{1}\"'>open {1} in {0}</button>".format(self.text, mainVerseReference)
                menu += "<hr><b>Books:</b> {0}".format(self.getBooks())
                bcList = [int(i) for i in items[1:]]
                if bcList:
                    check = len(bcList)
                    if check >= 1:
                        # i.e. book specified; add chapter menu
                        menu += "<hr><b>Selected book:</b> <span style='color: brown;' onmouseover='bookName(\"{0}\")'>{0}</span>".format(self.bcvToVerseReference(bcList[0], 1, 1)[:-4])
                        menu += "<hr><b>Chapters:</b> {0}".format(self.getChapters(bcList[0]))
                    if check >= 2:
                        # i.e. both book and chapter specified; add verse menu
                        menu += "<hr><b>Selected chapter:</b> <span style='color: brown;' onmouseover='document.title=\"_info:::Chapter {0}\"'>{0}</span>".format(bcList[1])
                        menu += "<hr><b>Verses:</b> {0}".format(self.getVerses(bcList[0], bcList[1]))
                    if check == 3:
                        menu += "<hr><b>Selected verse:</b> <span style='color: brown;' onmouseover='document.title=\"_instantVerse:::{0}:::{1}.{2}.{3}\"'>{3}</span> <button class='feature' onclick='document.title=\"COMMENTARY:::{0}:::{4}\"'>open HERE</button>".format(self.text, bcList[0], bcList[1], bcList[2], mainVerseReference)
            return menu
        else:
            return "INVALID_COMMAND_ENTERED"

    def getContent(self, verse):
        if self.text in self.getCommentaryList():
            b, c, v = verse
            chapter = "<h2>{0}{1}</ref></h2>".format(self.formChapterTag(b, c), self.bcvToVerseReference(b, c, v).split(":", 1)[0])
            query = "SELECT Scripture FROM Commentary WHERE Book=? AND Chapter=?"
            self.cursor.execute(query, verse[:-1])
            scripture = self.cursor.fetchone()
            chapter += re.sub('onclick="luV\(([0-9]+?)\)"', r'onclick="luV(\1)" onmouseover="qV(\1)" ondblclick="mV(\1)"', scripture[0])
            if not scripture:
                return "[No content is found for this chapter!]"
            else:
                return "<div>{0}</div>".format(chapter)
        else:
            return "INVALID_COMMAND_ENTERED"


class BookData:

    def __init__(self):
        # connect book.data
        self.database = os.path.join("marvelData", "data", "book.data")
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def getMenu(self, module=""):
        bookList = self.getBookList()
        if module == "":
            module = config.book
        if module in dict(bookList).keys():
            books = self.formatSelectList("listBookTopic(this.value)", bookList, module)
            topicList = self.getTopicList(module)
            topics = "<br>".join(["<ref onclick='document.title=\"BOOK:::{0}:::{1}\"'>{1}</ref>".format(module, topic) for topic in topicList])
            config.book = module
            return "<p>{0} &ensp;<button class='feature' onclick='document.title=\"_command:::SEARCHBOOK:::{1}:::\"'>search</button></p><p>{2}</p>".format(books, module, topics)
        else:
            return "INVALID_COMMAND_ENTERED"

    def getBookList(self):
        t = ("table",)
        query = "SELECT name FROM sqlite_master WHERE type=? ORDER BY name"
        self.cursor.execute(query, t)
        versions = self.cursor.fetchall()
        exclude = ("Details")
        return [(version[0], version[0]) for version in versions if not version[0] in exclude]

    def getTopicList(self, module):
        query = "SELECT DISTINCT Topic FROM {0} ORDER BY Topic".format(module)
        self.cursor.execute(query)
        return [topic[0] for topic in self.cursor.fetchall()]

    def getSearchedMenu(self, module, searchString):
        bookList = self.getBookList()
        if module in dict(bookList).keys():
            books = self.formatSelectList("listBookTopic(this.value)", bookList, module)
            topicList = self.getSearchedTopicList(module, searchString)
            topics = "<br>".join(["<ref onclick='document.title=\"BOOK:::{0}:::{1}\"'>{1}</ref>".format(module, topic) for topic in topicList])
            config.book = module
            return "<p>{0} &ensp;<button class='feature' onclick='document.title=\"_command:::SEARCHBOOK:::{1}:::\"'>search</button></p><p>{2}</p>".format(books, module, topics)
        else:
            return "INVALID_COMMAND_ENTERED"

    def getSearchedTopicList(self, module, searchString):
        searchString = "%{0}%".format(searchString)
        query = "SELECT DISTINCT Topic FROM {0} WHERE Topic LIKE ? OR Note LIKE ? ORDER BY Topic".format(module)
        self.cursor.execute(query, (searchString, searchString))
        return [topic[0] for topic in self.cursor.fetchall()]

    def formatSelectList(self, action, optionList, default):
        selectForm = "<select onchange='{0}'>".format(action)
        for value, description in optionList:
            if value == default:
                selectForm += "<option value='{0}' selected='selected'>{1}</option>".format(value, description)
            else:
                selectForm += "<option value='{0}'>{1}</option>".format(value, description)
        selectForm += "</select>"
        return selectForm

    def getContent(self, module, entry):
        query = "SELECT Note FROM {0} WHERE Topic=?".format(module)
        self.cursor.execute(query, (entry,))
        content = self.cursor.fetchone()
        if not content:
            return "[not applicable]"
        else:
            config.book = module
            content = content[0]
            if config.bookSearchString and not config.bookSearchString == "z":
                content = re.sub("("+config.bookSearchString+")", r"<z>\1</z>", content, flags=re.IGNORECASE)
                p = re.compile("(<[^<>]*?)<z>(.*?)</z>", flags=re.M)
                s = p.search(content)
                while s:
                    content = re.sub(p, r"\1\2", content)
                    s = p.search(content)
            return content
