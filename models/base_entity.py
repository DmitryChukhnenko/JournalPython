"""
Base entity module for the university schedule project.

This module provides the BaseEntity class, which serves as the foundation
for all domain entities (Teacher, Group, Subject, Classroom). It implements
common functionality like ID generation, serialization, and validation.
"""

import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseEntity(ABC):
    """
    Abstract base class for all domain entities.

    Provides common functionality:
    - Automatic UUID generation for unique identification
    - Encapsulation via private attributes and properties
    - Serialization/deserialization (to_dict/from_dict)
    - String representation
    - Validation interface

    Attributes:
        _id (str): Unique identifier for the entity (UUID4 format)

    Example:
        >>> class Teacher(BaseEntity):
        ...     def __init__(self, name: str):
        ...         super().__init__()
        ...         self._name = name
        ...
        ...     def _validate(self) -> bool:
        ...         return bool(self._name)
    """

    def __init__(self, entity_id: Optional[str] = None) -> None:
        """
        Initialize a new BaseEntity instance.

        Args:
            entity_id: Optional custom ID. If not provided, generates a new UUID4.
                      Useful for deserialization from stored data.

        Note:
            The ID is stored in a private attribute `_id` to enforce encapsulation.
            Access should be done through the `id` property.
        """
        self._id = entity_id if entity_id is not None else str(uuid.uuid4())

    @property
    def id(self) -> str:
        """
        Get the entity's unique identifier.

        Returns:
            str: The UUID4 identifier as a string.
        """
        return self._id

    @abstractmethod
    def _validate(self) -> bool:
        """
        Validate the entity's internal state.

        This method must be implemented by all subclasses to define
        their specific validation logic. Should check that all required
        fields are present and have valid values.

        Returns:
            bool: True if the entity is in a valid state, False otherwise.

        Note:
            This is an abstract method - subclasses MUST override it.
            Validation should be pure (no side effects).
        """
        pass  # pragma: no cover

    def is_valid(self) -> bool:
        """
        Public interface for validation.

        Calls the protected _validate() method. Can be extended in the future
        to add logging or additional checks without modifying subclass code.

        Returns:
            bool: Result of the _validate() method.
        """
        return self._validate()

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the entity to a dictionary.

        Converts the entity's state into a dictionary representation,
        suitable for JSON serialization or other storage formats.

        Returns:
            dict: Dictionary containing the entity's data with 'id' key.

        Note:
            Subclasses should extend this method to include their specific
            attributes. Always call super().to_dict() to include the ID.

        Example:
            >>> entity.to_dict()
            {'id': '550e8400-e29b-41d4-a716-446655440000', 'name': 'John Doe'}
        """
        return {
            'id': self._id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseEntity":
        """
        Deserialize an entity from a dictionary.

        Creates a new instance of the class from dictionary data.
        This is a factory method that handles the ID extraction.

        Args:
            data: Dictionary containing entity data, must include 'id' key.

        Returns:
            BaseEntity: A new instance of the class (or subclass).

        Raises:
            KeyError: If 'id' key is missing from the data.

        Note:
            Subclasses should extend this method to handle their specific
            attributes. Always extract 'id' first and pass to parent constructor.

        Example:
            >>> data = {'id': '550e8400-e29b-41d4-a716-446655440000', 'name': 'John'}
            >>> teacher = Teacher.from_dict(data)
        """
        entity_id = data.get('id')
        if entity_id is None:
            raise KeyError("Missing required 'id' field in entity data")
        return cls(entity_id=entity_id)

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the entity.

        Returns:
            str: String in format "ClassName(id={id})".

        Note:
            Subclasses may override this to provide more detailed information.
            This default implementation is useful for debugging and logging.
        """
        return f"{self.__class__.__name__}(id={self._id})"

    def __eq__(self, other: object) -> bool:
        """
        Check equality based on entity ID.

        Two entities are considered equal if they have the same ID,
        regardless of their concrete class (as long as both are BaseEntity).

        Args:
            other: Another object to compare with.

        Returns:
            bool: True if both objects are BaseEntity instances with the same ID.
        """
        if not isinstance(other, BaseEntity):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        """
        Generate hash based on entity ID.

        Allows entities to be used in sets and as dictionary keys.

        Returns:
            int: Hash of the entity ID.
        """
        return hash(self._id)
