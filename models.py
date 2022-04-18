"""
This will create the tables for the database
"""
# unusual errors are disabled
# pylint: disable=E1101, R0913, C0413, C0103, W1508, R0903, W0603, E0602, W0404, C0301, W0105, W0612, C0411, C0412, W0611, R0124, C0121
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, exc, asc
from flask import json


class Database:
    """This is the database class"""
    def __init__(self, app):
        self.db = SQLAlchemy(app)

        class User(self.db.Model):
            """Makes the user table"""
            id = self.db.Column(self.db.Integer, primary_key=True)
            username = self.db.Column(self.db.String(80),
                                      unique=True,
                                      nullable=False)
            password = self.db.Column(self.db.String(50),
                                      unique=False,
                                      nullable=False)
            name = self.db.Column(self.db.String(),
                                  unique=False,
                                  nullable=False)

            def __repr__(self):
                return '<User username=' + self.username + ' id=' + str(
                    self.id) + ' name=' + self.name + ' >'

        self.User_Table = User

        class Recipe(self.db.Model):
            """Makes the user recipe"""
            id = self.db.Column(self.db.Integer, primary_key=True)
            name = self.db.Column(self.db.String(), nullable=False)
            creator_id = self.db.Column(self.db.Integer,
                                        self.db.ForeignKey('user.id'),
                                        nullable=False)
            cuisine = self.db.Column(self.db.String(), nullable=False)
            description = self.db.Column(self.db.String(), nullable=True)
            instructions = self.db.Column(self.db.String(), nullable=True)
            ingredients = self.db.Column(self.db.String(), nullable=False)
            img = self.db.Column(self.db.String(), nullable=True)

            def __repr__(self):
                return '<Recipe id=' + str(
                    self.id
                ) + ' name=' + self.name + ' cuisine=' + self.cuisine + ' >'

        self.Recipe_Table = Recipe

        class Comments(self.db.Model):
            """Makes the user comments"""
            id = self.db.Column(self.db.Integer, primary_key=True)
            creator_id = self.db.Column(self.db.Integer,
                                        self.db.ForeignKey('user.id'),
                                        nullable=False)
            recipe_id = self.db.Column(self.db.Integer,
                                       self.db.ForeignKey('recipe.id'),
                                       nullable=False)
            comment = self.db.Column(self.db.String())

            def __repr__(self):
                return '<Comment ' + 'id=' + str(self.id) + ' creator=' + str(
                    self.creator_id) + ' recipe_id=' + str(
                        self.recipe_id) + ' >'

        self.Comment_Table = Comments

        class Favorite(self.db.Model):
            """ Favorite recipe table"""
            id = self.db.Column(self.db.Integer, primary_key=True)
            creator_id = self.db.Column(self.db.Integer,
                                        self.db.ForeignKey('user.id'),
                                        nullable=False)
            recipe_id = self.db.Column(self.db.Integer,
                                       self.db.ForeignKey('recipe.id'),
                                       nullable=False)

            def __repr__(self):
                return '<Favorite creator_id=' + str(
                    self.creator_id) + " id=" +str(self.id)+" recipe_id=" + str(
                        self.recipe_id) + " >"

        self.Favorite_Table = Favorite
        self.db.create_all()

    #inserts user and returns a user id
    def insertUser(self, username: str, password: str, name: str):
        """This methods inserts the users into the table"""
        try:
            entry = self.User_Table(username=username,
                                    password=password,
                                    name=name)
            self.db.session.add(entry)
            self.db.session.commit()
        except exc.SQLAlchemyError:
            return ({"code": 0, "message": "User already exist"})
        print('User ', entry, " was added to database")
        user = self.User_Table.query.filter_by(username=username).first()
        return ({"code": 1, "User_Id": user.id})

    #checks if user exist
    def User_Exist(self, username: str, password: str):
        """This method checks if the user exists or not"""
        exist = self.User_Table.query.filter_by(username=username,
                                                password=password).first()
        if exist == None:
            return ({"code": 0, "message": "Username or Password is wrong"})

        print(exist)
        return ({"code": 1, "id": exist.id})

    #inserts recipe to database
    def insertRecipe(self, name: str, creator_id: int, description: str,ingredients: str, cuisine: str, img, instructions):
        """This will insert a new recipe"""
        entry = self.Recipe_Table(name=name,
                                  creator_id=creator_id,
                                  description=description,
                                  ingredients=ingredients,
                                  cuisine=cuisine,
                                  img=img,
                                  instructions=instructions)
        self.db.session.add(entry)
        self.db.session.commit()
        print('Recipe ', entry, " was added to database")
        return {"Code": 1}
        
    #search recipes by id and returns recipe info with comments
    def getRecipesById(self, recipe_id: int):
        """This wil get the recipe by its id"""
        entry = self.Recipe_Table.query.join(
            self.User_Table,
            self.User_Table.id == self.Recipe_Table.creator_id).add_columns(
                self.User_Table.name).filter(
                    self.Recipe_Table.id == recipe_id).first()
        comments = self.Comment_Table.query.order_by(
            asc(self.Comment_Table.creator_id)).join(
                self.User_Table, self.Comment_Table.creator_id ==
                self.User_Table.id).add_columns(
                    self.User_Table.name, self.User_Table.id).filter(
                        self.Comment_Table.recipe_id == recipe_id).all()
        return {
            "name": entry[0].name,
            "creator_id": entry[0].creator_id,
            "creator_name": entry[1],
            "cuisine": entry[0].cuisine,
            "description": entry[0].description,
            "ingredients": json.loads(entry[0].ingredients),
            "instructions": json.loads(entry[0].instructions),
            "img": entry[0].img,
            "comments": {
                i: {
                    "name": comments[i][1],
                    "comment": comments[i][0].comment,
                    "id": comments[i][2],
                    "comment_id": comments[i][0].id
                }
                for i in range(len(comments))
            }
        }
    
    #deletes user by id
    def deleteUser(self, user_id):
        """This is to delete a users"""
        self.User_Table.query.filter_by(id=user_id).delete()
        self.db.session.commit()

    #deletes recipe by id
    def deleteRecipe(self, recipe_id):
        """This is to delete a recipe"""
        self.Recipe_Table.query.filter_by(id=recipe_id).delete()
        self.db.session.commit()

    #delete comment by id
    def deleteComment(self, comment_id):
        """This is to delete a comment"""
        self.Comment_Table.query.filter_by(id=comment_id).delete()
        self.db.session.commit()
        
    #delete favorite by id

    
    #changes user info
    def changeUser(self, user_id, newUsername, newName):
        """This is to change the user name"""
        entry = self.User_Table.query.filter_by(id=user_id).first()
        if entry.username != newUsername:
            entry.username = newUsername
        if entry.name != newName:
            entry.name = newName
        self.db.session.commit()

    #changes comment info
    def changeComment(self, comment_id, newComment):
        """This will change the comment"""
        entry = self.Comment_Table.query.filter_by(id=comment_id).first()
        if entry.comment != newComment:
            entry.comment = newComment
        self.db.session.commit()

    def getRecipes(self):
        """This will get recipes"""
        que=self.Recipe_Table.query.all()
        ret = []
        if len(que):
            for i in range(len(que)):
                ret.append({
                    "id": que[i].id,
                    "name": que[i].name,
                    "creator_id":que[i].creator_id,
                    "creator_name":self.User_Table.query.filter_by(id=que[i].creator_id).first().name,
                })
        else:
            ret = [{
                "id": 0,
                "name": "No",
                "creator_id": 0,
                "creator_name": "recipes"
                
            }]
        return {"returning": ret}
    
    def searchRecipes(self, search):
        """This will search recipes"""
        searchString = "%"+search+"%"
        que=self.Recipe_Table.query.filter(self.Recipe_Table.name.ilike(searchString)).all()
        print("que: ")
        print(que)
        ret = []
        if len(que):
            for i in range(len(que)):
                ret.append({
                    "id":
                    que[i].id,
                    "name":
                    que[i].name,
                    "creator_id":
                    que[i].creator_id,
                    "creator_name":
                    self.User_Table.query.filter_by(
                        id=que[i].creator_id).first().name,
                })
        else:
            ret = [{
                "id": 0,
                "name": "",
                "creator_id": 0,
                "creator_name": "No recipes"
            }]
        return {"returning": ret}

    def getRecipesbyCuisine(self, cuisine: str, recipe_limit: int):
        """This wil get the recipe by its cuisine"""
        print()
        que = self.Recipe_Table.query.filter(
            cuisine == cuisine,
            self.Recipe_Table.id > recipe_limit).limit(20).all()
        return {
            i: {
                "id":
                que[i].id,
                "name":
                que[i].name,
                "creator_id":
                que[i].creator_id,
                "creator_name":
                self.User_Table.query.filter_by(
                    id=que[i].creator_id).first().name,
            }
            for i in range(len(que))
        }

    def insertComment(self, creator_id, recipe_id, comment):
        """This lets the user add a comment"""
        ##
        entry = self.Comment_Table(creator_id=creator_id,
                                   recipe_id=recipe_id,
                                   comment=comment)
        self.db.session.add(entry)
        self.db.session.commit()
        print('Comment ', entry, " was added to database")
        
    def insertFavorite(self, creator_id, recipe_id):
        """This lets the user add a favorite recipe"""
        ##
        entry = self.Favorite_Table(creator_id=creator_id,
                                   recipe_id=recipe_id) 
        self.db.session.add(entry)
        self.db.session.commit()
        print('Favorite recipe ', entry, " was added to database")

    def changeRecipe(self, recipe_id, newName, newDescription, newIngredients):
        """This lets user edit its recipe"""
        entry = self.Recipe_Table.query.filter_by(id=recipe_id).first()
        if entry.name != newName:
            entry.name = newName
        if entry.description != newDescription:
            entry.description = newDescription
        if entry.ingredients != newIngredients:
            entry.ingredients = newIngredients

        self.db.session.commit()
    def deleteFavorite(self, favorite_id):
        """This is to delete a comment"""
        self.Favorite_Table.query.filter_by(id=favorite_id).delete()
        self.db.session.commit()
    def getFavorite(self,user_id):
        que=self.Favorite_Table.query.filter_by(creator_id=user_id).join(self.Recipe_Table,self.Favorite_Table.recipe_id==self.Recipe_Table.id).add_columns(self.Recipe_Table.id,self.Recipe_Table.name).join(self.User_Table,self.User_Table.id==self.Recipe_Table.creator_id).add_columns(self.User_Table.name,self.User_Table.id).all()
        
        returnval={
            i: {
                "favorite_id":
                que[i][0].id,
                "recipe_id":
                que[i][1],
                "recipe_name":
                que[i][2],
                "user_name":que[i][3],
                "user_id":que[i][4]
            }
            for i in range(len(que))
        }
        return returnval
    