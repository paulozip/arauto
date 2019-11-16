# Heroku Deploy file
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"youremail@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml