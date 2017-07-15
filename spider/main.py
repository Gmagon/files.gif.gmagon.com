#!/usr/bin/python
# -*- coding: UTF-8 -*-

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
if len(diff) > 0:
    index.commit("my test", author=author, committer=committer)
    want_commit = True





