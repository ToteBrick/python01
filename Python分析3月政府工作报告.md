### 概述

有时候我们抓不到一些文章里面的重点，python里`jieba`库分词很好的为我们提供了一个解决方案。下面就讲一个实际使用的一个例子来说明。

首先，我们要将网页的内容请求并解析出来，下面是政府工作报告的路径：

<`http://www.gov.cn/premier/2019-03/16/content_5374314.htm`>

利用`request`库的`get(url)`方法请求拿到响应的数据，发现报告文字内容大多在段落`p`标签中。可以引用`BeautifulSoup`的`find_all()`将`p`标签中所有标签拿到，再获取里面的内容。下面先封装一下：

```python
def extract_text(url):
    # 发送url请求并获取响应文件
    page_source = requests.get(url).content
    bs_source = BeautifulSoup(page_source, "lxml")

    # 解析出所有的p标签
    report_text = bs_source.find_all('p')

    text = ''
    # 将p标签里的所有内容都保存到一个字符串里
    for p in report_text:
        text += p.get_text()
        text += '\n'

    return text
```

### 词云的使用

使用词云，首先得准备一张背景图片，这里使用了前面比较火的小猪佩奇的图片。要读入图片，要使用`matplotlib`库中`pyplot`模块的`imread()`方法。

```python
import matplotlib.pyplot as plt
back_img = plt.imread('/peiqi.jpg') # 方法里传入图片的路径
```

下面介绍词云的基本使用：

```python
    cloud = WordCloud(font_path= '/simhei.ttf',  # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
                      background_color="white",  # 背景颜色
                      max_words=5000,  # 词云显示的最大词数
                      mask=back_img,  # 设置背景图片
                      max_font_size=100,  # 字体最大值
                      random_state=42,
                      width=360, height=591, margin=2,  # 设置图片默认的大小,但是如果使用背景图片的话,保存的图片大小将会按照其大小保存,margin为词语边缘距离
                      )
```

因为词云默认是不支持中文的，需要在网上搜索支持的字体，然后将下载好的字体`simhei.ttf`放在项目里面。

### `jieba`分词

下面按`jieba`的精确分词模式将解析到的内容传入，并传入词云，生成图形。

```python
    for li in content:
        comment_txt += ' '.join(jieba.cut(li, cut_all=False))
    wc = cloud.generate(comment_txt)
    image_colors = ImageColorGenerator(back_img)
    plt.figure("wordc")
    plt.imshow(wc.recolor(color_func=image_colors))
    wc.to_file('2019年3月政府工作报告.png')

```

下面是完整的代码：

```python
import matplotlib.pyplot as plt
import jieba
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud, ImageColorGenerator

def extract_text(url):
    # 发送url请求并获取响应文件
    page_source = requests.get(url).content
    bs_source = BeautifulSoup(page_source, "lxml")

    # 解析出所有的p标签
    report_text = bs_source.find_all('p')

    text = ''
    # 将p标签里的所有内容都保存到一个字符串里
    for p in report_text:
        text += p.get_text()
        text += '\n'

    return text

def word_cloud(content):
    comment_txt = ''
    back_img = plt.imread('/peiqi.jpg')
    cloud = WordCloud(font_path='/simhei.ttf',  # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
                      background_color="white",  # 背景颜色
                      max_words=5000,  # 词云显示的最大词数
                      mask=back_img,  # 设置背景图片
                      max_font_size=100,  # 字体最大值
                      random_state=42,
                      width=360, height=591, margin=2,  # 设置图片默认的大小,但是如果使用背景图片的话,保存的图片大小将会按照其大小保存,margin为词语边缘距离
                      )
    for li in content:
        comment_txt += ' '.join(jieba.cut(li, cut_all=False))
    wc = cloud.generate(comment_txt)
    image_colors = ImageColorGenerator(back_img)
    plt.figure("wordc")
    plt.imshow(wc.recolor(color_func=image_colors))
    wc.to_file('2019年3月政府工作报告.png')

if __name__ == "__main__":
    url = 'http://www.gov.cn/premier/2019-03/16/content_5374314.htm'
    text = extract_text(url)
    word_cloud(text)

```

用词云显示发现显示得并不太直观，下面用`matplotlib`的柱形图将前10关键词的数量显示出来。这里要重新优化一下词云的搜索。

```python
def word_frequency(text):
    # 返回所有分词后长度大于等于2 的词的列表
    word_list = []
    count_list = []
    words = [word for word in jieba.cut(text, cut_all=True) if len(word) >= 2]
    # Counter是一个简单的计数器，统计字符出现的个数
    c = Counter(words)

    for word_freq in c.most_common(10): # c.most_common(10)是列表里，里面每一个元素是一个元祖
        word, freq = word_freq
        word_list.append(word)
        count_list.append(freq)
        # print(word, freq,sep = ':')

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    colors = ['#00FFFF', '#7FFFD4', '#F08080', '#90EE90', '#AFEEEE',
                  '#98FB98', '#B0E0E6', '#00FF7F', '#FFFF00', '#9ACD32']
    index = np.arange(10)
    plt.bar(index, count_list, color=colors, width=0.5, align='center')

    plt.xticks(np.arange(10), word_list)  # 横坐轴标签
    for x, y in enumerate(count_list):
        # 在柱子上方1.2处标注值
        plt.text(x, y + 1.2, '%s' % y, ha='center', fontsize=10)
    plt.ylabel('出现次数')  # 设置纵坐标标签
    prov_title = '政府报告Top10关键词'
    plt.title(prov_title)    # 设置标题
    plt.savefig('/政府报告Top10关键词')  # 保存图片
    plt.legend()
    # 显示
    plt.show()
```

这里用到了`collections`类里的`Counter`将前10出现的词汇及次数统计出来，遍历出来分别放在两个列表里，然后设置在柱形图坐标轴上分别显示出来。显示效果如下：

![](G:\2019-05-03_224728.jpg)

下面是完整代码：

```python
![2019-05-03_224728](G:\2019-05-03_224728.jpg)import matplotlib.pyplot as plt
import jieba
import requests
from bs4 import BeautifulSoup
from collections import Counter
import numpy as np
def extract_text(url):
    # 发送url请求并获取响应文件
    page_source = requests.get(url).content
    bs_source = BeautifulSoup(page_source, "lxml")

    # 解析出所有的p标签
    report_text = bs_source.find_all('p')
    text = ''
    # 将p标签里的所有内容都保存到一个字符串里
    for p in report_text:
        text += p.get_text()
        text += '\n'

    return text


def word_frequency(text):
    # 返回所有分词后长度大于等于2 的词的列表
    word_list = []
    count_list = []
    words = [word for word in jieba.cut(text, cut_all=True) if len(word) >= 2]
    # Counter是一个简单的计数器，统计字符出现的个数
    c = Counter(words)

    for word_freq in c.most_common(10): # c.most_common(10)是列表里，里面每一个元素是一个元祖
        word, freq = word_freq
        word_list.append(word)
        count_list.append(freq)
        # print(word, freq,sep = ':')

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    colors = ['#00FFFF', '#7FFFD4', '#F08080', '#90EE90', '#AFEEEE',
                  '#98FB98', '#B0E0E6', '#00FF7F', '#FFFF00', '#9ACD32']
    index = np.arange(10)
    plt.bar(index, count_list, color=colors, width=0.5, align='center')

    plt.xticks(np.arange(10), word_list)  # 横坐轴标签
    for x, y in enumerate(count_list):
        # 在柱子上方1.2处标注值
        plt.text(x, y + 1.2, '%s' % y, ha='center', fontsize=10)
    plt.ylabel('出现次数')  # 设置纵坐标标签
    prov_title = '政府报告Top10关键词'
    plt.title(prov_title)    # 设置标题
    plt.savefig('/政府报告Top10关键词')  # 保存图片
    plt.legend()
    # 显示
    plt.show()

if __name__ == "__main__":
    url = 'http://www.gov.cn/premier/2019-03/16/content_5374314.htm'
    text = extract_text(url)
    word_frequency(text)
```

