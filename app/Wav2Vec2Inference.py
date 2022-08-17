
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import numpy as np
from scipy.io import wavfile
import librosa
import ffmpeg
from itertools import groupby

# Class to get the inference of the model
class Wav2VecInference:
    def __init__(self, model_name = "facebook/wav2vec2-large-960h"):
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name)
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
    def inference(self, audio_file):
        transcript = ""
        # # Ensure that the sample rate is 16k
        audio, sr = librosa.load(audio_file,  sr=16000)

        duration = librosa.get_duration(y=audio, sr=sr)
        chunks = librosa.effects.split(audio, frame_length=5000, top_db=30, hop_length=4000)
 
        print(f"Total chunks: {len(chunks)}")
        total_predicted_ids = []
        for i, speech in enumerate(chunks):
            print(f"Processing chunk: {i+1}")
            input_values = self.processor(audio[speech[0] : speech[1]], sampling_rate= 16000 , return_tensors='pt')
            with torch.no_grad():
                output = self.model(**input_values)
                predicted_ids = output[0].argmax(dim=-1).cpu().numpy()
            text=  self.processor.decode(predicted_ids[0]).lower()


            transcript += text + " "
            total_predicted_ids+= predicted_ids[0].tolist()
            print("Next chunk")

        words, word_start_times, word_end_times = self.timestamp(transcript, total_predicted_ids, input_values)
        word_dict = {}
        for i, word in enumerate(words):
            word_dict[i] = (word, word_start_times[i], word_end_times[i])
        # create a dictionary with transcript and word_dict
        final_dict={}
        final_dict["transcript"] = transcript
        final_dict["word_dict"] = word_dict
        return final_dict
        
    def timestamp(self, transcription, import_predicted_ids, input_values):
        # this is where the logic starts to get the start and end timestamp for each word

        ##############
        sample_rate = 16000
        words = [w for w in transcription.split(' ') if len(w) > 0]
        duration_sec = input_values["input_values"].shape[1] / sample_rate


        ids_w_time = [(i / len(import_predicted_ids) * duration_sec, _id) for i, _id in enumerate(import_predicted_ids)]
        # remove entries which are just "padding" (i.e. no characers are recognized)
        ids_w_time = [i for i in ids_w_time if i[1] != self.processor.tokenizer.pad_token_id]
        # now split the ids into groups of ids where each group represents a word
        split_ids_w_time = [list(group) for k, group
                          in groupby(ids_w_time, lambda x: x[1] == self.processor.tokenizer.word_delimiter_token_id) if not k]


        assert len(split_ids_w_time) == len(words)  # make sure that there are the same number of id-groups as words. Otherwise something is wrong

        word_start_times = []
        word_end_times = []
        for cur_ids_w_time, cur_word in zip(split_ids_w_time, words):
            _times = [_time for _time, _id in cur_ids_w_time]
            word_start_times.append(min(_times))
            word_end_times.append(max(_times))
            
        return words, word_start_times, word_end_times
