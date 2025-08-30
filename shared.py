# import threading

# # Shared state variables
# unit_test_response_global = ""
# unit_test_event = threading.Event()  # Event to signal when the response is ready

# # Function to set the unit test response
# def set_unit_test_response(response):
#     global unit_test_response_global
#     unit_test_response_global = response
#     print("Unit test response set.")
#     print("Generated unit test cases: ", unit_test_response_global)
#     unit_test_event.set()  # Signal that the response is ready

# def get_unit_test_response():
#     print("Waiting for event to be set...")
#     unit_test_event.wait()  # Wait until the response is ready
#     print("Event set, returning response.")
#     return unit_test_response_global

import asyncio

# Shared state variables
unit_test_response_global = ""
unit_test_event = asyncio.Event()  # Event to signal when the response is ready

# Function to set the unit test response
async def set_unit_test_response(response):
    global unit_test_response_global
    unit_test_response_global = response
    print("Unit test response set.")
    print("Generated unit test cases: ", unit_test_response_global)
    unit_test_event.set()  # Signal that the response is ready

async def get_unit_test_response():
    print("Waiting for event to be set...")
    await unit_test_event.wait()  # Wait until the response is ready
    print("Event set, returning response.")
    return unit_test_response_global

