import tensorflow as tf
import stow
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard

from utils.dataProvider import DataProvider
from utils.transformers import ImageResizer, LabelIndexer, LabelPadding
from utils.augmentors import RandomBrightness, RandomRotate, RandomErodeDilate
from utils.utils import ImageReader, CTCloss, Model2onnx, TrainLogger, CWERMetric

from modelNew import train_model
from config import ModelConfigs


dataset, vocab, max_len = [], set(), 0
for file in stow.ls(stow.join('Dataset')):
    dataset.append([stow.relpath(file), file.name])
    vocab.update(list(file.name))
    max_len = max(max_len, len(file.name))

config = ModelConfigs()

config.vocab = "".join(vocab)
config.max_text_length = max_len
config.saveConfig()

data_provider = DataProvider(
    dataset=dataset,
    skip_validation=True,
    batch_size=config.batch_size,
    data_preprocessors=[ImageReader()],
    transformers=[
        ImageResizer(config.width, config.height),
        LabelIndexer(config.vocab),
        LabelPadding(max_word_length=config.max_text_length, padding_value=len(config.vocab))
    ],
)

train_data_provider, val_data_provider = data_provider.split()

train_data_provider.augmentors = [RandomBrightness(), RandomRotate(), RandomErodeDilate()]

model = train_model(
    input_dim=(config.height, config.width, 3),
    output_dim=len(config.vocab),
)

# Compile the model and print summary
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=config.learning_rate),
    loss=CTCloss(),
    metrics=[CWERMetric()],
    run_eagerly=False
)
model.summary(line_length=110)
# Define path to save the model
stow.mkdir(config.model_path)

# Define callbacks
earlystopper = EarlyStopping(monitor='val_CER', patience=40, verbose=1)
checkpoint = ModelCheckpoint(f"{config.model_path}/model.h5", monitor='val_CER', verbose=1, save_best_only=True,
                             mode='min')
trainLogger = TrainLogger(config.model_path)
tb_callback = TensorBoard(f'{config.model_path}/logs', update_freq=1)
reduceLROnPlat = ReduceLROnPlateau(monitor='val_CER', factor=0.9, min_delta=1e-10, patience=20, verbose=1, mode='auto')
model2onnx = Model2onnx(f"{config.model_path}/model.h5")

# Train the model
model.fit(
    train_data_provider,
    validation_data=val_data_provider,
    epochs=config.train_epochs,
    callbacks=[earlystopper, checkpoint, trainLogger, reduceLROnPlat, tb_callback, model2onnx],
    workers=config.train_workers
)

# Save training and validation datasets as csv files
train_data_provider.to_csv(stow.join(config.model_path, 'train.csv'))
val_data_provider.to_csv(stow.join(config.model_path, 'val.csv'))