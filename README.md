# PicsAI 📸

## Table des Matières
1. [Introduction](#introduction)
2. [Installation](#installation)
   - [Prérequis](#prérequis)
   - [Installation manuelle des dépendances](#installation-manuelle-des-dépendances)
3. [Lancement de l'Interface Django](#lancement-de-linterface-django)
4. [Méthodes et Méthodologie](#méthodes-et-méthodologie)
   - [Extraction des Bounding Boxes avec YOLOv8](#extraction-des-bounding-boxes-avec-yolov8)
   - [Filtrage des Masques avec SAM](#filtrage-des-masques-avec-sam)
5. [À propos du projet](#à-propos-du-projet)
6. [Conclusion et Perspectives](#conclusion-et-perspectives)

## Introduction 🌟
PicsAI est une application avancée de segmentation d'image utilisant l'apprentissage profond. Ce projet intègre YOLOv8 pour la détection d'objets et SAM (Segment-Anything Model) pour une segmentation d'image précise et détaillée.

![preview](https://github.com/MathieuRodri/PicsAI/blob/main/screenshots/preview.png)

## À propos du projet 📘
Le projet PicsAI a été développé par Zicheng Fang, Lazar Andjelovic, et Mathieu Rodrigues Domingues dans le cadre du Master 2 Vision et Machine Intelligente à l'Université Paris Cité. L'objectif est de créer une solution complète pour l'identification et la segmentation d'objets spécifiques dans des images, en utilisant YOLOv8 et SAM, deux modèles avancés d'apprentissage profond.

## Installation 🔧

### Prérequis
Pour installer les dépendances nécessaires, exécutez :

`pip install -r requirements.txt`

Ou installer manuellement les dépendances suivantes :

`asgiref==3.7.2
certifi==2023.11.17
charset-normalizer==3.3.2
colorama==0.4.6
coloredlogs==15.0.1
contourpy==1.2.0
cycler==0.12.1
Django==5.0.1
filelock==3.13.1
flatbuffers==23.5.26
fonttools==4.47.2
fsspec==2023.12.2
humanfriendly==10.0
idna==3.6
Jinja2==3.1.3
kiwisolver==1.4.5
MarkupSafe==2.1.4
matplotlib==3.8.2
mpmath==1.3.0
networkx==3.2.1
numpy==1.26.3
onnx==1.15.0
onnxruntime==1.16.3
opencv-python==4.9.0.80
packaging==23.2
pandas==2.2.0
pillow==10.2.0
protobuf==4.25.2
psutil==5.9.8
py-cpuinfo==9.0.0
pycocotools==2.0.7
pyparsing==3.1.1
pyreadline3==3.4.1
python-dateutil==2.8.2
pytz==2023.3.post1
PyYAML==6.0.1
requests==2.31.0
scipy==1.12.0
seaborn==0.13.2
segment-anything @ git+https://github.com/facebookresearch/segment-anything.git@6fdee8f2727f4506cfbbe553e23b895e27956588
six==1.16.0
sqlparse==0.4.4
sympy==1.12
thop==0.1.1.post2209072238
torch==2.1.2
torchvision==0.16.2
tqdm==4.66.1
typing_extensions==4.9.0
tzdata==2023.4
ultralytics==8.1.6
urllib3==2.1.0`

### Pour commencer
Téléchargez d'abord un checkpoint du [modèle SAM](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth)

## Lancement de l'Interface Django 🚀
Pour lancer l'interface utilisateur Django :

1. S'assurer d'avoir Django d'installé :
`pip install django` si ce n'est pas le cas

2. Naviguez vers le dossier racine de votre projet Django.

3. Lancez le serveur :
`python manage.py runserver`

4. Accédez à `http://127.0.0.1:8000/` dans votre navigateur.
   
## Méthodes et Méthodologie 🛠️

### Extraction des Bounding Boxes avec YOLOv8
YOLOv8 est utilisé pour identifier et extraire les bounding boxes des objets dans une image. Cette étape est cruciale pour localiser précisément les objets d'intérêt dans l'image.

```python
IMAGE_PATH = '/content/th.jpg'
image = cv2.imread(IMAGE_PATH)

image_classes = []
results = model.predict(source=IMAGE_PATH)
result = results[0]

for box in result.boxes:
  class_id = result.names[box.cls[0].item()]
  # on prend les labels prédites
  if not(class_id in image_classes):
    image_classes.append(result.names[box.cls[0].item()])

print(image_classes)

select_objet = "person"
select_bbox = []

for box in result.boxes:
  class_id = result.names[box.cls[0].item()]
  if select_objet == class_id:
    cords = box.xyxy[0].tolist()
    cords = [round(x) for x in cords] + [round(box.conf[0].item(), 2)] + [box.cls[0].item()]
    select_bbox.append(cords)

  conf = round(box.conf[0].item(), 2)
  cords = box.xyxy[0].tolist()
  cords = [round(x) for x in cords]

print(f"seleted {select_objet} : {select_bbox}")
Image.fromarray(result.plot()[:,:,::-1])
```

### Filtrage des Masques avec SAM
Après l'extraction des bounding boxes, SAM est utilisé pour segmenter les objets sélectionnés. SAM offre une segmentation fine qui améliore la précision de l'identification des objets.

```python
boxes = np.array(select_bbox)
mask_predictor = SamPredictor(sam)
mask_predictor.set_image(image)
input_boxes = torch.tensor(boxes[:, :-2], device=mask_predictor.device)

transformed_boxes = mask_predictor.transform.apply_boxes_torch(input_boxes, image.shape[:2])
masks, _, _ = mask_predictor.predict_torch(
    point_coords=None,
    point_labels=None,
    boxes=transformed_boxes,
    multimask_output=False,
    )
masks = torch.squeeze(masks, 1)
segmented_image = draw_masks_fromList(image, masks.to('cpu'), boxes,COLORS)
cv2_imshow(segmented_image)
```
   
## Conclusion et Perspectives 🔭
PicsAI démontre l'efficacité de l'intégration des modèles YOLO et SAM pour une analyse approfondie des images. Toutefois, le projet reconnaît certaines limitations liées à la dépendance aux objets préalablement connus par les modèles. Les perspectives d'amélioration comprennent le fine-tuning pour des classes spécifiques d'objets et l'extension des fonctionnalités de l'application.
