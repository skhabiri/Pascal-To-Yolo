# Pascal-To-Yolo
convert labeled images in pascal voc format to yolo format

### Overview
The python script `voc2yolo.py` converts Pascal VOC XML annotation to YOLOv5 PyTorch TXT annotation.
We need to install pillow to handle image files on the disk.

### Dataset
Dataset includes synthetic images of drones and bird labeled using Pascal VOC XML Annotation Format.

### Install virtual environment:
Using pipenv we install dependencies and set the python version. If you need to install pipenv:
`pip install pipenv`
After cloning the repo, install the dependencies using:
`pipenv install`

You may activate the virtual environment with:
`pipenv shell`

### voc2yolo.py
This script converts Pascal VOC labeled images to yolo format

* *dirlst*: list of pascal voc directories containg labeled data
* *img_dir*: input image directory path
* *xml_dir*: xml directory path
* *classes*: list of classes of interest to be converted to yolo format
* *extlst*: The input image extension list to be considered for conversion
* *out*: path to the output directory
* All the output images are saved as jpg.

example:
```shell
python ./voc2yolo.py -d ./pascal_voc -i ./pascal_voc/JPEGImages -l ./pascal_voc/Annotations -c Bird Drone Quadcopter -e png jpeg -o ./yolo_format
```
