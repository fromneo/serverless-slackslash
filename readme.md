# Purpose
Respond to slack slash commands with data from a database.

# Local setup
Its best practice to use `venv` or some other virtual environment manager to install the files.

1. If you don't have an AWS account, create one.
2. Create a folder titled `.aws` and create a `config` file. Use this format for the file.
3. Create a .env file. This is only for local testing. On production, you have to paste the environment variables on AWS.
4. Go to Slack and create the slash command. Get the verification token and add it to your `.env` file.

- There are 2 things you need running to test on local only: Postman and Chalice.
- For testing with Slack, you need Ngrok and Chalice. Ngrok receives the requests and forwards them to your server.


# Deploying
Run `chalice deploy` on the command line.
Take note that each deploy clears out the environment variables on AWS.

# Useful Tools
- Ngrok allows you to create a tunnel to a local webserver. This is useful for testing.
- Postman allows you to test HTTP methods.
