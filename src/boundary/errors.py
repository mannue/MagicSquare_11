"""Boundary validation error models."""

from pydantic import BaseModel


class BoundaryErrorDetail(BaseModel):
    """Error payload for shape and input contract failures."""

    code: str
    message: str


class ValidationFailure(BaseModel):
    """Failed validation result returned by BoundaryValidator."""

    success: bool = False
    error: BoundaryErrorDetail
