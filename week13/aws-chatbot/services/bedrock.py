import boto3
import json
from app.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, MODEL_ID

class BedrockChatbot:
    def __init__(self, aws_access_key=None, aws_secret_key=None, region=None):
        self.aws_access_key = aws_access_key or AWS_ACCESS_KEY_ID
        self.aws_secret_key = aws_secret_key or AWS_SECRET_ACCESS_KEY
        self.region = region or AWS_REGION
        self.client = self._connect()

    def _connect(self):
        try:
            session = boto3.Session(
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.region
            )
            return session.client("bedrock-runtime")
        except Exception as e:
            raise Exception(f"Failed to connect to AWS Bedrock: {e}")

    def invoke(self, user_input):
        if not self.client:
            raise Exception("Bedrock client is not connected.")

        prompt = f"<|user|>\n{user_input}\n<|assistant|>\n"
        body = {
            "prompt": prompt,
            "temperature": 0.5,
            "top_p": 0.8,
            "max_gen_len": 300
        }

        try:
            response = self.client.invoke_model(
                modelId=MODEL_ID,
                body=json.dumps(body),
                contentType="application/json",
                accept="application/json"
            )

            response_body = json.loads(response["body"].read())
            output_text = response_body.get("generation", "No response")

            # Clean output
            if "Assistant:" in output_text:
                output_text = output_text.split("Assistant:")[-1].strip()

            if "<|assistant|>" in output_text:
                output_text = output_text.split("<|assistant|>")[-1].strip()

            return output_text

        except Exception as e:
            raise Exception(f"Error invoking model: {e}")
