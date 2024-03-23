# MLOps_pipeline

## Obtaining the necessary data to work with Telegram API

Step 1: Go to the Telegram developer tools section by clicking [here](https://my.telegram.org/auth?to=apps).

Step 2: Log in and click on the API Development Tools section.

Step 3: A form will open in which you need to fill in the empty fields (only "App title" and "Short name" are important to fill).

Step 4: After clicking Create application, a page will be displayed showing various data. You need to copy the api_id and api_hash parameters to a safe place, they will be needed for Telegram API.

## Working with the script

Step 1: Enter the obtained api_id and api_hash from the previous step in the tg_info.txt file in the appropriate places.

Step 2: Run the script, which will automatically connect to your account and give you access to the basic functionality of the script.

Step 3: Enter the id of the Telegram channel you are interested in and the number of recent posts for which you want to see information.

Step 4: Authenticate to your Telegram account via the console.

Step 5: Profit!

## Databases

Small database without media:

*[click](https://drive.google.com/file/d/1WYET6NpK6wSeQvCmuX7Nzcf2Gq2beCUG/view?usp=sharing)*

Large database + data with media:

*[click](https://drive.google.com/file/d/15iBSPtaUY58O7QHwxkqJKyGlLENR2OPq/view?usp=sharing)*

## How to launch the project

Step 1: Open the terminal.

Step 2: Enter the following code into the terminal to run the project.
```bash
./run.sh
```

Step 3: Enter the following code into the terminal to stop the project.
```bash
./stop.sh
```
