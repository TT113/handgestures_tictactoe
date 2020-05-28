from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import os
import neural_network.constants as constants
augmentedImagesGenerator = ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.2,
        height_shift_range=0.2,
        zoom_range=0.2,
        brightness_range=[0.1, 1],
        horizontal_flip=False,
        fill_mode='nearest')
image_labels = ['down', 'up', 'right', 'nothing', 'left']
for image_label in image_labels:
    path = 'training_images/' + image_label + '/'
    label_name = os.path.join(constants.TRAINING_IMAGES_FOLDER, image_label)
    image_name = len(os.listdir(label_name))
    for i in range(image_name-1):
        img = load_img(path + str(i+1)+'.jpg')
        x = x.reshape((1,) + x.shape)
        images_quantity = 0
        for batch in augmentedImagesGenerator.flow(x, batch_size=1,
                                                   save_to_dir='./training_images/augmented', save_prefix=image_label+str(i), save_format='jpg'):
            images_quantity += 1
            if images_quantity > 10:
                break  # otherwise the generator would loop indefinitely
    first_name = len(os.listdir(label_name))
    for count, filename in enumerate(os.listdir("training_images/augmented")):
        dst = str(first_name + count + 1) + ".jpg"
        src = 'training_images/augmented/' + filename
        dst = 'training_images/' +image_label+ '/' + dst
        os.rename(src, dst)