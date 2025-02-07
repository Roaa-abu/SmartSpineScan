from flask import Flask

app = Flask(__name__)
from app import views
# Set default environment if not already set
app.config['ENV'] = app.config.get('ENV', 'development')


if app.config['ENV'] == "production" :
    app.config.from_object("config.ProductionConfig")
elif app.config['ENV'] == "development" :
    app.config.from_object("config.DevelopmentConfig")
else :
    app.config.from_object("config.TestingConfig")