# Wikimedia Enterprise SDK: GO

Official Wikimedia Enterprise SDK for Go programming language.

See our [api documentation](https://enterprise.wikimedia.com/docs/) and [website](https://enterprise.wikimedia.com/) for more information about the APIs.

## Getting started

- installing the SDK:

```bash
go get github.com/wikimedia-enterprise/wme-sdk-go
```

- expose your credentials (if you don't have credentials already, [sign up](https://dashboard.enterprise.wikimedia.com/signup/)):

```bash
export WME_USERNAME="...your username...";
export WME_PASSWORD="...your password...";
```

- obtain your access token:

```go
package main

import (
	"context"
	"log"
	"os"

	"github.com/wikimedia-enterprise/wme-sdk-go/pkg/auth"
)

func main() {
	ctx := context.Background()
	ath := auth.NewClient()

	lgn, err := ath.Login(ctx, &auth.LoginRequest{
		Username: os.Getenv("WME_USERNAME"),
		Password: os.Getenv("WME_PASSWORD"),
	})

	if err != nil {
		log.Fatalln(err)
	}

	log.Println(lgn.AccessToken)
}
```
Auth APIs
The following are the main authentication APIs provided by the SDK:

Login
RefreshToken
RevokeToken
Helper APIs
These helper APIs provide reference implementations for clients on how token state management can be done and how tokens can be used in concurrent processes using WME APIs:

GetAccessToken
ClearState
Example Usage

- putting it all together and making your first API call (we will be querying the Structured Contents endpoint, which is part of the [On-demand API](https://enterprise.wikimedia.com/docs/on-demand/))

```go
package main

import (
	"context"
	"log"
	"os"

	"github.com/wikimedia-enterprise/wme-sdk-go/pkg/api"
	"github.com/wikimedia-enterprise/wme-sdk-go/pkg/auth"
)

func main() {
	ctx := context.Background()
	ath := auth.NewClient()

	lgn, err := ath.Login(ctx, &auth.LoginRequest{
		Username: os.Getenv("WME_USERNAME"),
		Password: os.Getenv("WME_PASSWORD"),
	})

	if err != nil {
		log.Fatalln(err)
	}

	defer func() {
		req := &auth.RevokeTokenRequest{
			RefreshToken: lgn.RefreshToken,
		}

		if err := ath.RevokeToken(ctx, req); err != nil {
			log.Println(err)
		}
	}()

	acl := api.NewClient()
	acl.SetAccessToken(lgn.AccessToken)

	req := &api.Request{
		Fields: []string{"name", "abstract"},
		Filters: []*api.Filter{
			{
				Field: "in_language.identifier",
				Value: "en",
			},
		},
	}
	scs, err := acl.GetStructuredContents(ctx, "Squirrel", req)

	if err != nil {
		log.Fatalln(err)
	}

	for _, sct := range scs {
		log.Println(sct.Name)
		log.Println(sct.Abstract)
	}
}

```

- additional examples, such as connecting to the [streaming API](/example/streaming/), can be found [here](/example/)
