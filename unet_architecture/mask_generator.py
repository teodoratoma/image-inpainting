from tensorflow import keras
import numpy as np
import cv2


class MaskGenerator(keras.utils.Sequence):
    def __init__(self, images, original_images, batch_size=8, image_dimension=(64, 64), no_of_channels=3, shuffle=True):
        self.indexes = []
        self.batch_size = batch_size
        self.images = images
        self.original_images = original_images
        self.image_dimension = image_dimension
        self.no_of_channels = no_of_channels
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        return int(np.floor(len(self.images) / self.batch_size))

    def __getitem__(self, index):
        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        return self.data_generator(indexes)

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.images))
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def data_generator(self, indexes):
        masked_batch = np.empty(
            (self.batch_size, self.image_dimension[0], self.image_dimension[1], self.no_of_channels))
        original_batch = np.empty(
            (self.batch_size, self.image_dimension[0], self.image_dimension[1], self.no_of_channels))

        for i, idx in enumerate(indexes):
            image_copy = self.images[idx].copy()
            masked_image = self.create_masked_image(image_copy)
            masked_batch[i, ] = masked_image / 255
            original_batch[i] = self.original_images[idx] / 255

        return masked_batch, original_batch

    def create_masked_image(self, image):
        mask = np.full((self.image_dimension[0], self.image_dimension[1], self.no_of_channels), 255, np.uint8)
        for _ in range(np.random.randint(1, 12)):
            x1, x2 = np.random.randint(self.image_dimension[1] + 1), np.random.randint(self.image_dimension[1] + 1)
            y1, y2 = np.random.randint(self.image_dimension[0] + 1), np.random.randint(self.image_dimension[0] + 1)
            thickness = np.random.randint(1, 6)
            cv2.line(mask, (x1, y1), (x2, y2), (0, 0, 0), thickness)
        masked_image = cv2.bitwise_and(image, mask)
        return masked_image
