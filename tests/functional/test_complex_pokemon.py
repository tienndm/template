import pytest

from tests.conftest import deepCompare

@pytest.mark.anyio
async def testPokemonEvolutionScenario(client):
    response = await client.post(
        '/pokemons', json={'no':'0002', 'name': 'Ivysaur', 'type_names': ['Grass', 'Poison']}
    )
    assert response.status_code == 201
    assert deepCompare(
        response.json(),
        {
            'no': '0002',
            'name': 'Ivysaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [],
            'next_evolutions': [],
        }
    )

    response = await client.post('/pokemons', json={'no': '0002', 'name': 'Ivysaur'})
    assert response.status_code == 409

    response = await client.post(
        '/pokemons', json={'no': '0001', 'name': 'Bulbasaur', 'type_names': ['Grass', 'Poison']}
    )
    assert response.status_code == 201
    assert deepCompare(
        response.json(),
        {
            'no': '0001',
            'name': 'Bulbasaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [],
            'next_evolutions': [],
        },
    )

    response = await client.post('/pokemons', json={'no': '0001', 'name': 'Bulbasaur'})
    assert response.status_code == 409

    response = await client.patch('/pokemons/0001', json={'next_evolution_numbers': ['0002']})
    assert response.status_code == 200
    assert deepCompare(
        response.json(),
        {
            'no': '0001',
            'name': 'Bulbasaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [],
            'next_evolutions': [
                {'no': '0002', 'name': 'Ivysaur'},
            ],
        },
    )

    response = await client.post(
        '/pokemons', json={'no': '0003', 'name': 'Venusaur', 'type_names': ['Grass', 'Poison']}
    )
    assert response.status_code == 201
    assert deepCompare(
        response.json(),
        {
            'no': '0003',
            'name': 'Venusaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [],
            'next_evolutions': [],
        },
    )

    response = await client.post('/pokemons', json={'no': '0003', 'name': 'Venusaur'})
    assert response.status_code == 409

    response = await client.patch(
        '/pokemons/0003', json={'previous_evolution_numbers': ['0001', '0002']}
    )
    assert response.status_code == 200
    assert deepCompare(
        response.json(),
        {
            'no': '0003',
            'name': 'Venusaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [
                {'no': '0001', 'name': 'Bulbasaur'},
                {'no': '0002', 'name': 'Ivysaur'},
            ],
            'next_evolutions': [],
        },
    )

    response = await client.get('/pokemons/0001')
    assert response.status_code == 200
    assert deepCompare(
        response.json(),
        {
            'no': '0001',
            'name': 'Bulbasaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [],
            'next_evolutions': [
                {'no': '0002', 'name': 'Ivysaur'},
                {'no': '0003', 'name': 'Venusaur'},
            ],
        },
    )

    response = await client.get('/pokemons/0002')
    assert response.status_code == 200
    assert deepCompare(
        response.json(),
        {
            'no': '0002',
            'name': 'Ivysaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [
                {'no': '0001', 'name': 'Bulbasaur'},
            ],
            'next_evolutions': [
                {'no': '0003', 'name': 'Venusaur'},
            ],
        },
    )

    response = await client.get('/pokemons/0003')
    assert response.status_code == 200
    assert deepCompare(
        response.json(),
        {
            'no': '0003',
            'name': 'Venusaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [
                {'no': '0001', 'name': 'Bulbasaur'},
                {'no': '0002', 'name': 'Ivysaur'},
            ],
            'next_evolutions': [],
        },
    )

    response = await client.delete('/pokemons/0002')
    assert response.status_code == 204

    response = await client.get('/pokemons/0001')
    assert response.status_code == 200
    assert deepCompare(
        response.json(),
        {
            'no': '0001',
            'name': 'Bulbasaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [],
            'next_evolutions': [
                {
                    'no': '0003',
                    'name': 'Venusaur',
                },
            ],
        },
    )

    # Step 6-2: Check 'Ivysaur' no longer exists
    response = await client.get('/pokemons/0002')
    assert response.status_code == 404

    response = await client.get('/pokemons/0003')
    assert response.status_code == 200
    assert deepCompare(
        response.json(),
        {
            'no': '0003',
            'name': 'Venusaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [
                {
                    'no': '0001',
                    'name': 'Bulbasaur',
                },
            ],
            'next_evolutions': [],
        },
    )