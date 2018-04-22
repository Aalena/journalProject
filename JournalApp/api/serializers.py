from rest_framework import serializers
from JournalApp.models import Journal

class JournalSerializer(serializers.ModelSerializer):
    url       = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Journal
        fields = [
            'url',
            'id',
            'owner',
            'title',
            'quote',
            'grateful_for',
            'today_view',
            'today_affrimation',
            'happened_today'
        ]
        read_only_fields = ['owner']


    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    def validate_title(self, value):
        qs = Journal.objects.filter(title__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This title already been used")
        else:
            return value
