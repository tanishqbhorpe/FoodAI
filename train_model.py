# ==========================================================
# FOOD AI V2 - TRAIN MODEL
# ==========================================================

import os
import json
import random
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ReduceLROnPlateau,
    ModelCheckpoint,
    CSVLogger
)

from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from config import *

# ==========================================================
# RANDOM SEED
# ==========================================================

SEED = 42

random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

AUTOTUNE = tf.data.AUTOTUNE

# ==========================================================
# LOAD DATASET
# ==========================================================

print("=" * 60)
print("Loading Dataset")
print("=" * 60)

train_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.20,
    subset="training",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.20,
    subset="validation",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

CLASS_NAMES = train_dataset.class_names
NUM_CLASSES = len(CLASS_NAMES)

with open("models/final/class_names.json", "w") as f:
    json.dump(CLASS_NAMES, f, indent=4)

train_dataset = train_dataset.prefetch(AUTOTUNE)
validation_dataset = validation_dataset.prefetch(AUTOTUNE)

print(f"\nClasses : {NUM_CLASSES}")
print(f"Images Loaded Successfully\n")

# ==========================================================
# DATA AUGMENTATION
# ==========================================================

data_augmentation = keras.Sequential([

    layers.RandomFlip("horizontal"),

    layers.RandomRotation(0.15),

    layers.RandomZoom(0.15),

    layers.RandomContrast(0.15),

])

# ==========================================================
# BUILD MODEL
# ==========================================================

print("=" * 60)
print("Building EfficientNetB0")
print("=" * 60)

base_model = EfficientNetB0(

    weights="imagenet",

    include_top=False,

    input_shape=(224,224,3)

)

base_model.trainable = False

inputs = keras.Input(shape=(224,224,3))

x = data_augmentation(inputs)

x = preprocess_input(x)

x = base_model(x, training=False)

x = layers.GlobalAveragePooling2D()(x)

x = layers.BatchNormalization()(x)

x = layers.Dropout(0.40)(x)

x = layers.Dense(
    512,
    activation="relu"
)(x)

x = layers.BatchNormalization()(x)

x = layers.Dropout(0.30)(x)

x = layers.Dense(
    256,
    activation="relu"
)(x)

outputs = layers.Dense(
    NUM_CLASSES,
    activation="softmax"
)(x)

model = keras.Model(
    inputs,
    outputs
)

# ==========================================================
# COMPILE
# ==========================================================

optimizer = keras.optimizers.AdamW(

    learning_rate=PHASE1_LR,

    weight_decay=1e-4

)

model.compile(

    optimizer=optimizer,

    loss="sparse_categorical_crossentropy",

    metrics=[

        "accuracy",

        keras.metrics.SparseTopKCategoricalAccuracy(

            k=3,

            name="top3_accuracy"

        )

    ]

)

print("\nModel Compiled Successfully\n")

# ==========================================================
# CALLBACKS
# ==========================================================

callbacks = [

    ModelCheckpoint(

        BEST_MODEL_PATH,

        monitor="val_accuracy",

        save_best_only=True,

        verbose=1

    ),

    EarlyStopping(

        monitor="val_loss",

        patience=5,

        restore_best_weights=True

    ),

    ReduceLROnPlateau(

        monitor="val_loss",

        factor=0.2,

        patience=2,

        verbose=1

    ),

    CSVLogger(

        "results/metrics/training_log.csv"

    )

]

print("Pipeline Ready")
# ==========================================================
# PHASE 1 TRAINING
# ==========================================================

print("\n" + "=" * 60)
print("PHASE 1 - TRAINING CLASSIFIER")
print("=" * 60)

history_phase1 = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=INITIAL_EPOCHS,
    callbacks=callbacks
)

# ==========================================================
# PHASE 2 - FINE TUNING
# ==========================================================

print("\n" + "=" * 60)
print("PHASE 2 - FINE TUNING")
print("=" * 60)

base_model.trainable = True

for layer in base_model.layers[:-50]:
    layer.trainable = False

model.compile(
    optimizer=keras.optimizers.AdamW(
        learning_rate=PHASE2_LR,
        weight_decay=1e-5
    ),
    loss="sparse_categorical_crossentropy",
    metrics=[
        "accuracy",
        keras.metrics.SparseTopKCategoricalAccuracy(
            k=3,
            name="top3_accuracy"
        )
    ]
)

history_phase2 = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=INITIAL_EPOCHS + FINE_TUNE_EPOCHS,
    initial_epoch=history_phase1.epoch[-1] + 1,
    callbacks=callbacks
)

# ==========================================================
# SAVE FINAL MODEL
# ==========================================================

model.save(FINAL_MODEL_PATH)

print("\n")
print("=" * 60)
print("TRAINING COMPLETED")
print("=" * 60)
print(f"Final model saved to : {FINAL_MODEL_PATH}")
print(f"Best model saved to  : {BEST_MODEL_PATH}")
print("=" * 60)