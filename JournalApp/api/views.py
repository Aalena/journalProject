from django.db.models import Q
from rest_framework import routers, serializers, viewsets
from rest_framework import generics, mixins
from JournalApp.models import Journal
from .permission import IsOwnerOrReadOnly
from .serializers import JournalSerializer

class JournalAPIView(mixins.CreateModelMixin, generics.ListAPIView): # It is used to create view of data
    lookup_field     = 'id'
    serializer_class = JournalSerializer
    # queryset = Journal.objects.all() # we can either use this for query or get_queryset method

    def get_queryset(self):
        qs = Journal.objects.all()
        query  = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(title__icontains=query)|Q(quote__icontains=query))
        return qs
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class JournalRudView(generics.RetrieveUpdateDestroyAPIView): # it is used to Update and destroy of data
    lookup_field       = 'id'
    serializer_class   = JournalSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Journal.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}
