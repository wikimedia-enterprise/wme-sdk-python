# Real-Time Stream Callback Demo

This script demonstrates the ability to programmatically stop a real-time stream from within the processing callback.

It connects to the `/v2/articles` real-time stream, processes articles one by one, and automatically stops and disconnects after receiving a predefined number of articles (5, by default).

## Key Features
- Connects to the real-time article stream (`api_client.stream_articles`).

- Implements a custom callback function (`stream_callback`).

- Uses the callback's bool return value to control the stream (returning `False` stops the stream).

- Handles authentication and graceful token revocation using `AuthClient` and `Helper`.

## How it Works
The core logic of this demo is inside the `stream_callback` function. The `api_client`'s internal streaming loop checks the boolean value returned by this callback after every article it processes.

- A list, `articles_received_tracker`, is used as a counter (it's a list so it can be mutated from within the callback).

- The callback receives an `article` (a `dict`) from the stream.

- It logs the article's details and appends it to the tracker.

- It checks the count: `if len(articles_received_tracker) >= STOP_AFTER_N_ARTICLES:`

- If the count is met, it logs a warning and returns `False`.

- If the count is not met, it returns `True`.

A `True` value tells the `api_client` to "keep processing." A `False` value tells the `api_client` to "stop immediately," at which point it closes the stream connection and the `api_client.stream_articles()` function returns.

## Running the Application

To run the application, use the following command from the project's root:

```sh
python -m example.callback.callback
```
