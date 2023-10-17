from method import crawlMethod
def main():
    time=1609434000 #data will crawl/created after creation of chat GPT (algorithm is sound but not complete)
    out='./data.jsonl'#output will have jsonl file
    reponame="keel"
    username ="Harium"
    crawler=crawlMethod(reponame,username)
    crawler.crawl(time,out)
if __name__=="__main__":
    main()