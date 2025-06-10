# # agent.py

# import asyncio
# import time
# import os

# from livekit.agents import stt, tts, llm, Agent, JobContext
# from livekit.agents.utils import AudioBuffer
# # THIS IS THE CORRECTED LINE:
# from livekit.plugins import deepgram, elevenlabs, openai

# from metrics import MetricsLogger

# # Use Groq as the LLM via its OpenAI-compatible API
# groq_llm = openai.LLM(
#     base_url="https://api.groq.com/openai/v1",
#     api_key=os.environ["GROQ_API_KEY"],
# )

# class VoiceAgent(Agent):
#     def __init__(self):
#         super().__init__()
#         self.metrics_logger = MetricsLogger()
#         self.chat_history = [
#             {"role": "system", "content": "You are a friendly voice assistant. Keep your responses concise and conversational."}
#         ]
        
#         # Initialize clients for STT and TTS
#         self.stt_client = deepgram.STT()
#         self.tts_client = elevenlabs.TTS()

#     async def start(self):
#         """
#         This method is called when a new agent job is started.
#         It sets up the streams and the main processing loop.
#         """
#         # Allow the agent to be interrupted by the user
#         self.ctx.job.set_interruptible(True)

#         # Create the STT stream
#         stt_stream = self.stt_client.stream()

#         # Task to forward audio from the room to the STT stream
#         self.ctx.create_task(self.forward_audio_to_stt(stt_stream))

#         # Main loop to process STT results
#         async for stt_event in stt_stream:
#             if stt_event.type == stt.SpeechEventType.FINAL_TRANSCRIPT:
#                 # We have a final transcript, process the user's turn
#                 # This is done in a separate task to allow the main loop to
#                 # immediately listen for the next STT event, enabling interruptions.
#                 self.ctx.create_task(self.process_user_turn(stt_event))
        
#         # This is a hook that is called when the agent job is shutting down
#         self.on_shutdown(self.metrics_logger.save_to_excel)

#     async def forward_audio_to_stt(self, stt_stream):
#         """
#         Forwards audio from the participant's track to the STT stream.
#         """
#         async for audio_frame_event in self.ctx.audio_in:
#             stt_stream.push_frame(audio_frame_event.frame)

#     async def process_user_turn(self, stt_event: stt.SpeechEvent):
#         """
#         Processes a single turn of the conversation:
#         1. Captures user text and timing.
#         2. Sends text to LLM.
#         3. Streams LLM response to TTS.
#         4. Sends synthesized audio back to the user.
#         5. Logs all metrics for the turn.
#         """
#         user_utterance = stt_event.alternatives[0].text
#         if not user_utterance.strip():
#             return

#         print(f"User: {user_utterance}")
        
#         # Timestamps for metrics
#         eou_time = time.time()  # End of user utterance (approximated by final STT result)
#         stt_latency = eou_time - stt_event.end_of_speech_ts / 1_000_000_000

#         self.chat_history.append({"role": "user", "content": user_utterance})

#         # Create LLM and TTS streams for this turn
#         llm_stream = groq_llm.chat(messages=self.chat_history)
#         tts_stream = self.tts_client.stream()
        
#         # Task to send synthesized audio from TTS to the participant
#         send_audio_task = self.ctx.create_task(self.send_audio_from_tts(tts_stream))

#         # Pipe the LLM response to the TTS stream and collect metrics
#         agent_response = ""
#         llm_first_token_time = None
        
#         async for chunk in llm_stream:
#             if llm_first_token_time is None:
#                 llm_first_token_time = time.time()
            
#             text_chunk = chunk.choices[0].delta.content
#             if text_chunk:
#                 agent_response += text_chunk
#                 tts_stream.push_text(text_chunk)
        
#         # All LLM tokens received, flush the TTS stream to finalize audio
#         tts_stream.flush()

#         # Wait for the audio to be fully sent
#         tts_first_byte_time = await send_audio_task
#         turn_end_time = time.time()
        
#         print(f"Agent: {agent_response}")
#         self.chat_history.append({"role": "assistant", "content": agent_response})

#         # Calculate final metrics for this turn
#         ttft = llm_first_token_time - eou_time if llm_first_token_time else 0
#         ttfb = tts_first_byte_time - eou_time
#         total_turn_latency = turn_end_time - eou_time

#         self.metrics_logger.log_turn(
#             stt_latency=stt_latency,
#             ttft=ttft,
#             ttfb=ttfb,
#             total_turn_latency=total_turn_latency,
#             user_utterance=user_utterance,
#             agent_response=agent_response,
#             llm_input_tokens=llm_stream.usage.prompt_tokens,
#             llm_output_tokens=llm_stream.usage.completion_tokens,
#             tts_characters=len(agent_response)
#         )
#     async def send_audio_from_tts(self, tts_stream: tts.TTS.Stream) -> float| None:
#         """
#         Consumes the TTS stream and sends audio chunks to the participant.
#         Returns the timestamp of the first audio byte received.
#         """
#         tts_first_byte_time = None
#         async for audio_chunk in tts_stream:
#             if tts_first_byte_time is None:
#                 tts_first_byte_time = time.time()

#             # The audio output stream is automatically cleared when the agent is interrupted
#             self.ctx.audio_out.send(audio_chunk.frame)
        
#         return tts_first_byte_time if tts_first_byte_time is not None else time.time()



# agent.py (Final Corrected Version)

# agent.py (Final, Corrected Version)

import asyncio
import time
import os

from livekit.agents import stt, tts, llm, Agent, JobContext
from livekit.plugins import deepgram, elevenlabs, openai
from metrics import MetricsLogger

# Use Groq as the LLM via its OpenAI-compatible API
groq_llm = openai.LLM(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)

# class VoiceAgent(Agent):
#     def __init__(self):
#         super().__init__()
#         self.metrics_logger = MetricsLogger()
#         self.chat_history = [
#             {"role": "system", "content": "You are a friendly voice assistant. Keep your responses concise and conversational."}
#         ]
        
#         # Initialize clients for STT and TTS
#         self.stt_client = deepgram.STT()
#         self.tts_client = elevenlabs.TTS()

class VoiceAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are a friendly voice assistant. Keep your responses concise and conversational.")
        
        self.metrics_logger = MetricsLogger()
        self.chat_history = [
            {"role": "system", "content": "You are a friendly voice assistant. Keep your responses concise and conversational."}
        ]

        self.stt_client = deepgram.STT()
        self.tts_client = elevenlabs.TTS()
    import asyncio  # Ensure this is at the top of your file

    async def start(self, ctx):

        self.ctx = ctx
        await self.ctx.connect()
        stt_stream = self.stt_client.stream()
        asyncio.create_task(self.forward_audio_to_stt(stt_stream))
        async for stt_event in stt_stream:
            if stt_event.type == stt.SpeechEventType.FINAL_TRANSCRIPT:
                asyncio.create_task(self.process_user_turn(stt_event))

        self.on_shutdown(self.metrics_logger.save_to_excel)


    # --- FIX #1 HERE: Correct type is stt.STT.stream (lowercase 's') ---
    async def forward_audio_to_stt(self, stt_stream: stt.STT.stream):
        """
        Forwards audio from the participant's track to the STT stream.
        """
        async for audio_frame_event in self.ctx.audio_in:
            stt_stream.push_frame(audio_frame_event.frame)

    async def process_user_turn(self, stt_event: stt.SpeechEvent):
        """
        Processes a single turn of the conversation.
        """
        user_utterance = stt_event.alternatives[0].text
        if not user_utterance.strip():
            return

        print(f"User: {user_utterance}")
        
        eou_time = time.time()
        stt_latency = eou_time - stt_event.end_of_speech_ts / 1_000_000_000

        self.chat_history.append({"role": "user", "content": user_utterance})

        llm_stream = groq_llm.chat(messages=self.chat_history)
        tts_stream = self.tts_client.stream()
        
        send_audio_task = self.ctx.create_task(self.send_audio_from_tts(tts_stream))

        agent_response = ""
        llm_first_token_time = None
        
        async for chunk in llm_stream:
            if llm_first_token_time is None:
                llm_first_token_time = time.time()
            
            text_chunk = chunk.choices[0].delta.content
            if text_chunk:
                agent_response += text_chunk
                tts_stream.push_text(text_chunk)
        
        tts_stream.flush()

        tts_first_byte_time = await send_audio_task
        turn_end_time = time.time()
        
        print(f"Agent: {agent_response}")
        self.chat_history.append({"role": "assistant", "content": agent_response})

        ttft = llm_first_token_time - eou_time if llm_first_token_time else 0
        ttfb = tts_first_byte_time - eou_time if tts_first_byte_time is not None else 0
        total_turn_latency = turn_end_time - eou_time

        self.metrics_logger.log_turn(
            stt_latency=stt_latency,
            ttft=ttft,
            ttfb=ttfb,
            total_turn_latency=total_turn_latency,
            user_utterance=user_utterance,
            agent_response=agent_response,
            llm_input_tokens=llm_stream.usage.prompt_tokens,
            llm_output_tokens=llm_stream.usage.completion_tokens,
            tts_characters=len(agent_response)
        )

    # --- FIX #2 HERE: Correct type is tts.TTS.stream (lowercase 's') ---
    async def send_audio_from_tts(self, tts_stream: tts.TTS.stream) -> float | None:
        """
        Consumes the TTS stream and sends audio chunks to the participant.
        Returns the timestamp of the first audio byte received.
        """
        tts_first_byte_time = None
        try:
            async for audio_chunk in tts_stream:
                if tts_first_byte_time is None:
                    tts_first_byte_time = time.time()
                self.ctx.audio_out.send(audio_chunk.frame)
        except asyncio.CancelledError:
            pass
        
        return tts_first_byte_time