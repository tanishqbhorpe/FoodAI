import os

# ==========================
# DATASET
# ==========================

DATASET_PATH = "dataset/Food101"

# ==========================
# IMAGE SETTINGS
# ==========================

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32

# ==========================
# TRAINING
# ==========================

INITIAL_EPOCHS = 10
FINE_TUNE_EPOCHS = 15

PHASE1_LR = 1e-3
PHASE2_LR = 1e-5

# ==========================
# MODEL PATHS
# ==========================

MODEL_DIR = "models"

CHECKPOINT_DIR = os.path.join(MODEL_DIR, "checkpoints")
FINAL_MODEL_DIR = os.path.join(MODEL_DIR, "final")

BEST_MODEL_PATH = os.path.join(
    CHECKPOINT_DIR,
    "best_model.keras"
)

FINAL_MODEL_PATH = os.path.join(
    FINAL_MODEL_DIR,
    "food_ai_model.keras"
)

# ==========================
# RESULTS
# ==========================

RESULTS_DIR = "results"

GRAPH_DIR = os.path.join(
    RESULTS_DIR,
    "graphs"
)

METRICS_DIR = os.path.join(
    RESULTS_DIR,
    "metrics"
)

os.makedirs(CHECKPOINT_DIR, exist_ok=True)
os.makedirs(FINAL_MODEL_DIR, exist_ok=True)
os.makedirs(GRAPH_DIR, exist_ok=True)
os.makedirs(METRICS_DIR, exist_ok=True)