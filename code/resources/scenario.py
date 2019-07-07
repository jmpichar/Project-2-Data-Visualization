from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.scenario import ScenarioModel


# api works with resources and the resource has to be a class
# define the Scenario resource
class Scenario(Resource):
    TABLE_NAME = 'scenarios'

    parser = reqparse.RequestParser()
    parser.add_argument('strategy',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    @jwt_required() # authenticate scenario
    def get(self, name):

        scenario = ScenarioModel.find_by_name(name)
        if scenario:
            return scenario.json()
        return {'message': 'Scenario not found'}, 404

    def post(self, name):
            if ScenarioModel.find_by_name(name):
                return {'message': f'A scenario with name {name} already exists'}, 400

            data = Scenario.parser.parse_args()

            # scenario = ScenarioModel(name, **data)
            scenario = ScenarioModel(name, data['strategy'])

            try:
                scenario.save_to_db()
            except:
                #raise
                return {'message':'an error occurred inserting the scenario.'}, 500

            return scenario.json(), 201

    def delete(self, name):
        scenario = ScenarioModel.find_by_name(name)

        if scenario:
            item.delete_from_db()

        return {'message':'Scenario deleted'}

    def put(self, name):
        data = Scenario.parser.parse_args()

        scenario = ScenarioModel.find_by_name(name)

        # ScenarioModel.insert(scenario)
        if scenario is None:
            scenario = ScenarioModel(name, data['strategy'])
        else:
            scenario.strategy = data['strategy']

        scenario.save_to_db()

        return scenario.json()

class ScenarioList(Resource):
    def get(self):
        ''' query the database for all items. the query will perform
            the following SQL command:
                SELECT * FROM items
            Can be done using a list comprehesion or a lambda function:
            return {'scenarios': list(map(lambda x: x.json() , ScenariuoModel.query.all()))}
        '''
        return {'scenarios':[scenario.json() for scenario in ScenarioModel.query.all()]}
