FROM aj1m0n/deep_sort:latest

WORKDIR /workspace

RUN pip3 install pika

CMD  ["bash", "/workspace/Deep_Sort/run.sh"]