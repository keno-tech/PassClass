from openai import OpenAI
client = OpenAI()

role = ""
transcript = ""

completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{role}"},
            {"role": "user", "content": f"{transcript}"}
        ]
    )
