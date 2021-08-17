"""
This script converts Pascal VOC labeled images to yolo format

dirlst: list of pascal voc directories to be converted
img_dir : input  directory path
xml_dir : xml directory path

classes: list of classes of interest to be converted to yolo format
extlst: The input image extension list to be considered for conversion

out: path to the output directory
with ./labels and ./images under it.

All the output images are saved as jpg.
"""

import glob
import os
import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join
import argparse
from PIL import Image

def msg(name=None):
    return """
        python ./voc2yolo.py -d ./pascal_voc -i ./pascal_voc/JPEGImages
        -l ./pascal_voc/Annotations -c Bird Drone Quadcopter -e png jpeg -o ./yolo_format
        """

parser = argparse.ArgumentParser('example:', usage=msg())
parser.add_argument('-d', '--dirlst', nargs='*', help='space separated list of pascal voc directories', dest="dirlst")
parser.add_argument('-i', '--imgd', help='image directory', dest="img_dir")
parser.add_argument('-l', '--xml', help='xml directory', dest="xml_dir")
parser.add_argument('-c', '--classes', nargs='*', help='list of desired classes space separated', dest="classes")
parser.add_argument('-e', '--ext', nargs='*', help='space separated input image extensions list', dest="ext")
parser.add_argument('-o', '--out', nargs='?', help='yolo format output directory', type=str,
                    const="./yolo_format", default="./yolo_format", dest="output")

args = vars(parser.parse_args())

# cwd = getcwd()
dirlst = args["dirlst"]

img_dir = args["img_dir"]
xml_dir = args["xml_dir"]

# classes to be considered for conversion
classes = args["classes"]

extlst = args["ext"]
output_path = args["output"]


def convert(size, box):
    """
    size = (image width, image height)
    box = (xmin, xmax, ymin, ymax)
    return:
    (x_center, y_center, width, height)
    0 <= x_center, y_center <= 1
    """
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(xml_path, output_path, img_name):
    """
    converts xml bounding boxes to yolo format
    """
    basename = os.path.basename(img_name)
    basename_no_ext = os.path.splitext(basename)[0]

    in_file = open(xml_path + '/' + basename_no_ext + '.xml')
    out_file = open(output_path + '/labels/' + basename_no_ext + '.txt', 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()

    # image size field in xml file
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    # object refers to each labeled object in xml file
    # filter out classes of difficult or not listed in classes variable
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(round(a, 6)) for a in bb]) + '\n')
    out_file.close()
    in_file.close()

def getFiles(img_path, xml_dir_path, output_path, extlst, extout):
    """
    Reads all the images from "img_path" with extlst extensions
    and saves them in output_path/images with extout extension.
    Additionally reads all the corresponding xml files from xml_dir_path
    directory and store them in output_path/labels as yolo format .txt file.
    img_path = string; ex/ /root/pascal/PNGs
    output_path = string; ex/ /root/pascal/yolo/Images
    extlst = input file extensions; list of strings; ["JPEG", "jpg", "PNG", ...]
    extout = output file extension; string "jpg"
    """
    count = 0
    with open('./imagelog.txt', 'w') as f:
        for filename in glob.glob(img_path + '/*'):
            basename = os.path.basename(filename)
            basename_no_ext, extension = (os.path.splitext(basename)[i] for i in [0, 1])
            if extension.lower()[1:] in [ext.lower() for ext in extlst]:
                f.write(basename + '\n')
                # image_list.append(filename)
                im = Image.open(img_path + '/' + basename)
                im.save(output_path + '/images/' + basename_no_ext + '.' + extout)
                convert_annotation(xml_dir_path, output_path, filename)
                count += 1

                if count % 500 == 0:
                    print(f"{count} input images processed")

    return

for dir_path in dirlst:

    output_label_path = output_path + '/labels'

    output_image_path = output_path + '/images'

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if not os.path.exists(output_label_path):
        os.makedirs(output_label_path)

    if not os.path.exists(output_image_path):
        os.makedirs(output_image_path)
    getFiles(img_dir, xml_dir, output_path, ["png", "jpg", "jpeg"], "jpg")
