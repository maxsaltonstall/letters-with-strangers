To start:
```sh
source venv/bin/activate
```

You can start monitoring with
```sh
npx pm2 start pm2.json 
# get/stream logs with 
npx pm2 logs
# or, write them to a file with:
npx pm2 logs --log latest.log
# or to stream output to the terminal
npx pm2 start pm2.json --no-daemon
```

Flags that might help:
- `--watch`: automatically restarts on file change
- `--cron [cron job]`: automatically restarts based on cron
- `--silent`: tell pm2 to shut up
- `--max-restarts`: pm2 automatically restarts on error, so here you can set how many times

To stop the program, just do:
```sh
npx pm2 stop lws-bot
```

