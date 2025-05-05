from prisma import Prisma

# Create a global client object
client = Prisma()


async def connect_db():
    try:
        await client.connect()
    except Exception as e:
        print(f"❌ Error connecting to DB: {e}")


async def disconnect_db():
    try:
        await client.disconnect()
    except Exception as e:
        print(f"❌ Error disconnecting from DB: {e}")

