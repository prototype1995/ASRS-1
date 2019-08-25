from PIL import Image

coords = (5, 5, 310, 195)
image_obj = Image.open("test_img.jpg")
cropped_image = image_obj.crop(coords)
cropped_image.save('cropped_img.jpg')
