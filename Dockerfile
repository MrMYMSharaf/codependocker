FROM python:3.12.7-slim

WORKDIR /code 

COPY  ./requirement.txt ./

RUN pip install --no-cache-dir -r requirement.txt

COPY ./src ./src
COPY ./static ./static

# Create the Streamlit configuration directory
RUN mkdir -p ~/.streamlit

# Copy the Streamlit config
COPY .streamlit/config.toml ~/.streamlit/config.toml

# Expose the default Streamlit port
EXPOSE 8080

CMD [ "streamlit","run","src/app.py"]
