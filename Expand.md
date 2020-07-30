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
## 模块扩展
* 输入隐藏
    ```
  imort getpass
  pwd = getpass.getpass('输入提示')
  ```
* 转换加密
    ```
  import hashlib
  hash = hashlib.md5() # 生成对象
  hash.updata(pwd.encode) # 算法加密
  pwd = hash.hexdigest() # 提取加密后的密码
  ```