To run code:
1) Pull project from github
3) Ensure Docker is installed and working on system
2) Ensure the current folder directory in the shell is where the project is located

Assuming no interfering docker images named pythonimage:
4) Run the following commands in the shell:
docker build -t pythonimage .
docker run -ti pythonimage


For considerations regarding using/storing info such as SSN:
- Use a secure backend database management system i.e. PostgreSQL
- Be careful with data stored client-side i.e. don't log sensitive data to the console
- Fully or partially redact the sensitive data on the client-side, depending on who is using/viewing the data