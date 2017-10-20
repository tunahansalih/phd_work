from enum import Enum

import tensorflow as tf


class GradientType(Enum):
    mixture_of_experts_unbiased = 0
    mixture_of_experts_biased = 1
    parallel_dnns_unbiased = 2
    parallel_dnns_biased = 3


class GlobalConstants:
    EPOCH_COUNT = 500
    BATCH_SIZE = 1000
    EVAL_BATCH_SIZE = 50000
    IMAGE_SIZE = 28
    NUM_CHANNELS = 1
    NO_FILTERS_1 = 20
    NO_FILTERS_2 = 10 # 10
    NO_HIDDEN = 30 # 30
    NUM_LABELS = 10
    WEIGHT_DECAY_COEFFICIENT = 0.0
    INITIAL_LR = 0.015
    DECAY_STEP = 5000
    DECAY_RATE = 0.5
    TREE_DEGREE = 3
    MOMENTUM_DECAY = 0.9
    DATA_TYPE = tf.float32
    SEED = None
    USE_CPU = False
    USE_CPU_MASKING = False
    USE_EMPTY_NODE_CRASH_PREVENTION = False
    USE_RANDOM_PARAMETERS = True
    USE_PROBABILITY_THRESHOLD = False
    SAVE_CONFUSION_MATRICES = False
    GRADIENT_TYPE = GradientType.mixture_of_experts_biased
    TRAIN_DATA_TENSOR = tf.placeholder(DATA_TYPE, shape=(BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, NUM_CHANNELS))
    TRAIN_LABEL_TENSOR = tf.placeholder(tf.int64, shape=(BATCH_SIZE,))
    TEST_DATA_TENSOR = tf.placeholder(DATA_TYPE, shape=(EVAL_BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, NUM_CHANNELS))
    TEST_LABEL_TENSOR = tf.placeholder(tf.int64, shape=(EVAL_BATCH_SIZE,))
