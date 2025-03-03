import time
from common.type import PokemonNumberStr
from di.unit_of_work import AbstractUnitOfWork
from models.exception import PokemonNotFound
from models.pokemon import CreatePokemonModel, PokemonModel, UpdatePokemonModel

async def createPokemon(
        asyncUnitOfWork: AbstractUnitOfWork, data: CreatePokemonModel
) -> PokemonModel:
    async with asyncUnitOfWork as auow:
        no = await auow.pokemonRepo.create(data)
        await auow.pokemonRepo.replace_types(data.no, data.type_names)

        if data.previous_evolution_numbers:
            if not await auow.pokemonRepo.are_existed(data.previous_evolution_numbers):
                raise PokemonNotFound(data.previous_evolution_numbers)
            await auow.pokemonRepo.replace_previous_evolutions(no, data.previous_evolution_numbers)
        if data.next_evolution_numbers:
            if not await auow.pokemonRepo.are_existed(data.next_evolution_numbers):
                raise PokemonNotFound(data.next_evolution_numbers)
            await auow.pokemonRepo.replace_next_evolutions(no, data.next_evolution_numbers)
        
        return await auow.pokemonRepo.get(no)
    
async def getPokemon(asyncUnitOfWork: AbstractUnitOfWork, no: PokemonNumberStr) -> PokemonModel:
    async with asyncUnitOfWork as auow:
        return await auow.pokemonRepo.get(no)
    
async def getPokemons(asyncUnitOfWork: AbstractUnitOfWork) -> list[PokemonModel]:
    async with asyncUnitOfWork as auow:
        return await auow.pokemonRepo.list()
    
async def updatePokemon(asyncUnitOfWork: AbstractUnitOfWork, no: PokemonNumberStr, data: UpdatePokemonModel):
    async with asyncUnitOfWork as auow:
        await auow.pokemonRepo.update(no, data)

        if data.type_names is not None:
            await auow.pokemonRepo.replace_types(no, data.type_names)

        if data.previous_evolution_numbers is not None:
            if not await auow.pokemonRepo.are_existed(data.previous_evolution_numbers):
                raise PokemonNotFound(data.previous_evolution_numbers)
            await auow.pokemonRepo.replace_previous_evolutions(no, data.previous_evolution_numbers)
        
        if data.next_evolution_numbers is not None:
            if not await auow.pokemonRepo.are_existed(data.next_evolution_numbers):
                raise PokemonNotFound(data.next_evolution_numbers)
            await auow.pokemonRepo.replace_next_evolutions(no, data.next_evolution_numbers)

        return await auow.pokemonRepo.get(no)
    
async def deletePokemon(asyncUnitOfWork: AbstractUnitOfWork, no: PokemonNumberStr):
    async with asyncUnitOfWork as auow:
        await auow.pokemonRepo.delete(no)