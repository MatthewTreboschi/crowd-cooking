https://crowd-cooking.herokuapp.com/

This app was made to innovate new recipes by mixing the qualities of social media with a recipe website so that the user may recieve feedback and adjust their recipe accordingly.

For future releases, I'd like to streamline the landing page, perhaps allowing users to swipe past/scroll past and potentially adding a "do not show me this again" option. I'd also like to add the ability to search for or sort foods easier. I think that would improve the user experience significantly and would make the app more scalable. 

## Requirements

1. `npm install`
2. `pip install -r requirements.txt`
3. `npm install axios`

## Setup

1. Clone the repository with `git clone https://github.com/MatthewTreboschi/crowd-cooking.git`
2. Run `echo "DANGEROUSLY_DISABLE_HOST_CHECK=true" > .env.development.local` in the project directory

## Run Application

1. Run command in terminal (in your project directory): `python app.py`
2. Run command in another terminal, `cd` into the project directory, and run `npm run start`
3. Preview web page in browser '/'

## Deploy to Heroku

1. Create a Heroku app: `heroku create --buildpack heroku/python`
2. Add nodejs buildpack: `heroku buildpacks:add --index 1 heroku/nodejs`
3. Add database to heroku: `heroku addons:create heroku-postgresql:hobby-dev`
4. Push to Heroku: `git push heroku main`
