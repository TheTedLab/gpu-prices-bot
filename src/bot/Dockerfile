FROM python:3.9
WORKDIR .
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./bot.py ./
COPY ./*.py ./src/bot/
COPY ./images/no_search_results.png ./images/no_search_results.png
COPY ./images/search.png ./images/search.png
COPY ./images/shops_logo.jpg ./images/shops_logo.jpg
CMD ["python", "bot.py"]