import os
import random

import numpy as np
import cv2

train_directory = '../../dataset3/coco2017/train2017'
test_directory = '../../dataset3/coco2017/test2017'


def load_data_resize():
    train_images = []
    test_images = []
    size = 64, 64

    for image in os.listdir(train_directory):
        temp_img = cv2.imread(train_directory + '/' + image)
        temp_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2RGB)
        temp_img = cv2.resize(temp_img, size)
        train_images.append(temp_img)

    train_images = np.array(train_images)
    train_images = train_images.astype('uint8')

    for image in os.listdir(test_directory):
        temp_img = cv2.imread(test_directory + '/' + image)
        temp_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2RGB)
        temp_img = cv2.resize(temp_img, size)
        test_images.append(temp_img)

    test_images = np.array(test_images)
    test_images = test_images.astype('uint8')

    print('Loaded', len(train_images), 'images for training,', 'Train data shape =', train_images.shape)
    print('Loaded', len(test_images), 'images for testing', 'Test data shape =', test_images.shape)

    return train_images, test_images


def load_data_split():
    train_images = []
    test_images = []
    size = 64

    for image in os.listdir(train_directory):
        temp_img = cv2.imread(train_directory + '/' + image)
        temp_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2RGB)
        train_images += split_image(temp_img, size)

    train_images = np.array(train_images)
    train_images = train_images.astype('uint8')

    for image in os.listdir(test_directory):
        temp_img = cv2.imread(test_directory + '/' + image)
        temp_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2RGB)
        test_images += split_image(temp_img, size)

    test_images = np.array(test_images)
    test_images = test_images.astype('uint8')

    print('Loaded', len(train_images), 'images for training,', 'Train data shape =', train_images.shape)
    print('Loaded', len(test_images), 'images for testing', 'Test data shape =', test_images.shape)

    return train_images, test_images


def load_data_split_sw():
    train_images = []
    test_images = []
    size = 64

    for image in os.listdir(train_directory):
        temp_img = cv2.imread(train_directory + '/' + image)
        temp_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2RGB)
        train_images += split_image_sliding_window(temp_img, size, 32)

    train_images = np.array(train_images)
    train_images = train_images.astype('uint8')

    for image in os.listdir(test_directory):
        temp_img = cv2.imread(test_directory + '/' + image)
        temp_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2RGB)
        test_images += split_image_sliding_window(temp_img, size, 32)

    test_images = np.array(test_images)
    test_images = test_images.astype('uint8')

    print('Loaded', len(train_images), 'images for training,', 'Train data shape =', train_images.shape)
    print('Loaded', len(test_images), 'images for testing', 'Test data shape =', test_images.shape)

    return train_images, test_images


def split_image(image, sub_images_size):
    number_sub_images_row = image.shape[1] // sub_images_size
    number_sub_images_col = image.shape[0] // sub_images_size
    sub_images = []

    i = 0
    for row in range(number_sub_images_col):
        for col in range(number_sub_images_row):
            x1 = col * sub_images_size
            y1 = row * sub_images_size
            x2 = x1 + sub_images_size
            y2 = y1 + sub_images_size
            sub_image = image[y1:y2, x1:x2]
            if random.random() < 0.2:
                sub_images.append(sub_image)
            i += 1
    return sub_images


def split_image_sliding_window(image, patch_size, stride):
    height, width = image.shape[:2]
    patches = []

    for y in range(0, height - patch_size + 1, stride):
        for x in range(0, width - patch_size + 1, stride):
            patch = image[y:y + patch_size, x:x + patch_size]
            if random.random() < 0.188:
                patches.append(patch)

    return patches
