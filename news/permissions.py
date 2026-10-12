"""
CustomDRF permission classes enforcing
role-based control (RBAC).
"""
from rest_framework import permissions


class IsJournalistCanCreateOrEditorCanApprove(permissions.BasePermission):
    """
    Enforces role-based permissions:
    - Safe methods (GET) require authentication.
    - Article creation (POST) is restricted to journalist.
    - Article modification/approval (PUT/PATCH) is
    restricted to editors and journalists.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if request.method == 'POST':
            return request.user and request.user.is_authenticated and request.user.role == 'journalist'  # noqa: E501

        if request.method in ['PUT', 'PATCH']:
            return request.user and request.user.is_authenticated and request.user.role in ['editor', 'journalist']  # noqa: E501

        return False
