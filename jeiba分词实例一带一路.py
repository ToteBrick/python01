import matplotlib.pyplot as plt
import jieba
import requests
from bs4 import BeautifulSoup
from collections import Counter
import os
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

def word_frequency(text):
    # 返回所有分词后长度大于等于2 的词的列表
    words = [word for word in jieba.cut(text, cut_all=True) if len(word) >= 2]
    # Counter是一个简单的计数器，统计字符出现的个数
    # 分词后的列表将被转化为字典
    c = Counter(words)

    for word_freq in c.most_common(10):
    # for word_freq in c.most_common(20):
        word, freq = word_freq
        print(word, freq,sep = ':')

def word_cloud(content):
    """
    词云图
    :param content:
    :return:
    """
    pwd_path = os.path.abspath(os.path.dirname(os.getcwd()))
    conf_path = os.path.join(pwd_path, 'conf/')
    comment_txt = ''
    back_img = plt.imread(conf_path + '/peiqi.jpg')
    cloud = WordCloud(font_path=conf_path + '/simhei.ttf',  # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
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
    wc.to_file('一带一路.png')

if __name__ == "__main__":
    url = 'http://www.gov.cn/guowuyuan/2019-05/01/content_5388150.htm'
    text = extract_text(url)
    # word_frequency(text)
    word_cloud(text)

    '''
发展:144
改革:109
经济:68
加强:62
企业:61
推进:60
建设:60
政策:60
社会:58
市场:57
    '''