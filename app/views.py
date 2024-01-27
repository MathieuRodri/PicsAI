from django.shortcuts import render
import subprocess
from django.http import JsonResponse


def home(request):
    return render(request, 'home.html')

def background_operation(request, IMAGE_PATH, operation_id):
    try:
        # Execute your script Python using subprocess, passing both IMAGE_PATH and operation_id.
        result = subprocess.check_output(['python', 'chemin_vers_votre_script/background.py', IMAGE_PATH, str(operation_id)], stderr=subprocess.STDOUT, text=True)

        # Assuming 'result' contains the processed image data, you can include it in the response.
        response_data = {
            'success': True,
            'image_data': result,  # Include the processed image data here
        }

        return JsonResponse(response_data)
    except subprocess.CalledProcessError as e:
        return JsonResponse({'success': False, 'error_message': str(e)})
