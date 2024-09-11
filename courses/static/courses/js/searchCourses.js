class Section {
  constructor(section_number, day, starting_hour, room_name, building_name, floor_name) {
    this.section_number = section_number;
    this.day = day;
    this.starting_hour = starting_hour;
    this.room_name = room_name;
    this.building_name = building_name;
    this.floor_name = floor_name;
  }
}

class Course {
  constructor(title, sections) {
    this.title = title;
    this.sections = sections;
  }
}

let courses = [];
let selectedCourses = [];


// Event listener to the search bar after the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  fetchCourses();
  // Attach the event listener for searching
  const searchBar = document.getElementById('courseSearchBar');
  searchBar.addEventListener('input', handleSearch);
});


async function fetchCourses() {
  try {
    const response = await fetch('/course/search/');
    const data = await response.json();

    courses = data.course_data.map(courseData => {
      const sections = courseData.sections.map(sectionData => new Section(
        sectionData.section_number,
        sectionData.day,
        sectionData.starting_hour,
        sectionData.room_name,
        sectionData.building_name,
        sectionData.floor_name
      ));

      return new Course(courseData.title, sections);
    });

    displayCourses(courses);

  } catch (error) {
    console.error('Error fetching the JSON:', error);
  }
}

function displayCourses(coursesToDisplay) {
  const courseResults = document.getElementById('courseResults');
  courseResults.innerHTML = ''; // Clear previous results

  if (coursesToDisplay.length === 0) {
    courseResults.style.display = 'none'; // Hide the results if no courses match
    return;
  }

  // Show the course results container
  courseResults.style.display = 'block';

  coursesToDisplay.forEach(course => {
    const courseDiv = document.createElement('div');
    courseDiv.className = 'search-result-item';
    courseDiv.innerHTML = `<strong>${course.title}</strong>`;

    // Attach click event listener to add course to selected list
    courseDiv.addEventListener('click', () => addCourseToSelected(course));

    courseResults.appendChild(courseDiv);
  });
}

// Function to handle search input and filter courses
function handleSearch(event) {
  const searchTerm = event.target.value.toLowerCase();

  // Filter courses based on the search term
  const filteredCourses = courses.filter(course =>
    course.title.toLowerCase().includes(searchTerm)
  );

  // Display the filtered courses
  displayCourses(filteredCourses);
}

// ADD COURSE TO SELECTED COURSES LIST IN THE LIST AND CREATE THE VISUALS FOR THE PAGE ALSO REMOVAL

function addCourseToSelected(course) {
  if (selectedCourses.includes(course)) {
    alert("This course is already selected.");
    return;
  }
  selectedCourses.push(course);

  const selectedCoursesDiv = document.getElementById('selectedCourses');

  const courseDiv = document.createElement('div');
  courseDiv.className = 'course-item';
  courseDiv.innerHTML = `<strong>${course.title}</strong>`;

  // REMOVAL BUTTON CREATION

  const removeBtn = document.createElement('button');
  removeBtn.className = 'remove-btn';
  removeBtn.textContent = 'X';

  removeBtn.addEventListener('click', () => {
    selectedCourses = selectedCourses.filter(selectedCourse => selectedCourse !== course);
    selectedCoursesDiv.removeChild(courseDiv);

  });
  // COLORING OF SECTIONS

  const SectionBtn = document.createElement('button');
  SectionBtn.className = 'add-btn';
  SectionBtn.textContent = '!';
  SectionBtn.style.color = 'blue';

  SectionBtn.addEventListener('click', () => {
    coloredSection(course);

  })

  // CHOOSING OF THE SECTIONS
  const choosingBtn = document.createElement('button');
  choosingBtn.className = 'choosing';


  courseDiv.appendChild(removeBtn);
  courseDiv.appendChild(SectionBtn);
  selectedCoursesDiv.appendChild(courseDiv);
}

// COLORRRRERRR

function coloredSection(course) {

    course.sections.forEach(section => {

      // Now search for matching divs in the DOM based on section's day and starting hour
      const divs = document.getElementsByClassName('subject');

      // Convert HTMLCollection to array to use forEach
      Array.from(divs).forEach((div) => {
        const divDay = div.getAttribute('data-day');
        const divHour = div.getAttribute('data-hour');
        if (divDay === String(section.day) && divHour === section.starting_hour) {
          // MANIPULATION TIME
          choosingSection(course);
          div.classList.add('blurling');
          console.log("help");
        }
      });

    });

}

function choosingSection(course) {
  choosingBtn.addEventListener('click', () => {

  })

}