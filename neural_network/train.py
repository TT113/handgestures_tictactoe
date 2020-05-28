import cv2
import numpy as np
from keras_squeezenet import SqueezeNet
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.layers import Activation, Dropout, Convolution2D, GlobalAveragePooling2D
from keras.models import Sequential
from neural_network.constants import *
import os


CATEGORY_MAP = {
    "up": 0,
    "left": 1,
    "down": 2,
    "right": 3,
    "enter": 4
}

def def_model_param():
    gesture_categories = len(CATEGORY_MAP)
    base_model = Sequential()
    base_model.add(SqueezeNet(input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3), include_top=False))
    base_model.add(Dropout(0.5))
    base_model.add(Convolution2D(gesture_categories, (1, 1), padding='valid'))
    base_model.add(Activation('relu'))
    base_model.add(GlobalAveragePooling2D())
    base_model.add(Activation('softmax'))
    return base_model


def label_mapper(val):
    return CATEGORY_MAP[val]


input_data = []
for sub_folder_name in os.listdir(TRAINING_IMAGES_FOLDER):
    path = os.path.join(TRAINING_IMAGES_FOLDER, sub_folder_name)
    if '.DS_Store' in path:
        continue
    for fileName in os.listdir(path):
        if fileName.endswith(".jpg"):
            img = cv2.imread(os.path.join(path, fileName))
            if img is None:
                continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))
            input_data.append([img, sub_folder_name])

img_data, labels = zip(*input_data)
labels = list(map(label_mapper, labels))
labels = np_utils.to_categorical(labels)

model = def_model_param()
model.compile(
    optimizer=Adam(lr=ADAM_LEARNING_RATE),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

X_trn, y_trn = np.array(img_data), np.array(labels)
model.fit(X_trn, y_trn, epochs=EPOCHS_QUANTITY)
model.save(WEIGHTS_FILE_NAME)
