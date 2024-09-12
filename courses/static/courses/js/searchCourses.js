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
  document.querySelector('.selected-section').innerHTML = ''; // Clear the data from the table
});
  // COLORING OF SECTIONS

  const SectionBtn = document.createElement('button');
  SectionBtn.className = 'add-btn';
  SectionBtn.textContent = '!';
  SectionBtn.style.color = 'blue';
  let sectionChosen = false;

  SectionBtn.addEventListener('click', () => {
    if (sectionChosen) {
      // If the section has already been chosen, do something else
      doSomethingElse();
    } else {
      // If the section has not been chosen, choose it
      coloredSection(course);
      SectionBtn.style.color = 'green';
      SectionBtn.textContent = '✓';
      sectionChosen = true; // Update the state variable
    }
  });

  // CHOOSING OF THE SECTIONS

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
          // MANIPULATION TIME className={'wrapper searchDiv ' + this.state.something}

          let noc = courses.findIndex(x => x.title === course.title);
          div.classList.add('potato');
          div.classList.add(noc.toString());
          console.log("added 1 potato");

          div.addEventListener('click', () => {
            choosingSection(div, course, section);
          });

        }
      });

    });

}
// SEÇİLEN SECTION'U YENI DIV YAPARAK YAZDIRIR VE LISTENER'I KALDIRIR

function choosingSection(div, course, section) {
  div.innerHTML = '';
  const courseInfo = document.createElement('div');
  courseInfo.className = 'course-info';
  courseInfo.innerHTML = `
    <strong>${course.title}</strong>  <br>
    <strong>Section: </strong> ${section.section_number} <br>
    <strong>Building: </strong> ${section.building_name} <br>
    <strong>Room: </strong> ${section.room_name} <br>
    <strong>Floor: </strong> ${section.floor_name}
  `;

  div.appendChild(courseInfo);
  div.classList.add('selected-section');

  // Remove all listeners from potato elements after the section is selected
  removePotato(course);
}

// O AN AKTİF OLAN LISTENER'I KALDIRIR

function removePotato(course) {
  noc = courses.findIndex(x => x.title === course.title);

  const potatoDivs = document.getElementsByClassName('potato');
  const potatoDiver = potatoDivs.getElementsByClassName(noc.toString());

  Array.from(potatoDiver).forEach((div) => {
    const newElement = div.cloneNode(true);
    div.parentNode.replaceChild(newElement, div);
    newElement.classList.remove('potato');
    console.log("potato, list_element & listener removed");
});
}


 /*
doSomethingElse = () => {
  const choice = confirm("You have chosen a section already, do you wish to change it?");
  if (choice) {

    }
  div = document.querySelector('.selected-section');
  console.log("help");
};
*/
