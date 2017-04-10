import jieba
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy
import time
from scipy.misc import imread


class WordCloud_CN:

    def __init__(self, text_path, picture_path=None):
        self.stopword_file = 'D:\Scrapy_Item\stopwords.txt'          # 停用词路径
        self.font_path = 'D:\Scrapy_Item\HYGuoQiangXingShuW.ttf'     # 字体路径
        self.text_path = text_path                                   # 文本路径
        self.picture_path = picture_path                             # 图片模板路径（默认None）
        self.stopwords = {}                                          # 构建停用词字典
        self.seg_dit = {}                                            # 结巴分词后 词字典（词频）

    @property
    def get_stopwords(self):                                         # 得到停用词字典
        with open(self.stopword_file, 'r', encoding='utf-8') as f:
            line = f.readline().rstrip('\n')
            while line:
                self.stopwords[line] = 1
                line = f.readline().rstrip('\n')
        return self.stopwords

    @property
    def Seg_list(self):                                               # 结巴分词后得到词频
        print('结巴分词中......')
        with open(self.text_path, 'r', encoding='utf-8') as f:
            get_text = ''.join(f.readlines())
            seg = jieba.cut(get_text, cut_all=False)
            for i in seg:
                if i not in self.get_stopwords:
                    if i in self.seg_dit:
                        self.seg_dit[i] += 1
                    else:
                        self.seg_dit[i] = 1
        return self.seg_dit

    def show(self):
        for i in self.get_stopwords:
            STOPWORDS.add(i)

        if self.picture_path:
            #  picture_mask = imread(self.picture_path)
            picture_mask = numpy.array(Image.open(self.picture_path))     # 得到图片像素
            image_color = ImageColorGenerator(picture_mask)               # 提取图片背景颜色
            save_path = '词云' + self.picture_path                         # 保存词云图片路径（为提供图片路径或py所在路径）
            w_c = WordCloud(font_path=self.font_path, background_color='white', max_words=200, mask=picture_mask,
                            stopwords=STOPWORDS, max_font_size=200, random_state=42)  # 生成词云
        else:
            picture_mask = None
            image_color = None
            save_path = '词云.jpg'
            w_c = WordCloud(font_path=self.font_path, background_color='black', width=800, height=400,
                            max_words=400, max_font_size=200, stopwords=STOPWORDS)

        w_c.generate_from_frequencies(self.Seg_list)
        plt.imshow(w_c.recolor(color_func=image_color), interpolation='bilinear')
        print('词云制作完成！')
        plt.axis('off')
        plt.figure()
        if self.picture_path:
            plt.imshow(picture_mask, interpolation='bilinear')
            plt.axis('off')
        plt.show()
        w_c.to_file(save_path)                                # 保存词云图片
        print('词云保存成功！')


if __name__ == '__main__':
    text = 'D:\jiaoyubao\data\\2017-03-28\第01版：要闻\“一流学科并非名牌大学专利”.txt'
    #picture = 'D:\Scrapy_Item\\71.jpg'
    start_time = time.time()
    #wc = WordCloud_CN(text, picture)
    wc = WordCloud_CN(text)
    wc.show()
    print("总共用时：" + str(time.time() - start_time))