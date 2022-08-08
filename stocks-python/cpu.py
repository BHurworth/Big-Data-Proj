import psutil
import datetime
import os
import socket
import json

#https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-capture-python

# These packages are needed to run this code
# pip install azure-eventhub
# pip install psutil

from azure.eventhub import EventHubProducerClient, EventData

event_hub_connection_string = 'Endpoint=sb://cloudd.servicebus.windows.net/;SharedAccessKeyName=policyname;SharedAccessKey=QmuQ6ViCAZaT71DiSTodWvpVTLE1WoQ6VtR9ZQoXWJg='
event_hub_name = 'pythonfeeddata'


# Create a producer client to produce and publish events to the event hub.

producer = EventHubProducerClient.from_connection_string(conn_str=event_hub_connection_string, eventhub_name=event_hub_name)

hostname = socket.gethostname()
try:
    while True:
        event_data_batch = producer.create_batch() # Create a batch. You will add events to the batch later. 
        cpu_percent = psutil.cpu_percent(2)
        mem_usage = psutil.virtual_memory()[2]
        reading = {'hostname': hostname, 'timestamp': str((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")), 'cpu_usage': cpu_percent, 'mem_usage': mem_usage}

        s = json.dumps(reading) # Convert the reading into a JSON string.
        print(s)
        event_data_batch.add(EventData(s)) # Add event data to the batch.
        producer.send_batch(event_data_batch)

except KeyboardInterrupt:
    #pass
    producer.close()