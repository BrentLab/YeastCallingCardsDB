from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin)
from ..models import ChrMap
from ..serializers import ChrMapSerializer


class ChrMapViewSet(ListModelFieldsMixin,
                    CustomCreateMixin,
                    PageSizeModelMixin,
                    viewsets.ModelViewSet,
                    CountModelMixin):
    """
    ChrMapViewSet is a Django viewset for the ChrMap model. It provides 
      a RESTful API for clients to interact with ChrMap objects, including 
      creating, reading, updating, and deleting instances.

    Inheritance:
        ListModelFieldsMixin: Provides a mixin to list all available fields 
          for the model.
        CustomCreateMixin: Allows for custom creation of instances.
        PageSizeModelMixin: Provides a mixin to handle pagination and 
          page size.
        viewsets.ModelViewSet: A base class for generic model viewsets.
        CountModelMixin: Provides a mixin to return the total count 
          of objects.

    Attributes:
        queryset: The base queryset for this viewset. Retrieves all ChrMap 
          objects and orders them by their ID.
        serializer_class: The serializer to use for handling ChrMap objects. 
        permission_classes: Defines the permission classes for this viewset.
                            Allows any user to access this viewset.

    API Endpoints:
        1. List: GET /api/chrmap/ - Retrieves a paginated list of all 
           ChrMap objects.
        2. Create: POST /api/chrmap/ - Creates a new ChrMap object with 
          the provided data.
        3. Retrieve: GET /api/chrmap/<id>/ - Retrieves a specific ChrMap 
          object by ID.
        4. Update: PUT/PATCH /api/chrmap/<id>/ - Updates a specific ChrMap 
          object by ID.
        5. Delete: DELETE /api/chrmap/<id>/ - Deletes a specific ChrMap 
          object by ID.
    """
    queryset = ChrMap.objects.all().order_by('id')  # noqa
    serializer_class = ChrMapSerializer  # noqa
    permission_classes = (AllowAny,)
