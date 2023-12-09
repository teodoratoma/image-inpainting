from tensorflow import keras


def create_model(input_size=(64, 64, 3)):
    start_neurons = 32
    inputs = keras.layers.Input(input_size)

    conv1, pool1 = ConvBlock(start_neurons, (3, 3), (2, 2), 'relu', 'same', inputs)
    conv2, pool2 = ConvBlock(start_neurons * 2, (3, 3), (2, 2), 'relu', 'same', pool1)
    conv3, pool3 = ConvBlock(start_neurons * 4, (3, 3), (2, 2), 'relu', 'same', pool2)
    conv4, pool4 = ConvBlock(start_neurons * 8, (3, 3), (2, 2), 'relu', 'same', pool3)

    conv5, up5 = UpConvBlock(start_neurons * 16, start_neurons * 8, (3, 3), (2, 2), (2, 2), 'relu', 'same', pool4,
                             conv4)
    conv6, up6 = UpConvBlock(start_neurons * 8, start_neurons * 4, (3, 3), (2, 2), (2, 2), 'relu', 'same', up5, conv3)
    conv7, up7 = UpConvBlock(start_neurons * 4, start_neurons * 2, (3, 3), (2, 2), (2, 2), 'relu', 'same', up6, conv2)
    conv8, up8 = UpConvBlock(start_neurons * 2, start_neurons, (3, 3), (2, 2), (2, 2), 'relu', 'same', up7, conv1)

    conv9 = ConvBlock(start_neurons, (3, 3), (2, 2), 'relu', 'same', up8, False)

    outputs = keras.layers.Conv2D(3, (3, 3), activation='sigmoid', padding='same')(conv9)

    return keras.models.Model(inputs=[inputs], outputs=[outputs])


def ConvBlock(filters, kernel_size, pool_size, activation, padding, connecting_layer, pool_layer=True):
    conv = keras.layers.Conv2D(filters=filters, kernel_size=kernel_size, activation=activation, padding=padding)(
        connecting_layer)
    conv = keras.layers.Conv2D(filters=filters, kernel_size=kernel_size, activation=activation, padding=padding)(
        conv)
    if pool_layer:
        pool = keras.layers.MaxPooling2D(pool_size)(conv)
        return conv, pool
    else:
        return conv


def UpConvBlock(filters, up_filters, kernel_size, up_kernel, up_stride, activation, padding,
                connecting_layer, shared_layer):
    conv = keras.layers.Conv2D(filters=filters, kernel_size=kernel_size, activation=activation, padding=padding)(
        connecting_layer)
    conv = keras.layers.Conv2D(filters=filters, kernel_size=kernel_size, activation=activation, padding=padding)(
        conv)
    up = keras.layers.Conv2DTranspose(filters=up_filters, kernel_size=up_kernel, strides=up_stride,
                                      padding=padding)(conv)
    up = keras.layers.concatenate([up, shared_layer], axis=3)

    return conv, up
