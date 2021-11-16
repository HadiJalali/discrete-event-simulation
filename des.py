class event:
    def __init__(self, time, _type):
        self.time = time
        self.type = _type


future_events = []
event_type_A = 1
event_type_D = 2
server_is_busy = 1
server_is_idle = 0

events_duration = [2.0, 0.7, 0.2, 1.1, 3.7, 0.6]
incoming_times = [0.4, 1.2, 0.5, 1.7, 0.2, 1.6, 0.2, 1.4, 1.9]

number_serviced = 0
total_delay = 0
area_under_Q = 0
area_under_B = 0
clock_sim = 0
server_status = 0
number_in_queue = 0
time_last_event = 0
arrival_time = []
total_busy_time = 0


def initialization():
    future_events.append(event(incoming_times.pop(0), event_type_A))


def execute_task(current_event):
    global number_serviced
    global server_status
    global number_in_queue
    global total_delay
    global area_under_Q
    global total_busy_time
    server_status = server_is_busy
    number_serviced += 1
    if arrival_time:
        area_under_Q += len(arrival_time) * (clock_sim - time_last_event)
        arrived = arrival_time.pop(0)
        total_delay += clock_sim - arrived
    if events_duration:
        event_duration = events_duration.pop(0)
        total_busy_time += event_duration
        task_time = clock_sim + event_duration
        future_events.append(event(task_time, event_type_D))
    number_in_queue -= 1


def handel_type_D(current_event):
    global server_status
    global time_last_event
    global area_under_B
    if number_in_queue > 0:
        execute_task(current_event)
    else:
        server_status = server_is_idle
    area_under_B += clock_sim - time_last_event
    time_last_event = clock_sim


def handel_type_A(current_event):
    global total_delay
    global number_in_queue
    global time_last_event
    global area_under_B
    global area_under_Q
    number_in_queue += 1
    if number_in_queue > 1:
        area_under_Q += len(arrival_time) * (clock_sim - time_last_event)
    if server_status == server_is_idle:
        execute_task(current_event)
    else:
        area_under_B += clock_sim - time_last_event
        arrival_time.append(clock_sim)
    if incoming_times:
        arrival = clock_sim + incoming_times.pop(0)
        future_events.append(event(arrival, event_type_A))
    time_last_event = clock_sim


def generate_report():
    rho = round(round(area_under_B, 2) / round(time_last_event, 2), 2)
    Lq = round(round(area_under_Q, 2) / round(time_last_event, 2), 2)
    Wq = round(total_delay/number_serviced, 2)
    Es = round(total_busy_time/number_serviced, 2)

    print(f'Wq = {Wq}')
    print(f'Lq = {Lq}')
    print(f'rho = {rho}')
    print(f'L = {Lq + rho}')
    print(f'E(S) = {Es}')
    print(f'W = {Es + Wq}')


def print_snapshots(counter):
    print(f"======={counter}========")
    print(f'area under Q = {area_under_Q}')
    print(f'area under B = {area_under_B}')
    print(f'last event time = {time_last_event}')
    print(f'clock = {clock_sim}')
    print(f'number served = {number_serviced}')
    print(f'server status = {server_status}')
    print(f'time of arrivals = {arrival_time}')


def main(debug=0):
    global clock_sim
    initialization()
    counter = 1
    while(number_serviced <= 6):
        if debug:
            print_snapshots(counter)
        task_to_run_index = future_events.index(
            min(future_events, key=lambda x: x.time))
        current_event = future_events.pop(task_to_run_index)
        clock_sim = current_event.time
        if number_serviced == 6:
            break
        if current_event.type == event_type_A:
            handel_type_A(current_event)
        else:
            handel_type_D(current_event)
        counter += 1
    generate_report()


if __name__ == '__main__':
    main()
