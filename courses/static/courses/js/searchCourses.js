async function fetchCourses() {
    const response = await fetch('search/courses');
    const data = await response.json();
    return data.courses;
}

let courses = [];

document.addEventListener('DOMContentLoaded', async () => {
    courses = await fetchCourses();
});

function searchCourses() {
    const input = document.getElementById('courseSearch');
    const filter = input.value.toUpperCase();
    const results = document.getElementById('searchResults');
    results.innerHTML = '';
    let matches = courses.filter(course => course.title.toUpperCase().indexOf(filter) > -1);

    if (matches.length === 0 && filter.trim() !== '') {
        results.innerHTML = '<div>No matches found</div>';
    } else {
        matches.forEach(course => {
            const div = document.createElement('div');
            div.className = 'search-result-item';
            div.textContent = course.title;
            div.onclick = () => addCourseToList(course);
            results.appendChild(div);
        });
    }
    results.style.display = 'block';
}

function addCourseToList(course) {
    const selectedCourses = document.getElementById('selectedCourses');
    const courseDiv = document.createElement('div');
    courseDiv.className = 'course-item';
    courseDiv.textContent = course.title;
    selectedCourses.appendChild(courseDiv);
    document.getElementById('searchResults').style.display = 'none'; // Hide search results
    document.getElementById('courseSearch').value = ''; // Clear search input
}

