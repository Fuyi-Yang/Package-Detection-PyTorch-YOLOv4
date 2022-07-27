from tool.utils import *
from PIL import Image
from tool.format_converter import to_yolo
from models import Yolov4


if __name__ == "__main__":

    n_classes = 1
    namesfile = './data/package.names'
    weightfile = './checkpoints/Yolov4_epoch200.pth'
    path = './data/train/new/usps_package_delivery'
    label_path = './data/train/new/annotations'

    model = Yolov4(yolov4conv137weight=None, n_classes=n_classes)

    pretrained_dict = torch.load(weightfile, map_location=torch.device('cuda'))
    model.load_state_dict(pretrained_dict)

    use_cuda = 1
    if use_cuda:
        model.cuda()

    num = 0
    overwrite = True
    for imgfile in os.listdir(path):
        if imgfile.endswith(('jpeg', 'jpg', 'png')):

            try:
                imgfile = os.path.join(path, imgfile)
                img = Image.open(imgfile).convert('RGB')
                sized = img.resize((608, 608))

                boxes = do_detect(model, sized, 0.8, n_classes, 0.4, use_cuda)

                class_names = load_class_names(namesfile)
                plot_boxes(img, boxes, f"data/result/prediction{num}.jpg", class_names)

                to_yolo(imgfile, label_path, boxes)

                overwrite = False
                num += 1

            except:
                raise Exception(f"you failed on image {imgfile} ... try again")