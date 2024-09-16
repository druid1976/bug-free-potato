
// EVENT DELEGATION - https://www.freecodecamp.org/news/event-delegation-javascript/

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

// global variables because why not ( I couldn't find another way to do it )
let courses = [];
let selectedCourses = [];
let me = {};


// Event listener to the search bar after the DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
  try {
    await fetchCourses();

    // Initialize search bar after courses are fetched successfully because why do it backwards?

    const searchBar = document.getElementById('courseSearchBar');
    searchBar.addEventListener('input', handleSearch);
  } catch (error) {
    console.error('Error fetching courses:', error);
  }
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

  const searchTerm = event.target.value.toLowerCase().trim();
  const courseResults = document.getElementById('courseResults');
  //hiding the results if nothing is seached initially
  if (searchTerm === '') {
    courseResults.innerHTML = '';
    courseResults.style.display = 'none';
    return;
  }
  //filterer
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
    if (!(selectedCourses.includes(course))) {
      alert("This course is not selected.");
    }
    else {
      console.log("remove button clicked");
      //deletes from array
      selectedCourses = selectedCourses.filter(selectedCourse => selectedCourse !== course);
      console.log( course + "removed the course inside selectedCourses");
      //deletes the visuals
      selectedCoursesDiv.removeChild(courseDiv);
      console.log("Also removed from the course class");
      removeTable(course);
      console.log("removed from the table");
    }

// SİLME İŞLEMİ CLİCK ATTRİBUTE KIYASLAMA ŞEKLİNDE DE YAPILABİLİR?
});


// SECTION CHOOSE BUTTON CREATION

const sectionBtn = document.createElement('button');
sectionBtn.className = 'add-btn';
sectionBtn.textContent = '!';
sectionBtn.style.color = 'blue';
sectionBtn.sectionChosen = false;

sectionBtn.addEventListener('click', () => {
  if (sectionBtn.sectionChosen) {
    const choice = confirm("This section is already chosen. Do you want to remove it and choose another?");
    if (choice) {
      removeTable(course);
      //re-color it
      coloredSection(course);
      // Reset button appearance
      sectionBtn.style.color = 'blue';
      sectionBtn.textContent = '!';
      sectionBtn.sectionChosen = false; // Update the state variable
    } else {
      console.log("Nothing happened.");
    }
  } else {
    coloredSection(course);
    sectionBtn.style.color = 'green';
    sectionBtn.textContent = '✓';
    sectionBtn.sectionChosen = true;
  }
});
  // CHOOSING OF THE SECTIONS
  courseDiv.appendChild(removeBtn);
  courseDiv.appendChild(sectionBtn);
  selectedCoursesDiv.appendChild(courseDiv);
}


// POTATO MAKER AND EVENTLISTENER ADDER FOR FUTURE CHOOSING OF THE ITEM
// BURADA COURSE NUMARASI DA EKLENİYOR

function coloredSection(course) {
  let noc = courses.findIndex(x => x.title === course.title);
  if (!me[noc]) {
    me[noc] = []; // Initializing array of sectionas for each course
  }
  course.sections.forEach(section => {
    const divs = document.getElementsByClassName('subject');
    Array.from(divs).forEach((div) => {
      const divDay = div.getAttribute('data-day');
      const divHour = div.getAttribute('data-hour');
      if (divDay === String(section.day) && divHour === section.starting_hour) {
        me[noc].push({ div: div });
        div.classList.add(noc.toString());
        div.classList.add('potato');
        console.log("added 1 potato (coloring)");
        div.addEventListener('click', () => {
          console.log("entering event listener");
          choosingSection(div, course, section);
        });
      }
    });
  });
}


// SEÇİLEN SECTION'U YENI DIV YAPARAK YAZDIRIR VE LISTENER'I KALDIRIR
function choosingSection(div, course, section) {
  div.innerHTML = ''; //iç boşaltırıcı
  const courseInfo = document.createElement('div');
  courseInfo.className = 'course-info';
  courseInfo.innerHTML = `
    <strong>${course.title}</strong>  <br>
    <strong>Section: </strong> ${section.section_number} <br>
    <strong>Building: </strong> ${section.building_name} <br>
    <strong>Room: </strong> ${section.room_name} <br>
    <strong>Floor: </strong> ${section.floor_name}
  `;
  let clickedDiv = div;
  div.appendChild(courseInfo);
  letMeBe(course, clickedDiv);
}


function letMeBe(course, clickedDiv) {
  console.log("letmebe working...");
  let noc = courses.findIndex(x => x.title === course.title);
  if (me[noc]) {
    me[noc].forEach((item) => {
      let div = item.div;
      let newDiv = div.cloneNode(true);
      newDiv.classList.remove('potato');
      console.log("deleting potato");
      if (div !== clickedDiv) {
        newDiv.classList.remove(noc.toString());
      }
      div.replaceWith(newDiv);
      // referansör kanks
      item.div = newDiv;
    });
  }
}


function removeTable(course) {
  let noc = courses.findIndex(x => x.title === course.title);
  if (me[noc]) {
    me[noc].forEach((item) => {
      let div = item.div; // Access the actual div
      div.innerHTML = '';

      let newDiv = div.cloneNode(true);

      newDiv.classList.remove('potato', noc.toString());
      console.log("RemoveTable works fine?");
      div.replaceWith(newDiv);

      // updating the REFERENCE in me[noc]
      item.div = newDiv;
    });
    // Clean up 'me'
    delete me[noc];
  }
}


