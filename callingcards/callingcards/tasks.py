from django.utils.module_loading import import_string
from ..celery import app


@app.task
def process_upload(data, many_flag, kwargs):
    """
    Function to upload records using a serializer with a request.user
    to determine the uploader field value.
    """
    serializer_class_path = kwargs.pop("serializer_class_path")
    serializer_class = import_string(serializer_class_path)
    
    if many_flag:
        serializer = serializer_class(data=data, many=True)
    else:
        serializer = serializer_class(data=data)
    
    serializer.is_valid(raise_exception=True)

    if many_flag:
        instances = []
        for item in serializer.validated_data:
            # Add the 'uploader' field to each record
            item.update(kwargs)  
            # Manually create instances using serializer's create() method
            instance = serializer.create(item)  
            instances.append(instance)
        serializer.instance = instances
    else:
        serializer.save(**kwargs)

    return serializer.data
