FROM aj1m0n/deep_sort:latest

VOLUME ./:/Deep_Sort

WORKDIR /Deep_Sort/src/deep-sort-yolov4/

RUN pip3 install pika

RUN pip3 install pytz

CMD  ["bash", "./run.sh"]
