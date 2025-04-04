import praw
from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Embedding, Flatten
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)
CORS(app)

texts = ["This is a sample text for testing", "Another text sample", "Positive vibes", "Negative outcome"]
labels = ["neutral", "neutral", "positive", "negative"]
label_mapping = {"negative": 0, "neutral": 1, "positive": 2}
y = np.array([label_mapping[label] for label in labels])

tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(texts)
x = tokenizer.texts_to_sequences(texts)
x = pad_sequences(x, maxlen=10)

model = Sequential([
    Embedding(input_dim=5000, output_dim=64, input_length=10),
    Flatten(),
    Dense(units=48, activation='relu'),
    Dense(units=32, activation='relu'),
    Dense(units=3, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
model.fit(x_train, y_train, epochs=10, batch_size=4, validation_data=(x_test, y_test))

reddit = praw.Reddit(
    client_id="KJUP4DtK9hfAkUBEQnwCbA",
    client_secret="4z46oF8ObhKebJaIoO9IcDM-EYIcPQ",
    user_agent="krishna",
    username="Technical-Swimmer-43"
)

@app.route('/api/fetch_reddit_comments', methods=['POST'])
def fetch_reddit_comments():
    data = request.json
    subreddit_name = data.get('subreddit')

    if not subreddit_name:
        return jsonify({"error": "No subreddit provided"}), 400

    try:
        subreddit = reddit.subreddit(subreddit_name)
        submissions = subreddit.new(limit=50)

        comments_data = []

        for submission in submissions:
            title = submission.title
            print(f"Fetched submission: {title}")  # Debugging log

            new_seq = tokenizer.texts_to_sequences([title])
            new_seq_padded = pad_sequences(new_seq, maxlen=10)
            print(f"Shape of new_seq_padded: {new_seq_padded.shape}")  # Debugging log

            try:
                prediction = model.predict(new_seq_padded)
                predicted_label = np.argmax(prediction, axis=1)[0]
                label_map = {0: "negative", 1: "neutral", 2: "positive"}
                sentiment = label_map[predicted_label]
                comments_data.append({"title": title, "sentiment": sentiment})
            except Exception as e:
                print(f"Prediction error: {e}")
                return jsonify({"error": "Prediction error"}), 500

        return jsonify({"comments": comments_data})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
