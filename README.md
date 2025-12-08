# Film Finder

This all-in-one web application allows you to find movies based on user recommendations. Inspired by Netflix and Letterboxd, users can now view films, create personalized watchlists, and rate what they watch all in one platform.

**Created by:** Julie Kim, Emma Gershman, Yasmine Bader, Dhruvi Kapadia


## Prerequisites
1. Clone this repository to your local machine
    - `git clone https://github.com/jjuliekim/film-finder.git`
2. Set up the `.env` file in the `api` folder based on the `.env.template` file.
    - Make a copy of the `.env.template` file and name it `.env`. 
    - Open the new `.env` file. 
    - On the last line, delete the `<...>` placeholder text, and put a password.
    ```
    SECRET_KEY=someCrazyS3cR3T!Key.!
    DB_USER=root
    DB_HOST=db
    DB_PORT=3306
    DB_NAME=film-finder
    MYSQL_ROOT_PASSWORD=<put a good password here>
    ```

## Start Application
Run these commands in the (Docker) terminal
- `docker compose up` to build and start all containers
- You should see the `web-app`, `web-api`, and `mysql_db` services running
- Access the application at `http://localhost:8501`

Run `docker compose down -v` to stop all services
