import sys
import cv2
from models import Yolov4
from tool.utils import *
import tool.alert

if __name__ == "__main__":

    n_classes = 1
    namesfile = './data/package.names'
    weightfile = './checkpoints/Yolov4_epoch200.pth'

    model = Yolov4(yolov4conv137weight=None, n_classes=n_classes)

    pretrained_dict = torch.load(weightfile, map_location=torch.device('cuda'))
    model.load_state_dict(pretrained_dict)

    use_cuda = 1
    if use_cuda:
        model.cuda()

    cap = cv2.VideoCapture(0)
    frames = 0
    start = time.time()
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            sized = cv2.resize(frame, (608, 608))
            sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)
            boxes = do_detect(model, sized, 0.6, n_classes, 0.4, use_cuda)

            orig_im = plot_boxes_cv2(frame, boxes, class_names=namesfile)

            cv2.imshow("frame", orig_im)
            key = cv2.waitKey(1)
            if key > -1:
                break
            frames += 1
            print("FPS of the video is {:5.2f}".format(frames / (time.time() - start)))
            #tool.alert.whatsapp_alert()
        else:
            break
