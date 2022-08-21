# Audiolytics

A **FastAPI** based tool that loads a .wav file and returns an output. The API is built using **wav2vec2.0** model. It has been uploaded to a **Docker** container and is hosted on an **AWS** EC2 instance. All the processes is automated using **Github Actions** (a CI/CD tool).



## How it works

Implementation of Facebook's wav2vec2.0 model to convert speech into text. The API also returns the start and stop times of each word, all of which are neatly packed in a .json file.


https://user-images.githubusercontent.com/63020303/185771372-d134f8fe-3983-4f30-b873-e9690df5b349.mov

Output generated:

```
Sample_Test_Small.json
{
    'transcript': 'for instance look at their behaviour in the matter of the ring ', 
    'word_dict': 
              {
               0: ('for', 0.04658385093167702, 0.09316770186335405),
               1: ('instance', 0.13975155279503107, 0.40372670807453415), 
               2: ('look', 0.6521739130434783, 0.7453416149068324), 
               3: ('at', 0.7763975155279502, 0.8074534161490683), 
               4: ('their', 0.8540372670807452, 0.9316770186335404), 
               5: ('behaviour', 0.9937888198757763, 1.3664596273291927), 
               6: ('in', 1.5062111801242237, 1.5217391304347827), 
               7: ('the', 1.5838509316770186, 1.6304347826086958), 
               8: ('matter', 1.7080745341614905, 1.8633540372670807), 
               9: ('of', 1.9099378881987579, 1.9409937888198758), 
               10: ('the', 2.0031055900621118, 2.0341614906832297), 
               11: ('ring', 2.111801242236025, 2.251552795031056)
               }
}
```

## Liscence

[MIT](https://choosealicense.com/licenses/mit/)
