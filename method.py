from getData import getData
class crawlMethod:
    def __init__(self,reponame,username):
        self.reponame=reponame
        self.username=username
    def crawl(self,time=1609434000,out="./data.jsonl",delete=True):
        hex= getData(self.reponame,self.username,time,out)
        if delete:
            shutil.rmtree("./repos/"+self.reponame)
        return hex
