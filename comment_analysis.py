import re
import logging
from collections import Counter
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
import json
import text2emotion as te
from gensim.models import CoherenceModel, LdaModel
from gensim import corpora
import traceback
from openai_api import generate_key_phrases

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

lemmatizer = WordNetLemmatizer()

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

def preprocess_text(text):
    try:
        text = str(text).lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english')) - {'not', 'no', 'very', 'too', 'only', 'but', 'and'}
        tokens = [lemmatizer.lemmatize(token, pos='v') for token in tokens if token not in stop_words and token.isalnum()]
        processed_text = ' '.join(tokens)
        return processed_text
    except Exception as e:
        logger.error(f'Error in preprocess_text: {str(e)}')
        return ''

def classify_comment(comment):
    try:
        blob = TextBlob(comment)
        sentiment_score = blob.sentiment.polarity

        if sentiment_score > 0.1:
            return 'Positive'
        elif sentiment_score < -0.1:
            return 'Negative'
        else:
            return 'Neutral'
    except Exception as e:
        logger.error(f'Error in classify_comment: {str(e)}')
        return 'Neutral'

def generate_summary(classification_counts, total_comments):
    try:
        summary = f"Analysis of {total_comments} comments:\n"
        for category, count in classification_counts.items():
            percentage = (count / total_comments) * 100
            summary += f"- {category}: {count} ({percentage:.1f}%)\n"
        return summary
    except Exception as e:
        logger.error(f'Error in generate_summary: {str(e)}')
        return ''

def determine_optimal_topics(processed_comments, dictionary, corpus, start=2, limit=10, step=1):
    try:
        coherence_scores = []
        model_list = []
        for num_topics in range(start, limit + 1, step):
            model = LdaModel(
                corpus=corpus,
                id2word=dictionary,
                num_topics=num_topics,
                random_state=42,
                update_every=1,
                chunksize=100,
                passes=10,
                alpha='auto',
                per_word_topics=True
            )
            model_list.append(model)
            coherencemodel = CoherenceModel(
                model=model,
                texts=[doc.split() for doc in processed_comments],
                dictionary=dictionary,
                coherence='c_v'
            )
            coherence = coherencemodel.get_coherence()
            coherence_scores.append(coherence)
            logger.info(f"Coherence Score for {num_topics} topics: {coherence}")
        optimal_index = coherence_scores.index(max(coherence_scores))
        optimal_num_topics = start + optimal_index * step
        logger.info(f"Optimal number of topics determined: {optimal_num_topics}")
        return optimal_num_topics
    except Exception as e:
        logger.error(f'Error in determine_optimal_topics: {str(e)}')
        return 5

def create_sentiment_chart(classification_counts):
    try:
        labels = list(classification_counts.keys())
        values = list(classification_counts.values())
        colors = ['#45B7D1', '#FF6B6B', '#FFA07A']

        trace = go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hole=0.4,
            textinfo='label+percent',
            hoverinfo='label+percent+value',
            textfont=dict(size=14),
        )
        layout = go.Layout(
            title='Sentiment Distribution',
            annotations=[dict(text='Sentiment', x=0.5, y=0.5, font_size=20, showarrow=False)],
            showlegend=True,
            margin=dict(t=50, b=50, l=50, r=50),
        )
        fig = go.Figure(data=[trace], layout=layout)
        return json.dumps(fig, cls=PlotlyJSONEncoder)
    except Exception as e:
        logger.error(f'Error creating sentiment chart: {str(e)}')
        return '{}'

def create_topics_chart(top_topics):
    try:
        top_topics = top_topics[:5]
        topics = [f"Topic {topic['id']}: {', '.join(topic['words'][:3])}" for topic in top_topics]
        weights = [topic['weight'] for topic in top_topics]

        trace = go.Bar(
            y=topics,
            x=weights,
            orientation='h',
            marker=dict(
                color=weights,
                colorscale='Viridis',
                colorbar=dict(title='Weight'),
            ),
            hoverinfo='y+x',
            textposition='auto',
        )
        layout = go.Layout(
            title='Top 5 Topics Discussed',
            yaxis=dict(title='Topics', automargin=True),
            xaxis=dict(title='Weight'),
            height=400,
            margin=dict(t=50, b=50, l=150, r=50),
        )

        fig = go.Figure(data=[trace], layout=layout)
        return json.dumps(fig, cls=PlotlyJSONEncoder)
    except Exception as e:
        logger.error(f'Error creating topics chart: {str(e)}')
        return '{}'

def create_emotion_chart(emotion_counts):
    try:
        emotions = list(emotion_counts.keys())
        counts = list(emotion_counts.values())
        colors = ['#FFD700', '#FF6347', '#1E90FF', '#9370DB', '#FF69B4']

        trace = go.Bar(
            x=emotions,
            y=counts,
            marker=dict(
                color=colors[:len(emotions)],
            ),
            hoverinfo='x+y',
            textposition='auto',
        )
        layout = go.Layout(
            title='Emotional Tone of Comments',
            xaxis=dict(title='Emotions'),
            yaxis=dict(title='Counts'),
            height=400,
            margin=dict(t=50, b=50, l=50, r=50),
        )

        fig = go.Figure(data=[trace], layout=layout)
        return json.dumps(fig, cls=PlotlyJSONEncoder)
    except Exception as e:
        logger.error(f'Error creating emotion chart: {str(e)}')
        return '{}'

def analyze_comments_with_model(comments):
    try:
        logger.info("Starting comment analysis...")

        processed_comments = [preprocess_text(comment) for comment in comments]
        logger.info(f"Processed {len(processed_comments)} comments.")

        tokenized_comments = [comment.split() for comment in processed_comments]
        dictionary = corpora.Dictionary(tokenized_comments)
        corpus = [dictionary.doc2bow(text) for text in tokenized_comments]
        logger.info(f"Created dictionary with {len(dictionary)} tokens and corpus with {len(corpus)} documents.")

        optimal_num_topics = determine_optimal_topics(processed_comments, dictionary, corpus)
        logger.info(f"Optimal number of topics: {optimal_num_topics}")

        lda_model = LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=optimal_num_topics,
            random_state=42,
            update_every=1,
            chunksize=100,
            passes=10,
            alpha='auto',
            per_word_topics=True
        )
        logger.info("LDA model trained.")

        top_topics = []
        for topic_idx in range(optimal_num_topics):
            topic = lda_model.show_topic(topic_idx, topn=10)
            words = [word for word, prob in topic]
            top_topics.append({
                'id': topic_idx,
                'words': words,
                'weight': float(sum([prob for word, prob in topic]))
            })
        logger.info("Top topics extracted.")

        classifications = [classify_comment(comment) for comment in processed_comments]
        classification_counts = Counter(classifications)
        logger.info("Sentiment classification completed.")

        summary = generate_summary(classification_counts, len(comments))

        key_phrases = generate_key_phrases(comments)
        logger.info("Key phrases generated using OpenAI.")

        emotion_counts = Counter()
        for comment in comments:
            emotions = te.get_emotion(comment)
            for emotion, score in emotions.items():
                if score > 0:
                    emotion_counts[emotion] += 1
        logger.info("Emotion analysis completed.")

        sentiment_chart = create_sentiment_chart(classification_counts)
        topics_chart = create_topics_chart(top_topics)
        emotion_chart = create_emotion_chart(emotion_counts)

        logger.info("Visualizations created.")

        classification_html = classification_html_func(classification_counts)
        top_topics_html = topics_html_func(top_topics)
        key_phrases_html = key_phrases_html_func(key_phrases)

        return {
            'summary': summary,
            'classification': classification_html,
            'top_topics': top_topics_html,
            'key_phrases': key_phrases_html,
            'sentiment_chart': sentiment_chart,
            'topics_chart': topics_chart,
            'emotion_chart': emotion_chart
        }

    except Exception as e:
        logger.error(f"Error in analyze_comments_with_model: {str(e)}")
        logger.error(traceback.format_exc())
        return None

def classification_html_func(classification_counts):
    try:
        html = "<ul>"
        for category, count in classification_counts.items():
            percentage = (count / sum(classification_counts.values())) * 100
            html += f"<li><strong>{category}:</strong> {count} ({percentage:.1f}%)</li>"
        html += "</ul>"
        return html
    except Exception as e:
        logger.error(f"Error in classification_html_func: {str(e)}")
        return "<p>Error generating classification HTML.</p>"

def topics_html_func(top_topics):
    try:
        html = "<ul>"
        for topic in top_topics[:5]:
            words = ', '.join(topic['words'][:5])
            html += f"<li><strong>Topic {topic['id']}:</strong> {words}</li>"
        html += "</ul>"
        return html
    except Exception as e:
        logger.error(f"Error in topics_html_func: {str(e)}")
        return "<p>Error generating topics HTML.</p>"

def key_phrases_html_func(key_phrases):
    try:
        if not key_phrases:
            return "<p>No key phrases extracted.</p>"
        html = "<ul>"
        for phrase in key_phrases:
            html += f"<li>{phrase}</li>"
        html += "</ul>"
        return html
    except Exception as e:
        logger.error(f"Error in key_phrases_html_func: {str(e)}")
        return "<p>Error generating key phrases HTML.</p>"