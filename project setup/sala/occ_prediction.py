from tensorflow.keras.models import Model, load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array, array_to_img
import glob

imgs = glob.glob(SiamMask/data/occ_frames/*.png)
print(len(imgs))
print(s)

imageloc = 'SiamMask/data/occ_frames/%d.png'%d(frame)
    img = img_to_array(load_img(imageloc))
    model = load_model(save_weights3.h5)
    preds = model.predict(img)
    print(preds)