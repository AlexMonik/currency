# currency
Test app to obtain currencies from russian bank.

## Some api endpoints
### Registrattion



**url**

``server:port/api/registration``

**method**

``post``

**required authorization**

`false`

**JSON request**

```json
{
    "username": "name5",
    "password": "pass3"
}
```

**JSON response**

```json
{
    "message": "User registration",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDU1MDI2NDMsIm5iZiI6MTYwNTUwMjY0MywianRpIjoiYWIwMDJmZGEtYTU5Mi00NzUzLTk5ZDItMWRkMTg4MmY4NTkzIiwiZXhwIjoxNjA1NTAzNTQzLCJpZGVudGl0eSI6Im5hbWU1IiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.S5EkJ7M8j-HX1UZ-4wRRdRHe5rGvxwZf399vpGElmrA",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDU1MDI2NDMsIm5iZiI6MTYwNTUwMjY0MywianRpIjoiODIwOTg0ODItYTQxZi00M2JjLWI2NWMtOGY1MzViZTE5YzIzIiwiZXhwIjoxNjA4MDk0NjQzLCJpZGVudGl0eSI6Im5hbWU1IiwidHlwZSI6InJlZnJlc2gifQ.FSvUTfn5zEKsCvT59JSeVfHEWkHAL1bhThlD7OTzgCM"
}
```

### Авторизация

**url**

`server:port/api/login`

**method**

`post`

**required authorization**

`true`

**JSON request**

```json
{
    "username": "name5",
    "password": "pass3"
}
```

**JSON response**

```json
{
    "message": "Logged as name5",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDU0NTA5NjksIm5iZiI6MTYwNTQ1MDk2OSwianRpIjoiNTVjMjlmYzgtNzFhZi00NWMzLTg3ODctNTMwYmY1OTNlOWM5IiwiZXhwIjoxNjA1NDUxODY5LCJpZGVudGl0eSI6Im5hbWU0IiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.r5kttPPcL_3ck7XT3npFUusWTbb3UqswzoSvmDzp0HM",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDU0NTA5NjksIm5iZiI6MTYwNTQ1MDk2OSwianRpIjoiYTg0YTg3NmUtZTQzZC00MzMyLWJjYWItNjkzZDEzMzAzMTU4IiwiZXhwIjoxNjA4MDQyOTY5LCJpZGVudGl0eSI6Im5hbWU0IiwidHlwZSI6InJlZnJlc2gifQ.1yqU0YhNBRiRp3aKtUt9S2Ani3An2PlhmsyXdVkYOlw"
}
```



### Get currency's prices

**url**

`server:port/api/currency`

**method**

`post`

**required authorization**

`false`

**JSON запрос **

```json
{
    "date1": "02/11/2020",
    "date2": "05/11/2020",
    "name": "Australian Dollar"
}
```

**JSON ответ**

```json
{
    "currency": [
        {
            "@Date": "03.11.2020",
            "@Id": "R01010",
            "Nominal": "1",
            "Value": "56,3702"
        },
        {
            "@Date": "04.11.2020",
            "@Id": "R01010",
            "Nominal": "1",
            "Value": "56,7684"
        }
    ]
}
```



### Save to database

**url**

`server:port/api/save`

**method**

`post`

**required authorization**

`true`

**JSON запрос **

```json
{
    "name": "Australian Dollar",
    "date": [
        "05/11/2020",
        "02/11/2020"
    ],
    "price": [
        1.1,
        2.2
    ]
}
```

**JSON ответ**

```json
{
    "message": "Saved"
}
```

