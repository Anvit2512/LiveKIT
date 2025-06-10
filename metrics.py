# metrics.py

import pandas as pd
import time
from datetime import datetime
import threading

class MetricsLogger:
    def __init__(self):
        self._lock = threading.Lock()
        self.entries = []
        self.call_start_time = time.time()

    def log_turn(self, stt_latency, ttft, ttfb, total_turn_latency, user_utterance, agent_response, llm_input_tokens, llm_output_tokens, tts_characters):
        """Logs all metrics for a single conversation turn."""
        with self._lock:
            self.entries.append({
                "User Utterance": user_utterance,
                "Agent Response": agent_response,
                "STT Latency (s)": round(stt_latency, 3),
                "LLM TTFT (s)": round(ttft, 3),
                "TTS TTFB (EOU Delay) (s)": round(ttfb, 3),
                "Total Turn Latency (s)": round(total_turn_latency, 3),
                "LLM Input Tokens": llm_input_tokens,
                "LLM Output Tokens": llm_output_tokens,
                "TTS Characters": tts_characters,
            })
        print(f"METRICS: TTFT: {ttft:.3f}s, TTFB: {ttfb:.3f}s, Total Latency: {total_turn_latency:.3f}s")


    def save_to_excel(self):
        """Calculates summary and saves all logged data to a timestamped Excel file."""
        if not self.entries:
            print("No metrics to save.")
            return

        with self._lock:
            df = pd.DataFrame(self.entries)
            
            # Calculate Usage Summary
            total_call_duration = time.time() - self.call_start_time
            total_input_tokens = df["LLM Input Tokens"].sum()
            total_output_tokens = df["LLM Output Tokens"].sum()
            total_tts_chars = df["TTS Characters"].sum()
            
            # Calculate Performance Summary
            summary_data = {
                "User Utterance": "--- SUMMARY ---",
                "STT Latency (s)": df["STT Latency (s)"].mean(),
                "LLM TTFT (s)": df["LLM TTFT (s)"].mean(),
                "TTS TTFB (EOU Delay) (s)": df["TTS TTFB (EOU Delay) (s)"].mean(),
                "Total Turn Latency (s)": df["Total Turn Latency (s)"].mean(),
                "LLM Input Tokens": f"TOTAL: {total_input_tokens}",
                "LLM Output Tokens": f"TOTAL: {total_output_tokens}",
                "TTS Characters": f"TOTAL: {total_tts_chars}",
                "Agent Response": f"Call Duration: {total_call_duration:.2f}s",
            }

            # Convert summary dictionary to DataFrame and append
            summary_df = pd.DataFrame([summary_data])
            df = pd.concat([df, summary_df], ignore_index=True)

            # Generate filename and save
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"agent_session_metrics_{timestamp}.xlsx"
            
            df.to_excel(filename, index=False, engine='openpyxl')
            print(f"Metrics successfully saved to {filename}")