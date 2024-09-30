let questions = [];

document.addEventListener('DOMContentLoaded', function () {
    fetchQuestions();
});

function fetchQuestions() {
    fetch('/questionaire/json_pull_request/')
        .then(response => response.json())
        .then(data => {
            questions = data.questions;
        })
        .catch(error => console.error('Error fetching questions:', error));
}


function handleSearch(event) {
    const searchTerm = event.target.value.toLowerCase().trim();
    const searchResults = document.getElementById('searchResults');

    if (searchTerm === '') {
        searchResults.innerHTML = '';
        searchResults.style.display = 'none';
        return;
    }

    if (!Array.isArray(questions) || questions.length === 0) {
        console.error('No questions available for search.');
        return;
    }

    const filteredQuestions = questions.filter(question =>
        question.question.toLowerCase().includes(searchTerm) ||
        question.author.toLowerCase().includes(searchTerm)
    );

    displayQuestions(filteredQuestions);
}

function displayQuestions(questionsToDisplay) {
    const searchResults = document.getElementById('searchResults');
    searchResults.innerHTML = '';
    if (questionsToDisplay.length === 0) {
        searchResults.style.display = 'none'; // Hide the results if -match
        return;
    }

    searchResults.style.display = 'block'; // show them resultos
    questionsToDisplay.forEach(question => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'search-result-item';
        questionDiv.innerHTML = `<strong>${question.question}</strong>`;
        questionDiv.addEventListener('click', () => {
            window.location.href = question.url; //JSON packetleme
        });
        searchResults.appendChild(questionDiv);
    });
}
