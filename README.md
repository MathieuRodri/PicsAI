# PicsAI

# Code pour la segmentation
## Environnement
```ruby
!pip install git+https://github.com/facebookresearch/segment-anything.git
!pip install opencv-python pycocotools matplotlib onnxruntime onnx
!pip install ultralytics

from urllib.request import urlopen
from ultralytics import YOLO
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import cv2
from google.colab.patches import cv2_imshow
import torch
from segment_anything import SamPredictor, sam_model_registry
from segment_anything import SamAutomaticMaskGenerator

#chargement modèle SAM
sam = sam_model_registry["default"](checkpoint="/content/drive/MyDrive/sam_vit_h_4b8939.pth").to(device=torch.device('cuda:0'))
#chargement modèle YOLO
model = YOLO('yolov8m.pt')
```

## Extraction des boundings boxes avec YOLOv8 :
```ruby
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
## Ajout des boundings boxes à SAM pour le filtrage des masques prédites par SAM:

```ruby
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


