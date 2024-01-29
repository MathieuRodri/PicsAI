from django.shortcuts import render
import subprocess
from django.http import JsonResponse
import base64

from app.scripts.background import main

def home(request):
    return render(request, 'home.html')

def background_operation(request, operation_id):
    if request.method == 'POST':
        try:
            # Récupérez les données de l'image du corps de la requête POST
            image_data = request.POST.get('image_data', None)
            if image_data:
                # Décodage de l'image base64 en bytes
                image_bytes = base64.b64decode(image_data.split(',')[1])

                
                # Enregistrez l'image dans un fichier temporaire (facultatif)
                with open('temp_image.jpg', 'wb') as temp_image_file:
                    temp_image_file.write(image_bytes)
                

                # Vous pouvez utiliser l'image dans votre script Python ici
                result = main('temp_image.jpg', operation_id)
                print(result)
                
                # Retournez une réponse JSON en cas de succès
                return JsonResponse({'success': True, 'message': 'Image traitée avec succès', 'image_data':result})
            else:
                return JsonResponse({'success': False, 'error_message': 'Données d\'image manquantes dans la requête'})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': str(e)})
    else:
        return JsonResponse({'success': False, 'error_message': 'Méthode non autorisée'})
