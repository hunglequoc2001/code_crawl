# code_crawl
crawl code for code summarization dataset

Features:
- Crawl for Java only
- Time stamp required for crawling method later than that time 
- Get author names

Code input filter:
- Remove get/set method
- Remove method shorter than 3 code lines

Ground-truth filter:
- Javadoc for method
- Using first sentence of description only
- Remove in-line code tag such as {@code} or {@link} and keep the content
- Ground-truth length longer than 5 tokens and shorter than method itself

For quick start
- install libraries from 'requirements.txt'
- run python file from `experiment.py`
