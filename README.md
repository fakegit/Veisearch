# Veisearch 技术无罪
我们不生产资源，我们不存储资源，我们也不是资源搬运工。

### 项目演示地址
+ 项目演示地址：[http://www.veisearch.com/](http://www.veisearch.com/)  
仅界面演示，上传脚本并未执行。由于并未找到可靠的免费代理池，而我们爬取的网站对访问限制比较严重，所以多次尝试后最终放弃在服务器上运行，不过本地运行完全可以。
+ 开发者后台地址：[http://www.veisearch.com/pro/](http://www.veisearch.com/pro/)  
用户可以在后台开发者页面浏览其他用户上传的脚本，并对脚本进行相应的测试，评论，点赞等操作。
+ 网站后台地址：[http://www.veisearch.com/admin/](http://www.veisearch.com/admin/)  
后台采用开源框架[django-simpleui](https://github.com/newpanjing/simpleui)，一款基于vue+element-ui的django admin现代化主题。
  - 账号：admin
  - 密码：admin123456  
### 实现功能
1. 搜索页。当用户选择搜索类型并输入搜索关键词点击搜索时，后台会运行数据库中对应类型的非停止状态下的所有脚本并将结果返回。后台多脚本的执行使用多线程。
2. 开发者后台首页。各种数据的展示，包括滚动条、轮播图、已上传脚本展示、脚本运行情况、系统已安装Python库、最新评论、代理展示。由于后台页面多处属于重复区块，我们将一些重复数据存在session中以减少服务器与数据库的交互，从而加速网页的渲染。
3. 脚本列表页。分类展示脚本信息。
4. 脚本详情页。对于不同状态的脚本，会有不同状态的展示，主要体现在脚本测试方面。除此之外，用户可以对脚本进行无登录点赞及评论操作。注意，点赞数据亦存储在session中。
5. 脚本报错记录。无论用户执行搜索或者在后太对单个脚本进行调试，只要脚本运行系统都会对脚本进行监测，一旦报错会立马记录在数据库。当报错记录超过50条系统会自动修改脚本的状态为`error`，即`出现问题`。同理，当报错记录超过100条系统会自动修改脚本的状态为`stop`，即`停止运行`，并停止脚本的运行。
6. Celery+redis任务管理。  
    1. 邮件任务
        1. 当用户上传脚本后脚本处于待审核状态，此时需要管理员对脚本代码进行安全性检查，检查完成后可在后台修改脚本状态。此时系统会给开发者发送邮件提醒用户脚本审核通过
        2. 除此之外，当系统监测到脚本报错次数达到限制后会自动修改脚本状态，此时也会触发邮件事件给上传当前脚本的用户发送邮件进行提醒。 
    2. 代理定时任务
        1. 代理爬取。我们设定每10分钟爬取一批代理并存入数据库。
        2. 测试代理。我们设定每20分钟检测所有库中ip代理。
    ```python
          CELERYBEAT_SCHEDULE = {
        u'获取代理': {
            "task": "vei.tasks.getproxy",
            "schedule": timedelta(minutes=10),
            "args": (),
        },
        u'测试代理': {
            "task": "vei.tasks.proxytest",
            "schedule": timedelta(minutes=10),
            "args": (),
        },
      }
    ```

### 脚本示例
+ [80s电影网](https://github.com/Weibw162/Veisearch/blob/master/media/spider_files/Spider_80s.py)  
使用requests+threading实现多线程并发爬取
+ [80s电影网](https://github.com/Weibw162/Veisearch/blob/master/media/spider_files/Spider_80s_t.py)  
使用asyncio+aiohttp实现多协程并发爬取

### 网站页面展示
+ 搜索页（PC端）  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/index_pc.PNG)
+ 搜索页（移动端）  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/index_m.PNG)
+ 搜索结果展示（PC端）  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/result_pc.PNG)
+ 搜索结果展示（移动端）  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/result_m.PNG)
+ 开发者后台首页（PC端）  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/pro_pc.PNG)
+ 开发者后台首页（完整展示移动端）  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/pro_m.jpg)
+ 脚本上传页  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/upload.jpg)
+ 脚本详情页  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/detail.jpg)
