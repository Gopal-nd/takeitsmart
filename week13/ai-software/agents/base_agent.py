import json
import boto3
from app.config import AWS_REGION, MODEL_ID


class BaseAgent:
    def __init__(self, role, system_prompt):
        self.role = role
        self.system_prompt = system_prompt
        self.client = boto3.client("bedrock-runtime", region_name=AWS_REGION)

    def run(self, input_text):
        prompt = f"""
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
You are a professional {self.role}.

STRICT RULES:
- Stay relevant to the user request
- Do NOT switch domain
- No repetition
- Be clear and structured
- If code → clean, minimal, working

{self.system_prompt}
<|eot_id|>

<|start_header_id|>user<|end_header_id|>
{input_text}
<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
"""
        body = {
            "prompt": prompt,
            "max_gen_len": 2048,
            "temperature": 0.2,
            "top_p": 0.9
        }

        response = self.client.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body)
        )

        result = json.loads(response["body"].read())
        return result.get("generation", "").strip()

    def run_stream(self, input_text):
        prompt = f"""
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
You are a professional {self.role}.

STRICT RULES:
- Stay relevant to the user request
- Do NOT switch domain
- No repetition
- Be clear and structured
- If code → clean, minimal, working

{self.system_prompt}
<|eot_id|>

<|start_header_id|>user<|end_header_id|>
{input_text}
<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
"""
        body = {
            "prompt": prompt,
            "max_gen_len": 2048,
            "temperature": 0.2,
            "top_p": 0.9
        }

        try:
            response = self.client.invoke_model_with_response_stream(
                modelId=MODEL_ID,
                body=json.dumps(body)
            )
            for event in response.get("body", []):
                chunk = event.get("chunk")
                if chunk:
                    chunk_data = json.loads(chunk.get("bytes").decode("utf-8"))
                    text = chunk_data.get("generation", "")
                    if text:
                        yield text
        except Exception as e:
            yield f"Error in streaming: {str(e)}"