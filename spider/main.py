#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
#
from git import Actor, Repo

repo_path = u'/Users/ian/gmagon_projects/gmagon_all/files.gif.gmagon.com/'
repo_url = u'https://github.com/Gmagon/files.gif.gmagon.com.git'
repo = Repo(repo_path)

assert repo.bare == False # 版本库是否为空版本库

author = Actor("Ian", "ian@gmagon.com")
committer = Actor("Ian", "ian@gmagon.com")
want_add =  want_commit = False

#### 处理
index = repo.index

# 判断是否有新文件变化
untracked_files = repo.untracked_files # 版本库中未跟踪的文件列表
if len(untracked_files) > 0:
   index.add(untracked_files)
   want_add = True

# 判断是否有更改的文件
diff = index.diff(None)
if len(diff) > 0 or want_add:
    now = datetime.datetime.now()
    nowStr = now.strftime('%Y-%m-%d %H:%M:%S')

    git = repo.git
    git.commit('-am', 'this is test')

    #new_commit = index.commit("my test %s" % nowStr, author=author, committer=committer)
    #print (new_commit)

    want_commit = True

print (u'#检测是否需要上传到远程服务器.....')
if want_commit:
    origin=repo.remotes.origin

    def progress(op_code, cur_count, max_count=None, message=''):
        print (u'上传进度:', op_code, cur_count, max_count, message)

    print(u'git push')
    #print (origin.push(refspec='master:master', progress=progress))
    print ('git end')



