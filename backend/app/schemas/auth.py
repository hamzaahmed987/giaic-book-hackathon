"""
Authentication schemas.
"""
from typing import Optional, List

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str
    name: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class ProfileUpdate(BaseModel):
    """Schema for updating user profile."""
    experience_level: Optional[str] = None
    known_languages: Optional[List[str]] = None
    hardware_tier: Optional[str] = None
    goals: Optional[List[str]] = None


class ProfileResponse(BaseModel):
    """Schema for profile response."""
    experience_level: str
    known_languages: List[str]
    hardware_tier: str
    goals: List[str]

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """Schema for user response."""
    id: str
    email: str
    name: Optional[str] = None
    profile: Optional[ProfileResponse] = None

    class Config:
        from_attributes = True
