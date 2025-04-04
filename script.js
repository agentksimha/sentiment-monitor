document.getElementById("fetch-reddit-comments").addEventListener("click", async function() {
    const subredditName = document.getElementById("subreddit-name").value;

    // POST request to the Flask backend to fetch Reddit comments
    const response = await fetch('http://127.0.0.1:5000/api/fetch_reddit_comments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ subreddit: subredditName }),
    });

    const data = await response.json();
    
    if (response.ok) {
        displayRedditComments(data.comments);  // Call new display function
    } else {
        alert("Error: " + data.error);
    }
});

// Function to display fetched Reddit comments and their sentiments
function displayRedditComments(comments) {
    const commentsDiv = document.getElementById("reddit-comments-list");
    commentsDiv.innerHTML = ""; // Clear existing comments

    comments.forEach(comment => {
        const commentDiv = document.createElement("div");
        commentDiv.textContent = `Title: ${comment.title} - Sentiment: ${comment.sentiment}`;
        
        // Optionally, style the sentiment text
        if (comment.sentiment === "positive") {
            commentDiv.classList.add("positive");
        } else if (comment.sentiment === "neutral") {
            commentDiv.classList.add("neutral");
        } else {
            commentDiv.classList.add("negative");
        }

        commentsDiv.appendChild(commentDiv);
    });
}

// Existing functions for displaying sentiment and updating charts would remain unchanged...
function addFeedbackToList(text, sentiment) {
    const feedbackUl = document.getElementById("feedbackUl");
    const li = document.createElement("li");
    li.textContent = `User: ${text} - Sentiment: ${sentiment}`;
    li.classList.add(sentiment);
    feedbackUl.appendChild(li);
}

let chart;
function updateChart(sentiment) {
    const positiveCount = document.querySelectorAll('#feedbackUl .positive').length;
    const neutralCount = document.querySelectorAll('#feedbackUl .neutral').length;
    const negativeCount = document.querySelectorAll('#feedbackUl .negative').length;

    if (!chart) {
        const ctx = document.getElementById('myChart').getContext('2d');
        chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Positive', 'Neutral', 'Negative'],
                datasets: [{
                    label: 'Sentiment Counts',
                    data: [positiveCount, neutralCount, negativeCount],
                    backgroundColor: [
                        'rgba(76, 175, 80, 0.6)', // Green for positive
                        'rgba(255, 193, 7, 0.6)', // Orange for neutral
                        'rgba(244, 67, 54, 0.6)'   // Red for negative
                    ],
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    } else {
        chart.data.datasets[0].data = [positiveCount, neutralCount, negativeCount];
        chart.update();
    }
}