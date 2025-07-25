# Reflex Knowledge Base

## Core Concepts

*   **State Management:** `rx.State` is the central hub for application data. Changes to `@rx.var`s automatically update the UI.
*   **UI Components:** Reflex provides a rich library of components (`rx.button`, `rx.text`, etc.) for building user interfaces.
*   **Event Handling:** Events like `on_click` trigger methods in the `State` class to update the application's state.

## Configuration (`rxconfig.py`)

*   **Logging:** To enable detailed logging for debugging, set the `loglevel` in `rx.Config`.
    *   **Correct Usage:** `loglevel=rx.constants.LogLevel.DEBUG`
    *   **Incorrect Usage:** `loglevel="debug"` (This will cause a `TypeError`).

## JavaScript Integration

*   **`rx.script`:** Use `rx.script(src="/path/to/script.js")` to include custom JavaScript files.
    *   **Best Practice:** Place `rx.script` in `rx.App(head_components=[...])` for global scripts.
*   **`rx.call_script`:**  A safe way to call JavaScript functions from Python event handlers.
    *   **Critical:** Avoid calling `rx.call_script` within the same event handler that modifies the state. This can cause race conditions with React's rendering cycle.
    *   **Solution:** Separate state-modifying logic and `rx.call_script` calls into different event handlers. Chain them in the `on_click` event using a list: `on_click=[State.modifier, State.caller]`
*   **API Calls from JS:** When using `fetch` in custom JavaScript to call a backend API route:
    *   **Critical:** Use an **absolute URL** including the backend port (default: `http://localhost:8000`).
    *   **Example:** `fetch('http://localhost:8000/api/my_endpoint', ...)`
    *   **Reason:** A relative path (`/api/my_endpoint`) will be sent to the frontend dev server (port 3000), not the backend, resulting in a `405 Method Not Allowed` error.

## Error Patterns & Solutions

*   **`405 Method Not Allowed` in browser console:**
    *   **Cause:** A `fetch` request from custom JavaScript is likely using a relative path and hitting the frontend dev server instead of the backend API.
    *   **Solution:** Change the `fetch` URL to an absolute path pointing to the backend (e.g., `http://localhost:8000/...`).

*   **`TypeError: Cannot read properties of null (reading 'useEffect')`:**
    *   **Cause:** Often indicates a problem with the React component lifecycle, potentially triggered by improper use of `rx.call_script` during the render cycle.
    *   **Solution:** Ensure `rx.call_script` is only called from event handlers and not directly within a state-modifying method that is part of the render path.

*   **`TypeError: App.add_page() got an unexpected keyword argument 'head_components'`:**
    *   **Cause:** `head_components` is an argument for the `rx.App` constructor, not for the `app.add_page` method.
    *   **Solution:** Move `head_components` to the `rx.App` initialization: `app = rx.App(head_components=[...])`.

*   **`TypeError: log_level must be a LogLevel enum value`:**
    *   **Cause:** Passing a string (e.g., `"debug"`) to the `loglevel` config.
    *   **Solution:** Use the `rx.constants.LogLevel` enum: `loglevel=rx.constants.LogLevel.DEBUG`.
