from openai import OpenAI
import os

#client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

summary = ("Maria Salomea Skłodowska-??? (Polish: [ˈmarja salɔˈmɛa skwɔˈdɔfska kʲiˈri] ;"
           "née Skłodowska; 7 November 1867 – 4 July 1934), known as ??? ??? ( KURE-ee; French:"
           "[maʁi kyʁi] ), was a Polish and naturalised-French physicist and chemist who conducted"
           "pioneering research on radioactivity.")


completion = client.chat.completions.create(
  model="gpt-5-nano",
  messages=[
    {"role": "user", "content": f"In our wikipedia guessing game, the player has to guess the name of the article."
                                f"He already got a summary of the article with hidden keywords: {summary}"
                                f"Give the player a tiny hint he did not already know, but don't tell any name related stuff."}
  ]
)


print(completion.choices[0].message.content)