from puanchen import HeraldMQ
import json

rmq_param = ()
rmq_con = HeraldMQ(
    "159.138.82.57", "15672", "perfee-dev", 'pfadmin-dev', "7M9Yrym4L9G6cxhNe9Xf")


def send_message_to_queue(queue_name, msg, is_delay=False, ttl=0):
    retry_times = 0
    try:
        retry_times += 1
        if is_delay:
            rmq_con.send_delay_message(queue_name, json.dumps(msg))
        elif ttl:
            rmq_con.send_ttl_message(
                queue_name, json.dumps(msg), str(ttl))
        else:
            rmq_con.send_message(queue_name, json.dumps(msg))
    except Exception as exc:
        print(exc)


if __name__ == "__main__":
    queue_name = "delay-36-hour-dev"
    msg = {"xiao": 12}
    send_message_to_queue(queue_name, msg, is_delay=False, ttl=40000)