import matplotlib.pyplot as plt
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
    # plt.legend()
    # 显示
    plt.show()

if __name__ == "__main__":
    url = 'http://www.gov.cn/premier/2019-03/16/content_5374314.htm'
    text = extract_text(url)
    word_frequency(text)