import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline, WhisperForConditionalGeneration
import librosa
import threading
import json


class WhisperUIService:
    def __init__(self):
        self.model_id = ""
        self.audio_path = ""

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

    def __thread(self, on_finish):
        try:
            device = "cuda:0" if torch.cuda.is_available() else "cpu"
            torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
            processor = AutoProcessor.from_pretrained(self.model_id)

            model = WhisperForConditionalGeneration.from_pretrained(self.model_id)
            # model = AutoModelForSpeechSeq2Seq.from_pretrained(
            #     self.model_id,
            #     torch_dtype=torch_dtype,
            #     low_cpu_mem_usage=True,
            #     use_safetensors=True
            # )
            model.to(device)


            # pipe = pipeline(
            #     "automatic-speech-recognition",
            #     model=model,
            #     tokenizer=processor.tokenizer,
            #     feature_extractor=processor.feature_extractor,
            #     batch_size=16,
            #     return_timestamps=True,
            #     dtype=torch_dtype,
            #     device=device,
            #     generate_kwargs={"language": "fr"}
            # )

            audio, sample_rate = librosa.load(self.audio_path, sr=16000, mono=True)
            inputs = processor(audio, return_tensors="pt", truncation=False, padding="longest", return_attention_mask=True, sampling_rate=16_000).input_features

            generated_ids = model.generate(
                inputs, 
                return_timestamps=True,
                task="transcribe", 
                language="fr"
                )
            
            for pidi, pid in enumerate(generated_ids):
                # timestamps = processor.tokenizer.decode(pid, decode_with_timestamps=True)
                timestamps = processor.tokenizer.decode(pid, output_offset=True)
                pdict = processor.tokenizer.decode(pid, output_offsets=True)
                print(f"Predicted id [{pidi}]: {pdict['text']}")
                print(f"Predicted id [{pidi}]: {pdict['offsets']}")
            
            # transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)
            # # result = pipe(audio, chunk_length_s = 10)

            # on_finish(transcription)

        except FileNotFoundError as e:
            print("file not found")

        except RuntimeError as e:
            print("run time error")
            print(e)

        except Exception as e:
            print("unhandeld exception")
            print(e)
            