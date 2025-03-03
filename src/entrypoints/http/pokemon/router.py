from fastapi import APIRouter, Body, Path, status
from fastapi.responses import JSONResponse

from common.type import PokemonNumberStr
from di.dependency_injection import injector
from di.unit_of_work import AbstractUnitOfWork
from usecases import pokemon as pokemonUsecases

from .mapper import PokemonRequestMapper, PokemonResponseMapper
from .schema import CreatePokemonRequest, PokemonResponse, UpdatePokemonRequest

router = APIRouter()


@router.post("/pokemons")
async def createPokemon(body: CreatePokemonRequest) -> PokemonResponse:
    asyncUnitOfWork = injector.get(AbstractUnitOfWork)
    createPokemonData = PokemonRequestMapper.createRequestToEntity(body)
    createdPokemon = await pokemonUsecases.createPokemon(
        asyncUnitOfWork, createPokemonData
    )
    return PokemonResponseMapper.entityToResponse(createdPokemon)


@router.get("/pokemon/{no}")
async def getPokemon(
    no: str = Path(..., description=PokemonNumberStr.__doc__)
) -> PokemonResponse:
    asyncUnitOfWork = injector.get(AbstractUnitOfWork)
    no = PokemonNumberStr(no)
    pokemon = await pokemonUsecases.getPokemon(asyncUnitOfWork, no)

    return PokemonResponseMapper.entityToResponse(pokemon)


@router.get("/pokemons")
async def getPokemons() -> list[PokemonResponse]:
    asyncUnitOfWork = injector.get(AbstractUnitOfWork)
    pokemons = await pokemonUsecases.getPokemons(asyncUnitOfWork)

    return list(map(PokemonResponseMapper.entityToResponse, pokemons))


@router.patch("/pokemons/{no}")
async def updatePokemon(
    no: str = Path(..., description=PokemonNumberStr.__doc__),
    body: UpdatePokemonRequest = Body(...),
) -> PokemonResponse:
    asyncUnitOfWork = injector.get(AbstractUnitOfWork)
    no = PokemonNumberStr(no)
    updatePokemonData = PokemonRequestMapper.updateRequestToEntity(body)
    updatePokemonData._validateNoNotOnEvolution(no)
    updatedPokemon = await pokemonUsecases.updatePokemon(asyncUnitOfWork, no, updatePokemonData)

    return PokemonResponseMapper.entityToResponse(updatedPokemon)


@router.delete("/pokemons/{no}", status_code=status.HTTP_204_NO_CONTENT)
async def deletePokemon(no: str = Path(..., description=PokemonNumberStr.__doc__)):
    asyncUnitOfWork = injector.get(AbstractUnitOfWork)
    no = PokemonNumberStr(no)
    await pokemonUsecases.deletePokemon(asyncUnitOfWork, no)