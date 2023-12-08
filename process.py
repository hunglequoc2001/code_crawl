import javalang
import re
def getDocstring(doc):
    string=javalang.javadoc.parse(doc)
    ret=string.description
    index = ret.find(". ")
    index=min(index,ret.find(".\n"))
    if index == -1:
        return ret
    else:
        return ret[:index]
    # for param in doc.params:
    #     docstring+="\n"+"@param "+ param[0]+"\t"+param[1]
    # if doc.return_doc !=None:
    #     docstring+="\n"+"@return"+ doc.return_doc
def rm_link(text):
    # Define a regular expression to match and extract {@link ...} tags
    pattern = re.compile(r'\{@link(.*?)\}')

    # Use the findall method to extract all matching {@link ...} tags
    matches = pattern.findall(text)

    # Replace each {@link ...} tag with the extracted content
    for match in matches:
        text = text.replace(f'{{@link{match}}}', match)

    return text
from english_words import get_english_words_set

def isEnglish(doc):
    cnt=0
    doc_split=doc.split(" ")
    for word in doc_split:
        word=word.replace(" ","").replace(".","").replace(",","").replace("\"","").replace("\'","")
        if all(char.isalpha() and ord(char) < 128 for char in word):
            cnt+=1
    if 2*cnt>=len(doc_split):
        return True
    else:
        print(doc)
        return False
def rm_code(text):
    # Define a regular expression to match and extract {@link ...} tags
    pattern = re.compile(r'\{@code(.*?)\}')

    # Use the findall method to extract all matching {@link ...} tags
    matches = pattern.findall(text)

    # Replace each {@link ...} tag with the extracted content
    for match in matches:
        text = text.replace(f'{{@code{match}}}', match)

    return text
def rm_tag(string):
    """Removes any substring similar to `{@....}` from the given string.

    Args:
        string: A string.

    Returns:
        A string with the substrings removed.
    """

    # Create a regular expression to match the substrings.
    regex = re.compile(r'\{@[^\}]+\}')

    # Remove all matches from the string.
    return regex.sub('', string)
def rm_html(string):
    """Removes all HTML tags from the given string.

    Args:
        string: A string.

    Returns:
        A string with the HTML tags removed.
    """

    # Create a regular expression to match the HTML tags.
    regex = re.compile(r'<[^>]+>')

    # Remove all matches from the string.
    return regex.sub('', string)
def CSN_process(doc):
    doc = getDocstring(doc)
    doc=rm_link(doc)
    doc=rm_code(doc)
    doc=rm_tag(doc)
    doc=rm_html(doc)
    return doc
