from method import crawlMethod
import json

def main():
    time=1609434000 #data will crawl/created after creation of chat GPT (algorithm is sound but not complete)
    out='./data.jsonl'#output will have jsonl file
    
    repos=[]
    with open("./repos_list.txt","r") as file:
        for line in file.readlines():
            repos.append(line.strip())
    for repo in repos:
        username,reponame=repo.split("/")
        crawler=crawlMethod(reponame,username)
        crawler.crawl(time=time,out=out)
if __name__=="__main__":
    main()