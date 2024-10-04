// Class to represent a Section
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

// Class to represent a Section Packet
class SectionPacket {
  constructor(packet_id, sections) {
    this.packet_id = packet_id;
    this.sections = sections; // List of Section objects
  }
}

// Class to represent a Course
class Course {
  constructor(title, course_code, section_packets) {
    this.title = title;
    this.course_code = course_code;
    this.section_packets = section_packets; // List of SectionPacket objects
  }
}

// Global variables
let courses = [];
let selectedCourses = [];
let selectedSectionPackets = {};
// Fetch course data from the server and populate the courses array
async function fetchCourseData() {
    try {
        const response = await fetch('/course/search/');

        // Check if response is OK (status code 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const contentType = response.headers.get("content-type");
        if (contentType && contentType.indexOf("application/json") === -1) {
            throw new Error("Expected JSON, but got a different content-type");
        }

        // Log the raw response text to check for issues
        const rawData = await response.text();
        console.log("Raw response data:", rawData);

        const data = JSON.parse(rawData);
        console.log("Parsed course data:", data);

        courses = data.course_data.map(courseData => {
            const sectionPackets = courseData.section_packets.map(packetData => {
                const sections = packetData.sections.map(sectionData => new Section(
                    sectionData.section_number,
                    sectionData.day,
                    sectionData.starting_hour,
                    sectionData.room_name,
                    sectionData.building_name,
                    sectionData.floor_name
                ));
                return new SectionPacket(packetData.packet_id, sections);
            });
            return new Course(courseData.title, courseData.course_code, sectionPackets);
        });
        console.log("Courses populated:", courses); // Log the populated courses

    } catch (error) {
        console.error('Error fetching course data:', error);
    }
}

// Call the function to fetch and store the data when the page loads
document.addEventListener('DOMContentLoaded', () => {
  fetchCourseData();
});

// Function to display filtered courses
function displayCourses(filteredCourses) {
  const courseResults = document.getElementById('courseResults');
  courseResults.innerHTML = ''; // Clear previous results

  if (filteredCourses.length === 0) {
    courseResults.style.display = 'none'; // Hide if no matches found
    return;
  }

  courseResults.style.display = 'block'; // Show results if matches are found

  // Display each filtered course
  filteredCourses.forEach(course => {
    const courseDiv = document.createElement('div');
    courseDiv.className = 'search-result-item';
    courseDiv.innerHTML = `<strong>${course.title} (${course.course_code})</strong>`;

    // Add click event to select the course
    courseDiv.addEventListener('click', () => selectCourse(course));

    courseResults.appendChild(courseDiv);
  });
}

// Function to select a course
// ... (previous code remains unchanged)













// Function to select a course
function selectCourse(course) {
  // Check if the course is already selected
  if (selectedCourses.some(selectedCourse => selectedCourse.title === course.title)) {
    alert("This course is already selected!");
    return; // Course is already selected
  }

  // Add the course to selected courses
  selectedCourses.push(course);
  // Initialize the selected section packet for this course in the dictionary
  selectedSectionPackets[course.course_code] = null; // No section packet selected initially
  console.log("Selected courses:", selectedCourses); // Log selected courses

  // Update the display of selected courses
  displaySelectedCourses();
}


// Function to display selected courses
// Function to display selected courses
function displaySelectedCourses() {
  const selectedCoursesContainer = document.getElementById('selectedCourses');
  selectedCoursesContainer.innerHTML = ''; // Clear previous selections

  if (selectedCourses.length === 0) {
    selectedCoursesContainer.style.display = 'none';
    return;
  }

  selectedCoursesContainer.style.display = 'block'; // Show container if there are selected courses

  // Create an unordered list
  const ul = document.createElement('ul');

  selectedCourses.forEach(course => {
    const li = document.createElement('li');
    li.innerHTML = `<strong>${course.title} (${course.course_code})</strong>`;

    // Create the "!" button
    const exclamationButton = document.createElement('button');
    exclamationButton.textContent = '!';
    exclamationButton.disabled = false; // Initially enabled
    exclamationButton.addEventListener('click', () => {
      addCourseToSchedule(course);
      exclamationButton.disabled = true; // Disable after adding
    });

    // Create the "x" button
    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'x';
    deleteButton.addEventListener('click', () => {
      removeCourse(course);
      removeCourseFromSchedule(course); // Remove from schedule as well
      exclamationButton.disabled = false; // Re-enable the exclamation button when course is removed
    });

    // Append buttons to the list item
    li.appendChild(exclamationButton);
    li.appendChild(deleteButton);

    // Append the list item to the unordered list
    ul.appendChild(li);
  });

  // Clear the previous contents and append the unordered list
  selectedCoursesContainer.innerHTML = ''; // Clear previous selections
  selectedCoursesContainer.appendChild(ul); // Append the new list
}

// Function to add course sections to the schedule
function addCourseToSchedule(course) {
  course.section_packets.forEach(packet => {
    packet.sections.forEach(section => {
      const divs = document.getElementsByClassName('subject');

      Array.from(divs).forEach((div) => {
        const divDay = div.getAttribute('data-day');
        const divHour = div.getAttribute('data-hour');

        // Match the div with the section's day and starting hour
        if (divDay === String(section.day) && divHour === section.starting_hour) {
          // Check if the section box already exists to prevent duplicates
          const existingBoxes = div.getElementsByClassName('section-box');
          const sectionExists = Array.from(existingBoxes).some(box => {
            return box.getAttribute('data-section-number') === section.section_number &&
                   box.getAttribute('data-course-code') === course.course_code;
          });

          if (!sectionExists) { // Only add if it does not already exist
            // Create a small box for the section information
            const sectionBox = document.createElement('div');
            sectionBox.className = 'section-box';
            sectionBox.style.display = 'none'; // Initially hidden
            sectionBox.setAttribute('data-course-code', course.course_code);
            sectionBox.setAttribute('data-section-number', section.section_number);
            sectionBox.innerHTML = `${course.course_code} - Section ${section.section_number}`;

            // Add click event listener to the section box
            sectionBox.addEventListener('click', () => {
              handleSectionClick(course, section.section_number);
            });

            div.appendChild(sectionBox); // Append the box to the div
            sectionBox.style.display = 'block'; // Show the box
          }
        }
      });
    });
  });
}

// Function to handle section click event
// Function to handle section click event
function handleSectionClick(course, sectionNumber) {
  const divs = document.getElementsByClassName('subject');

  Array.from(divs).forEach((div) => {
    const sectionBoxes = div.getElementsByClassName('section-box');

    Array.from(sectionBoxes).forEach(sectionBox => {
      const courseCode = sectionBox.getAttribute('data-course-code');
      const secNum = sectionBox.getAttribute('data-section-number');

      // If it's the same course but a different section, remove it
      if (courseCode === course.course_code && secNum !== sectionNumber) {
        div.removeChild(sectionBox); // Remove the other section's box
      }

      // If it's the selected section, add additional information only if not already added
      if (courseCode === course.course_code && secNum === sectionNumber) {
        // Check if the additional info is already in the section box
        const hasAdditionalInfo = sectionBox.querySelector('.additional-info');

        // Only add additional information if it doesn't exist
        if (!hasAdditionalInfo) {
          // Get the current section that was clicked
          const selectedSection = course.section_packets.flatMap(packet => packet.sections)
            .find(section => section.section_number === sectionNumber);

          if (selectedSection) {
            // Create additional information to display
            const additionalInfo = document.createElement('div');
            additionalInfo.className = 'additional-info'; // Add a class for easy selection later
            additionalInfo.innerHTML = `Room: ${selectedSection.room_name}, Building: ${selectedSection.building_name}, Floor: ${selectedSection.floor_name}`;

            // Append additional information to the section box
            sectionBox.appendChild(additionalInfo);

            // Optionally, update the display style to show the box
            sectionBox.style.backgroundColor = '#f0f0f0'; // Light background for visibility
            sectionBox.style.border = '1px solid #ccc'; // Border for definition
          }
        }
      }
    });
  });
}


// ... (rest of the previous code remains unchanged)


// Function to remove a course from selected courses
function removeCourse(courseToRemove) {
  selectedCourses = selectedCourses.filter(course => course.title !== courseToRemove.title);
  console.log("Updated selected courses:", selectedCourses); // Log the updated selected courses
  displaySelectedCourses(); // Update the display
}

// Function to remove course sections from the schedule
function removeCourseFromSchedule(course) {
  course.section_packets.forEach(packet => {
    packet.sections.forEach(section => {
      const divs = document.getElementsByClassName('subject');

      Array.from(divs).forEach((div) => {
        const divDay = div.getAttribute('data-day');
        const divHour = div.getAttribute('data-hour');

        // Match the div with the section's day and starting hour
        if (divDay === String(section.day) && divHour === section.starting_hour) {
          // Remove the section box by checking against the specific section
          const sectionBoxes = div.getElementsByClassName('section-box');

          Array.from(sectionBoxes).forEach(sectionBox => {
            const courseCode = sectionBox.getAttribute('data-course-code');
            const sectionNumber = sectionBox.getAttribute('data-section-number');

            // Check if the course code and section number match
            if (courseCode === course.course_code && sectionNumber === String(section.section_number)) {
              div.removeChild(sectionBox); // Remove the section box
            }
          });
        }
      });
    });
  });
}


// ... (rest of the previous code remains unchanged)

















// Function to handle search input and filter courses
function handleSearch(event) {
  const searchTerm = event.target.value.toLowerCase().trim();
  const courseResults = document.getElementById('courseResults');

  // If search input is empty, clear the results and hide the display
  if (searchTerm === '') {
    courseResults.innerHTML = '';
    courseResults.style.display = 'none';
    return;
  }

  // Filter the courses by matching the search term to the course title or course code
  const filteredCourses = courses.filter(course =>
    course.title.toLowerCase().includes(searchTerm) ||
    course.course_code.toLowerCase().includes(searchTerm)
  );

  // Display the filtered courses
  displayCourses(filteredCourses);
}

// Add event listener to the search bar after the data is loaded
document.addEventListener('DOMContentLoaded', async () => {
  try {
    await fetchCourseData(); // Fetch the course data first
    const searchBar = document.getElementById('courseSearchBar');
    searchBar.disabled = false; // Enable the search bar after courses are fetched
    searchBar.addEventListener('input', handleSearch); // Add search input handler
  } catch (error) {
    console.error('Error fetching courses:', error);
  }
});

// Function to submit the Academic Dream
// Function to submit the Academic Dream
async function submitAcademicDream() {
  const academicDreamData = [];

  // Iterate over selected courses and collect data
  for (const course of selectedCourses) {
    const packetId = selectedSectionPackets[course.course_code];
    console.log(selectedSectionPackets)
    console.log(course, packetId);
    // Check if a section packet is selected
    if (packetId) {
      const data = {
        course_code: course.course_code,
        grade: 101,
        section_packet_id: packetId,
         // Set grade to 101 as per requirement
      };
      academicDreamData.push(data);
    }
  }

  // Send data to the server
  try {
    const response = await fetch('/course/submit_academic_dream/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken() // CSRF token for security
      },
      body: JSON.stringify(academicDreamData)
    });

    if (response.ok) {
      const result = await response.json();
      alert("Academic Dream submitted successfully!");
      console.log(result);
    } else {
      alert("Error submitting Academic Dream.");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred. Please try again.");
  }
}

// Function to get CSRF token from cookies
function getCSRFToken() {
    const cookieValue = document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}


// Add event listener to the submit button
document.getElementById('submitAcademicDream').addEventListener('click', submitAcademicDream);
















