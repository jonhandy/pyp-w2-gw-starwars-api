import responses

from tests import BaseStarWarsAPITestCase
from starwars_api.exceptions import SWAPIClientError
from starwars_api.models import *


class PeopleTestCase(BaseStarWarsAPITestCase):

    @responses.activate
    def test_people_model(self):
        luke = People.get(1)
        self.assertEqual(luke.name, 'Luke Skywalker')
        self.assertEqual(luke.name, 'Luke Skywalker')
        self.assertEqual(luke.height, '172')
        self.assertEqual(luke.mass, '77')
        self.assertEqual(luke.hair_color, 'blond')
        self.assertEqual(luke.skin_color, 'fair')
        self.assertEqual(luke.eye_color, 'blue')
        self.assertEqual(luke.birth_year, '19BBY')
        self.assertEqual(luke.gender, 'male')

    @responses.activate
    def test_people_model_not_found(self):
        error = ('Request to SWAPI "/api/people/100" failed with '
                 'status "404". Reason: {"detail": "Not found"}')
        with self.assertRaisesRegexp(SWAPIClientError, error):
            People.get(100)

class FilmsTestCase(BaseStarWarsAPITestCase):
    @responses.activate
    def test_films_model(self):
        new_hope = Films.get(1)
        self.assertTrue(new_hope.title, 'A New Hope')
        self.assertTrue(new_hope.director, 'George Lucas')
        self.assertTrue(new_hope.release_date, '1977-05-25')

    @responses.activate
    def test_films_model_not_found(self):
        error = ('Request to SWAPI "/api/films/100" failed with '
                 'status "404". Reason: {"detail": "Not found"}')
        with self.assertRaisesRegexp(SWAPIClientError, error):
            Films.get(100)

class PeopleQuerySetTestCase(BaseStarWarsAPITestCase):

    @responses.activate
    def test_people_qs_next(self):
        qs = People.all()
        obj = qs.next()
        self.assertTrue(isinstance(obj, People))
        self.assertEqual(obj.name, 'Luke Skywalker')

    @responses.activate
    def test_people_qs_iterable(self):
        qs = People.all()
        self.assertEqual(len([elem for elem in qs]), 15)  # 10 in page1, 5 in page2

    @responses.activate
    def test_people_qs_count(self):
        qs = People.all()
        self.assertEqual(qs.count(), 15)

class FilmsQuerySetTestCase(BaseStarWarsAPITestCase):

    @responses.activate
    def test_films_qs_next(self):
        qs = Films.all()
        obj = qs.next()
        self.assertTrue(isinstance(obj, Films))
        self.assertEqual(obj.title, 'A New Hope')

    @responses.activate
    def test_films_qs_iterable(self):
        qs = Films.all()
        self.assertEqual(len([elem for elem in qs]), 7)

    @responses.activate
    def test_films_qs_count(self):
        qs = Films.all()
        self.assertEqual(qs.count(), 7)
