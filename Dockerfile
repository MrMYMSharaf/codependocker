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

# Install the spaCy model
RUN python -m spacy download en_core_web_sm 
RUN python -m spacy download en_core_web_lg
 

# Expose the default Streamlit port
EXPOSE 8501

CMD [ "streamlit","run","src/app.py"]