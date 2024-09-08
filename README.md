# Hackathon Submission API

This is a simple Django REST API for hosting and participating in hackathons. The API allows authorized users to create hackathons, while other users can submit their hackathon projects. Users can also enroll in hackathons and view their participation.

## Features
- **Hackathon Creation**: Authorized users can create new hackathons, providing details such as title, description, type of submission, start/end times, and reward prizes.
- **Hackathon Enrollment**: Users can enroll in any hackathon.
- **Hackathon Submissions**: Users can submit their projects to the hackathon based on the type of submission (image, file, or link).
- **View Hackathons**: Users can view a list of hackathons and specific hackathon details.
- **View Hackathon Participants**: Users can view the list of participants for a specific hackathon.
- **View User’s Hackathon Enrollment**: Users can view all the hackathons they have enrolled in.

## API Endpoints

### Hackathon Endpoints

- **GET /hackathons/**
  - Fetches a list of all hackathons.
  - No authentication required.

- **POST /hackathons/**
  - Creates a new hackathon. Only authenticated users are allowed to create.
  - Requires authentication (Token).
  - **Example payload**:
    ```json
    {
      "title": "AI Hackathon",
      "description": "An event to showcase AI skills",
      "type_of_submission": "file",
      "start_datetime": "2023-09-01T09:00:00Z",
      "end_datetime": "2023-09-30T17:00:00Z",
      "reward_prize": "$5000"
    }
    ```

- **GET /hackathons/<id>/**
  - Fetches details of a specific hackathon.
  - No authentication required.

- **PUT /hackathons/<id>/**
  - Updates an existing hackathon. Only the creator can update it.
  - Requires authentication.

- **DELETE /hackathons/<id>/**
  - Deletes a specific hackathon. Only the creator can delete it.
  - Requires authentication.

### Participant Endpoints

- **GET /hackathons/<id>/participants/**
  - Fetches a list of participants for the specified hackathon.
  - Requires authentication.

- **POST /hackathons/<id>/participants/**
  - Enrolls the user in the specified hackathon.
  - Requires authentication.

### Submission Endpoints

- **GET /hackathons/<id>/submissions/**
  - Fetches the list of submissions made by the authenticated user for the specified hackathon.
  - Requires authentication.

- **POST /hackathons/<id>/submissions/**
  - Creates a new submission for the specified hackathon.
  - Requires authentication.
  - **Example payload**:
    ```json
    {
      "name": "AI Project",
      "summary": "A project that uses AI to predict stock prices",
      "submission": "https://github.com/user/repo"
    }
    ```

### User Enrollment Endpoints

- **GET /hackathons/enrolled/**
  - Fetches the list of hackathons in which the authenticated user is enrolled.
  - Requires authentication.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/hackathon-api.git
   cd hackathon-api


2. Install dependencies:
  ```bash
   pip install -r requirements.txt


3. Run migrations:
  ```bash
   python manage.py migrate


4. Run the development server:
  ```bash
   python manage.py runserver

