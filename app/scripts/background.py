# Importation des bibliothèques nécessaires
import numpy as np
import cv2
from ultralytics import YOLO
import torch
from segment_anything import SamPredictor, sam_model_registry
from google.colab.patches import cv2_imshow
import argparse

# Configuration et initialisation des modèles
def initialize_models():
    """
    Initialise et configure les modèles nécessaires.
    Retourne les modèles YOLO et SAM.
    """
    model = YOLO('yolov8m.pt')  # Assurez-vous que le modèle YOLO est correctement spécifié
    sam = sam_model_registry["default"](checkpoint="/content/drive/MyDrive/sam_vit_h_4b8939.pth").to(device=torch.device('cuda:0'))
    return model, SamPredictor(sam)

# Initialisation des modèles
yolo_model, sam_predictor = initialize_models()

def fill_masks(masks):
    """
    Remplit complètement l'intérieur des masques.

    Args:
    - masks: Liste des masques à traiter sous forme de Tensors PyTorch.

    Retourne:
    - filled_masks: Liste des masques remplis.
    """
    filled_masks = []
    for mask in masks:
        # Assurez-vous que le masque est un tableau numpy en format uint8
        if isinstance(mask, torch.Tensor):
            mask_np = mask.cpu().numpy()
        else:
            mask_np = mask

        # Conversion en format binaire attendu par findContours
        mask_bin = np.uint8(mask_np > 0)

        # Trouver les contours sur le masque
        contours, _ = cv2.findContours(mask_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Créer un masque de la même taille que le masque original, mais rempli de zéros (noir)
        filled_mask = np.zeros_like(mask_bin)

        # Remplir le plus grand contour trouvé avec la couleur blanche (255)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            cv2.drawContours(filled_mask, [largest_contour], contourIdx=-1, color=255, thickness=cv2.FILLED)

        filled_masks.append(filled_mask)

    return filled_masks

def apply_blur_except_masks(image, masks, blur_percentage):
    """
    Applique un flou sur l'image sauf sur les zones définies par les masques.

    Args:
    - image: Image d'origine.
    - masks: Liste des masques à préserver.
    - blur_percentage: Pourcentage de la largeur de l'image à utiliser pour l'intensité du flou.

    Retourne:
    - blurred_image: Image floue avec les masques préservés.
    """
    # Calculer l'intensité du flou basée sur la largeur de l'image
    blur_intensity = int((blur_percentage / 100.0) * image.shape[1])
    # Assurer que l'intensité du flou est un nombre impair pour le kernel de flou gaussien
    blur_intensity = blur_intensity + 1 if blur_intensity % 2 == 0 else blur_intensity

    # Appliquer un flou sur toute l'image
    blurred_image = cv2.GaussianBlur(image, (blur_intensity, blur_intensity), 0)

    # Superposer les zones masquées originales sur l'image floue
    for mask in masks:
        mask_np = mask.cpu().numpy() if isinstance(mask, torch.Tensor) else mask
        blurred_image[mask_np > 0] = image[mask_np > 0]

    return blurred_image

def replace_background_with_color(image, masks, color):
    """
    Remplace le fond de l'image par une couleur définie, en préservant les zones masquées.

    Args:
    - image: Image d'origine.
    - masks: Liste des masques à préserver.
    - color: Couleur de fond à appliquer.

    Retourne:
    - color_replaced_image: Image avec le fond remplacé par la couleur définie.
    """
    # Créer une image de fond de la couleur souhaitée
    background = np.full(image.shape, color, dtype=np.uint8)

    # Superposer les zones masquées originales sur le fond coloré
    for mask in masks:
        if isinstance(mask, torch.Tensor):
            mask_np = mask.cpu().numpy()
        else:
            mask_np = mask

        background[mask_np > 0] = image[mask_np > 0]

    return background

# Fonction pour dessiner les masques sur l'image
def draw_masks(image, masks, boxes):
    """
    Dessine les masques sur l'image à partir d'une liste de masques.

    Args:
    - image: Image sur laquelle dessiner.
    - masks: Masques à appliquer.
    - boxes: Boîtes englobantes des objets.

    Retourne l'image avec les masques appliqués.
    """
    # Définir les couleurs pour les masques (à personnaliser)
    colors = [(89, 161, 197),(67, 161, 255),(19, 222, 24),(186, 55, 2),(167, 146, 11),(190, 76, 98),(130, 172, 179),(115, 209, 128),(204, 79, 135),(136, 126, 185),(209, 213, 45),(44, 52, 10),(101, 158, 121),(179, 124, 12),(25, 33, 189),(45, 115, 11),(73, 197, 184),(62, 225, 221),(32, 46, 52),(20, 165, 16),(54, 15, 57),(12, 150, 9),(10, 46, 99),(94, 89, 46),(48, 37, 106),(42, 10, 96),(7, 164, 128),(98, 213, 120),(40, 5, 219),(54, 25, 150),(251, 74, 172),(0, 236, 196),(21, 104, 190),(226, 74, 232),(120, 67, 25),(191, 106, 197),(8, 15, 134),(21, 2, 1),(142, 63, 109),(133, 148, 146),(187, 77, 253),(155, 22, 122),(218, 130, 77),(164, 102, 79),(43, 152, 125),(185, 124, 151),(95, 159, 238),(128, 89, 85),(228, 6, 60),(6, 41, 210),(11, 1, 133),(30, 96, 58),(230, 136, 109),(126, 45, 174),(164, 63, 165),(32, 111, 29),(232, 40, 70),(55, 31, 198),(148, 211, 129),(10, 186, 211),(181, 201, 94),(55, 35, 92),(129, 140, 233),(70, 250, 116),(61, 209, 152),(216, 21, 138),(100, 0, 176),(3, 42, 70),(151, 13, 44),(216, 102, 88),(125, 216, 93),(171, 236, 47),(253, 127, 103),(205, 137, 244),(193, 137, 224),(36, 152, 214),(17, 50, 238),(154, 165, 67),(114, 129, 60),(119, 24, 48),(73, 8, 110)]
    masked_image = image.copy()

    filled_masks = fill_masks(masks)

    for i in range(len(filled_masks)):
        mask = filled_masks[i]
        color = colors[int(boxes[i][-1])]
        masked_image = np.where(np.repeat(mask[:, :, np.newaxis], 3, axis=2), np.asarray(color, dtype='uint8'), masked_image)

    return cv2.addWeighted(image, 0.3, masked_image.astype(np.uint8), 0.7, 0)

# Fonction pour afficher les résultats
def display_results(image):
    """
    Affiche l'image résultante.

    Args:
    - image: Image à afficher.
    """
    cv2_imshow(image)  # Utiliser cv2.imshow() si hors de Google Colab

# Fonction principale
def main(IMAGE_PATH, operation_id):
    print(f"Operation ID: {operation_id}")
    image = cv2.imread(IMAGE_PATH)
    height, width, _ = image.shape

    # Seuils normalisés par rapport aux dimensions de l'image (20% de la largeur/hauteur de l'image)
    min_width, min_height = 0.3 * width, 0.3 * height

    results = yolo_model.predict(source=IMAGE_PATH)
    result = results[0]

    # Extraction des boîtes englobantes et des classes
    boxes = []
    largest_box = None
    max_area = 0
    for box in result.boxes:
        cords = box.xyxy[0].tolist()
        # Calcul de la largeur et de la hauteur de la boîte
        box_width = cords[2] - cords[0]
        box_height = cords[3] - cords[1]
        # Calcul de l'aire pour trouver la plus grande boîte
        area = box_width * box_height
        if area > max_area:
            max_area = area
            largest_box = [round(x) for x in cords] + [round(box.conf[0].item(), 2)] + [box.cls[0].item()]
        # Vérification si la boîte est plus grande que le seuil minimum
        if box_width > min_width and box_height > min_height:
            cords = [round(x) for x in cords] + [round(box.conf[0].item(), 2)] + [box.cls[0].item()]
            boxes.append(cords)

    # Si aucune boîte n'est plus grande que le seuil, ajouter la plus grande boîte trouvée
    if not boxes and largest_box is not None:
        boxes.append(largest_box)

    # Définir l'image dans l'objet SamPredictor
    sam_predictor.set_image(image)

    # Conversion des boîtes pour SAM et prédiction des masques
    boxes_tensor = torch.tensor([box[:-2] for box in boxes], device=sam_predictor.device)
    transformed_boxes = sam_predictor.transform.apply_boxes_torch(boxes_tensor, image.shape[:2])
    masks, _, _ = sam_predictor.predict_torch(
        point_coords=None,
        point_labels=None,
        boxes=transformed_boxes,
        multimask_output=False,
    )
    masks = torch.squeeze(masks, 1)

    filled_masks = fill_masks(masks.to('cpu'))

    # Application des masques et affichage des résultats
    #segmented_image = draw_masks(image, masks.to('cpu'), boxes)

    if operation_id == 1:
        res = apply_blur_except_masks(IMAGE_PATH, filled_masks, 2)
    elif operation_id == 2:
        res = apply_blur_except_masks(IMAGE_PATH, filled_masks, 5)
    elif operation_id == 3:
        res = apply_blur_except_masks(IMAGE_PATH, filled_masks, 10)
    elif operation_id == 4:
        res = replace_background_with_color(IMAGE_PATH, filled_masks, (255, 128, 0))
    elif operation_id == 5:
        res = replace_background_with_color(IMAGE_PATH, filled_masks, (255, 128, 128))
    elif operation_id == 6:
        res = replace_background_with_color(IMAGE_PATH, filled_masks, (255, 128, 255))
    else:
        res = "Opération non reconnue"
    
    # Utilisez res comme nécessaire ou renvoyez-le
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("IMAGE_PATH", type=str, help="Path to the image")
    parser.add_argument("operation_id", type=int, help="Operation ID to pass to the script")
    args = parser.parse_args()
    main(args.IMAGE_PATH, args.operation_id)