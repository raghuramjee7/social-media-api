FROM python:3.9.7

# optional, it tells docker where the commands are run from
WORKDIR /usr/src/app 

# copy the requirements.txt file to the working directory
COPY requirements.txt ./

# install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the files to the working directory
COPY . .

# run the command to start the app
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

