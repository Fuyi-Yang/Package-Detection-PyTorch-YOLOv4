import os
from PIL import Image
import json
from collections import defaultdict
from tqdm import tqdm


def yolo_to_input(image_path, label_path, out_file, path, overwrite=True):
    labels = []

    if not overwrite:
        try:
            with open(out_file, 'r') as f:
                lines = f.readlines()
                for i in range(len(lines)):
                    labels.append(lines[i][:-1])
        except:
            pass

    for imgfile in os.listdir(image_path):
        if imgfile.endswith(('jpeg', 'jpg', 'png')):
            txtfile = os.path.splitext(imgfile)[0] + '.txt'
            txtfile = os.path.join(label_path, txtfile)
            img_path = os.path.join(image_path, imgfile)
            try:
                img = Image.open(img_path).convert('RGB')
            except:
                raise Exception(f"failed on {imgfile}")
            h, w = img.height, img.width
            res = os.path.join(path, imgfile)
            with open(txtfile, 'r') as f:
                lines = f.readlines()
                for i in lines:
                    label = [float(j) for j in i.split(' ')]
                    category = str(int(label[0]))
                    x1 = str(int(w * label[1] - 0.5 * w * label[3]))
                    x2 = str(int(w * label[1] + 0.5 * w * label[3]))
                    y1 = str(int(h * label[2] - 0.5 * h * label[4]))
                    y2 = str(int(h * label[2] + 0.5 * h * label[4]))
                    res += " " + ','.join([x1, y1, x2, y2, category])
            labels.append(res)

    with open(out_file, 'w') as f:
        for i in labels:
            f.write(i)
            f.write('\n')


def to_yolo(imgfile, label_path, bboxes):
    imgfile = os.path.basename(imgfile)
    txtfile = os.path.splitext(imgfile)[0] + '.txt'
    txtfile = os.path.join(label_path, txtfile)
    with open(txtfile, 'w') as f:
        labels = ""
        for box in bboxes:
            class_id = box.pop()
            box = box[:4]
            labels += ' '.join([str(class_id), ' '.join([str(i) for i in box])])
            labels += '\n'

        f.write(labels[:-1])


def coco_to_input(json_file_path, images_dir_path, output_path):

    """load json file"""
    name_box_id = defaultdict(list)
    id_name = dict()
    with open(json_file_path, encoding='utf-8') as f:
        data = json.load(f)

    """generate labels"""
    images = data['images']
    annotations = data['annotations']
    for ant in tqdm(annotations):
        id = ant['image_id']
        name = os.path.join(images_dir_path, images[id]['file_name'])
        cat = ant['category_id']

        if cat >= 1 and cat <= 11:
            cat = cat - 1
        elif cat >= 13 and cat <= 25:
            cat = cat - 2
        elif cat >= 27 and cat <= 28:
            cat = cat - 3
        elif cat >= 31 and cat <= 44:
            cat = cat - 5
        elif cat >= 46 and cat <= 65:
            cat = cat - 6
        elif cat == 67:
            cat = cat - 7
        elif cat == 70:
            cat = cat - 9
        elif cat >= 72 and cat <= 82:
            cat = cat - 10
        elif cat >= 84 and cat <= 90:
            cat = cat - 11

        name_box_id[name].append([ant['bbox'], cat])

    """write to txt"""
    with open(output_path, 'w') as f:
        for key in tqdm(name_box_id.keys()):
            f.write(key)
            box_infos = name_box_id[key]
            for info in box_infos:
                x_min = int(info[0][0])
                y_min = int(info[0][1])
                x_max = x_min + int(info[0][2])
                y_max = y_min + int(info[0][3])

                box_info = " %d,%d,%d,%d,%d" % (
                    x_min, y_min, x_max, y_max, int(info[1]))
                f.write(box_info)
            f.write('\n')


image_path = "../data/packages/train/new/amazon_package_delivery"
label_path = "../data/packages/train/new/annotations"
out_file = "../data/packages/train/new/output.txt"
path = "data/packages/train/new/amazon_package_delivery"

if __name__ == '__main__':
    yolo_to_input(image_path, label_path, out_file, path, overwrite=False)