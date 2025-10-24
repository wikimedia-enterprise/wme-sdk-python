# Authentication API examples
Used for managing access token and changing password. Refer to the documentation [here](https://enterprise.wikimedia.com/docs/authentication/).

## Running the Application

To run the application, use the following command from the project's root:

```sh
python -m example.login.login
```

## Login example
Get access token and refresh token by sending in username and password.


```bash
POST https://auth.enterprise.wikimedia.com/v1/login
```
with request parameter:
```json
{
    "username" : "usernamexyz",
    "password": "passwordxyz"
}
```

Response:
```json
{
    "id_token": "abc....",
    "access_token": "abc...",
    "refresh_token": "abc..",
    "expires_in": 86400
}
```

The access token is required to use any of our data and metadata APIs. An access token is valid for 24 hours. You may generate a fresh access token using refresh token.

Note: For Realtime Streaming API, the connection is long-lived. Once connected to the API, you will not be disconnected because the `access_token` expires after 24 hours. Your connection will stay alive.


## Token refresh example
Get new access token by sending in username and refresh_token.
A valid user can have up to 90 access tokens at any time.

```bash
POST https://auth.enterprise.wikimedia.com/v1/token-refresh
```
with request parameter:
```json
{
    "username" : "usernamexyz",
    "refresh_token": "abc.."
}
```

Response:
```json
{
    "id_token": "xyz..",
    "access_token": "xyz...",
    "expires_in": 86400
}
```


## Token revoke example
Invalidates all the access tokens for a user, by sending in refresh_token.

```bash
POST https://auth.enterprise.wikimedia.com/v1/token-revoke
```
with request parameter:
```json
{
    "refresh_token": "abc.."
}
```

## Forgot password example
Allows you to set a new password by sending in a code to your associated email.

```bash
POST https://auth.enterprise.wikimedia.com/v1/forgot-password
```
with request parameter:
```json
{
    "username": "abc.."
}
```

Send in the confirmation_code and new password as follows:

```bash
POST https://auth.enterprise.wikimedia.com/v1/forgot-password-confirm
```
with request parameter:
```json
{
    "username": "abc..",
	"password": "new_password",
	"confirmation_code" : "123456"
}
```

## Change password example
When you haven't forgotten your current password, but want to update it.

```bash
POST https://auth.enterprise.wikimedia.com/v1/change-password
```
with request parameter:
```json
{
    "access_token": "xyz...",
    "previous_password": "password1",
    "proposed_password": "password2"
}
```
