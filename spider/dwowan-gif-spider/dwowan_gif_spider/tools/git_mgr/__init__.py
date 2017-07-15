# -*- coding: utf-8 -*-
# coding：UTF-8
import datetime


from git import Actor, Repo
def runGit(working_dir):
    """执行Git提交及push动作"""
    rorepo_working_tree_dir = working_dir
    repo = Repo(rorepo_working_tree_dir)
    gitShell = repo.git


    assert repo.bare == False  # 版本库是否为空版本库

    print ('git status: \n %s' % repo.git.status())

    author = Actor("Ian", "ian@gmagon.com")
    committer = Actor("Ian", "ian@gmagon.com")
    want_add = want_commit = False


    index = repo.index

    # 检查是否有新增的文件
    print (u'#检测是否有新增的文件.....')
    untracked_files = repo.untracked_files  # 版本库中未跟踪的文件列表
    if len(untracked_files) > 0:
        #print (index.add(untracked_files))
        gitShell.add(untracked_files)

        want_add = True

    # 检查是否有变化的文件
    print (u'#检测是否有修改的文件.....')
    diffObj = index.diff(None)
    if len(diffObj) > 0 or want_add:
        now = datetime.datetime.now()
        nowStr = now.strftime('%Y-%m-%d %H:%M:%S')

        commit_msg = '%s dwowan gif update [fileChanges=%d] [fileAdd=%d]' \
                            % (nowStr, len(diffObj), len(untracked_files))

        #print (index.commit(commit_msg))
        gitShell.commit('-am', '\"' + commit_msg + '\"')

        want_commit = True

    # 检测是否需要push到远程服务器中
    print (u'#检测是否需要上传到远程服务器.....')
    if want_commit:
        origin=repo.remotes.origin

        def progress(op_code, cur_count, max_count=None, message=''):
            print (u'上传进度:')
            print (op_code, cur_count, max_count, message)

        print(u'git push')
        print (origin.push(refspec='master:master', progress=progress))
        print ('git end')

