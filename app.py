from flask import Flask, render_template, request, jsonify
import csv
import openai

app = Flask(__name__)
openai.api_key = '' 

# Function to read proverbs from dataset
def read_proverbs():
    proverbs = []
    with open('datasets/proverbsforproject.txt', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) == 8:
                proverbs.append(row)
    return proverbs

# Extract unique genres
def get_genres(proverbs):
    genres = set()
    for proverb in proverbs:
        genres.add(proverb[4].strip())
    return sorted(list(genres))

# Extract unique languages
def get_languages(proverbs):
    languages = set()
    for proverb in proverbs:
        languages.add(proverb[7].strip())
    return sorted(list(languages))

# Get proverbs by genre and language
def get_proverbs_by_genre_and_language(proverbs, genre, language):
    filtered_proverbs = []
    for proverb in proverbs:
        if proverb[4].strip() == genre and proverb[7].strip() == language:
            filtered_proverbs.append(proverb)
    return filtered_proverbs

# Function to generate GPT explanation
def generate_gpt_explanation(proverb):
    try:
        response = openai.completions.create(
            engine="text-davinci-003",  
            prompt=f"Explain the meaning and significance of the proverb: '{proverb}'.",
            max_tokens=100
        )
        explanation = response.choices[0].text.strip()
        return explanation
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/')
def home():
    proverbs = read_proverbs()
    genres = get_genres(proverbs)
    languages = get_languages(proverbs)
    return render_template('home.html', genres=genres, languages=languages)

@app.route('/language', methods=['POST'])
def language():
    selected_genre = request.form['genre']
    proverbs = read_proverbs()
    languages = get_languages(proverbs)
    return render_template('language.html', genre=selected_genre, languages=languages)

@app.route('/proverbs', methods=['POST'])
def proverbs():
    selected_genre = request.form['genre']
    selected_language = request.form['language']
    proverbs = read_proverbs()
    filtered_proverbs = get_proverbs_by_genre_and_language(proverbs, selected_genre, selected_language)
    return render_template('proverbs.html', proverbs=filtered_proverbs, genre=selected_genre, language=selected_language)

@app.route('/aboutus')
def about_us():
    return render_template('aboutus.html')

@app.route('/explanation')
def explanation():
    selected_proverb = request.args.get('proverb', '')

    # For demonstration purposes, let's assume you have a model-generated explanation
    our_model_generated = "Our model explanation here for: " + selected_proverb

    # Generate GPT explanation
    gpt_generated = generate_gpt_explanation(selected_proverb)

    return render_template('explanation.html', selected_proverb=selected_proverb, our_model_generated=our_model_generated, gpt_generated=gpt_generated)

if __name__ == '__main__':
    app.run(debug=True)
