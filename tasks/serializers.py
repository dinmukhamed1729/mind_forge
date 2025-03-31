from rest_framework import serializers
from .models import Task, TestCase, Tag, Difficulty


class TestCaseSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)

    class Meta:
        model = TestCase
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def to_internal_value(self, data):
        if isinstance(data, dict) and "name" in data:
            instance = Tag.objects.get_or_create(**data)[0]
            if instance:
                return instance
        return super().to_internal_value(data)


class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        fields = '__all__'

    def to_internal_value(self, data):
        if isinstance(data, dict) and "name" in data:
            instance = Difficulty.objects.get_or_create(**data)[0]
            if instance:
                return instance
        return super().to_internal_value(data)


class TaskSerializer(serializers.ModelSerializer):
    difficulty = DifficultySerializer()
    tags = TagSerializer(many=True)
    testcases = TestCaseSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        difficulty = validated_data.pop('difficulty', None)
        tags_data = validated_data.pop('tags', [])
        testcases_data = validated_data.pop('testcases', [])

        task = Task.objects.create(difficulty=difficulty, **validated_data)
        task.tags.set(tags_data)

        testcases = [TestCase(task=task, **tc_data) for tc_data in testcases_data]
        TestCase.objects.bulk_create(testcases)

        return task
