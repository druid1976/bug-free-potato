

async function fetchCourses() {

    try {
        const response = await fetch('/course/search/');
        const data = await response.json();
        courses = data.course_data.map(courseData => {});
    }
    catch (error) {

    }

}