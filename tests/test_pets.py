import pytest

from src.expected_response_data import responses_from_pet_api as erd


@pytest.mark.get_pet
def test_finding_of_existing_pet(create_pet_api, pc_create_new_pet):
    api = create_pet_api
    pet_id = pc_create_new_pet
    response = api.get_pet(pet_id)
    assert response.status_code == 200, 'Wrong response status code'
    response_body = response.json()
    assert api.validate_pet_schema(response_body)
    assert api.is_pet_exist(pet_id), 'Wrong pet ID in response'


@pytest.mark.get_pet
def test_finding_of_unexisting_pet(create_pet_api, pc_delete_pet_if_exists):
    api = create_pet_api
    pet_id = pc_delete_pet_if_exists()
    response = api.get_pet(pet_id)
    assert response.status_code == 404, 'Wrong response status code'
    assert api.validate_dict_data(erd.pet_not_found, response.json())  # if data in response is equal to expected


@pytest.mark.get_pet
@pytest.mark.parametrize('pet_id', (-1, 0, 'qwe', [10], {300}, {1: '1'}, None))
def test_finding_of_pet_with_invalid_id(create_pet_api, pet_id):
    api = create_pet_api
    invalid_pet_id = pet_id
    response = api.get_pet(invalid_pet_id)
    assert response.status_code == 400, 'Wrong response status code'
    assert api.validate_dict_data(erd.invalid_id_supplied, response.json())  # if data in response is equal to expected


@pytest.mark.post_pet
def test_pet_creating_with_valid_data(create_pet_api, pc_generate_pet_object, pc_delete_pet_if_exists):
    api = create_pet_api
    new_pet = pc_generate_pet_object(data='new')

    pc_delete_pet_if_exists(new_pet.id)
    response = api.add_pet(new_pet)
    assert response.status_code == 200, 'Wrong response status code'
    response_body = response.json()
    assert api.validate_pet_schema(response_body)
    request_body = new_pet.to_dict()
    assert api.validate_dict_data(request_body, response_body)  # if response body match to request body
    assert api.validate_dict_data(request_body,
                                  api.get_pet(new_pet.id).json())  # if data from updated api matches to request body


@pytest.mark.post_pet
@pytest.mark.parametrize('field, value', [('id', 'qwe'), ('category', {'id': [123], 'name': 'name'}),
                                          ('status', {'status': 'available'})])
def test_pet_creating_with_invalid_data(create_pet_api, pc_delete_pet_if_exists, pc_generate_pet_object, field, value):
    api = create_pet_api
    pet_id = pc_delete_pet_if_exists()
    pet = pc_generate_pet_object(data='new', pet_id=pet_id, fields_to_replace={field: value})
    response = api.add_pet(pet)
    assert response.status_code == 405, 'Wrong response status code'
    assert api.validate_dict_data(erd.invalid_input, response.json())  # if data in response is equal to expected


@pytest.mark.post_pet
def test_pet_creating_with_unsupported_content_type_header(create_pet_api, pc_generate_pet_object,
                                                           pc_delete_pet_if_exists):
    api = create_pet_api
    new_pet = pc_generate_pet_object(data='new')
    pc_delete_pet_if_exists(new_pet.id)
    response = api.add_pet(new_pet, is_unsupported_content_type=True)
    assert response.status_code == 415, 'Wrong response status code'
    reason = response.raw.reason
    assert api.validate_dict_data(erd.unsupported_media_type, reason)  # if data in response is equal to expected


@pytest.mark.put_pet
def test_pet_updating_with_valid_data(create_pet_api, pc_create_new_pet, pc_generate_pet_object):
    api = create_pet_api
    pet_id = pc_create_new_pet
    pet_object_for_updating = pc_generate_pet_object(data='new', pet_id=pet_id)
    request_body = pet_object_for_updating.to_dict()
    response = api.update_pet(pet_object_for_updating)
    assert response.status_code == 200, 'Wrong response status code'
    response_body = response.json()
    assert api.validate_pet_schema(response_body)
    assert api.validate_dict_data(request_body, response_body)  # if data in response body matches to request body
    assert api.validate_dict_data(request_body,
                                  api.get_pet(pet_id).json())  # if data from updated api matches to request body


@pytest.mark.put_pet
def test_updating_of_unexisting_pet(create_pet_api, pc_delete_pet_if_exists, pc_generate_pet_object):
    api = create_pet_api
    pet_id = pc_delete_pet_if_exists()
    pet = pc_generate_pet_object(data='new', pet_id=pet_id)
    response = api.update_pet(pet)
    assert response.status_code == 404, 'Wrong response status code'
    assert api.validate_dict_data(erd.pet_not_found, response.json())  # if data in response is equal to expected


@pytest.mark.put_pet
@pytest.mark.parametrize('field, value', [('id', 'qwe'), ('category', {'id': [123], 'name': 'name'}),
                                          ('status', {'status': 'available'})])
def test_pet_updating_with_invalid_data(create_pet_api, pc_create_new_pet, pc_generate_pet_object, field, value):
    api = create_pet_api
    pet_id = pc_create_new_pet
    pet_object_for_updating = pc_generate_pet_object(data='update', pet_id=pet_id, fields_to_replace={field: value})
    response = api.update_pet(pet_object_for_updating)
    assert response.status_code == 405, 'Wrong response status code'
    assert api.validate_dict_data(erd.validation_exception, response.json())  # if data in response is equal to expected


@pytest.mark.delete_pet
def test_deleting_of_existing_pet(create_pet_api, pc_create_new_pet):
    api = create_pet_api
    pet_id = pc_create_new_pet
    response = api.delete_pet(pet_id)
    assert response.status_code == 200, 'Wrong response status code'
    assert not api.is_pet_exist(pet_id), 'Pet still exists'


@pytest.mark.delete_pet
def test_deleting_of_unexisting_pet(create_pet_api, pc_delete_pet_if_exists):
    api = create_pet_api
    pet_id = pc_delete_pet_if_exists()
    response = api.delete_pet(pet_id)
    assert response.status_code == 404, 'Wrong response status code'
    assert api.validate_dict_data(erd.pet_not_found, response.json())  # if data in response is equal to expected


@pytest.mark.delete_pet
@pytest.mark.parametrize('pet_id', (-1, 0, 'qwe', [10], {300}, {1: '1'}, None))
def test_deleting_with_invalid_id(create_pet_api, pet_id):
    api = create_pet_api
    response = api.delete_pet(pet_id)
    assert response.status_code == 400, 'Wrong response status code'
    assert api.validate_dict_data(erd.invalid_id_supplied, response.json())  # if data in response is equal to expected
