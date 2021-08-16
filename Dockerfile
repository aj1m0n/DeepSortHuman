FROM aj1m0n/deep_sort:latest

VOLUME ./:/DeepSortHuman

WORKDIR /DeepSortHuman/src/deep-sort-yolov4/

RUN pip3 install pika

RUN pip3 install pytz

CMD  ["bash", "./run.sh"]
