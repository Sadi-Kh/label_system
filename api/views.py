from rest_framework import viewsets
from .models import Dataset, Category, TextEntry, Operator
from .serializers import DatasetSerializer, CategorySerializer, TextEntrySerializer, OperatorSerializer
from .permissions import IsOperator
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class DatasetViewSet(viewsets.ModelViewSet):
    serializer_class = DatasetSerializer
    permission_classes = [IsOperator]

    # Default queryset to avoid AssertionError
    queryset = Dataset.objects.all()

    def get_queryset(self):
        operator = self.request.user.operator
        return self.queryset.filter(operators=operator)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsOperator]

    # Default queryset to avoid AssertionError
    queryset = Category.objects.all()

    def get_queryset(self):
        operator = self.request.user.operator
        return self.queryset.filter(dataset__operators=operator)

class TextEntryViewSet(viewsets.ModelViewSet):
    serializer_class = TextEntrySerializer
    permission_classes = [IsOperator]

    # Default queryset to avoid AssertionError
    queryset = TextEntry.objects.all()

    def get_queryset(self):
        operator = self.request.user.operator
        return self.queryset.filter(dataset__operators=operator)

class OperatorViewSet(viewsets.ModelViewSet):
    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer
    permission_classes = [IsAdminUser]

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()  # Deletes the token
        return Response(status=204)  # No content response
