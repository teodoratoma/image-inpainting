from keras.losses import mean_absolute_error
from tensorflow import keras
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import tensorflow as tf
import numpy as np


def dice_coefficient(original, generated):
    original_flatten = keras.backend.flatten(original)
    generated_flatten = keras.backend.flatten(generated)
    intersection = keras.backend.sum(original_flatten * generated_flatten)
    return (2. * intersection) / (keras.backend.sum(original_flatten + generated_flatten))


def SSIM_loss(original, generated):
    return 1 - tf.reduce_mean(tf.image.ssim(original, generated, 1.0))


def SSIM_MAE_loss(original, generated, alpha=0.3):
    ssim_loss = 1 - tf.image.ssim(original, generated, max_val=1.0)
    mae_loss = mean_absolute_error(original, generated)
    total_loss = alpha * ssim_loss + (1 - alpha) * mae_loss
    return total_loss


def PSNR(original, generated):
    return tf.image.psnr(original, generated, max_val=1.0)


def SSIM(original, generated):
    return tf.image.ssim(original, generated, max_val=1.0)


def mae(original, generated):
    original, generated = np.array(original), np.array(generated)
    return np.mean(np.abs(original - generated))


def visualize_dataset(train_data):
    sample_idx = 40

    sample_masked_images, sample_original_images, sample_masks = train_data[sample_idx]
    sample_images = [None] * (len(sample_masked_images) + len(sample_original_images) + len(sample_masks))
    sample_images[::3] = sample_original_images
    sample_images[1::3] = sample_masks
    sample_images[2::3] = sample_masked_images

    fig = plt.figure(figsize=(16., 8.))
    grid = ImageGrid(fig, 111, nrows_ncols=(4, 6), axes_pad=0.3)

    for ax, image in zip(grid, sample_images):
        ax.imshow(image)

    plt.savefig('dataset_visualization2.png')
    plt.close()


def plot_evaluation_metric(model, metric_eval, title, file_location):
    plt.plot(model.history[metric_eval])
    plt.plot(model.history['val_' + metric_eval])
    plt.title(title)
    plt.ylabel(metric_eval)
    plt.xlabel('epoch')
    plt.legend(['train', 'test'])
    plt.savefig(file_location + '/' + metric_eval)
    plt.close()
