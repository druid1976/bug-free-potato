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
  // added event linstener
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
    courseResults.style.display = 'none'; // Hide the results if match == none
    return;
  }
  // Course result shower :)
  courseResults.style.display = 'block';
  coursesToDisplay.forEach(course => {
    console.log("showing courses")
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
  console.log( course + "added the course inside selectedCourses")
  const selectedCoursesDiv = document.getElementById('selectedCourses');
  const courseDiv = document.createElement('div');
  courseDiv.className = 'course-item';
  courseDiv.innerHTML = `${course.title}`;

  // REMOVAL BUTTON CREATION

  const removeBtn = document.createElement('button');
  removeBtn.className = 'remove-btn';
  removeBtn.textContent = 'X';

  removeBtn.addEventListener('click', () => {
    if (!(selectedCourses.includes(course)) {
      alert("This course is not selected.");
    }
    else {
      selectedCourses.pop(course);
      selectedCoursesDiv.removeChild(courseDiv);
      console.log( course + "removed the course inside selectedCourses")
      console.log("Also removed from the course class")
      if (){}
    }

    console.log("remove button clicked")
    selectedCourses = selectedCourses.filter(selectedCourse => selectedCourse !== course);
    selectedCoursesDiv.removeChild(courseDiv);
    document.querySelector('.selected-section').innerHTML = '';
    courseDiv.classList.remove("selected-section")// Clear the data from the table
});


  // COLORING OF SECTIONS
  const sectionBtn = document.createElement('button');
  sectionBtn.className = 'add-btn';
  sectionBtn.textContent = '!';
  sectionBtn.style.color = 'blue';
  let sectionChosen = false;

  sectionBtn.addEventListener('click', () => {
    if (sectionChosen) {
      doSomethingElse();
    }
    else {
      // If the section has not been chosen, choose it
      coloredSection(course);
      sectionBtn.style.color = 'green';
      sectionBtn.textContent = '✓';
      sectionChosen = true; // Update the state variable
    }
  });

  // CHOOSING OF THE SECTIONS
  courseDiv.appendChild(removeBtn);
  courseDiv.appendChild(sectionBtn);
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
        div.classList.add('potato');
        console.log("added 1 potato (coloring) ");
        div.addEventListener('click', () => {
          choosingSection(div, course, section);
        });
      }
    });
  });
}


// SEÇİLEN SECTION'U YENI DIV YAPARAK YAZDIRIR VE LISTENER'I KALDIRIR
function choosingSection(div, course, section) {
  div.innerHTML = ''; //iç boşaltırıcı
  let noc = courses.findIndex(x => x.title === course.title);
  div.classList.add(noc.toString());
  const courseInfo = document.createElement('div');
  courseInfo.className = 'course-info';
  courseInfo.classList.add(noc.toString()); // HANGİ DERSE AİT OLDUĞUNUN TAKİBİ İÇİN
  courseInfo.innerHTML = `
    <strong>${course.title}</strong>  <br>
    <strong>Section: </strong> ${section.section_number} <br>
    <strong>Building: </strong> ${section.building_name} <br>
    <strong>Room: </strong> ${section.room_name} <br>
    <strong>Floor: </strong> ${section.floor_name}
  `;

  div.appendChild(courseInfo);
  // Remove all listeners from potato elements after the section is selected
  removePotato(course);
}


// O AN AKTİF OLAN LISTENER'I KALDIRIR
function removePotato(course) {
  noc = courses.findIndex(x => x.title === course.title);
  const potatoDivs = document.getElementsByClassName('potato');
  for (let i = 0; i < potatoDivs.length; i++) {
    if (potatoDivs[i].classList.contains(noc.toString())) {
      // do something with element have 'potato' and 'noc' classes
      const div = potatoDivs[i];
      newElement.classList.remove('potato');
      newElement.classList.remove(noc.toString());
      console.log("potato, noc & listener removed");
    }
    else {
      console.log("potato found, but not noc");
    }
  }
}


doSomethingElse = () => {
  choice = confirm("This section is already chosen. Do you want to remove it?");
  if (choice) {
    div.classList.remove('potato');
    div.classList.remove(noc.toString());
    console.log("removed 1 potato (coloring) ");
    div.innerHTML = '';
    div.classList.remove("selected-section")
  }
  else {
    console.log("nothing happened");
  }
}
