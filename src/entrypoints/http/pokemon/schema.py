from typing import Optional

from pydantic import BaseModel, Field

from common.type import UUIDStr, PokemonNumberStr

class CreatePokemonRequest(BaseModel):
    no: str = Field(..., description=PokemonNumberStr.__doc__)
    name: str
    type_name: Optional[list[str]] = None
    previous_evolution_numbers: Optional[list[str]] = Field(
        default=[], description=PokemonNumberStr.__doc__
    )
    next_evolution_numbers: Optional[list[str]] = Field(
        default=[], description=PokemonNumberStr.__doc__
    )

class UpdatePokemonRequest(BaseModel):
    name: Optional[str] = None
    type_name: list[str] = []
    previous_evolution_numbers: Optional[list[str]] = Field(
        default=[], description=PokemonNumberStr.__doc__
    )
    next_evolution_numbers: Optional[list[str]] = Field(
        default=[], description=PokemonNumberStr.__doc__
    )

class PokemonResponse(BaseModel):
    no: str = Field(..., description=PokemonNumberStr.__doc__)
    name: str
    types: list['TypeResponse']
    previous_evolution: list['EvolutionResponse']
    next_evolution: list['EvolutionResponse']

class TypeResponse(BaseModel):
    id: str = Field(..., description=UUIDStr.__doc__)
    name: str

class EvolutionResponse(BaseModel):
    no: str = Field(..., description=PokemonNumberStr.__doc__)
    name: str

PokemonResponse.model_rebuild()