from django.utils.module_loading import import_string
from django.contrib.auth import get_user_model
from ..celery import app

@app.task
def process_upload(data, many_flag, kwargs):
    """
    Function to upload records using a serializer with a request.user
    to determine the uploader field value.
    """
    serializer_class_path = kwargs.pop("serializer_class_path")
    serializer_class = import_string(serializer_class_path)

    user_pk = kwargs.pop("uploader")
    User = get_user_model()
    user = User.objects.get(pk=user_pk)
    kwargs["uploader"] = user

    if many_flag:
        serializer = serializer_class(data=data, many=True)
    else:
        serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(**kwargs)
    return serializer.data
