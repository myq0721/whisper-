"""
文本分析工具 - 使用NLTK/spaCy/Stanza
作者: Ayanami
日期: 2026-01-06
"""

import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
import spacy
import stanza

# 设置中文字体(解决matplotlib中文显示问题)
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


class TextAnalyzer:
    """文本分析器"""
    
    def __init__(self, language="zh"):
        """
        初始化分析器
        
        参数:
            language: 'zh'(中文) 或 'en'(英文)
        """
        self.language = language
        print(f"正在初始化{language}文本分析器...")
        
        # 下载NLTK数据(首次运行需要)
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
        except:
            pass
        
        # 加载spaCy模型
        try:
            if language == "zh":
                self.nlp_spacy = spacy.load("zh_core_web_sm")
            else:
                self.nlp_spacy = spacy.load("en_core_web_sm")
            print("spaCy模型加载成功")
        except:
            print("警告: spaCy模型未安装")
            print(f"请运行: python -m spacy download {'zh_core_web_sm' if language=='zh' else 'en_core_web_sm'}")
            self.nlp_spacy = None
        
        # 加载Stanza模型
        try:
            self.nlp_stanza = stanza.Pipeline(language, download_method=None)
            print("Stanza模型加载成功")
        except:
            print("警告: Stanza模型未安装,首次使用需下载...")
            stanza.download(language)
            self.nlp_stanza = stanza.Pipeline(language)
    
    def clean_text(self, text):
        """
        清理文本
        
        参数:
            text: 原始文本
        
        返回:
            str: 清理后的文本
        """
        # 中文填充词
        zh_fillers = ['嗯', '啊', '呃', '哦', '诶', '那个', '这个', '就是', '然后']
        # 英文填充词
        en_fillers = ['um', 'uh', 'like', 'you know', 'I mean', 'sort of', 'kind of']
        
        fillers = zh_fillers if self.language == "zh" else en_fillers
        
        cleaned = text
        for filler in fillers:
            # 使用正则表达式删除填充词
            pattern = r'\b' + re.escape(filler) + r'\b'
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # 去除多余空格
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    def extract_keywords_nltk(self, text, top_n=20):
        """
        使用NLTK提取关键词
        
        参数:
            text: 输入文本
            top_n: 返回前N个关键词
        
        返回:
            list: [(词, 频率), ...]
        """
        # 分词
        if self.language == "zh":
            # 简单的中文分词(实际项目建议用jieba)
            words = list(text)
        else:
            words = nltk.word_tokenize(text.lower())
        
        # 去除停用词
        try:
            if self.language == "zh":
                # 自定义中文停用词
                stopwords = set(['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个'])
            else:
                stopwords = set(nltk.corpus.stopwords.words('english'))
        except:
            stopwords = set()
        
        # 过滤
        words = [w for w in words if w.isalpha() and w not in stopwords]
        
        # 统计频率
        word_freq = Counter(words)
        
        return word_freq.most_common(top_n)
    
    def extract_keywords_spacy(self, text, top_n=20):
        """
        使用spaCy提取关键词(基于词性)
        
        参数:
            text: 输入文本
            top_n: 返回前N个关键词
        
        返回:
            list: [(词, 词性, 频率), ...]
        """
        if not self.nlp_spacy:
            return []
        
        doc = self.nlp_spacy(text)
        
        # 提取名词和动词
        keywords = []
        for token in doc:
            if token.pos_ in ['NOUN', 'VERB', 'PROPN'] and not token.is_stop:
                keywords.append((token.text, token.pos_))
        
        # 统计频率
        keyword_freq = Counter(keywords)
        
        return [(word, pos, freq) for (word, pos), freq in keyword_freq.most_common(top_n)]
    
    def analyze_sentiment_simple(self, text):
        """
        简单情感分析(基于词典)
        
        返回:
            dict: 情感统计
        """
        # 简单的情感词典(实际项目应使用专业词典)
        if self.language == "zh":
            positive_words = set(['好', '喜欢', '优秀', '成功', '快乐', '美好', '棒', '赞'])
            negative_words = set(['不好', '讨厌', '失败', '痛苦', '糟糕', '差', '坏'])
        else:
            positive_words = set(['good', 'great', 'excellent', 'happy', 'love', 'wonderful', 'amazing'])
            negative_words = set(['bad', 'terrible', 'awful', 'sad', 'hate', 'horrible', 'poor'])
        
        words = text.lower().split()
        
        pos_count = sum(1 for w in words if w in positive_words)
        neg_count = sum(1 for w in words if w in negative_words)
        
        return {
            'positive_words': pos_count,
            'negative_words': neg_count,
            'sentiment_score': pos_count - neg_count
        }
    
    def generate_wordcloud(self, text, output_path="output/wordcloud.png"):
        """
        生成词云图
        
        参数:
            text: 输入文本
            output_path: 保存路径
        """
        # 清理文本
        cleaned_text = self.clean_text(text)
        
        # 生成词云
        if self.language == "zh":
            # 中文需要指定字体
            wc = WordCloud(
                font_path='C:/Windows/Fonts/simhei.ttf',  # 黑体
                width=800,
                height=400,
                background_color='white',
                max_words=100
            ).generate(cleaned_text)
        else:
            wc = WordCloud(
                width=800,
                height=400,
                background_color='white',
                max_words=100
            ).generate(cleaned_text)
        
        # 保存图片
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title('词云图', fontsize=16)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"词云图已保存至: {output_path}")
        plt.close()
    
    def plot_top_keywords(self, keywords, output_path="output/keywords_bar.png"):
        """
        绘制关键词频率柱状图
        
        参数:
            keywords: [(词, 频率), ...]
            output_path: 保存路径
        """
        words = [k[0] for k in keywords]
        freqs = [k[1] for k in keywords]
        
        plt.figure(figsize=(12, 6))
        plt.barh(words[::-1], freqs[::-1], color='steelblue')
        plt.xlabel('频率', fontsize=12)
        plt.title('高频关键词统计', fontsize=14)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"关键词柱状图已保存至: {output_path}")
        plt.close()
    
    def generate_report(self, text, output_path="output/analysis_report.txt"):
        """
        生成完整分析报告
        
        参数:
            text: 输入文本
            output_path: 报告保存路径
        """
        report = []
        report.append("=" * 50)
        report.append("文本分析报告")
        report.append("=" * 50)
        report.append("")
        
        # 1. 基础统计
        report.append("【基础统计】")
        report.append(f"总字符数: {len(text)}")
        report.append(f"总词数: {len(text.split())}")
        cleaned = self.clean_text(text)
        report.append(f"清理后字符数: {len(cleaned)}")
        report.append("")
        
        # 2. 关键词分析
        report.append("【高频关键词 TOP 10】")
        keywords = self.extract_keywords_nltk(cleaned, top_n=10)
        for i, (word, freq) in enumerate(keywords, 1):
            report.append(f"{i}. {word}: {freq}次")
        report.append("")
        
        # 3. 情感分析
        report.append("【情感分析】")
        sentiment = self.analyze_sentiment_simple(cleaned)
        report.append(f"积极词汇数: {sentiment['positive_words']}")
        report.append(f"消极词汇数: {sentiment['negative_words']}")
        report.append(f"情感得分: {sentiment['sentiment_score']}")
        report.append("")
        
        # 保存报告
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report))
        
        print(f"分析报告已保存至: {output_path}")
        return "\n".join(report)


def main():
    """主函数 - 演示完整分析流程"""
    
    # 1. 读取转录文本
    text_file = "output/sample_transcription.txt"
    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    # 2. 创建分析器
    analyzer = TextAnalyzer(language="zh")
    
    # 3. 清理文本
    cleaned_text = analyzer.clean_text(text)
    print("\n清理后的文本片段:")
    print(cleaned_text[:200] + "...")
    
    # 4. 提取关键词
    print("\n正在提取关键词...")
    keywords = analyzer.extract_keywords_nltk(cleaned_text, top_n=20)
    
    print("\n【高频关键词 TOP 10】")
    for i, (word, freq) in enumerate(keywords[:10], 1):
        print(f"{i}. {word}: {freq}次")
    
    # 5. 生成可视化
    print("\n正在生成可视化...")
    analyzer.generate_wordcloud(cleaned_text)
    analyzer.plot_top_keywords(keywords[:15])
    
    # 6. 生成完整报告
    print("\n正在生成分析报告...")
    report = analyzer.generate_report(cleaned_text)
    print("\n" + report)


if __name__ == "__main__":
    main()