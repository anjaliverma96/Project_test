WHERE=Local
CONFIG=config.yml
BUCKET=bin


.PHONY: venv create_db run_app

JokeRecommender/${BUCKET}/activate: requirements.txt
	test -d JokeRecommender || virtualenv JokeRecommender

	. JokeRecommender/${BUCKET}/activate; pip install -r requirements.txt
	touch JokeRecommender/${BUCKET}/activate

venv: JokeRecommender/${BUCKET}/activate
	
create_db: venv
	. JokeRecommender/${BUCKET}/activate; python run.py create_db --where=${WHERE}


app: create_db venv
	. JokeRecommender/${BUCKET}/activate; python run.py run_app

all: app venv




