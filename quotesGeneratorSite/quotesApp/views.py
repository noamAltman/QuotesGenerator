from django.shortcuts import render, redirect
from .forms import QuoteForm

import pandas as pd
import openai
openai.api_key = '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'

characters =['Marilyn Monroe', 'Dr. Seuss', 'Albert Einstein', 'Mahatma Gandhi', 'J.K. Rowling',
             'Steve Jobs', 'Bob Dylan', 'Bob Marley', 'John Lennon', 'Michael Jordan',
             'David Ben-Gurion', 'Jennifer Aniston', 'Margaret Thatcher', 'Adele', 'Leonardo DiCaprio',
             'Gal Gadot', ]

def get_json_data(filename):
    df = pd.read_json(filename)
    return df

def extract_text(response):
    ans = response.to_dict()["choices"][0]["text"]
    index = ans[2:].rfind('\n')
    ans = ans[2:index] if index != -1 else ans[2:]
    index = ans.rfind('.')
    ans = ans[:index+1] + '"' if index != -1 else ans + '"'
    return ans

def generate_prompt(quotes_df, character, topic):
    prompt = f"Generate a quote of {character} about {topic}"
    length = quotes_df.shape[0]
    if length > 0:
        prompt = f'Add a quote to these {length} quotes of {character} about {topic}:\n'
        for i in range(length):
            prompt += f'{i+1}: {quotes_df.iloc[i]["Quote"]}\n'
        prompt += f'{length+1}: '
    return prompt

def filter_quotes(df, character, topic):
    condition1 = df['Author'] == character
    filtered_df = df[condition1]
    condition2 = filtered_df['Category'] == topic
    filtered_df = filtered_df[condition2]
    return filtered_df

def few_shots(df, character, topic, engine):
    quotes_df = filter_quotes(df, character, topic)
    prompt = generate_prompt(quotes_df, character, topic)
    res = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        # temperature=0.9,
        top_p=0.1,
        max_tokens=64,
        frequency_penalty=0.5,
        best_of=5,
    )
    answer = extract_text(res)
    return answer

def generate_quote(character, topic):
    df = get_json_data('../quotes.json')
    engine_zero_few_shot = "text-davinci-002"
    answer = few_shots(df, character, topic, engine_zero_few_shot)
    return answer

def index(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        character = form['character'].value()
        topic = form['topic'].value()
        form.save()
        quote = generate_quote(character, topic)
        return redirect('output', quote=quote)
    else:
        form = QuoteForm()
        return render(request, 'quotesApp/input.html', {"form": form})

def output_quote(request, quote):
    return render(request, 'quotesApp/quote.html', {"var": quote})
