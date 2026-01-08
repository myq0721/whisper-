"""
文本分析工具 - 改进版(增强清理功能)
只使用jieba和基础工具
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
    
    def __init__(self, language="en"):
        """
        初始化分析器
        
        参数:
            language: 'zh'(中文) 或 'en'(英文)
        """
        self.language = language
        print(f"初始化{language}文本分析器...")
        
        # 中文停用词(扩展版)
        self.zh_stopwords = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
            '都', '一', '个', '上', '也', '很', '到', '说', '要', '去',
            '你', '会', '着', '没有', '看', '好', '自己', '这', '那',
            '他', '她', '它', '们', '啊', '吗', '呢', '吧', '与', '及',
            '等', '但', '而', '为', '以', '之', '将', '能', '对', '从',
            '把', '向', '往', '给', '被', '让', '叫', '用', '比', '跟'
        }
        
        # 英文停用词(扩展版)
        self.en_stopwords = {
            'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or',
            'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by', 'was',
            'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'this', 'that',
            'these', 'those', 'am', 'are', 'can', 'may', 'might', 'must',
            'shall', 'from', 'up', 'down', 'out', 'over', 'under', 'again',
            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
            'all', 'each', 'every', 'both', 'few', 'more', 'most', 'some',
            'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
            'too', 'very', 'just', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'its', 'his',
            'her', 'their', 'our', 'your', 'my', 'me', 'you', 'he', 'she',
            'it', 'they', 'we', 'us', 'them'
        }
        
        # 中文填充词
        self.zh_fillers = ['嗯', '啊', '呃', '哦', '诶', '那个', '这个', '就是', '然后', '所以', '其实']
        
        # 英文填充词
        self.en_fillers = ['um', 'uh', 'like', 'you know', 'i mean', 'sort of', 'kind of', 'basically', 'actually', 'literally']
        
        print("✓ 分析器初始化完成")
    
    def clean_text(self, text):
        """
        深度清理文本,去除填充词、标点、数字和多余空格
        
        参数:
            text: 原始文本
        
        返回:
            str: 清理后的文本
        """
        cleaned = text.lower() if self.language == "en" else text
        
        # 1. 去除填充词
        fillers = self.zh_fillers if self.language == "zh" else self.en_fillers
        for filler in fillers:
            pattern = r'\b' + re.escape(filler) + r'\b'
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # 2. 去除标点符号(保留空格)
        cleaned = re.sub(r'[^\w\s]', ' ', cleaned)
        
        # 3. 去除数字
        cleaned = re.sub(r'\d+', '', cleaned)
        
        # 4. 去除多余空格
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    def extract_keywords(self, text, top_n=20):
        """
        提取关键词(改进版,先彻底清理文本)
        
        参数:
            text: 输入文本
            top_n: 返回前N个关键词
        
        返回:
            list: [(词, 频率), ...]
        """
        # 先彻底清理文本
        cleaned = self.clean_text(text)
        
        # 分词
        if self.language == "zh":
            words = jieba.lcut(cleaned)
            stopwords = self.zh_stopwords
        else:
            # 英文按空格分词(已清理标点)
            words = cleaned.split()
            stopwords = self.en_stopwords
        
        # 过滤:去除停用词、单字符
        filtered_words = []
        for word in words:
            word = word.strip()
            # 更严格的过滤条件
            if (len(word) > 1 and                    # 长度>1
                word not in stopwords and             # 不在停用词表
                word.isalpha() and                    # 只包含字母
                not word.isnumeric()):                # 不是纯数字
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
                'amazing', 'perfect', 'best', 'awesome', 'fantastic', 'success',
                'positive', 'effective', 'beneficial', 'improvement', 'progress'
            }
            negative_words = {
                'bad', 'terrible', 'awful', 'sad', 'hate', 'horrible',
                'poor', 'worst', 'disappointing', 'wrong', 'fail', 'negative',
                'crisis', 'problem', 'issue', 'concern', 'threat', 'risk'
            }
        
        # 清理文本
        cleaned = self.clean_text(text)
        words = cleaned.split() if self.language == "en" else list(jieba.cut(cleaned))
        
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
        
        # 彻底清理文本
        cleaned_text = self.clean_text(text)
        
        # 提取关键词用于词云
        keywords = self.extract_keywords(text, top_n=100)
        word_freq_dict = dict(keywords)
        
        try:
            # 生成词云
            if self.language == "zh":
                # 中文需要先分词
                wc = WordCloud(
                    font_path='C:/Windows/Fonts/simhei.ttf',
                    width=800,
                    height=400,
                    background_color='white',
                    max_words=100,
                    relative_scaling=0.5
                ).generate_from_frequencies(word_freq_dict)
            else:
                wc = WordCloud(
                    width=800,
                    height=400,
                    background_color='white',
                    max_words=100,
                    relative_scaling=0.5
                ).generate_from_frequencies(word_freq_dict)
            
            # 保存图片
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            plt.figure(figsize=(10, 5))
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            plt.title('High-Frequency Keywords Word Cloud' if self.language == 'en' else '词云图', fontsize=16)
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
            plt.xlabel('Frequency' if self.language == 'en' else '频率', fontsize=12)
            plt.title('Top Keywords Frequency' if self.language == 'en' else '高频关键词统计', fontsize=14)
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
        report.append("Text Analysis Report" if self.language == 'en' else "文本分析报告")
        report.append("=" * 60)
        report.append("")
        
        # 1. 基础统计
        report.append("【一、Basic Statistics】" if self.language == 'en' else "【一、基础统计】")
        report.append(f"Total characters: {len(text)}" if self.language == 'en' else f"总字符数: {len(text)}")
        
        cleaned = self.clean_text(text)
        if self.language == "zh":
            words = list(jieba.cut(text))
            report.append(f"总词数: {len(words)}")
        else:
            words = text.split()
            report.append(f"Total words: {len(words)}")
        
        report.append(f"Characters after cleaning: {len(cleaned)}" if self.language == 'en' else f"清理后字符数: {len(cleaned)}")
        
        # 显示清理效果
        reduction_rate = (1 - len(cleaned) / len(text)) * 100 if len(text) > 0 else 0
        report.append(f"Text reduction rate: {reduction_rate:.1f}%" if self.language == 'en' else f"文本精简率: {reduction_rate:.1f}%")
        report.append("")
        
        # 2. 关键词分析
        report.append("【二、Top 15 Keywords】" if self.language == 'en' else "【二、高频关键词 TOP 15】")
        keywords = self.extract_keywords(text, top_n=15)
        for i, (word, freq) in enumerate(keywords, 1):
            report.append(f"{i:2d}. {word:15s} - {freq:3d} times" if self.language == 'en' else f"{i:2d}. {word:15s} - {freq:3d}次")
        report.append("")
        
        # 3. 情感分析
        report.append("【三、Sentiment Analysis】" if self.language == 'en' else "【三、情感分析】")
        sentiment = self.analyze_sentiment_simple(text)
        if self.language == 'en':
            report.append(f"Positive words: {sentiment['positive_words']}")
            report.append(f"Negative words: {sentiment['negative_words']}")
            report.append(f"Sentiment: {sentiment['sentiment']}")
            report.append(f"Sentiment score: {sentiment['sentiment_score']:+d}")
        else:
            report.append(f"积极词汇数: {sentiment['positive_words']}")
            report.append(f"消极词汇数: {sentiment['negative_words']}")
            report.append(f"情感倾向: {sentiment['sentiment']}")
            report.append(f"情感得分: {sentiment['sentiment_score']:+d}")
        report.append("")
        
        # 4. 文本特征
        report.append("【四、Text Features】" if self.language == 'en' else "【四、文本特征】")
        avg_word_len = sum(len(w) for w in words) / len(words) if words else 0
        report.append(f"Average word length: {avg_word_len:.2f} characters" if self.language == 'en' else f"平均词长: {avg_word_len:.2f}字符")
        
        unique_words = len(set(words))
        vocab_richness = unique_words / len(words) * 100 if words else 0
        if self.language == 'en':
            report.append(f"Vocabulary richness: {vocab_richness:.1f}% ({unique_words} unique words)")
        else:
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
    print("Text Analysis Tool - Enhanced Version")
    print("="*60)
    
    # 1. 自动查找转录文件
    output_dir = Path("output")
    if not output_dir.exists():
        print(f"\n✗ Error: output folder not found")
        print("Please complete transcription first")
        input("\nPress Enter to exit...")
        return
    
    # 查找所有txt文件
    txt_files = list(output_dir.glob("*transcription.txt"))
    if not txt_files:
        txt_files = list(output_dir.glob("*转录.txt"))
    if not txt_files:
        txt_files = list(output_dir.glob("*.txt"))
    
    if not txt_files:
        print(f"\n✗ Error: No transcription text files found in output folder")
        print("Please run the transcription program first")
        input("\nPress Enter to exit...")
        return
    
    # 如果有多个文件,使用最新的
    text_file = max(txt_files, key=lambda p: p.stat().st_mtime)
    
    print(f"\n✓ Found transcription file: {text_file.name}")
    
    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    print(f"Text length: {len(text)} characters")
    
    if len(text) < 50:
        print(f"\n⚠️ Warning: Text too short ({len(text)} chars), may affect analysis")
        choice = input("Continue? (y/n): ")
        if choice.lower() != 'y':
            return
    
    # 检测语言
    # 简单判断:如果中文字符>10%,认为是中文
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    language = "zh" if chinese_chars / len(text) > 0.1 else "en"
    print(f"Detected language: {'Chinese' if language == 'zh' else 'English'}")
    
    # 2. 创建分析器
    analyzer = SimpleTextAnalyzer(language=language)
    
    # 3. 清理文本并显示效果
    print("\nCleaning text...")
    cleaned_text = analyzer.clean_text(text)
    reduction = (1 - len(cleaned_text) / len(text)) * 100
    print(f"✓ Cleaning completed")
    print(f"  Original: {len(text)} chars")
    print(f"  After cleaning: {len(cleaned_text)} chars")
    print(f"  Reduction rate: {reduction:.1f}%")
    
    # 4. 提取关键词
    print("\nExtracting keywords...")
    keywords = analyzer.extract_keywords(text, top_n=20)
    
    print("\n【Top 10 Keywords】")
    print("-" * 40)
    for i, (word, freq) in enumerate(keywords[:10], 1):
        print(f"{i:2d}. {word:15s} - {freq:3d} times")
    print("-" * 40)
    
    # 5. 情感分析
    print("\nPerforming sentiment analysis...")
    sentiment = analyzer.analyze_sentiment_simple(text)
    print(f"✓ Sentiment: {sentiment['sentiment']}")
    print(f"  Positive words: {sentiment['positive_words']}")
    print(f"  Negative words: {sentiment['negative_words']}")
    
    # 6. 生成可视化
    analyzer.generate_wordcloud(text)
    analyzer.plot_top_keywords(keywords[:15])
    
    # 7. 生成完整报告
    report = analyzer.generate_report(text)
    
    print("\n" + "="*60)
    print("✓ Analysis completed!")
    print("="*60)
    print("\nGenerated files:")
    print("  📊 output/wordcloud.png          (Word cloud)")
    print("  📈 output/keywords_bar.png       (Keyword chart)")
    print("  📄 output/analysis_report.txt    (Analysis report)")
    
    # 询问是否显示报告
    print("\n" + "="*60)
    choice = input("Display full report? (y/n): ")
    if choice.lower() == 'y':
        print("\n" + report)
    
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted")
    except Exception as e:
        print(f"\n✗ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
