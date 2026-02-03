import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import librosa
import threading


class WhisperUIService:
    def __init__(self):
        self.__model_id = r"C:\Users\clever\Documents\python\tkinter_whisper\model\small"
        self.audio_path = r"C:\Users\clever\Documents\python\tkinter_whisper\small_audio.mp3"

    def transcribe(self, on_finish):
        t = threading.Thread(target=self.__thread, daemon=True, args=(on_finish,))
        t.start()

    def __thread(self, on_finish):
        try:
            device = "cuda:0" if torch.cuda.is_available() else "cpu"
            torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

            model_id = r"C:\Users\clever\Documents\python\tkinter_whisper\model\small"
            audio_file = r"C:\Users\clever\Documents\python\tkinter_whisper\audio.mp3"

            model = AutoModelForSpeechSeq2Seq.from_pretrained(
                model_id,
                torch_dtype=torch_dtype,
                low_cpu_mem_usage=True,
                use_safetensors=True
            )
            model.to(device)

            processor = AutoProcessor.from_pretrained(model_id)

            pipe = pipeline(
                "automatic-speech-recognition",
                model=model,
                tokenizer=processor.tokenizer,
                feature_extractor=processor.feature_extractor,
                batch_size=16,
                return_timestamps=True,
                dtype=torch_dtype,
                device=device,
                generate_kwargs={"language": "fr"}
            )

            audio, sample_rate = librosa.load(audio_file, sr=16000, mono=True)

            result = pipe(audio)

            on_finish(result)

        except FileNotFoundError as e:
            print("file not found")

        except RuntimeError as e:
            print("run time error")
            print(e)

        except Exception as e:
            print("unhandeld exception")
            print(e)
            