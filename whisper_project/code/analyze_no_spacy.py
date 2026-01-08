"""
文本分析工具 - 简化版(不依赖spaCy)
只使用jieba和基础工具
保存为: analyze_simple.py
运行: python analyze_simple.py
"""

import re
from collections import Counter
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
    import jieba
except ImportError as e:
    print(f"缺少依赖库: {e}")
    print("请运行: python -m pip install jieba matplotlib wordcloud")
    input("按Enter退出...")
    exit(1)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


class SimpleTextAnalyzer:
    """简化版文本分析器(不依赖spaCy)"""
    
    def __init__(self, language="zh"):
        """
        初始化分析器
        
        参数:
            language: 'zh'(中文) 或 'en'(英文)
        """
        self.language = language
        print(f"初始化{language}文本分析器...")
        
        # 中文停用词
        self.zh_stopwords = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
            '都', '一', '个', '上', '也', '很', '到', '说', '要', '去',
            '你', '会', '着', '没有', '看', '好', '自己', '这', '那',
            '他', '她', '它', '们', '啊', '吗', '呢', '吧', '与', '及',
            '等', '但', '而', '为', '以', '之', '将', '能', '对', '从'
        }
        
        # 英文停用词
        self.en_stopwords = {
            'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or',
            'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by', 'was',
            'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'this', 'that'
        }
        
        # 中文填充词
        self.zh_fillers = ['嗯', '啊', '呃', '哦', '诶', '那个', '这个', '就是', '然后', '所以', '其实']
        
        # 英文填充词
        self.en_fillers = ['um', 'uh', 'like', 'you know', 'i mean', 'sort of', 'kind of']
        
        print("✓ 分析器初始化完成")
    
    def clean_text(self, text):
        """
        清理文本,去除填充词和多余空格
        
        参数:
            text: 原始文本
        
        返回:
            str: 清理后的文本
        """
        fillers = self.zh_fillers if self.language == "zh" else self.en_fillers
        
        cleaned = text
        for filler in fillers:
            pattern = r'\b' + re.escape(filler) + r'\b'
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # 去除多余空格
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    def extract_keywords(self, text, top_n=20):
        """
        提取关键词
        
        参数:
            text: 输入文本
            top_n: 返回前N个关键词
        
        返回:
            list: [(词, 频率), ...]
        """
        # 分词
        if self.language == "zh":
            words = jieba.lcut(text)
            stopwords = self.zh_stopwords
        else:
            words = text.lower().split()
            stopwords = self.en_stopwords
        
        # 过滤:去除停用词、单字符、纯数字
        filtered_words = []
        for word in words:
            word = word.strip()
            if (len(word) > 1 and 
                word not in stopwords and 
                not word.isdigit() and
                word.isalpha()):
                filtered_words.append(word)
        
        # 统计词频
        word_freq = Counter(filtered_words)
        
        return word_freq.most_common(top_n)
    
    def analyze_sentiment_simple(self, text):
        """
        简单情感分析(基于词典)
        
        返回:
            dict: 情感统计
        """
        if self.language == "zh":
            positive_words = {
                '好', '喜欢', '优秀', '成功', '快乐', '美好', '棒', '赞',
                '幸福', '开心', '满意', '精彩', '出色', '卓越', '完美',
                '发展', '进步', '创新', '机会', '希望', '前景'
            }
            negative_words = {
                '不好', '讨厌', '失败', '痛苦', '糟糕', '差', '坏',
                '难过', '悲伤', '困难', '问题', '错误', '遗憾', '挑战'
            }
        else:
            positive_words = {
                'good', 'great', 'excellent', 'happy', 'love', 'wonderful',
                'amazing', 'perfect', 'best', 'awesome', 'fantastic', 'success'
            }
            negative_words = {
                'bad', 'terrible', 'awful', 'sad', 'hate', 'horrible',
                'poor', 'worst', 'disappointing', 'wrong', 'fail'
            }
        
        words = text.lower().split() if self.language == "en" else list(jieba.cut(text))
        
        pos_count = sum(1 for w in words if w in positive_words)
        neg_count = sum(1 for w in words if w in negative_words)
        
        total = pos_count + neg_count
        if total > 0:
            sentiment = "积极" if pos_count > neg_count else "消极" if neg_count > pos_count else "中性"
        else:
            sentiment = "中性"
        
        return {
            'positive_words': pos_count,
            'negative_words': neg_count,
            'sentiment_score': pos_count - neg_count,
            'sentiment': sentiment
        }
    
    def generate_wordcloud(self, text, output_path="output/wordcloud.png"):
        """
        生成词云图
        
        参数:
            text: 输入文本
            output_path: 保存路径
        """
        print("\n正在生成词云图...")
        
        # 清理文本
        cleaned_text = self.clean_text(text)
        
        try:
            # 生成词云
            if self.language == "zh":
                # 中文需要先分词
                words = ' '.join(jieba.cut(cleaned_text))
                wc = WordCloud(
                    font_path='C:/Windows/Fonts/simhei.ttf',
                    width=800,
                    height=400,
                    background_color='white',
                    max_words=100,
                    stopwords=self.zh_stopwords
                ).generate(words)
            else:
                wc = WordCloud(
                    width=800,
                    height=400,
                    background_color='white',
                    max_words=100,
                    stopwords=self.en_stopwords
                ).generate(cleaned_text)
            
            # 保存图片
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            plt.figure(figsize=(10, 5))
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            plt.title('词云图', fontsize=16)
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"✓ 词云图已保存至: {output_path}")
            
        except Exception as e:
            print(f"✗ 词云生成失败: {e}")
    
    def plot_top_keywords(self, keywords, output_path="output/keywords_bar.png"):
        """
        绘制关键词频率柱状图
        
        参数:
            keywords: [(词, 频率), ...]
            output_path: 保存路径
        """
        print("\n正在生成关键词柱状图...")
        
        try:
            words = [k[0] for k in keywords]
            freqs = [k[1] for k in keywords]
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            plt.figure(figsize=(12, 6))
            plt.barh(words[::-1], freqs[::-1], color='steelblue')
            plt.xlabel('频率', fontsize=12)
            plt.title('高频关键词统计', fontsize=14)
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"✓ 关键词柱状图已保存至: {output_path}")
            
        except Exception as e:
            print(f"✗ 图表生成失败: {e}")
    
    def generate_report(self, text, output_path="output/analysis_report.txt"):
        """
        生成完整分析报告
        
        参数:
            text: 输入文本
            output_path: 报告保存路径
        """
        print("\n正在生成分析报告...")
        
        report = []
        report.append("=" * 60)
        report.append("文本分析报告")
        report.append("=" * 60)
        report.append("")
        
        # 1. 基础统计
        report.append("【一、基础统计】")
        report.append(f"总字符数: {len(text)}")
        
        if self.language == "zh":
            words = list(jieba.cut(text))
            report.append(f"总词数: {len(words)}")
        else:
            words = text.split()
            report.append(f"总单词数: {len(words)}")
        
        cleaned = self.clean_text(text)
        report.append(f"清理后字符数: {len(cleaned)}")
        report.append("")
        
        # 2. 关键词分析
        report.append("【二、高频关键词 TOP 15】")
        keywords = self.extract_keywords(cleaned, top_n=15)
        for i, (word, freq) in enumerate(keywords, 1):
            report.append(f"{i:2d}. {word:15s} - {freq:3d}次")
        report.append("")
        
        # 3. 情感分析
        report.append("【三、情感分析】")
        sentiment = self.analyze_sentiment_simple(cleaned)
        report.append(f"积极词汇数: {sentiment['positive_words']}")
        report.append(f"消极词汇数: {sentiment['negative_words']}")
        report.append(f"情感倾向: {sentiment['sentiment']}")
        report.append(f"情感得分: {sentiment['sentiment_score']:+d}")
        report.append("")
        
        # 4. 文本特征
        report.append("【四、文本特征】")
        avg_word_len = sum(len(w) for w in words) / len(words) if words else 0
        report.append(f"平均词长: {avg_word_len:.2f}字符")
        
        unique_words = len(set(words))
        vocab_richness = unique_words / len(words) * 100 if words else 0
        report.append(f"词汇丰富度: {vocab_richness:.1f}% ({unique_words}个不同词汇)")
        report.append("")
        
        # 保存报告
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report))
        
        print(f"✓ 分析报告已保存至: {output_path}")
        return "\n".join(report)


def main():
    """主函数 - 演示完整分析流程"""
    
    print("="*60)
    print("文本分析工具 - 简化版")
    print("="*60)
    
    # 1. 自动查找转录文件
    output_dir = Path("output")
    if not output_dir.exists():
        print(f"\n✗ 错误: 找不到output文件夹")
        print("请先完成语音转录")
        input("\n按Enter键退出...")
        return
    
    # 查找所有txt文件
    txt_files = list(output_dir.glob("*转录.txt"))
    if not txt_files:
        txt_files = list(output_dir.glob("*.txt"))
    
    if not txt_files:
        print(f"\n✗ 错误: output文件夹中没有找到转录文本文件")
        print("请先运行语音转录程序")
        input("\n按Enter键退出...")
        return
    
    # 如果有多个文件,使用最新的
    text_file = max(txt_files, key=lambda p: p.stat().st_mtime)
    
    print(f"\n✓ 找到转录文件: {text_file.name}")
    
    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    print(f"文本长度: {len(text)} 字符")
    
    if len(text) < 50:
        print(f"\n⚠️ 警告: 文本太短({len(text)}字符),可能影响分析结果")
        choice = input("是否继续? (y/n): ")
        if choice.lower() != 'y':
            return
    
    # 2. 创建分析器
    analyzer = SimpleTextAnalyzer(language="zh")
    
    # 3. 清理文本
    print("\n正在清理文本...")
    cleaned_text = analyzer.clean_text(text)
    print(f"✓ 清理完成,处理后长度: {len(cleaned_text)} 字符")
    
    # 4. 提取关键词
    print("\n正在提取关键词...")
    keywords = analyzer.extract_keywords(cleaned_text, top_n=20)
    
    print("\n【高频关键词 TOP 10】")
    print("-" * 40)
    for i, (word, freq) in enumerate(keywords[:10], 1):
        print(f"{i:2d}. {word:10s} - {freq:3d}次")
    print("-" * 40)
    
    # 5. 情感分析
    print("\n正在进行情感分析...")
    sentiment = analyzer.analyze_sentiment_simple(cleaned_text)
    print(f"✓ 情感倾向: {sentiment['sentiment']}")
    print(f"  积极词汇: {sentiment['positive_words']}个")
    print(f"  消极词汇: {sentiment['negative_words']}个")
    
    # 6. 生成可视化
    analyzer.generate_wordcloud(cleaned_text)
    analyzer.plot_top_keywords(keywords[:15])
    
    # 7. 生成完整报告
    report = analyzer.generate_report(cleaned_text)
    
    print("\n" + "="*60)
    print("✓ 分析完成!")
    print("="*60)
    print("\n生成的文件:")
    print("  📊 output/wordcloud.png          (词云图)")
    print("  📈 output/keywords_bar.png       (关键词柱状图)")
    print("  📄 output/analysis_report.txt    (分析报告)")
    
    # 询问是否显示报告
    print("\n" + "="*60)
    choice = input("是否显示完整报告? (y/n): ")
    if choice.lower() == 'y':
        print("\n" + report)
    
    input("\n按Enter键退出...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已中断")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按Enter键退出...")
