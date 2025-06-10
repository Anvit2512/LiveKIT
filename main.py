# # main.py

# import asyncio
# import logging
# import os
# from dotenv import load_dotenv
# # Load environment variables from .env file
# load_dotenv()
# from livekit.agents import JobRequest, Worker
# from agent import VoiceAgent


# async def main():
#     """
#     Main function to start the agent worker.
#     """
#     logging.basicConfig(level=logging.INFO)

#     # Check for required environment variables
#     required_env_vars = ["LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]
#     for var in required_env_vars:
#         if var not in os.environ:
#             logging.error(f"Missing required environment variable: {var}")
#             return

#     async def job_request_cb(job: JobRequest):
#         logging.info("Accepting job %s", job.id)
        
#         # Create an instance of our agent
#         agent = VoiceAgent()
        
#         # Start the agent
#         await agent.start(job.context)

#     # Create and run the worker
#     worker = Worker(
#         request_handler=job_request_cb,
#         worker_type="tk_agent_worker_type" # A unique name for your worker type
#     )
#     logging.info("Agent worker started.")
#     await worker.run()

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("\nShutting down gracefully.")


import asyncio
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from livekit.agents import JobRequest, Worker, WorkerOptions
from agent import VoiceAgent

async def main():
    """
    Main function to start the agent worker.
    """
    logging.basicConfig(level=logging.INFO)

    # async def job_request_cb(job: JobRequest):
    #     logging.info("Accepting job %s", job.id)
    #     agent = VoiceAgent()
    #     await agent.start(job.context)

    async def job_request_cb(ctx):
        logging.info("Accepting new job...")

        agent = VoiceAgent()
        await agent.start(ctx)


    # ✅ Correct usage: Pass callback as the first positional argument
    options = WorkerOptions(
        job_request_cb,  # <-- This is required now
        ws_url=os.environ.get("LIVEKIT_URL"),
        api_key=os.environ.get("LIVEKIT_API_KEY"),
        api_secret=os.environ.get("LIVEKIT_API_SECRET"),
    )

    worker = Worker(options)

    logging.info("Agent worker started.")
    await worker.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down gracefully.")
