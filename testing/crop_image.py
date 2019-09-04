from PIL import Image

coords = (20, 18, 295, 180)
image_obj = Image.open("test_img.jpg")
cropped_image = image_obj.crop(coords)
cropped_image.save('cropped_img.jpg')
