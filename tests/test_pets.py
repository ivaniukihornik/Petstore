import pytest

from src.data.pet.category import Category
from src.data.pet.pet import Pet
from src.data.pet.tag import Tag


@pytest.mark.get_pet
def test_finding_of_existing_pet(create_pet_api):
    api = create_pet_api
    pet_id = 174232
    pet = Pet(id=pet_id, category=Category(3, 'Dog'), name='Jiber', photo_urls=[
            'https://photo1.jpg', 'https://photo2.jpg'], tags=[Tag(1, 'tag1'), Tag(2, 'tag2')], status='availabe')
    api.delete_pet(pet_id)  # create new pet before getting
    api.add_pet(pet)
    response = api.get_pet(pet_id)
    assert response.status_code == 200, 'Wrong response status code'
    response_body = response.json()
    assert api.validate_pet_schema(response_body)
    assert response_body.get('id') == pet_id, 'Wrong pet ID in response'


@pytest.mark.get_pet
def test_finding_of_unexisting_pet(create_pet_api):
    api = create_pet_api
    pet_id = 123817213827318
    api.delete_pet(pet_id)  # delete pet before getting
    response = api.get_pet(pet_id)
    assert response.status_code == 404, 'Wrong response status code'
    assert response.json() == {
        "code": 1,
        "type": "error",
        "message": "Pet not found"
    }, 'Wrong error in response'


@pytest.mark.get_pet
@pytest.mark.parametrize('pet_id', (-1, 0, 'qwe', [10], {300}, {1: '1'}, None))
def test_finding_of_pet_with_invalid_id(create_pet_api, pet_id):
    api = create_pet_api
    invalid_pet_id = pet_id
    response = api.get_pet(invalid_pet_id)
    assert response.status_code == 400, 'Wrong response status code'
    assert response.json() == {
        "code": 2,
        "type": "error",
        "message": "Invalid ID supplied"
    }, 'Wrong error in response'


@pytest.mark.post_pet
def test_pet_creating_with_valid_data(create_pet_api):
    api = create_pet_api
    new_pet_id = 12001213
    pet = Pet(id=new_pet_id, category=Category(3, 'Dog'), name='Jiber', photo_urls=[
        'https://photo1.jpg', 'https://photo2.jpg'], tags=[Tag(1, 'tag1'), Tag(2, 'tag2')], status='availabe')
    if api.is_pet_exist(new_pet_id):  # delete pet before creating if exists
        api.delete_pet(new_pet_id)
    response = api.add_pet(pet)
    assert response.status_code == 200, 'Wrong response status code'
    response_body = response.json()
    assert api.validate_pet_schema(response_body)
    assert response_body == pet.to_dict(), 'Response body doesn\'t match to request body'
    assert api.get_pet(new_pet_id).json() == pet.to_dict(), 'Data in created pet doesn\'t match to data used when ' \
                                                            'creating'


@pytest.mark.post_pet
@pytest.mark.parametrize('field, value', [('id', 'qwe'), ('category', {'id': [123], 'name': 'name'}),
                                          ('status', {'status': 'available'})])
def test_pet_creating_with_invalid_data(create_pet_api, field, value):
    api = create_pet_api
    new_pet_id = 12001214
    pet = Pet(id=new_pet_id, category=Category(123, 'Dog'), name='Jiber', photo_urls=[
        'https://photo1.jpg', 'https://photo2.jpg'], tags=[Tag(1, 'tag1'), Tag(2, 'tag2')], status='availabe')
    setattr(pet, field, value)
    if api.is_pet_exist(new_pet_id):  # delete pet before creating if exists
        api.delete_pet(new_pet_id)
    response = api.add_pet(pet)
    assert response.status_code == 405, 'Wrong response status code'
    assert response.json() == {
        "code": 3,
        "type": "error",
        "message": "Invalid ID supplied"
    }, 'Wrong error in response'


@pytest.mark.post_pet
def test_pet_creating_with_unsupported_content_type(create_pet_api):
    api = create_pet_api
    new_pet_id = 12001215
    pet = Pet(id=new_pet_id, category=Category(3, 'Dog'), name='Jiber', photo_urls=[
        'https://photo1.jpg', 'https://photo2.jpg'], tags=[Tag(1, 'tag1'), Tag(2, 'tag2')], status='availabe')
    if api.is_pet_exist(new_pet_id):  # delete pet before creating if exists
        api.delete_pet(new_pet_id)
    response = api.add_pet(pet, is_unsupported_content_type=True)
    assert response.status_code == 415, 'Wrong response status code'
    reason = response.raw.reason
    assert reason == 'Unsupported Media Type', 'Wrong error reason'


@pytest.mark.put_pet
def test_pet_updating_with_valid_data(create_pet_api):
    api = create_pet_api
    pet_id = 120032743
    new_pet = Pet(id=pet_id, category=Category(1000, 'NEW_CATEGORY'), name='NEW_NAME', photo_urls=[
        'https://NEWphoto1.jpg', 'https://NEWphoto2.jpg'], tags=[Tag(1, 'NEW_TAG1'), Tag(2, 'NEW_TAG1')], status='NEW')
    if api.is_pet_exist(pet_id):  # recreate new pet before updating to control data
        api.delete_pet(pet_id)
    api.add_pet(new_pet)
    updated_pet = Pet(id=pet_id, category=Category(1000, 'UODATED_CATEGORY'), name='UODATED_NAME',
                      photo_urls=['https://UODATEDphoto1.jpg', 'https://UODATEDphoto2.jpg'],
                      tags=[Tag(1, 'UODATED_TAG1'), Tag(2, 'UODATED_TAG1')], status='UODATED')
    response = api.update_pet(updated_pet)
    assert response.status_code == 200, 'Wrong response status code'
    response_body = response.json()
    assert api.validate_pet_schema(response_body)
    assert response_body == updated_pet.to_dict(), 'Response body doesn\'t match to request body'
    assert api.get_pet(pet_id).json() == updated_pet.to_dict(), 'Data in updated pet doesn\'t match to data used ' \
                                                                'when updating'


@pytest.mark.put_pet
def test_updating_of_unexisting_pet(create_pet_api):
    api = create_pet_api
    pet_id = 1203312743
    if api.is_pet_exist(pet_id):   # delete pet before updating if exists
        api.delete_pet(pet_id)
    new_pet = Pet(id=pet_id, category=Category(1000, 'NEW_CATEGORY'), name='NEW_NAME', photo_urls=[
        'https://NEWphoto1.jpg', 'https://NEWphoto2.jpg'], tags=[Tag(1, 'NEW_TAG1'), Tag(2, 'NEW_TAG1')], status='NEW')
    response = api.update_pet(new_pet)
    assert response.status_code == 404, 'Wrong response status code'
    assert response.json() == {
        "code": 1,
        "type": "error",
        "message": "Pet not found"
    }, 'Wrong error in response'


@pytest.mark.put_pet
@pytest.mark.parametrize('field, value', [('id', 'qwe'), ('category', {'id': [123], 'name': 'name'}),
                                          ('status', {'status': 'available'})])
def test_pet_updating_with_invalid_data(create_pet_api, field, value):
    api = create_pet_api
    pet_id = 1203312743
    new_pet = Pet(id=pet_id, category=Category(1000, 'NEW_CATEGORY'), name='NEW_NAME', photo_urls=[
        'https://NEWphoto1.jpg', 'https://NEWphoto2.jpg'], tags=[Tag(1, 'NEW_TAG1'), Tag(2, 'NEW_TAG1')], status='NEW')
    if not api.is_pet_exist(pet_id):  # create pet before updating if exists
        api.add_pet(new_pet)
    updated_pet = Pet(id=pet_id, category=Category(123, 'Dog'), name='Jiber', photo_urls=[
        'https://photo1.jpg', 'https://photo2.jpg'], tags=[Tag(1, 'tag1'), Tag(2, 'tag2')], status='availabe')
    setattr(updated_pet, field, value)
    response = api.update_pet(updated_pet)
    assert response.status_code == 405, 'Wrong response status code'
    assert response.json() == {
        "code": 4,
        "type": "error",
        "message": "Validation Exception"
    }, 'Wrong error in response'


@pytest.mark.delete_pet
def test_deleting_of_existing_pet(create_pet_api):
    api = create_pet_api
    new_pet_id = 120012333
    pet = Pet(id=new_pet_id, category=Category(3, 'Dog'), name='Jiber', photo_urls=[
        'https://photo1.jpg', 'https://photo2.jpg'], tags=[Tag(1, 'tag1'), Tag(2, 'tag2')], status='availabe')
    if not api.is_pet_exist(new_pet_id):  # add pet before deleting if it doesn't exist
        api.add_pet(pet)
    response = api.delete_pet(new_pet_id)
    assert response.status_code == 200, 'Wrong response status code'
    assert not api.is_pet_exist(new_pet_id), 'Pet still exists'


@pytest.mark.delete_pet
def test_deleting_of_unexisting_pet(create_pet_api):
    api = create_pet_api
    pet_id = 120012334
    if api.is_pet_exist(pet_id):  # delete pet before one more deleting if exists
        api.delete_pet(pet_id)
    response = api.delete_pet(pet_id)
    assert response.status_code == 404, 'Wrong response status code'
    assert response.json() == {
        "code": 1,
        "type": "error",
        "message": "Pet not found"
    }, 'Wrong error in response'


@pytest.mark.delete_pet
@pytest.mark.parametrize('pet_id', (-1, 0, 'qwe', [10], {300}, {1: '1'}, None))
def test_deleting_with_invalid_id(create_pet_api, pet_id):
    api = create_pet_api
    response = api.delete_pet(pet_id)
    assert response.status_code == 400, 'Wrong response status code'
    assert response.json() == {
        "code": 2,
        "type": "error",
        "message": "Invalid ID supplied"
    }, 'Wrong error in response'
