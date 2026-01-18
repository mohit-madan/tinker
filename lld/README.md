# LLD Functions Index

## api.py
- `health_check()` - Health check endpoint
- `get_user(user_id)` - Get user by ID
- `create_user(user)` - Create new user
- `UserCreate` - Request model

## cache.py
- `TTLCache` - Thread-safe TTL cache with LRU eviction
  - `set(tenant_id, model, prompt, value, ttl_seconds)`
  - `get(key)`
  - `delete(tenant_id, model, prompt)`

## cursor.py
- Pseudocode for cursor planning logic

## logger.py
- `Logger` - Singleton logger with chain of responsibility
- `LogLevel` - Enum (DEBUG, INFO, WARN, ERROR, FATAL)
- `LogMessage` - Log message model
- `LogFormatter` - Base formatter (PlainTextFormatter, JsonFormatter)
- `LogAppender` - Base appender (ConsoleAppender, FileAppender)
- `LogHandler` - Base handler (InfoHandler, WarnHandler, ErrorHandler)
- `LogHandlerConfiguration` - Configuration builder

## lru.py
- `LRUCache` - LRU cache implementation
  - `get(key)`
  - `put(key, value)`

## tictactoe.py
- `TicTacToe` - Tic-tac-toe game with O(1) win detection
  - `make_move(row, col, player)`
- `Player` - Player model
- `Symbol` - Enum (X, O, EMPTY)
