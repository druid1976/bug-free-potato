
// EVENT DELEGATION - https://www.freecodecamp.org/news/event-delegation-javascript/
// BURASI SAYFADA ARAMA TARAMA SALLAMA YAPABİLMEK İÇİN VAR



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
        const searchBar = document.getElementById('courseSearchBar');
        searchBar.disabled = false; // Enable the search bar after courses are fetched
        searchBar.addEventListener('input', handleSearch);
    } catch (error) {
        console.error('Error fetching courses:', error);
    }
});



async function fetchCourses() {
    try {
        const response = await fetch('/course/search/');
        const data = await response.json();
        console.log("Fetched course data:", data); // Log the entire response
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
        console.log("Courses populated:", courses); // Log the populated courses
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

    if (searchTerm === '') {
        courseResults.innerHTML = '';
        courseResults.style.display = 'none';
        return;
    }

    if (!Array.isArray(courses) || courses.length === 0) {
        console.error('No courses available for search.');
        return;
    }

    const filteredCourses = courses.filter(course =>
        course.title.toLowerCase().includes(searchTerm)
    );
    displayCourses(filteredCourses);
}





// ADD COURSE TO SELECTED COURSES LIST IN THE LIST AND CREATE THE VISUALS FOR THE PAGE ALSO REMOVAL


function addCourseToSelected(course) {
  if (selectedCourses.includes(course)) {
    alert("This course is already selected.");
    return;
  }

  selectedCourses.push(course);
  console.log(" ${course.title} added the course inside selectedCourses")
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
        me[noc] = []; // Initialize array of sections for each course
    }

    course.sections.forEach(section => {
        const divs = document.getElementsByClassName('subject');

        Array.from(divs).forEach((div) => {
            const divDay = div.getAttribute('data-day');
            const divHour = div.getAttribute('data-hour');

            // Match the div with the section's day and starting hour
            if (divDay === String(section.day) && divHour === section.starting_hour) {
                // Push this div and section to the 'me' array for this course
                me[noc].push({ div: div, section: section });

                div.classList.add(noc.toString()); // Add a class based on course index
                div.classList.add('potato');       // Add a 'potato' class for selected

                console.log(`Added section ${section.section_number} for course ${course.title}`);
                console.log('Sending me[' + noc + ']: to selection chamber', me[noc]);

                // Add click event for selecting section
                div.addEventListener('click', () => {
                    console.log("Selecting section");
                    choosingSections( course, section);
                });
            }
        });
    });
}



// SEÇİLEN SECTION'U YENI DIV YAPARAK YAZDIRIR VE LISTENER'I KALDIRIR
// Function to select and display section details

function choosingSections(course, section) {

    // Clear the div and display the selected section's details
    let noc = courses.findIndex(x => x.title === course.title);
    console.log('Accessing me[' + noc + ']:', me[noc]);
    me[noc].forEach((item) => {
        if (section.section_number === item.section.section_number) {
            console.log("section numbers match")
            let div = item.div;
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
        }

        // adding the course info to the div
    })

    // for deletion purpose
    letMeBe(course, section);
}



function letMeBe(course, section) {
    console.log("letMeBe working...");

    let noc = courses.findIndex(x => x.title === course.title);

    if (me[noc]) {
        me[noc].forEach((item) => {
            let div = item.div;
            let newDiv = div.cloneNode(true); // Clone the current div for updating

            // Remove 'potato' class from all except clickedDiv
            newDiv.classList.remove('potato');
            if (div !== section) {
                newDiv.classList.remove(noc.toString()); // Remove course-specific class
            }

            div.replaceWith(newDiv); // Replace old div with the updated div
            item.div = newDiv; // Update the reference to the new div in the 'me' array
        });
    }
}



function removeTable(course) {
    let noc = courses.findIndex(x => x.title === course.title);

    if (me[noc]) {
        me[noc].forEach((item) => {
            let div = item.div; // Access the actual div
            div.innerHTML = ''; // Clear the div content

            let newDiv = div.cloneNode(true); // Clone the div to update its appearance

            // Remove styles and reset the div
            newDiv.classList.remove('potato', noc.toString());
            console.log(`RemoveTable: Removed section for ${course.title}`);
            div.replaceWith(newDiv); // Replace old div with updated div

            item.div = newDiv; // Update the reference in 'me' array
        });

        // Clean up 'me' for this course
        delete me[noc];
    }
}


