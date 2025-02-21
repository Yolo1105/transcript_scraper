import logging
from faster_whisper import WhisperModel, BatchedInferencePipeline
import os
import torch
import ctypes

print(torch.cuda.is_available())
os.environ['CUDA_HOME'] = r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Adjust if you have multiple GPUs

print("CUDA Available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("Device Name:", torch.cuda.get_device_name(0))
else:
    print("CUDA not available in PyTorch")


# ctypes.windll.LoadLibrary('cudnn_ops_infer64_8.dll')
ctypes.windll.LoadLibrary(r"D:\Python38\Lib\site-packages\torch\lib\cudnn_ops_infer64_8.dll")
print("cuDNN loaded successfully")

# 配置日志
logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

# 选择模型大小，可以根据需要调整为 "small", "medium", "large-v2", "large-v3", "distil-large-v3"
model_size = "small"

# 初始化 WhisperModel，使用 GPU 和 FP16 精度
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# 输入文件路径和输出文件夹
input_file = r"C:\Users\mohan\OneDrive\Desktop\aiya\java.mp3"
output_folder = r"C:\Users\mohan\OneDrive\Desktop\aiya"
output_file = os.path.join(output_folder, "java.txt")

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 执行语言检测并将结果保存到文件
with open(output_file, 'w', encoding='utf-8') as f:
    segments, info = model.transcribe(input_file, beam_size=5)
    f.write("检测到的语言: '%s', 概率: %f\n" % (info.language, info.language_probability))

    # 批处理推理，使用批量大小为16
    batched_model = BatchedInferencePipeline(model=model)
    batched_segments, batched_info = batched_model.transcribe(input_file, batch_size=16)

    # # 遍历批处理结果并将每个段落的起止时间及文本写入文件
    # f.write("批处理推理结果:\n")
    # for segment in batched_segments:
    #     f.write("[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end, segment.text))

    # # 获取每个单词的时间戳并将结果写入文件
    # word_level_segments, _ = model.transcribe(input_file, word_timestamps=True)
    # f.write("单词级别时间戳:\n")
    # for segment in word_level_segments:
    #     for word in segment.words:
    #         f.write("[%.2fs -> %.2fs] %s\n" % (word.start, word.end, word.word))

    # 使用 VAD 过滤器来去除音频中没有语音的部分并写入文件
    vad_segments, _ = model.transcribe(input_file, vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500))
    f.write("VAD 过滤后结果:\n")
    for segment in vad_segments:
        f.write("[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end, segment.text))

print(f"转录结果已保存到 {output_file}")
