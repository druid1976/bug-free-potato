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

// JUST FOR DELETION
let clickedDiv = null
let clickedCourse = null

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
    if (!(selectedCourses.includes(course))) {
      alert("This course is not selected.");
    }
    else {
      console.log( course + "removed the course inside selectedCourses")
      console.log("Also removed from the course class")
      console.log("remove button clicked")
      //deletes from array
      selectedCourses = selectedCourses.filter(selectedCourse => selectedCourse !== course);
      //deletes the visuals
      selectedCoursesDiv.removeChild(courseDiv);
      let noc = courses.findIndex(x => x.title === course.title);
      const hero = document.getElementsByClassName(noc.toString())
      Array.from(hero).forEach((div) => {
          // !!!
      })
      // if (){}
    }

// SİLME İŞLEMİ CLİCK ATTRİBUTE KIYASLAMA ŞEKLİNDE DE YAPILABİLİR?
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


// POTATO MAKER AND EVENTLISTENER ADDER FOR FUTURE CHOOSING OF THE ITEM
// BURADA COURSE NUMARASI DA EKLENİYOR

function coloredSection(course) {
  let me = []
  course.sections.forEach(section => {
    // Now search for matching divs in the DOM based on section's day and starting hour
    const divs = document.getElementsByClassName('subject');
    // Convert HTMLCollection to array to use forEach
    Array.from(divs).forEach((div) => {
      const divDay = div.getAttribute('data-day');
      const divHour = div.getAttribute('data-hour');
      if (divDay === String(section.day) && divHour === section.starting_hour) {
        me.push(div)
        let noc = courses.findIndex(x => x.title === course.title);
        div.classList.add(noc.toString());
        div.classList.add('potato');
        console.log("added 1 potato (coloring) ");
        div.addEventListener('click', () => {
          console.log("aaa")
          choosingSection(div, course, section);
          clickedDiv = div
          clickedCourse = course
        });
      }

    });
     letMeBe(me, clickedDiv, clickedCourse)
  });
}


function letMeBe(me, clickedDiv, clickedCourse) {

  let noc = courses.findIndex(x => x.title === clickedCourse.title);
  Array.from(me).forEach((div) => {
    if (div !== clickedDiv) {
      div.replaceWith(div.cloneNode(true));  // Replace div with a clone to remove event listeners
      div.classList.remove('potato');
      div.classList.remove(noc.toString());
    }
  })
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

  div.appendChild(courseInfo);
}


doSomethingElse = () => {
  let noc = courses.findIndex(x => x.title === clickedCourse.title);
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
