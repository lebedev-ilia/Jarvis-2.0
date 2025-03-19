import pyaudio

class JarvisMetaConfig():
    g4f_image_model_name = 'flux'
    g4f_chat_model_name = 'gpt-4'


class JTTS_config():

    seed = 1234
    main_path = '/Users/user/Desktop/Jarvis-2.0/Jarvis'
    ratio_set = [80, 20]
    batch_size = 1
    lr = 0.001
    wd = 0.00001
    epoch = 50
    log_interval = 2
    speaker_wav = '/Users/user/Desktop/Jarvis-2.0/Jarvis/jarvis_dataset/jar58_out.wav'
    MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
    USE_GPU = False


class JSTT_config():

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 512
    os_environ = ''
    MODEL_NAME = "stt_multilingual_fastconformer_hybrid_large_pc" # 'stt_ru_conformer_ctc_large', 'stt_ru_conformer_transducer_large', 'stt_ru_fastconformer_hybrid_large_pc', 'stt_ru_quartznet15x5'


class JTC_config():

    BERT_MODEL = "bert-base-uncased"
    MAX_SEQ_LENGTH=100
    BATCH_SIZE = 16
    GRADIENT_ACCUMULATION_STEPS = 1
    NUM_TRAIN_EPOCHS = 20
    LEARNING_RATE = 5e-5
    WARMUP_PROPORTION = 0.1
    MAX_GRAD_NORM = 5
    OUTPUT_DIR = "/Users/user/Desktop/Jarvis-2.0/Jarvis/"
    MODEL_FILE_NAME = "textclass{epoch}.pt"
    PATIENCE = 2
    CHECKPOINT_PATH = '/Users/user/Desktop/Jarvis-2.0/Jarvis/jarvis_text_classifier/checkpoints/textclass19.pt'
    NUM_LABELS = 9