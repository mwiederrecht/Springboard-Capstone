import tensorflow as tf
import tensorflow.keras.backend as K
from app.config import TRAINING_CONFIG as tc

def weighted_cross_entropy_fn(y_true, y_pred):
    from_logits = False
    tf_y_true = tf.cast(y_true, dtype=y_pred.dtype)
    tf_y_pred = tf.cast(y_pred, dtype=y_pred.dtype)

    weights_v = tf.where(tf.equal(tf_y_true, 1), tc.WEIGHTS[1], tc.WEIGHTS[0])
    ce = K.binary_crossentropy(tf_y_true, tf_y_pred, from_logits=from_logits)
    loss = K.mean(tf.multiply(ce, weights_v))
    return loss

def f1(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val

def MCC(y_true, y_pred):
    y_pred_pos = K.round(K.clip(y_pred, 0, 1))
    y_pred_neg = 1 - y_pred_pos
    y_pos = K.round(K.clip(y_true, 0, 1))
    y_neg = 1 - y_pos
    tp = K.sum(y_pos * y_pred_pos)
    tn = K.sum(y_neg * y_pred_neg)
    fp = K.sum(y_neg * y_pred_pos)
    fn = K.sum(y_pos * y_pred_neg)
    numerator = (tp * tn - fp * fn)
    denominator = K.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    return numerator / (denominator + K.epsilon())

def binary_acc(y_true, y_pred, THRESHOLD):
    results = []
    for (a, b) in list(zip(y_true, y_pred)):
        results.append(int(a == int(b > THRESHOLD)))
    return sum(results) / len(results)