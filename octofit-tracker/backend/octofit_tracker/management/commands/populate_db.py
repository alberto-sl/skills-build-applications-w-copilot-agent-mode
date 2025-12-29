
from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient, ASCENDING

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating octofit_db with test data...'))

        # Get MongoDB connection info from Django settings
        client_settings = settings.DATABASES['default']['CLIENT']
        client = MongoClient(host=client_settings.get('host', 'localhost'), port=client_settings.get('port', 27017))
        db = client['octofit_db']

        # Drop collections if they exist
        for col in ['users', 'teams', 'activities', 'leaderboard', 'workouts']:
            if col in db.list_collection_names():
                db[col].drop()

        # Users (superheroes)
        users = [
            {"name": "Superman", "email": "superman@dc.com", "team": "DC"},
            {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
            {"name": "Black Widow", "email": "widow@marvel.com", "team": "Marvel"},
        ]
        db.users.insert_many(users)
        db.users.create_index([("email", ASCENDING)], unique=True)

        # Teams
        teams = [
            {"name": "Marvel", "members": ["Iron Man", "Captain America", "Black Widow"]},
            {"name": "DC", "members": ["Superman", "Batman", "Wonder Woman"]},
        ]
        db.teams.insert_many(teams)

        # Activities
        activities = [
            {"user": "Superman", "activity": "Flying", "duration": 120},
            {"user": "Batman", "activity": "Martial Arts", "duration": 90},
            {"user": "Iron Man", "activity": "Flight Suit Training", "duration": 100},
            {"user": "Wonder Woman", "activity": "Lasso Practice", "duration": 80},
            {"user": "Captain America", "activity": "Shield Training", "duration": 110},
            {"user": "Black Widow", "activity": "Espionage", "duration": 95},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {"user": "Superman", "points": 1000},
            {"user": "Iron Man", "points": 950},
            {"user": "Batman", "points": 900},
            {"user": "Captain America", "points": 850},
            {"user": "Wonder Woman", "points": 800},
            {"user": "Black Widow", "points": 750},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {"name": "Strength Training", "suggested_for": ["Superman", "Captain America"]},
            {"name": "Agility Drills", "suggested_for": ["Black Widow", "Batman"]},
            {"name": "Endurance Run", "suggested_for": ["Wonder Woman", "Iron Man"]},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db successfully populated!'))
