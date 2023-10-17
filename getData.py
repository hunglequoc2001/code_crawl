import git
from git import Repo
import os
from datetime import datetime
import javalang
import re
import json
def getRepo(repo,username):
    repo_url = f'https://github.com/{username}/{repo}.git'
    local_path = f'./repos/{repo}'
    # Clone the repository if it doesn't exist locally
    if not os.path.exists(local_path):
        x=1/0
    repo = git.Repo(local_path)
    return repo
def findJavafile(root,javafiles,depth=0):
    
    if depth>100:
        return 
    for file in root:
        if file.path.endswith(".java"):
            javafiles.append(file.path)
            
        elif file.type=='tree':
            depth+=1
            findJavafile(file,javafiles,depth)
def getSHAcommit(repo,files,time):
    sha=[]
    for file_path in files:
        file_history = []
        for commit in repo.iter_commits(paths=file_path):
            if int(commit.committed_date)< time:
                file_history.append(commit.hexsha)
                break
            file_history.append(commit.hexsha)
            # commit_info = {
            #     'commit_sha': commit.hexsha,
            #     'commit_message': commit.message.strip(),
            #     'commit_date': commit.committed_date,
            #     'parents': [],
            #     'file_content': None,
            # }

            # # Get the content of the file at this commit
            # try:
            #     file_content = repo.git.show(f"{commit.hexsha}:{file_path}")
            #     commit_info['file_content'] = file_content
                
            #     for parent in commit.parents:    
            #         try:
            #             commit_info['parents'].append(repo.git.show(f"{repo.hexsha}:{file_path}"))
            #         except:
            #             continue
            #     file_history.append(commit_info)
                
            #except git.GitCommandError:
                #pass  # File may not exist in this commit
        sha.append(file_history)
    return sha
def getMethod(method,content):
    method_lines=[]
    inside_method=False
    start_line_number=method.position[0]
    for line_number, line in enumerate(content.split("\n"), start=1):
    # Check if the current line starts the method
        if line_number == start_line_number:
            inside_method = True
            method_lines.append(line)
        elif inside_method:
            # Continue capturing lines until the method ends
            method_lines.append(line)
            if line.strip() == "}":
                break  # Exit the loop when the method ends
    
# Join the captured lines to reconstruct the method
    return '\n'.join(method_lines)
import re
def remove_html_tags(input_string):
    # Define the regular expression to match HTML tags
    html_tags_pattern = re.compile(r'<.*?>')
    
    # Use re.sub to replace HTML tags with an empty string
    cleaned_string = re.sub(html_tags_pattern, '', input_string)
    
    return cleaned_string
def parse_javadoc(input_string):
    # Regular expression to match Javadoc tags like {@tag content}
    tag_pattern = re.compile(r'\{@(.*?)\s(.*?)\}')
    
    def replace_tag(match):
        tag_name = match.group(1)
        tag_content = match.group(2)
        return get_replacement_for_tag(tag_name, tag_content)

    # Use the re.sub function to replace matched tags with their content
    parsed_string = re.sub(tag_pattern, replace_tag, input_string)
    return remove_html_tags(parsed_string
)

def get_replacement_for_tag(tag_name, tag_content):
    # Define replacement logic for specific tags
    if tag_name == "code":
        return tag_content  # Replace {@code ...} with its content
    
    else:
        # Handle other tags or return the tag as is
        return " "+tag_content+" "

def getDoc(docnode):
    if not docnode is  None:
        ret=""
        doc=javalang.javadoc.parse(docnode)
        # if doc.deprecated:
        #     return None
        # if len(doc.params)>0:
            
        #     ret+=f"The method receive "
        #     for param in doc.params:
        #         ret+=parse_javadoc(param[1])+", "
            
        ret+=parse_javadoc(doc.description)+" "
        # if not doc.return_doc is None:
        #     if parse_javadoc(doc.return_doc).startswith("return") or parse_javadoc(doc.return_doc).startswith("Return"):
        #         ret+="return "
        #     ret+="return "+parse_javadoc(doc.return_doc)
        
        return ret.replace("\n","")
    else:
        return None

def getNewmethod(repo,sha_list,javafiles):
    methods=[]
    docs=[]
    for file, sha in zip(javafiles,sha_list):
        new_method=[]
        new_doc=[]
        existed_method=[]
        if len(sha)>1:
            try:
                file_content = repo.git.show(f"{sha[-1]}:{file}")
                tree = javalang.parse.parse(file_content)
                for _,node in tree.filter(javalang.tree.MethodDeclaration):
                    existed_method.append(node.name)
            except Exception as e:
                print(e)
                continue
            for commithex in sha[:-1]:
                try:
                    file_content = repo.git.show(f"{commithex}:{file}")
                    tree = javalang.parse.parse(file_content)
                    for _,node in tree.filter(javalang.tree.MethodDeclaration):
                        if not node.name in existed_method:
                            
                            if  getDoc(node.documentation) != ""and node.body !=None and len(node.body)>=2:
                                if len(getDoc(node.documentation))>4:
                                    new_doc.append(getDoc(node.documentation))
                                    new_method.append(getMethod(node,file_content))

                                    existed_method.append(node.name)
                except Exception as e:
                    print(e)
        methods.append(new_method)
        docs.append(new_doc)
        #print(methods,docs)
    return methods,docs
import shutil
def writeData(username,reponame,java_files,methods,docs,out):
    data=[]
    for file,new_methods,new_docs in zip(java_files,methods,docs):
        for method,doc in zip(new_methods,new_docs):
            if doc ==None:
                continue
            data.append({
                'repo':username+"/"+reponame,
                'file':file,
                'source':method,
                'target':doc
            })
    # if data==[]:
    #     shutil.rmtree("./repos/"+reponame)
    with open(out,'a+')as f:
        for dt in data:
            f.write(json.dumps(dt)+"\n")

import shutil
def getData(reponame,username,time_unix=1609434000,output_file="./data.jsonl"):
    #get repo
    print("getting repo")
    try:
        repo=getRepo(reponame,username)
    except Exception as e:
        exception_message = str(e)
        print("Exception Message:", exception_message)
        return
    tree = repo.head.commit.tree
    #get javafiles
    java_files=[]
    print("extracting java files")
    findJavafile(tree,java_files)
    print("getting commit hex code")
    #get commit sha list
    sha=getSHAcommit(repo,java_files,time_unix)
    print('getting methods and documents')
    #get new method
    methods,docs=getNewmethod(repo,sha,java_files)
    print(docs)
    #write
    print("writing data file")
    writeData(username,reponame,java_files,methods,docs,output)
    #delete repo
    #shutil.rmtree("./repos/"+reponame)
    
    