import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VeiSearch.settings")

import django

django.setup()

from vei.models import Spider_type,Broadcast


spider_type_data_list = [
    {
        "name":"电影",
        "data_format":"""
        [
	{
		"movie_name":"斗破苍穹",    # 电影名
		"movie_size":"1.3G",    # 文件大小
		"thunder_link":"thunder://QUFtYWduZXQ6P3h0PXVybjpidGloOjkyNTcyMDYzNjI4NUVCODBEMUFFMTc1OEM0NzMwQTI0MTIzQTlFOEFaWg==",     # 迅雷链接
		"movie_online_view_address":"https://bili.meijuzuida.com/share/8a27c2ddc3d3fe74aa037f4b7d262e34"    # 在线观看地址
		"source":"80s电影网"       # 资源来源网站
	},
	# 注意，属性获取不到的必须填null；
]
        """
    },
{
        "name":"百度网盘",
        "data_format":"""
        [
	{
		"file_name":"复仇者联盟",     # 文件名
		"file_size":"12M",      # 文件大小
		"file_address":"https://pan.baidu.com/mbox/homepage?short=b20rKi",      # 网盘地址
		"source":"盘多多"      # 资源来源网站
	},
]
        """
    },
    {
        "name":"音乐",
        "data_format":"""
        [
	{
		"music_name":"胡萝卜须",        #音乐名
		"music_size":"12M",     # 文件大小
		"music_singer":"许嵩",    #歌手
		"music_download_address":"www.music2536.cn/8123892302"      # 下载地址
		"source":"qq音乐"
	},
]
        """
    },
{
        "name":"磁力",
        "data_format":"""
        [
	{
		"magnet_name":"千与千寻",        #文件名
		"magnet_size":"1。5G",     # 文件大小
		"magnet_link":"magnet:?xt=urn:btih:925720636285EB80D1AE1758C4730A24123A9E8A",    # 磁力链接
		"thunder_link":"thunder://QUFtYWduZXQ6P3h0PXVybjpidGloOjkyNTcyMDYzNjI4NUVCODBEMUFFMTc1OEM0NzMwQTI0MTIzQTlFOEFaWg=="     # 迅雷链接
		"source":"bt下载"
		
	},
]
        """
    }
]

spider_import_list = []
for item in spider_type_data_list:
    spider_type = Spider_type()
    spider_type.name = item["name"]
    spider_type.data_format = item["data_format"]
    spider_import_list.append(spider_type)
Spider_type.objects.bulk_create(spider_import_list)

# 播报
broadcast = Broadcast()
broadcast.cast_content = "大家好我是播报小能手！窗前明月光，疑是地上霜。举头望明月，低头思故乡。大家好我是播报小能手！窗前明月光，疑是地上霜。举头望明月，低头思故乡。"
broadcast.is_used = True
broadcast.save()