from unet_architecture.load_dataset import load_data_split
from unet_architecture.mask_generator import MaskGenerator
from unet_architecture.neural_network import create_model
from unet_architecture.util import dice_coefficient, PSNR, SSIM


def train_model(train_images, test_images, model_name, number_of_epochs=20):
    train_data = MaskGenerator(train_images, train_images, batch_size=64, image_dimension=(64, 64))
    test_data = MaskGenerator(test_images, test_images, batch_size=64, image_dimension=(64, 64), shuffle=False)
    model = create_model(input_size=(64, 64, 3))
    model.compile(optimizer='adam', loss='mean_absolute_error', metrics=[dice_coefficient, PSNR, SSIM])

    model_history = model.fit(train_data,
                              validation_data=test_data,
                              epochs=number_of_epochs,
                              steps_per_epoch=len(train_data),
                              validation_steps=len(test_data))
    model.save(model_name)
    return model_history


x_train, x_test = load_data_split()
history = train_model(x_train, x_test, "unet_architecture/trained_models/model_split_into_64x64", number_of_epochs=30)
