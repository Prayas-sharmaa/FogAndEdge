import asyncio
from temperature_sensor import TemperatureSensor
from ph_sensor import PHSensor
from oxygen_sensor import OxygenSensor

async def main():
    print("Initializing Smart Aquaculture Sensor Network...")
    
    # Instantiate all 3 sensor types
    sensors = [
        TemperatureSensor("temp_p1", "pond_1", "farm/pond_1/temp", frequency_sec=2.0, base_temp=20.0),
        PHSensor("ph_p1", "pond_1", "farm/pond_1/ph", frequency_sec=3.0, base_ph=7.2),
        OxygenSensor("do_p1", "pond_1", "farm/pond_1/oxygen", frequency_sec=4.0, base_do=8.5)
    ]

    print(f"Starting {len(sensors)} sensors concurrently. Press Ctrl+C to stop.\n" + "-"*50)
    
    # Run all sensor coroutines simultaneously using asyncio.gather
    tasks = [sensor.run() for sensor in sensors]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSimulation stopped by user. Shutting down sensors.")