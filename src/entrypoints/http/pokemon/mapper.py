from common.docstring import MAPPER_DOCSTRING
from common.type import PokemonNumberStr
from models.pokemon import (
    CreatePokemonModel,
    PokemonEvolutionModel,
    PokemonModel,
    TypeModel,
    UpdatePokemonModel,
)

from .schema import (
    CreatePokemonRequest,
    EvolutionResponse,
    PokemonResponse,
    TypeResponse,
    UpdatePokemonRequest,
)

__doc__ = MAPPER_DOCSTRING


class PokemonRequestMapper:
    @staticmethod
    def createRequestToEntity(instance: CreatePokemonRequest) -> CreatePokemonModel:
        return CreatePokemonModel(
            no=PokemonNumberStr(instance.no),
            name=instance.name,
            type_names=instance.type_name or [],
            previous_evolution_numbers=list(
                map(PokemonNumberStr, instance.previous_evolution_numbers or [])
            ),
            next_evolution_numbers=list(
                map(PokemonNumberStr, instance.next_evolution_numbers or [])
            ),
        )

    @staticmethod
    def updateRequestToEntity(instance: UpdatePokemonRequest) -> UpdatePokemonModel:
        if instance.previous_evolution_numbers:
            instance.previous_evolution_numbers = list(
                map(PokemonNumberStr, instance.previous_evolution_numbers)
            )

        if instance.next_evolution_numbers:
            instance.next_evolution_numbers = list(
                map(PokemonNumberStr, instance.next_evolution_numbers)
            )
        kwarg = instance.model_dump(exclude_unset=True)
        return UpdatePokemonModel(**kwarg)


class PokemonResponseMapper:
    @staticmethod
    def entityToResponse(instance: PokemonModel) -> PokemonResponse:
        return PokemonResponse(
            no=instance.no,
            name=instance.name,
            types=list(map(TypeResponseMapper.entityToResponse, instance.types)),
            previous_evolution=list(
                map(EvolutionResponseMapper.entityToResponse, instance.previous_evolution)
            ),
            next_evolution=list(
                map(EvolutionResponseMapper.entityToResponse, instance.next_evolution)
            ),
        )


class TypeResponseMapper:
    @staticmethod
    def entityToResponse(instance: TypeModel) -> TypeResponse:
        return TypeResponse(id=instance.id, name=instance.name)


class EvolutionResponseMapper:
    @staticmethod
    def entityToResponse(instace: PokemonEvolutionModel) -> EvolutionResponse:
        return EvolutionResponse(no=instace.no, name=instace.name)
