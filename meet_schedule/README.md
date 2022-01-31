# Meetings Schedule Application

## Setup

The first thing to do is to clone the repository:


```sh
$ git clone --------/------------
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ cd meet_schedule
(env)$ pip install -r requirements.txt
```

## Postgresql DB Setup

```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'YOUR_USER_NAME',
        'NAME': 'YOUR_DB_NAME',
        'PASSWORD': 'YOUR_DB_PASSWORD',
        'HOST': 'localhost',
        'ATOMIC_REQUESTS': True,
    }
}
```

## Once pip has finished downloading the dependencies:

```sh
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```

## API Testing

```sh
http://127.0.0.1:8000/graphql/
```

User Sigunp :- 

```sh
mutation {
  register(
    email: "test4@gmail.com",
    username: "user4",
    password1: "Test@123",
    password2: "Test@123",
  ) {
    success,
    errors,
    token,
    refreshToken,
  }
}
```
Result :-

```sh
{
  "data": {
    "register": {
      "success": true,
      "errors": null,
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXI1IiwiZXhwIjoxNjQzMDM0MzIwLCJvcmlnSWF0IjoxNjQzMDM0MDIwfQ.7vA1FD_mcPk69J-s-Z9RMM5oGf7eD0yMHz5m4WQuuMk",
      "refreshToken": "72ee767793ff6e328a4f72ce2fccec16f008be7d"
    }
  }
}
```

User Login :- 

```sh
mutation {
  tokenAuth(username: "user4", password: "Test@123") {
    success,
    errors,
    token,
    refreshToken,
    user {
      username
    }
  }
}
```

Result :-

```sh
{
  "data": {
    "tokenAuth": {
      "success": true,
      "errors": null,
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXI0IiwiZXhwIjoxNjQzMDM0NDE2LCJvcmlnSWF0IjoxNjQzMDM0MTE2fQ.LwyhdVrk-Vuw2YVfvlnDYTYLuamE1RV2myv4YpHXUzI",
      "refreshToken": "a1874d8114b844fbb5ec21451225e0a4ae4b21e7",
      "user": {
        "username": "user4"
      }
    }
  }
}

```

Add Request Header for Authorization as :-

Take token from login API result

```sh
    {  
    "Authorization": "JWT << token >>"
}

```


User Schedule Creation :-

```sh
mutation{create_meet:createMeet(input:{startDateTime:"2022-04-09T04:32" ,intervalTime:"15"}){
   data{
    id,
   startDateTime,
    intervalTime,
  }
}}

```

Result :-

```sh
{
  "data": {
    "create_meet": {
      "data": {
        "id": "5",
        "startDateTime": "2022-04-09T04:32:00",
        "intervalTime": "A_15"
      }
    }
  }
}
```

Schedule Update :-

```sh
mutation{update_meet:updateMeet(input:{startDateTime:"2022-09-11T06:00",intervalTime:"30"}id:4){
   data{
     id,
     startDateTime,
     intervalTime,
   }
 }}

```

Result :-

```sh
{
  "data": {
    "update_meet": {
      "data": {
        "id": "4",
        "startDateTime": "2022-09-11T06:00:00",
        "intervalTime": "A_30"
      }
    }
  }
}

```

Schedule Deletion :-

```sh
mutation 
{
delete_meet:deleteMeet(id:4){
ok 
}
}

```

Result :-

```sh
{
  "data": {
    "delete_meet": {
      "ok": true
    }
  }
}

```

## API for Non-User

Remove Authentication Header

User List :-

```sh
query {
  users {
    edges {
      node {
        id
        username
        email
        isActive
      }
    }
  }
}

```

Result :-

```sh
{
  "data": {
    "users": {
      "edges": [
        {
          "node": {
            "id": "VXNlck5vZGU6OA==",
            "username": "user2",
            "email": "c@gmail.com",
            "isActive": true
          }
        },
        {
          "node": {
            "id": "VXNlck5vZGU6MTE=",
            "username": "user5",
            "email": "test5@gmail.com",
            "isActive": true
          }
        }
      ]
    }
  }
}

```

User specific schedule list :-

```sh
mutation{schedule_list:scheduleList(id:2){
   data{
     id,
     startDateTime,
     endDateTime,
     intervalTime,
   }
 }}


```

Result :-

```sh
{
  "data": {
    "schedule_list": {
      "data": [
        {
          "id": "1",
          "startDateTime": "2022-09-11T06:00:00+00:00",
          "endDateTime": "2022-09-11T06:30:00+00:00",
          "intervalTime": "A_30"
        }
      ]
    }
  }
}
```

Reserve Non-User Schedule :-

```sh

mutation{create_reserve:createReserve(input:{schedule:1,firstName:"kari",lastName:"chou",email:"k@gmail.com"}){
   data{
    id,
    schedule{    
    id  
    startDateTime,
    endDateTime,
    intervalTime
    }
   	firstName,
    lastName,
    email,
  }
}}


```

Result :-

```sh
{
  "data": {
    "create_reserve": {
      "data": {
        "id": "2",
        "schedule": {
          "id": "1",
          "startDateTime": "2022-09-11T06:00:00+00:00",
          "endDateTime": "2022-09-11T06:30:00+00:00",
          "intervalTime": "A_30"
        },
        "firstName": "kari",
        "lastName": "chou",
        "email": "k@gmail.com"
      }
    }
  }
}

```

