import os
import asyncio
import json

# Ensure the mock raspi URL is used
os.environ.setdefault('RASPI_API_URL', 'http://127.0.0.1:5000')

from api.routes.actuator import set_actuator_state, get_actuator_status, ActuatorCommand

async def main():
    print('Sending ON command to actuator...')
    resp = await set_actuator_state(ActuatorCommand(state='ON'))
    print('Response:', resp.json())

    print('Querying status...')
    status = await get_actuator_status()
    print('Status:', status.json())

    print('Sending OFF command to actuator...')
    resp2 = await set_actuator_state(ActuatorCommand(state='OFF'))
    print('Response:', resp2.json())

if __name__ == '__main__':
    asyncio.run(main())
