from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Submission
from .serializers import SubmissionSerializer
from .services import SubmissionService, CodeExecutorFactory

from rest_framework.parsers import MultiPartParser


# Представление для работы с отправками кода

class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()
    parser_classes = (MultiPartParser,)
    submission_service = SubmissionService(CodeExecutorFactory())

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            submission = serializer.save(user=request.user, status='pending')
            self.submission_service.run_tests(submission)

        return Response(SubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)
