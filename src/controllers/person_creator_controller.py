from typing import Dict
import re
from src.models.sqlite.interfaces.people_repository import PeopleRepositoryInterface
from src.errors.error_types.http_bad_request import HttpBadRequestError
from .interfaces.person_creator_controller import PersonCreatorControllerInterface

class PersonCreatorController(PersonCreatorControllerInterface):
  def __init__(self, people_repository: PeopleRepositoryInterface):
    self.__people_repository = people_repository

  def create(self, person_info: Dict) -> Dict:
    first_name = person_info["first_name"]
    last_name = person_info["last_name"]
    age = person_info["age"]
    pet_id = person_info["pet_id"]

    self.__validate_first_and_last_name(first_name, last_name)
    # self.__validate_age_and_pet_id(age, pet_id)
    self.__insert_person_in_db(first_name, last_name, age, pet_id)
    formated_response = self.__format_response(person_info)
    return formated_response

  def __validate_first_and_last_name(self, first_name: str, last_name: str) -> None:
    # Expressão Regular para caracteres que não são letras
    non_valid_characters = re.compile(r'[^a-zA-Z]')

    if non_valid_characters.search(first_name) or non_valid_characters.search(last_name):
      raise HttpBadRequestError("Nome da pessoa invalido!")

  # def __validate_age_and_pet_id(self, age: str, pet_id: str) -> None:
  #   # Expressão Regular para caracteres que não são números
  #   non_valid_characters = re.compile(r'\D')

  #   if non_valid_characters.search(age) or non_valid_characters.search(pet_id):
  #     raise Exception("Idade ou ID do pet invalidos!")

  def __insert_person_in_db(self, first_name: str, last_name: str, age: int, pet_id: int) -> None:
    self.__people_repository.insert_person(first_name, last_name, age, pet_id)

  def __format_response(self, person_info: Dict) -> Dict:
    return {
      "data": {
        "type": "Person",
        "count": 1,
        "attributes": person_info
      }
    }
