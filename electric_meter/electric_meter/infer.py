from paddleocr import PaddleOCR, draw_ocr
import os
from .settings import BASE_DIR
from PIL import Image
# 模型路径下必须含有model和params文件
ocr = PaddleOCR(det_model_dir=os.path.join(BASE_DIR, "det_db"),
                use_angle_cls=True)


def electric_meter(img_path):
    print(img_path)
    img_path = os.path.join(img_path)
    result = ocr.ocr(img_path, cls=True)
    for line in result:
        print(line)

    # 显示结果
    print("可视化")
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores)
    im_show = Image.fromarray(im_show)
    im_show.save(os.path.join(BASE_DIR, "rec_result", os.path.basename(img_path)))
    # im_show.show()
    return result


# electric_meter(r"C:\Users\boyif\Desktop\paddle\electric\M2021\IMG_20210724_132657.jpg")

