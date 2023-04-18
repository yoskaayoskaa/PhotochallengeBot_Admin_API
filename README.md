# PhotochallengeBot Admin API

### A small API for [Telegram chatbot](https://github.com/yoskaayoskaa/PhotochallengeBot)

API contains three endpoints:
* POST /admin.login - Admin authentication via password & email
* GET /admin.current - show info about current admin if authenticated (id & email)
* POST /game.whole_game - get the current Game information by chat id (bot state, current round, players info, game accounts)
