import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline, WhisperForConditionalGeneration
import librosa
import threading
import json
#https://github.com/huggingface/transformers/issues/30815#issuecomment-2254296338
#https://github.com/huggingface/transformers/issues/20057
#https://huggingface.co/docs/transformers/model_doc/whisper#transformers.WhisperForConditionalGeneration.generate
#https://github.com/m-bain/whisperX

class WhisperUIService:
    def __init__(self, root, progress_bar_status):
        self.model_id = ""
        self.audio_path = ""
        self.root = root
        self.progress_bar_status = progress_bar_status

    def load_config(self, config_file_path):
        with open(config_file_path, "r") as f:
            models = json.load(f)

        for model in models:
            if model.get("default") is True:
                self.model_id = model.get("model_path")
                return
            

    def transcribe(self, on_finish):
        t = threading.Thread(target=self.__thread, daemon=True, args=(on_finish,))
        t.start()

    def __progress_callback(self, t):
        i = torch.argmax(t[:, 1])
        p = t[i].detach().cpu()
        self.progress_bar_status["percentage_done"] = (int(p[0]) / int(p[1])) * 100
        self.root.event_generate("<<update_progress_bar_event>>", when="tail", state=0)
        # print(int(p[1]))
        # print(int(p[0]))

    def __thread(self, on_finish):
        try:
            device = "cuda:0" if torch.cuda.is_available() else "cpu"
            torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
            processor = AutoProcessor.from_pretrained(self.model_id)

            model = WhisperForConditionalGeneration.from_pretrained(self.model_id)
            model.to(device, torch_dtype)

            audio, sample_rate = librosa.load(self.audio_path, sr=16000, mono=True)
            inputs = processor(audio, return_tensors="pt", truncation=False, padding="longest", return_attention_mask=True, sampling_rate=16_000)

            generated_ids = model.generate(
                inputs.input_features,
                attention_mask=inputs.attention_mask,
                return_timestamps=True,
                task="transcribe", 
                language="fr",
                monitor_progress=self.__progress_callback
            )

            pid = generated_ids[0]
            pdict = processor.tokenizer.decode(pid, output_offsets=True)

            on_finish(pdict)
            

        except Exception as e:
            print("unhandeld exception")
            print(e)
            self.root.event_generate("<<update_progress_bar_event>>", when="tail", state=1)
            