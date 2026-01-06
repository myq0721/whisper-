"""
Whisper语音转录完整实现
作者: Ayanami
日期: 2026-01-06
"""

import whisper
import time
import json
from pathlib import Path

class WhisperTranscriber:
    """Whisper转录器类"""
    
    def __init__(self, model_size="base"):
        """
        初始化转录器
        
        参数:
            model_size: 模型大小 ('tiny', 'base', 'small', 'medium', 'large')
        """
        print(f"正在加载Whisper {model_size} 模型...")
        self.model = whisper.load_model(model_size)
        print("模型加载完成!")
        
    def transcribe_audio(self, audio_path, language="zh", output_dir="output"):
        """
        转录音频文件
        
        参数:
            audio_path: 音频文件路径
            language: 语言代码 ('zh'=中文, 'en'=英文)
            output_dir: 输出目录
        
        返回:
            dict: 包含转录结果的字典
        """
        # 创建输出目录
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 获取音频文件名(不含扩展名)
        audio_name = Path(audio_path).stem
        
        print(f"\n开始转录: {audio_path}")
        print(f"语言设置: {language}")
        
        # 记录开始时间
        start_time = time.time()
        
        # 执行转录
        result = self.model.transcribe(
            audio_path,
            language=language,
            task="transcribe",  # 'transcribe' 或 'translate'
            verbose=True,       # 显示进度
            fp16=False          # 如果CPU运行,设为False
        )
        
        # 计算耗时
        elapsed_time = time.time() - start_time
        
        # 提取结果
        full_text = result["text"]
        segments = result["segments"]
        detected_language = result["language"]
        
        print(f"\n转录完成! 耗时: {elapsed_time:.2f}秒")
        print(f"检测到的语言: {detected_language}")
        print(f"总段落数: {len(segments)}")
        
        # 保存完整文本
        text_file = Path(output_dir) / f"{audio_name}_transcription.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"转录文本已保存至: {text_file}")
        
        # 保存详细结果(带时间戳)
        detailed_file = Path(output_dir) / f"{audio_name}_detailed.json"
        with open(detailed_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"详细结果已保存至: {detailed_file}")
        
        # 保存带时间戳的文本
        timestamp_file = Path(output_dir) / f"{audio_name}_timestamps.txt"
        with open(timestamp_file, "w", encoding="utf-8") as f:
            for segment in segments:
                start = segment['start']
                end = segment['end']
                text = segment['text']
                f.write(f"[{start:.2f}s - {end:.2f}s] {text}\n")
        print(f"时间戳文本已保存至: {timestamp_file}")
        
        # 返回结果字典
        return {
            'full_text': full_text,
            'segments': segments,
            'language': detected_language,
            'elapsed_time': elapsed_time,
            'word_count': len(full_text.split()),
            'segment_count': len(segments)
        }
    
    def calculate_wer(self, reference_text, hypothesis_text):
        """
        计算词错误率(WER - Word Error Rate)
        
        参数:
            reference_text: 参考文本(正确答案)
            hypothesis_text: 假设文本(转录结果)
        
        返回:
            float: WER百分比
        """
        # 分词
        ref_words = reference_text.split()
        hyp_words = hypothesis_text.split()
        
        # 动态规划计算编辑距离
        d = [[0] * (len(hyp_words) + 1) for _ in range(len(ref_words) + 1)]
        
        for i in range(len(ref_words) + 1):
            d[i][0] = i
        for j in range(len(hyp_words) + 1):
            d[0][j] = j
            
        for i in range(1, len(ref_words) + 1):
            for j in range(1, len(hyp_words) + 1):
                if ref_words[i-1] == hyp_words[j-1]:
                    d[i][j] = d[i-1][j-1]
                else:
                    substitution = d[i-1][j-1] + 1
                    insertion = d[i][j-1] + 1
                    deletion = d[i-1][j] + 1
                    d[i][j] = min(substitution, insertion, deletion)
        
        wer = (d[len(ref_words)][len(hyp_words)] / len(ref_words)) * 100
        return wer


def main():
    """主函数 - 演示如何使用"""
    
    # 1. 创建转录器(可选: tiny, base, small, medium, large)
    transcriber = WhisperTranscriber(model_size="base")
    
    # 2. 转录音频文件
    audio_file = "audio/sample.mp3"  # 替换为你的音频文件路径
    
    result = transcriber.transcribe_audio(
        audio_path=audio_file,
        language="zh",  # 中文用"zh", 英文用"en"
        output_dir="output"
    )
    
    # 3. 打印统计信息
    print("\n=== 转录统计 ===")
    print(f"总字数: {result['word_count']}")
    print(f"段落数: {result['segment_count']}")
    print(f"耗时: {result['elapsed_time']:.2f}秒")
    print(f"检测语言: {result['language']}")
    
    # 4. 如果有参考文本,计算准确率
    reference_file = "audio/sample_reference.txt"  # 参考文本路径
    if Path(reference_file).exists():
        with open(reference_file, "r", encoding="utf-8") as f:
            reference_text = f.read()
        
        wer = transcriber.calculate_wer(reference_text, result['full_text'])
        accuracy = 100 - wer
        print(f"\n转录准确率: {accuracy:.2f}%")
        print(f"词错误率(WER): {wer:.2f}%")
    
    # 5. 显示前5个段落示例
    print("\n=== 转录片段示例(前5段) ===")
    for i, segment in enumerate(result['segments'][:5]):
        print(f"{i+1}. [{segment['start']:.1f}s-{segment['end']:.1f}s] {segment['text']}")


if __name__ == "__main__":
    main()