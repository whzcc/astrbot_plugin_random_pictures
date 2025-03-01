from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.all import *
import os,json
import random

# 自定义的 Jinja2 模板，支持 CSS
TMPL = '''
<div style="font-size: 32px;">
<h1 style="color: black">Todo List</h1>

<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</ul>

<!-- 使用模板变量控制图片 -->
<img src="{{ footer_image }}"
     style="display: block;
            width: 100%;
            margin-top: 20px;"
     alt="列表插图">
</div>
'''

@register("random-pictures", "whzc", "随机发一些图片", "1.0.0", "repo url")

class Main(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    # 插件目录下的图片
        try:
            os.makedir("pictures")
            logger.info("成功为随机图片创建文件夹")
        except:
            logger.info("本次未为随机图片创建文件夹")
        global pictures_dir
        pictures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"pictures") # 获取图片所在目录
        # pictures_dir = os.path.dirname(os.path.abspath(__file__))+"\\pictures"  
        files = os.listdir(pictures_dir)   # 读入文件夹
        global num_png
        num_png = len(files)-1       # 统计文件夹中的文件个数（减1是因为有info.json）
        logger.info(f"将在{pictures_dir}中寻找{num_png}张图片")

@event_message_type(EventMessageType.PRIVATE_MESSAGE)
async def random_pictures(self, event: AstrMessageEvent):
    message_str = event.message_str # 获取消息的纯文本内容
    if message_str.startswith("/抽明信片"):

        # 随机获取图片文件的路径
        i = random.randint(1,num_png)
        pictures_file = os.path.join(pictures_dir,f"{i}.jpg")
        sender_id = event.get_sender_id()

        # 获取图片的解释说明
        with open(os.path.join(pictures_dir,"info.json"),encoding='utf-8') as f:
            info = json.load(f)[str(i)] # 读到的解释说明

        # chain = [
        #     Image.fromFileSystem(pictures_file), # 从本地文件目录发送图片
        #     Plain(f"Agrato为你抽取到了{i}号图片："),
        #     Plain(info)
        # ]
        # yield event.chain_result(chain)

        

        url = await self.html_render(TMPL,
    {"items": ["吃饭", "睡觉", f"{info}"],"footer_image": pictures_file}) # 第二个参数是 Jinja2 的渲染数据
        logger.info(pictures_file)
        yield event.image_result(url)

        event.stop_event()

