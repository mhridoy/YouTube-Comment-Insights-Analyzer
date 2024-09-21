import os
import openai
import logging
import traceback

# Initialize logging
logger = logging.getLogger(__name__)

# Configure OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_ai_image(summary):
    """
    Generates an AI image based on the provided summary using OpenAI's DALL·E API.
    """
    try:
        if not openai.api_key:
            logger.error("OpenAI API key not found.")
            return None

        prompt = f"Create an abstract representation of the following YouTube comment analysis summary: {summary}"

        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512",
            response_format="url"
        )

        image_url = response['data'][0]['url']
        logger.info("AI image generated successfully.")
        return image_url

    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in generate_ai_image: {str(e)}")
        logger.error(traceback.format_exc())
    return None

def generate_key_phrases(comments):
    """
    Generates key phrases from comments using OpenAI's API.
    """
    try:
        if not openai.api_key:
            logger.error("OpenAI API key not found.")
            return []

        # Concatenate comments and limit to a reasonable length to avoid exceeding prompt size limits
        concatenated_comments = " ".join(comments[:100])  # Use the first 100 comments

        prompt = (
            "Extract the most significant key phrases from the following comments:\n\n"
            f"{concatenated_comments}\n\n"
            "Provide a list of the top 20 key phrases."
        )

        # Use the ChatCompletion API with gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are an assistant that extracts key phrases from text.'},
                {'role': 'user', 'content': prompt},
            ],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.5,
        )

        key_phrases_text = response.choices[0].message['content'].strip()
        # Parse the key phrases from the response
        key_phrases = []
        for line in key_phrases_text.split("\n"):
            line = line.strip("-• \t1234567890.")
            if line:
                key_phrases.append(line)
        logger.info("Key phrases generated using OpenAI.")
        return key_phrases

    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in generate_key_phrases: {str(e)}")
        logger.error(traceback.format_exc())
    return []
