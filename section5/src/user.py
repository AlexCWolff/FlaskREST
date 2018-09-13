from db import with_db_connection

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
        
    @classmethod
    @with_db_connection
    def find_by_username(cursor, cls, username):
        # '?' will match to the parameter
        query = "SELECT * FROM {table} WHERE username=?".format(table=cls.TABLE_NAME)
        # param always has to be in the form of a tuple
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        
        if row:
            # *row is just the set of arguments 
            user = cls(*row)
        else:
            user = None

        return user

    @classmethod
    @with_db_connection
    def find_by_id(cursor, cls, _id):
        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        
        if row:
            user = cls(*row)
        else:
            user = None

        return user


class UserRegister(Resource):
    TABLE_NAME = 'users'

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        # Prevent duplicates
        if User.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400
                                    
        @with_db_connection
        def create_user(cursor):
            # self should be implicit here
            query = "INSERT INTO {table} VALUES (NULL, ?, ?)".format(table=self.TABLE_NAME)
            cursor.execute(query, (data['username'], data['password']))

            return {"message": "User created successfully."}, 201