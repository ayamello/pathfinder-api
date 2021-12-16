<h1 style="text-align:center;">
    PathFinder - API
</h1>

<p style="text-align:center;">
    An API that records travel paths built by traveler users.
</p>

<h2>Overview</h2>

<p>
    The API flow is composed of the Path which is the journey. Inside the Path are the Points, which are the places that will be visited during the trip. And in Points, there are Activities, which are the actions of the traveler at each point. In addition, there are also Subscribers, which is the list of subscribers on a given Path. That is, a traveler user creates a Path and other users can subscribe to it. And yet, within Path, there are reviews, which are the ratings that users can give to a Point.
</p>

<blockquote> 🔗 Base URL: https://pathfinder-q3.herokuapp.com/</blockquote>

</br>

<h2 style="border-bottom:1px solid;text-align:center;"><strong>Routes that do not need authentication</strong></h2>

</br>

<h3 style="text-align:center;font-size:21px;">Creating user</h3>

`POST /users - Request format`
```json
{
    "name": "Kenzo Traveler",   
    "username": "kenzot",
    "birthdate": "04/12/1999",
    "email": "kenzotraveler@gmail.com",
    "password": "123456"
}
```

`POST /users - Response format - STATUS 201`
```json
{
  "id": 2,
  "name": "Kenzo Traveler",
  "username": "kenzot",
  "email": "kenzotraveler@gmail.com",
  "birthdate": "04/12/1999",
  "url_image": null,
  "created_at": "Tue, 14 Dec 2021 22:11:47 GMT",
  "updated_at": "Tue, 14 Dec 2021 22:11:47 GMT",
  "paths_lists": []
}
```

<h3 style="text-align:center;">Possible errors</h3>

<p>
    If username or email already exist:
</p>

`POST /users - Response format - STATUS 409`

```json
{
  "error": "This username already exists."
}
```

or

```json
{
  "error": "This email already exists."
}
```

<p>
    if missing or there is an error in the field syntax:
</p>

<span style="font-size:12px;">In the example, the request was made without the 'birthdate' field</span>

`POST /users - Response format - STATUS 400`

```json
{
  "error": {
    "required_keys": [
      "name",
      "username",
      "email",
      "birthdate",
      "password"
    ],
    "missing_key": "birthdate"
  }
}
```

<h3 style="text-align:center;font-size:21px;">Login</h3>

`POST /login - Request format`
```json
{
    "email": "kenzotraveler@mail.com",
    "password": "123456"
}
```

`POST /login - Response format - STATUS 200`
```json
{
    "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzOTM1NjIyMSwianRpIjoiM2Q0NDY4NjgtNDcwYi00M2JkLWEyMTEtMWQyNTU3MjAwMGIwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MSwibmFtZSI6IkF5YW5hIiwidXNlcm5hbWUiOiJheWFuYWIiLCJlbWFpbCI6ImF5YW5hYkBnbWFpbC5jb20iLCJiaXJ0aGRhdGUiOiJTYXQsIDA0IERlYy"
}
```

<h2 style="border-bottom:1px solid;text-align:center;"><strong>Routes that need authentication</strong></h2>

</br>

<h2>👤 USER</h2>

<h3 style="text-align:center;font-size:21px;">List all users</h3>

`GET /users - Response format - STATUS 200`
```json
[
  {
    "id": 1,
    "name": "Kenzo Smith",
    "username": "kenzot",
    "email": "kenzotraveler@gmail.com",
    "birthdate": "Sat, 04 Dec 1999 02:00:00 GMT",
    "url_image": null,
    "created_at": "Tue, 14 Jul 2020 11:01:56 GMT",
    "updated_at": "Tue, 14 Sep 2021 22:11:47 GMT",
    "paths_list": []
  },
  {
    "id": 2,
    "name": "Hiro",
    "username": "hiro",
    "email": "hiro123@gmail.com",
    "birthdate": "Wed, 20 May 1998 03:00:00 GMT",
    "url_image": null,
    "created_at": "Sun, 12 Jan 2020 17:11:47 GMT",
    "updated_at": "Sat, 28 Aug 2021 19:34:16 GMT",
    "paths_list": []
  },
  {
    "id": 3,
    "name": "Joe",
    "username": "backpacker",
    "email": "joebackpacker@gmail.com",
    "birthdate": "Fri, 02 Aug 1985 03:00:00 GMT",
    "url_image": null,
    "created_at": "Tue, 01 Sep 2020 14:10:42 GMT",
    "updated_at": "Fri, 10 Dec 2021 16:23:58 GMT",
    "paths_list": []
  }
]
```

<h3 style="text-align:center;font-size:21px;">List user by id</h3>

`GET /users/:id - Response format - STATUS 200`
```json
{
    "id": 2,
    "name": "Hiro",
    "username": "hiro",
    "email": "hiro123@gmail.com",
    "birthdate": "Wed, 20 May 1998 03:00:00 GMT",
    "url_image": null,
    "created_at": "Sun, 12 Jan 2020 17:11:47 GMT",
    "updated_at": "Sat, 28 Aug 2021 19:34:16 GMT",
    "paths_list": []
  }
```

<h3 style="text-align:center;font-size:21px;">Update user data</h3>

<p>
    Data that can be changed: <strong>name, username, birthdate, email, url_image, password</strong>
</p>

`PATCH /users/:user_id - Request format`
```json
{
	"username": "kenzot"
}
```

`PATCH /users/:user_id - Response formart - STATUS 200`
```json
{
  "id": 2,
  "name": "Kenzo Smith",
  "username": "kenzot",
  "email": "kenzotraveler@gmail.com",
  "birthdate": "Sat, 04 Dec 1999 02:00:00 GMT",
  "url_image": null,
  "created_at": "Tue, 14 Jul 2020 11:01:56 GMT",
  "updated_at": "Tue, 14 Dec 2021 23:11:02 GMT",
  "paths_list": []
}
```

<h3 style="text-align:center;font-size:21px;">Delete user</h3>

`DELETE /users/:user_id - Request format`
```
No body
```

<hr>
</br>

<h2>🗺️ PATH</h2>

<h3 style="text-align:center;font-size:21px;">Create path</h3>

<p>
    In the example, <strong>initial_date</strong> and <strong>end_date</strong> were used, however both are optional. The traveler may or may not set a date. As well as there is a field called <strong>duration</strong>, which is also optional and can be used if the traveler does not have or prefer not to define dates.
</p>

`POST /paths - Request format`
```json
{
    "name": "Tour throught Europe",
    "description": "Backpacking across Europe",
    "initial_date": "21/01/2022",
    "end_date": "22/02/2022"
}
```

`POST /paths - Response format - STATUS 201`
```json
{
    "id": 1,
    "name": "Tour throught Europe",
    "description": "Backpacking across Europe",
    "initial_date": "21/01/2022",
    "end_date": "22/02/2022",
    "duration": null,
    "created_at": "Tue, 15 Dec 2020 16:46:18 GMT",
    "updated_at": "Sun, 20 Dec 2021 20:31:26 GMT",
    "admin_user": {
        "name": "Kenzo Smith",
        "email": "kenzotraveler@gmail.com"
    },
    "points": [],
    "subscribers": []
}
```

<h3 style="text-align:center;font-size:21px;">List all paths</h3>

`GET /paths - Response format - STATUS 200`
```json
[
  {
    "id": 1,
    "name": "Tour throught Europe",
    "description": "Backpacking across Europe",
    "initial_date": "21/01/2021",
    "end_date": "22/02/2021",
    "duration": null,
    "created_at": "Tue, 15 Dec 2020 16:46:18 GMT",
    "updated_at": "Sun, 20 Dec 2021 20:31:26 GMT",
    "admin_user": {
      "name": "Kenzo Smith",
      "email": "kenzotraveler@gmail.com"
    },
    "points": [
      {
        "id": 2,
        "name": "Forte São João Batista",
        "description": "Visit to the Fort",
        "initial_date": null,
        "end_date": null,
        "duration": 3,
        "created_at": "Wed, 15 Dec 2021 11:04:10 GMT",
        "updated_at": "Wed, 15 Dec 2021 11:04:10 GMT",
        "activities": [
          {
            "id": 1,
            "name": "Going To The Beach",
            "description": "Day at the beach with friends",
            "created_at": "Wed, 15 Dec 2021 12:30:56 GMT",
            "updated_at": "Wed, 15 Dec 2021 12:30:56 GMT",
            "reviews": [
              {
                "id": 1,
                "name": "5 estrelas",
                "review": "The beach is amazing, it was the best day",
                "created_at": "Wed, 15 Dec 2021 15:02:10 GMT",
                "updated_at": "Wed, 15 Dec 2021 15:02:10 GMT",
                "activity_id": 1
              },
              {
                "id": 6,
                "name": "5 estrelas",
                "review": "The beach is amazing, it was the best day",
                "created_at": "Wed, 15 Dec 2021 15:04:08 GMT",
                "updated_at": "Wed, 15 Dec 2021 15:04:08 GMT",
                "activity_id": 1
              }
            ],
            "point_id": 2
          },
          {
            "id": 2,
            "name": "Going To The Beach",
            "description": "Day at the beach with friends",
            "created_at": "Wed, 15 Dec 2021 12:33:47 GMT",
            "updated_at": "Wed, 15 Dec 2021 12:33:47 GMT",
            "reviews": [
              {
                "id": 2,
                "name": "5 estrelas",
                "review": "The beach is amazing, it was the best day",
                "created_at": "Wed, 15 Dec 2021 15:03:15 GMT",
                "updated_at": "Wed, 15 Dec 2021 15:03:15 GMT",
                "activity_id": 2
              }
            ],
            "point_id": 2
          }
        ]
      }
    ],
    "subscribers": [
      {
        "username": "thebackpacking"
      }
    ]
  },
  {
    "id": 2,
    "name": "Tour throught Paris",
    "description": "Tour with my girlfriend across Paris",
    "initial_date": null,
    "end_date": null,
    "duration": "15 dias",
    "created_at": "Sun, 18 Jul 2021 10:13:58 GMT",
    "updated_at": "Sat, 13 Nov 2021 11:12:26 GMT",
    "admin_user": {
      "name": "Joe",
      "email": "joebackpacking@gmail.com"
    },
    "points": [],
    "subscribers": []
  }
]
```

<h3 style="text-align:center;font-size:21px;">List path by user id</h3>

`GET /paths/:user_id - Response format - STATUS 200`
```json
[
  {
    "id": 2,
    "name": "Tour throught Paris",
    "description": "Tour with my girlfriend across Paris",
    "initial_date": null,
    "end_date": null,
    "duration": "15 dias",
    "created_at": "Sun, 18 Jul 2021 10:13:58 GMT",
    "updated_at": "Sat, 13 Nov 2021 11:12:26 GMT",
    "admin_user": {
      "name": "Joe",
      "email": "joebackpacking@gmail.com"
    },
    "points": [],
    "subscribers": []
  }
]
```

<h3 style="text-align:center;font-size:21px;">Update path</h3>

<p>
    Data that can be changed: <strong>name, description, initial_date, end_date</strong> and <strong>duration</strong>
</p>

`PATCH /paths/:path_id - Request format`
```json
{
    "initial_date": "20/12/2022",
}
```

`PATCH /paths/:path_id - Response format - STATUS 200`
```json
{
    "id": 2,
    "name": "Tour throught Paris",
    "description": "Tour with my girlfriend across Paris",
    "initial_date": "Mon, 20 Dec 2021",
    "end_date": null,
    "duration": "15 dias",
    "created_at": "Sun, 18 Jul 2021 10:13:58 GMT",
    "updated_at": "Sat, 13 Nov 2021 11:12:26 GMT",
    "subscribers": []
}
```

<h3 style="text-align:center;font-size:21px;">Delete path</h3>

`DELETE /paths/:path_id - Request format`
```
No body
```

<hr>
</br>

<h2>📍 POINT</h2>

<h3 style="text-align:center;font-size:21px;">Create point</h3>

<p>
    In the example, <strong>duration</strong> was used, but it is optional. There are also fields called <strong>initial_date</strong> and <strong>end_date</strong>, which are also optional and can be used if the traveler wants to define dates.
</p>

`POST /paths/points - Request format`
```json
{
	"path_id": 1,
	"street": "Foz do D'ouro",
	"number": 153,
	"state": "Porto",
	"country": "Portugal",
	"postal_code": "4150-196",
	"coordenadas": "41.149078 -8.674254",
	"name": "Forte São João Batista",
	"description": "Visit to the Fort",
	"duration": "8h",
	"activities": []
}
```

`POST /paths/points - Response format - STATUS 201`
```json
{
  "id": 2,
  "name": "Forte São João Batista",
  "description": "Visit to the Fort",
  "initial_date": null,
  "end_date": null,
  "duration": "5h",
  "created_at": "Wed, 01 Dec 2021 11:09:18 GMT",
  "updated_at": "Wed, 01 Dec 2021 11:09:18 GMT",
  "activities": [],
  "address_id": 5
}
```

<h3 style="text-align:center;font-size:21px;">List points by path</h3>

`GET /paths/:path_id/points - Response format - STATUS 200`
```json
{
  "points": [
    {
      "id": 1,
      "name": "Forte São João Batista",
      "description": "Visit to the Fort",
      "initial_date": null,
      "end_date": null,
      "duration": "8 horas",
      "created_at": "Wed, 01 Dec 2021 11:09:18 GMT",
      "updated_at": "Wed, 01 Dec 2021 11:09:18 GMT",
      "activities": []
    },
    {
      "id": 2,
      "name": "Villaverde Alto",
      "description": "Visit to the Madrid",
      "initial_date": null,
      "end_date": null,
      "duration": "5 dias",
      "created_at": "Wed, 01 Dec 2021 11:30:26 GMT",
      "updated_at": "Wed, 01 Dec 2021 11:30:26 GMT",
      "activities": []
    },
    {
      "id": 3,
      "name": "Paris",
      "description": "Visit to the Paris",
      "initial_date": null,
      "end_date": null,
      "duration": "4 dias",
      "created_at": "Fri, 03 Dec 2021 10:23:11 GMT",
      "updated_at": "Fri, 03 Dec 2021 10:23:11 GMT",
      "activities": []
    }
]
```

<h3 style="text-align:center;font-size:21px;">Update point</h3>

<p>
    Data that can be changed: <strong>name, description, initial_date, end_date</strong> and <strong>duration</strong>
</p>

`PATCH /paths/points/:point_id - Request format`
```json
{
    "initial_date": "20/12/2022",
}
```

`PATCH /paths/points/:point_id - Response format - STATUS 200`
```json
{
    "id": 3,
    "name": "Paris",
    "description": "Visit to the Paris",
    "initial_date": "Sun, 20 Feb 2022",
    "end_date": null,
    "duration": "4 dias",
    "created_at": "Fri, 03 Dec 2021 10:23:11 GMT",
    "updated_at": "Fri, 03 Dec 2021 10:23:11 GMT",
    "activities": []
}
```

<h3 style="text-align:center;font-size:21px;">Delete point</h3>

`DELETE /paths/points/:point_id - Request format`
```
No body
```

<hr>
</br>

<h2>📝 ACTIVITY</h2>

<h3 style="text-align:center;font-size:21px;">Create activity</h3>

`POST /paths/points/activities - Request format`
```json
{
	"name": "Going to the beach",
	"description": "Day at the beach with friends",
	"point_id": 2
}
```

<h3 style="text-align:center;font-size:21px;">List activities by path</h3>

`GET /paths/points/:point_id/activities - Response format - STATUS 200`
```json
{
  "activities": [
    {
      "id": 1,
      "name": "Going To The Beach",
      "description": "Day at the beach with friends",
      "created_at": "Wed, 15 Dec 2021 12:30:56 GMT",
      "updated_at": "Wed, 15 Dec 2021 12:30:56 GMT",
      "reviews": [],
      "point_id": 2
    },
    {
      "id": 2,
      "name": "Lunch",
      "description": "Lunch at the restaurant A Capoeira",
      "created_at": "Wed, 15 Dec 2021 12:33:47 GMT",
      "updated_at": "Wed, 15 Dec 2021 12:33:47 GMT",
      "reviews": [],
      "point_id": 2
    }
  ]
}
```

<h3 style="text-align:center;font-size:21px;">Update activity</h3>

<p>
    Data that can be changed: <strong>name</strong> and <strong>description</strong>
</p>

`PATCH /paths/points/activities/:activity_id - Request format`
```json
{
    "description": "Lunch at the restaurant Praia do Ourigo"
}
```

`PATCH /paths/points/activities/:activity_id - Response format - STATUS 200`
```json
{
    "id": 2,
    "name": "Lunch",
    "description": "Lunch at the restaurant Praia do Ourigo",
    "created_at": "Wed, 15 Dec 2021 12:33:47 GMT",
    "updated_at": "Wed, 15 Dec 2021 12:33:47 GMT",
    "reviews": [],
    "point_id": 2
}
```

<h3 style="text-align:center;font-size:21px;">Delete activity</h3>

`DELETE /paths/points/activities/:activity_id - Request format`
```
No body
```

<hr>
</br>

<h2>👥 SUBSCRIBER</h2>

<h3 style="text-align:center;font-size:21px;">Enroll user in a route</h3>

`POST /paths/subscribers - Request format`
```json
{
	"path_id": 4
}
```

`POST /paths/subscribers - Response format - STATUS 201`
```json
{
  "id": 1,
  "user_id": 2,
  "path_id": 3,
  "users": {
    "id": 2,
    "name": "Joe",
    "username": "thebackpacking",
    "email": "joebackpacking@gmail.com",
    "birthdate": "Sun, 12 Oct 1980 03:00:00 GMT",
    "url_image": null,
    "created_at": "Wed, 15 Dec 2021 10:05:23 GMT",
    "updated_at": "Wed, 15 Dec 2021 10:05:23 GMT",
    "paths_list": []
  }
}
```

<hr>
</br>

<h2>⭐ REVIEWS</h2>

<h3 style="text-align:center;font-size:21px;">Add a review</h3>

`POST /paths/points/activities/reviews - Request format`
```json
{
	"name": "5 stars",
	"review": "The beach is amazing, it was the best day",
	"activity_id": 1
}
```

`POST /paths/points/activities/reviews - Response format - STATUS 201`
```json
{
    "id": 1,
    "name": "5 estrelas",
    "review": "The beach is amazing, it was the best day",
    "created_at": "Wed, 15 Dec 2021 15:02:10 GMT",
    "updated_at": "Wed, 15 Dec 2021 15:02:10 GMT",
    "activity_id": 1,
}
```

<h3 style="text-align:center;font-size:21px;">List reviews by activity</h3>

`GET /paths/points/activities/reviews - Response format - STATUS 200`
```json
{
  "reviews": [
    {
      "id": 1,
      "name": "5 estrelas",
      "review": "The beach is amazing, it was the best day",
      "created_at": "Wed, 15 Dec 2021 15:02:10 GMT",
      "updated_at": "Wed, 15 Dec 2021 15:02:10 GMT",
      "activity_id": 1
    },
    {
      "id": 6,
      "name": "Lunch very good",
      "review": "Good restaurant Praia do Ourigo",
      "created_at": "Wed, 15 Dec 2021 15:04:08 GMT",
      "updated_at": "Wed, 15 Dec 2021 15:04:08 GMT",
      "activity_id": 1
    }
  ]
}
```

<h3 style="text-align:center;font-size:21px;">Update review</h3>

<p>
    Data that can be changed: <strong>name</strong> and <strong>review</strong>
</p>

`PATCH /paths/points/activities/reviews/:review_id - Request format`
```json
{
    "name": "Forte São João Batista is incrible!"
}
```

`PATCH /paths/points/activities/reviews/:review_id - Response format - STATUS 200`
```json
{
    "id": 1,
    "name": "Forte São João Batista is incrible!",
    "review": "The beach is amazing, it was the best day",
    "created_at": "Wed, 08 Dec 2021 15:02:10 GMT",
    "updated_at": "Fri, 10 Dec 2021 18:21:01 GMT",
    "activity_id": 1
}
```

<h3 style="text-align:center;font-size:21px;">Delete review</h3>

`DELETE /paths/points/activities/reviews/:review_id - Request format`
```
No body
```