## Merge from master (CScarame)

1. Pull changes to local repository
```
git remote add upstream https://github.com/CScarame/Fourthbot.git
```
You only have to do this once to check it use ` git remote -v`

Then...
```
git fetch upstream/master
git checkout master
git merge upstream/master
```
2. Push changes from local to your github repository

```
git push
```

## Prep a pull request to make changes to CScarame repository
```
git push
```
THis is to push the changes you made.
Go to github.com and click on one of the many "New Pull request buttons"