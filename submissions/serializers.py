from rest_framework import serializers

from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ('user', 'status', 'execution_time', 'test_cases_passed', 'total_test_cases')

    def create(self, validated_data):
        file = validated_data.pop('file', None)
        if file:
            validated_data['code'] = file.read().decode()
        return super().create(validated_data)
