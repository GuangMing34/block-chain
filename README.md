

[TOC]

# English Version
如果需要看中文版，请[点这里](#中文版)

# What is the key point of this app

As we all know, the one of the important features of block-chain is that data can't be modified once uploaded. So, the key point of this program is to create a block chain and upload, check, and maintain the record, rather than to get involved in how to encypt the file.

## File Encryption
About file ENc


---

# 中文版
For English Version, plese [click me](#english-version)

## 重点
blockchanin的关键是数据的不可修改，这个是和blockchain的设计理念相关的  
所以本程序重点方向是blockchain，而不是文件加密的部分.
>这里用来讲述相关的设计理念  
1  
1  
1  

## 加密的密码
文件加密的部分，使用一个密码进行加密, 密码的原始字符串使用设备唯一的ID  
ID部分，可以参考的有HW的uuid，以及设备的MAC地址  
UUID部分，python上不方便获取，选取MAC地址进行文件加密.   
## 加密的方式
简单点，用以加密的密码(上面获取到的设备的唯一ID进行再加密)和文件内容进行  
异或处理，或者python库自带的加密方式  

## 流程
### 加密阶段
* **检测当前的block chain是否初始化过.**  
  * **未初始化过**
    1. 创建block chain(block chain初始化)
    2. 添加当前设备为可信设备，并获取ID作为原始的密码(第一个block块)
    3. 询问是否需要添加别的可信设备
       * 如果需要，输入可信设备的ID，添加可信设备(block添加), 返回 3
       * 如果不需要，结束.
  * **初始化过**
    > **初始化的文件应该仅存在于可信设备中，不能存在于其他设备上**  

    检测当前设备是否存在于block中
      1. 不在，退出并提示异常.
      2. 在，进入是否添加可信设备的循环中.
* **获取block中的密码**
    
    block可能有很多块(多个可信设备)  
    但是本程序中，每一个block中都存在完整的加密密码.
    所以，****只要获取到其中一个block中存储的完整信息即可.****

* **文件加密**

    加密的文件我们就选一个word文件，这样的话，加密过后正常来说是会无法打开的.  
    如果需要指定文件加密的话，可以自行添加函数去实现修改文件路径，达到对指定文件加密的方式
### 解密阶段  
* **文件解密**  
  
    解密的话，也是一样的，解密脚本和文件放在同一位置，防止识别出错.
    如果需要指定文件解密的话, 和加密一样，自行完善可以修改路径的方式.