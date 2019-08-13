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
1. 开发者后台首页。各种数据的展示，包括滚动条、轮播图、已上传脚本展示、脚本运行情况、系统已安装Python库、最新评论、代理展示。由于后台页面多处属于重复区块，我们将一些重复数据存在session中以减少服务器与数据库的交互，从而加速网页的渲染。
2. 脚本列表页。分类展示脚本信息。
3. 

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
