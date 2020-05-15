from flask_migrate import MigrateCommand
from flask_script import Manager
from app import create_app

# Setup Flask-Script with command line commands
manager = Manager(create_app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
