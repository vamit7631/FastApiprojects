from fastapi import status

class StatusCodes:
    SUCCESS = status.HTTP_200_OK
    CREATED = status.HTTP_201_CREATED
    BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    NOT_FOUND = status.HTTP_404_NOT_FOUND
    UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED
    FORBIDDEN = status.HTTP_403_FORBIDDEN
    CONFLICT = status.HTTP_409_CONFLICT
    SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR

class Messages:
    SUCCESS = "Request successful"
    CREATED = "Resource created successfully"
    BAD_REQUEST = "Invalid request"
    NOT_FOUND = "Resource not found"
    UNAUTHORIZED = "Unauthorized access"
    FORBIDDEN = "Forbidden"
    CONFLICT = "Resource already exists"
    SERVER_ERROR = "Internal server error"
