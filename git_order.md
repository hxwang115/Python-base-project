## git 扩展命令
* 删除远程仓库标签
     ```
     git push origin --delete [tagname]
     ```
* 删除远程分支
    ```
    git push oregin [:brabch]
    ```
* 强行推送旧版本到远程仓库
    ```
    git push --force origin
    ```
* 查看所有分支
    ```
  git branch -a  
  ```
* 推送标签/推送所有标签
    ```
  git push origin [tag]/git push origin --tags
  ```
* 拉取远程仓库并合并
     ```
     git pull
     ```
* 拉取远程仓库到tmp分支 + 合并
     ```
     git fetch origin master:tmp   +   git merge tmp
     ```
