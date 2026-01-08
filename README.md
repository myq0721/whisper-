
### **1.1 安装Python**

```bash
# Windows系统:
# 1. 访问 https://www.python.org/downloads/
# 2. 下载Python 3.8-3.11版本(推荐3.10)
# 3. 安装时勾选 "Add Python to PATH"
# 4. 验证安装
python --version
```

### **1.2 安装Chocolatey(Windows包管理器)**

以**管理员身份**打开PowerShell:

```powershell
# 设置执行策略
Set-ExecutionPolicy Bypass -Scope Process -Force

# 安装Chocolatey
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 验证安装
choco --version
```

### **1.3 安装FFmpeg(音频处理工具)**

```bash
# 使用Chocolatey安装
choco install ffmpeg

# 验证安装
ffmpeg -version
```

### **1.4 安装Git**

```bash
# 使用Chocolatey安装
choco install git

# 验证安装
git --version
```

### **1.5 安装Whisper及相关库**

```bash
# 1. 升级pip
python -m pip install --upgrade pip

# 2. 安装Whisper
pip install openai-whisper

# 3. 安装必要的依赖
pip install tiktoken  # Whisper的分词器
pip install setuptools-rust  # 编译工具

# 4. 安装文本处理库
pip install nltk spacy stanza

# 5. 安装数据分析和可视化库
pip install pandas matplotlib wordcloud

# 验证Whisper安装
python -c "import whisper; print(whisper.__version__)"
```
### **2.1 项目文件结构**

创建以下文件夹结构:
```
whisper_project/
├── audio/              # 存放音频文件
├── output/             # 存放转录结果
├── code/               # 存放Python代码
│   ├── transcribe.py   # 转录主程序
│   ├── analyze.py      # 文本分析程序
│   └── utils.py        # 工具函数
└── report/             # 存放报告
```

### **2.2 核心代码:语音转录**

创建 `transcribe.py`:### **2.3 文本分析代码**

创建 `analyze.py`:---

## 第三部分:关键名词深度解释

### **3.1 语音转录相关**

| 名词 | 英文 | 解释 | 举例 |
|------|------|------|------|
| **转录** | Transcription | 将语音信号转换为文字的过程 | 录音→"你好世界" |
| **WER** | Word Error Rate | 词错误率,衡量转录准确度的指标<br>WER = (替换+删除+插入)/总词数×100% | 参考:"我爱北京"<br>转录:"我在北京"<br>WER=25% |
| **Token** | Token | 文本的最小单位,可以是字、词或子词 | 中文:"我/爱/你"(3个token)<br>英文:"I love you"(3个token) |
| **模型尺寸** | Model Size | Whisper有5个版本:tiny<base<small<medium<large<br>越大越准确但越慢 | base:74M参数,速度快<br>large:1550M参数,最准确 |
| **语言检测** | Language Detection | 自动识别音频的语言类型 | 输入日语音频→检测出"ja" |
| **时间戳** | Timestamp | 记录每句话的起止时间 | [0.5s-3.2s] "大家好" |

### **3.2 文本处理相关**

| 名词 | 英文 | 解释 | 核心功能 |
|------|------|------|----------|
| **NLTK** | Natural Language Toolkit | Python基础NLP库,适合学习 | 分词、词性标注、情感分析 |
| **spaCy** | spaCy | 工业级NLP库,速度快 | 命名实体识别、依存句法 |
| **Stanza** | Stanza | 斯坦福NLP库,多语言支持 | 神经网络分词、句法树 |
| **停用词** | Stop Words | 高频但无实际意义的词 | 中文:的、了、在<br>英文:the、is、a |
| **词性标注** | POS Tagging | 标注每个词的语法属性 | "我/代词 爱/动词 你/代词" |
| **依存句法** | Dependency Parsing | 分析词与词之间的语法关系 | "我"←nsubj─"爱"→obj→"你" |

### **3.3 模型架构相关**

| 名词 | 解释 | Whisper中的应用 |
|------|------|------------------|
| **Transformer** | 基于自注意力机制的神经网络架构 | Whisper的底层结构 |
| **编码器** | Encoder,将输入转换为向量表示 | 处理音频信号 |
| **解码器** | Decoder,根据向量生成输出 | 生成文字转录 |
| **注意力机制** | Attention,让模型关注重要信息 | 关联音频片段和对应文字 |

---

## 第四部分:实战操作步骤

### **步骤1:准备音频文件**

```python
# 音频要求:
# - 格式: mp3/wav/m4a等常见格式
# - 时长: 3-5分钟
# - 质量: 清晰无杂音
```

### **步骤2:运行转录代码**

```bash
# 1. 将音频文件放入 audio/ 文件夹
# 2. 运行转录程序
python code/transcribe.py

# 3. 查看结果
# output/xxx_transcription.txt - 纯文本
# output/xxx_detailed.json - 详细数据
# output/xxx_timestamps.txt - 带时间戳
```

### **步骤3:计算准确率**(如果有参考文本)

```python
# 在transcribe.py中添加:
reference_text = "这是正确的文本内容..."
hypothesis_text = result['full_text']

wer = transcriber.calculate_wer(reference_text, hypothesis_text)
accuracy = 100 - wer
print(f"准确率: {accuracy:.2f}%")
```

### **步骤4:文本分析**

```bash
# 运行分析程序
python code/analyze.py
# 生成结果:
# output/wordcloud.png - 词云图
# output/keywords_bar.png - 关键词柱状图
# output/analysis_report.txt - 文本报告
```


### **问题1:模型下载慢**

```python
# 方案1:使用国内镜像
pip install openai-whisper -i https://pypi.tuna.tsinghua.edu.cn/simple

# 方案2:手动下载模型文件
# 访问 https://github.com/openai/whisper
# 下载.pt文件后放入 ~/.cache/whisper/
```

### **问题2:中文分词效果差**

```bash
# 安装jieba中文分词库
pip install jieba

# 在代码中使用
import jieba
words = jieba.lcut(text)
```

### **问题3:spaCy模型安装失败**

```bash
# 直接下载模型
python -m spacy download zh_core_web_sm
python -m spacy download en_core_web_sm

# 如果网络问题,使用离线安装
# 1. 下载模型文件
# 2. pip install zh_core_web_sm-x.x.x.tar.gz
```

### **问题4:内存不足**

```python
# 使用更小的模型
model = whisper.load_model("tiny")  # 只需39MB内存

# 或分段处理长音频
from pydub import AudioSegment
audio = AudioSegment.from_mp3("long.mp3")
chunk = audio[0:60000]  # 前60秒
chunk.export("chunk.mp3")
```

### ps：由于pythonspaCy在Python 3.14下无法使用
# 选择只依赖jieba和matplotlib功能完全够用
python code/analyze_no_spacy.py
