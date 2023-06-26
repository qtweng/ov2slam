import cv2
from glob import glob

for name in glob("calibration_images/*.jpg"):
    print(name.split("\\")[1])

    img = cv2.imread(name)
    
    # img = cv2.resize(img, (1280,720))
    img = cv2.resize(img, (752,480))
    
    cv2.imwrite("calibration_resized/{}".format(name.split("\\")[1]), img)
