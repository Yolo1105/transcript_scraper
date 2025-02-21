# **Audio Transcription Pipeline (YouTube Video to Text)**  

This script automates the process of **downloading a video using yt-dlp**, **converting it to audio using ffmpeg**, **transcribing the audio into text with Faster-Whisper**, and **compiling the text into a final document**.  

---

## **Installation**  

Ensure you have the following installed:  

### **1️⃣ Install Dependencies**  
- Install `yt-dlp` (for downloading YouTube videos):  
  ```sh
  pip install yt-dlp
  ```
- Install `ffmpeg` (for audio conversion):  
  - **Windows**: [Download ffmpeg](https://ffmpeg.org/download.html) and add it to PATH.  
  - **Linux/macOS**: Install via package manager:  
    ```sh
    sudo apt install ffmpeg  # Debian-based (Ubuntu)
    brew install ffmpeg       # macOS (Homebrew)
    ```
- Install `faster-whisper` (for audio transcription):  
  ```sh
  pip install faster-whisper
  ```
- Install additional dependencies:  
  ```sh
  pip install torch numpy tqdm
  ```

---

## **Usage**  

### **1️⃣ Download the Video from YouTube**  
You can download the video using **two different methods**:

#### **(A) Without Cookies (Public Videos)**
If the video is **public**, you can download it directly without cookies:

```sh
yt-dlp -o "<OUTPUT_VIDEO_PATH>" "<YOUTUBE_VIDEO_URL>"
```

**Example:**
```sh
yt-dlp -o "C:\Users\mohan\OneDrive\Desktop\video.mp4" https://www.youtube.com/watch?v=Kbn2ab0-sGE
```

#### **(B) With Cookies (Private/Unlisted Videos)**
If the video **requires login**, you must pass your **cookies file**:

```sh
yt-dlp --cookies "<PATH_TO_COOKIES_FILE>" -o "<OUTPUT_VIDEO_PATH>" "<YOUTUBE_VIDEO_URL>"
```

**Example:**  
```sh
yt-dlp --cookies "C:\Users\mohan\OneDrive\Desktop\cookies.txt" -o "C:\Users\mohan\OneDrive\Desktop\video.mp4" https://www.youtube.com/watch?v=Kbn2ab0-sGE
```

---

### **How to Get YouTube Cookies for Authentication**
If you need to download private or unlisted videos, you must extract cookies from your browser. Follow these steps:

#### **Method 1: Using the `cookies.txt` extension (Recommended)**
1. **Install the extension:**
   - **Chrome:** [Get cookies.txt extension](https://chrome.google.com/webstore/detail/get-cookies-txt/gbcnpjimlcefpbkkipcdbcknkbhlgdkl)
   - **Firefox:** [Get cookies.txt extension](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)
   
2. **Go to YouTube** and log in to your account.

3. **Open the video** you want to download.

4. Click on the **cookies.txt extension** and **download the cookies file**.

5. Save the cookies file, e.g., `C:\Users\mohan\OneDrive\Desktop\cookies.txt`.

6. Use it with `yt-dlp`:
   ```sh
   yt-dlp --cookies "C:\Users\mohan\OneDrive\Desktop\cookies.txt" -o "C:\Users\mohan\OneDrive\Desktop\video.mp4" https://www.youtube.com/watch?v=Kbn2ab0-sGE
   ```

---

### **2️⃣ Convert Video to Audio (MP3/WAV using FFmpeg)**  
Convert the downloaded file (`<OUTPUT_VIDEO_PATH>`) into an **MP3** or **WAV** file.

- Convert to **MP3**:  
  ```sh
  ffmpeg -i "<OUTPUT_VIDEO_PATH>" -vn -acodec libmp3lame -q:a 2 "<OUTPUT_AUDIO_PATH>.mp3"
  ```

- Convert to **WAV** (for better transcription accuracy):  
  ```sh
  ffmpeg -i "<OUTPUT_VIDEO_PATH>" -vn -acodec pcm_s16le -ar 16000 -ac 1 "<OUTPUT_AUDIO_PATH>.wav"
  ```

**Example:**  
```sh
ffmpeg -i "C:\Users\mohan\OneDrive\Desktop\video.mp4" -vn -acodec libmp3lame -q:a 2 "C:\Users\mohan\OneDrive\Desktop\audio.mp3"
```

---

### **3️⃣ Transcribe Audio to Text with Faster-Whisper**  
Run **Faster-Whisper** to transcribe the audio file.

```sh
python faster-whisper/whisper.py --model <WHISPER_MODEL_SIZE> --device <DEVICE> --output_dir "<OUTPUT_TEXT_DIR>" "<OUTPUT_AUDIO_PATH>.mp3"
```

- `<WHISPER_MODEL_SIZE>`: Choose from `tiny`, `base`, `small`, `medium`, `large-v2`.
- `<DEVICE>`: Use `cuda` for GPU acceleration or `cpu` for standard processing.

**Example:**  
```sh
python faster-whisper/whisper.py --model small --device cuda --output_dir "C:\Users\mohan\OneDrive\Desktop\output" "C:\Users\mohan\OneDrive\Desktop\audio.mp3"
```

The transcription results will be saved in the `output/` folder.

---

### **4️⃣ Combine All Transcriptions into a Single Text File**  
Use `convert.py` to merge all transcribed text into a final document.

```sh
python convert.py "<OUTPUT_TEXT_DIR>"
```

**Example:**  
```sh
python convert.py "C:\Users\mohan\OneDrive\Desktop\output"
```

This script will:
- Read all transcribed segments from `output/`.
- Merge them into a single `.txt` file.

---

## **Final Output**
The final transcribed text will be saved as:

```
<OUTPUT_TEXT_DIR>/final_transcript.txt
```

---

## **Example Workflow (All Steps Combined)**
```sh
yt-dlp --cookies "C:\Users\mohan\OneDrive\Desktop\cookies.txt" -o "C:\Users\mohan\OneDrive\Desktop\video.mp4" https://www.youtube.com/watch?v=Kbn2ab0-sGE
ffmpeg -i "C:\Users\mohan\OneDrive\Desktop\video.mp4" -vn -acodec libmp3lame -q:a 2 "C:\Users\mohan\OneDrive\Desktop\audio.mp3"
python faster-whisper/whisper.py --model small --device cuda --output_dir "C:\Users\mohan\OneDrive\Desktop\output" "C:\Users\mohan\OneDrive\Desktop\audio.mp3"
python convert.py "C:\Users\mohan\OneDrive\Desktop\output"
```

If the video is **public**, remove the `--cookies` flag and run:

```sh
yt-dlp -o "C:\Users\mohan\OneDrive\Desktop\video.mp4" https://www.youtube.com/watch?v=Kbn2ab0-sGE
```

---

## **Notes**
- **Replace placeholders (`<...>`)** with actual file paths.
- **Use the cookies method only if the video is private or unlisted.**
- **Make sure your cookies file is up to date** for YouTube authentication.
- **Use a larger Whisper model (`medium`, `large-v2`)** for better accuracy.
- **If you don’t have a GPU,** set `--device cpu` in the transcription step.