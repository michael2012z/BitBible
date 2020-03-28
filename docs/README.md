# Documentation

## Plan
- ~~Convert Sword modules into OSIS XML files~~
- ~~Convert OSIS XML files into Markdown files and upload to github.~~
- ~~Add NIV Markdown.~~
- Improve the presentation of verses in poem style.
- Develop curses based application to display text.
- ~~Handle key input.~~
- ~~Switch focus between windows.~~
- ~~Show a line in highlight, and move up and down.~~
- ~~Show a selected word in highlighted line, and move left and right.~~
- ~~Display the selected word of text window in dictionary window.~~
- ~~Dictionary~~
- - ~~Find and parse dictionary meta data file.~~
- - ~~Build word frequency list~~
- - ~~Seprate Vocabulary dictionary xml file into folders and files~~
- - ~~Display dictionary.~~
- ~~Display the explanation of the selected word in dictionary window.~~
- ~~Display bible and book list.~~
- Display commentary in application.



## History

### Feb 16, 2020
- Downloaded OSIS XML files from repo: https://github.com/gratis-bible/bible
- Converted the OSIS files into Markdown format
- Converted a set of HTML files for NIV into Markdown format

### Feb 22, 2020
- Downloaded Sword modules from official site: http://www2.crosswire.org/sword/modules/ModDisp.jsp?modType=Bibles
- Converted modules into OSIS XML files with Sword tool `mod2osis`
- Re-wrote Python code to convert OSIS files into Markdown format
- Failed to convert some OSIS files, need to debug.
- Markdown text need to be improved, like the verse titles of Psalms.

### Feb 29, 2020
- Debugged the failures in converting some OSIS files, like version AB. It turned out a broken module. Both mod2osis and pysword tools returned wrong texts while parsing the module.
- Different errors are among those problematic modules.
- Will not do more conversion works recently. Will containue to curses program.

### Mar 14, 2020
- Implement the highlight effect in text window.

### Mar 21, 2020
- Parsed Collins dictionary data, raw file was obtained from MDict community.
- Parsed Vocabulary dictionary data, raw file was obtained from MDict community.
- Build a new dictionary XML in own format. Will use it in BitBible.

### Mar 28, 2020
- Implemented book sellection. Now you can choose version, book and chapters.
- Integrated dictionary into BitBible. But the display effect is not good. Further improved is required.

