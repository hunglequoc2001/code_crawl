from getData import getData
class crawlMethod:
    def __init__(self,reponame,username):
        self.reponame=reponame
        self.username=username
    def crawl(self,time=1609434000,out="./data.jsonl"):
        getData(self.reponame,self.username,time,out)