# Coffee Shop Full Stack


## Instroduction

This API serves as a virtual digital coffee shop and helps users explore the menu. The application will:

1) Display graphics representing the ratios of ingredients in each drink.
2) Allow public users to view drink names and graphics.
3) Allow the shop baristas to see the recipe information.
4) Allow the shop managers to create new drinks and edit existing drinks.


## About the Stack

### Backend

The `./backend` directory contains a Flask server with SQLAlchemy module. 

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. You will only need to update the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app. 

[View the README.md within ./frontend for more details.](./frontend/README.md)


## Reference 
Base project framework https://github.com/udacity/FSND/tree/master/projects/03_coffee_shop_full_stack/starter_code