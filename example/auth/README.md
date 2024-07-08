# Auth Helper Example

This repository contains an example Go application that demonstrates how to use an authentication helper to manage access and refresh tokens for making authenticated API calls easier. The `main.go` script logs in, checks the validity of tokens, and refreshes the token periodically using a background goroutine.

## Prerequisites

- Go 1.15+ installed on your machine.
- Environment variables for your username and password stored in a `.env` file.

## Setup

### 1. Clone the Repository

```sh
git clone https://github.com/wikimedia-enterprise/wme-sdk-go.git
cd wme-sdk-go
```

### 2. Environment Variables

There is a sample environment file `sample.env` provided in the repository. Rename it to `.env` and add your username and password.

```sh
mv sample.env .env
```

Edit the `.env` file to include your credentials:

```
WME_USERNAME=your_username
WME_PASSWORD=your_password
```

### 3. Install Dependencies

Install the necessary Go dependencies:

```sh
go mod tidy
```

## Running the Application

To run the application, use the following command:

```sh
cd example/auth
go run main.go
```

This will start the application, log in, and display the access token. It will also start a background goroutine that refreshes the token every 23 hours and 59 seconds, or whenever an API call is made.

## Project Structure

- `main.go`: The main application file that logs in and handles token refresh.
- `auth/`: Directory containing the authentication helper code.
  - `auth.go`: Contains the authentication client and helper methods for managing tokens.

## `auth` Package

The `auth` package provides a client and helper for managing authentication tokens. Below are the key components:

### Auth Package Components

- `Client`: HTTP client for making authentication requests.
- `Helper`: Manages the state and validity of tokens.
- `Tokenstore`: Struct for storing token data.
- `LoginRequest`, `LoginResponse`, `RefreshTokenRequest`, `RefreshTokenResponse`, `RevokeTokenRequest`: Structs for making API requests and handling responses.

### Helper Methods

- `GetToken() (string, error)`: Manages the token state and returns a valid access token.
- `loginAndStoreTokens(tokenStoreFile string) (string, error)`: Logs in and stores the tokens.
- `refreshAndStoreTokens(tokenStoreFile string, tokenStore *Tokenstore) (string, error)`: Refreshes the access token and stores the new tokens.
- `storeTokens(tokenStoreFile string, tokenStore *Tokenstore) error`: Writes the token data to the tokenstore file in JSON format.

## Example Usage in `main.go`

```go
package main

import (
	"context"
	"fmt"
	"log"
	"sync"
	"time"

	"github.com/wikimedia-enterprise/wme-sdk-go/pkg/auth"
)

func main() {
	client := auth.NewClient()
	helper, err := auth.NewHelper(client)
	if err != nil {
		log.Fatalf("Failed to create helper: %v", err)
	}

	var mu sync.Mutex
	tokenRefreshChan := make(chan struct{})

	go func() {
		for {
			select {
			case <-tokenRefreshChan:
				continue
			case <-time.After(23*time.Hour + 59*time.Second):
				mu.Lock()
				_, err := helper.GetToken()
				if err != nil {
					log.Printf("Failed to refresh token: %v", err)
				} else {
					log.Println("Token refreshed successfully")
				}
				mu.Unlock()
			}
		}
	}()

	for {
		token, err := helper.GetToken()
		if err != nil {
			log.Fatalf("Failed to get token: %v", err)
		}

		fmt.Printf("Access token: %s\n", token)
		tokenRefreshChan <- struct{}{}
		time.Sleep(10 * time.Minute)
	}
}
```

## Contributing

If you want to contribute to this project, feel free to open issues or submit pull requests.

## License

This project is licensed under the  Apache-2.0 license License. See the LICENSE file for details.

---

Feel free to adjust the repository URL, structure, and any other details to better fit your actual project setup.
