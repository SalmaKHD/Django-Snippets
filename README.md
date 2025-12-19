## Overview
A simple website to demonstrate basic functionalities of the Django framework.

## Features
Stores and displays movies in a movie store.
Fetches top news on Microsoft, Apple, Google, and Tesla.
- Functionalities:
  - Main Screen: Displays all the available movies in the store.
  - Detail Screen: Shows details of the selected movie
  - Search feature: Allows searching for movies based on title or description
  - Pagination: Returns paginated items for movies list
  - Authentication: Sign-in and Sign-up features across website + protected features
  - DRF: allows apis with JSON data for movie CRUD operations
  - JWT: generates and returns access and refresh tokens using simplejwt and protects apis
  - Movie creation: Creating new movies with image upload for movie cover
  - Radis: used for caching movies every 5 mins

Tech Stack
- Python
- Django
- Admin
- Paginator
- Auth
- DRF for APIs
- Simple JWT for acceess and refresh tokens
- Pillow for image upload
- Radis for caching

## Future Enhancements
- better styling
- tests for all features

# Screenshots
![home_search](https://github.com/user-attachments/assets/071caf63-4a94-47ad-adec-28c04908f815)
![detail_new-movie_reg-form](https://github.com/user-attachments/assets/6f7955aa-114d-4f26-a8ac-b45837e0ba73)

## License
Licensed under the MIT License.
