from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Employee
from .serializers import EmployeeSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class EmployeeAPI(APIView):
    permission_classes = [IsAuthenticated]
    # CREATE EMPLOYEE
    def post(self, request):
        try:
            serializer = EmployeeSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    # GET ALL EMPLOYEE OR SINGLE EMPLOYEE
    def get(self, request, id=None):

        try:
            # GET ALL
            if id is None:
                employees = Employee.objects.all()
                 # Apply pagination
                paginator = PageNumberPagination()
                paginator.page_size = 2  # default page size, can be overridden
                result_page = paginator.paginate_queryset(employees, request)
                serializer = EmployeeSerializer(result_page, many=True)
                #return Response(serializer.data, status=status.HTTP_200_OK)
                return paginator.get_paginated_response(serializer.data)

            # GET BY ID
            employee = Employee.objects.get(id=id)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    # UPDATE EMPLOYEE
    def put(self, request, id):

        try:
            employee = Employee.objects.get(id=id)

            serializer = EmployeeSerializer(employee, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    # DELETE EMPLOYEE
    def delete(self, request, id):

        try:
            employee = Employee.objects.get(id=id)

            employee.delete()

            return Response(
                {"message": "Employee deleted successfully"},
                status=status.HTTP_200_OK
            )

        except Employee.DoesNotExist:return Response({"error": "Employee not found"},status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )