docker build -t streamlit-bocapp . 
docker run --name streamlit-container -p 8501:8501 -d -v ${pwd}:/code streamlit-Bocapp

docker run --env-file .env -p 8501:8501 streamlitboc-app
