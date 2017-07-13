# -*- coding: utf-8 -*-

from git import Repo


rorepo_working_tree_dir = u'/Users/ian/gmagon_projects/gmagon_all/files.gif.gmagon.com/'
repo = Repo(rorepo_working_tree_dir)
assert not repo.bare


print ('git status: \n %s' % repo.git.status())
print (repo.git.add('--all'))
print (repo.git.commit('-m "fix bugs"'))

origin=repo.remotes.origin
print (origin.push())
print ('end')

