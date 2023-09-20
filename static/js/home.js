async function get_data(id) {
  const url = '/get_task/' + id + '/';

  const response = await fetch(url)
  const data = await response.json()
  return data
}

window.onload = function() {
  const tasks = document.querySelectorAll("input[type='checkbox']")
  tasks.forEach(task => {
    task.addEventListener('change', function() {
      const id = this.id.split('-')[1];
      const url = '/complete/' + id + '/' ;
      fetch(url)
        .then(function(response) {
        if (response.ok) {
          console.log('Task updated');
          window.history.replaceState(null, null, '/home');
          return;
        }
        throw new Error('Request failed.');
      }).catch(function(error) {
        console.log(error);
      });
    });
  });

  const deleteButtons = document.querySelectorAll(".remove-logo")
  console.log(deleteButtons)

  deleteButtons.forEach(button => {

    button.addEventListener('click', function() {
      console.log('delete button clicked')
      const id = this.id.split('-')[1];
      const url = '/delete/' + id + '/' ;
      fetch(url)
        .then(function(response) {
        if (response.ok) {
          console.log('Task deleted');
          document.getElementById(id).remove();
          window.history.replaceState(null, null, '/home'); //
          return;
        }
        throw new Error('Request failed.');
      }).catch(function(error) {
        console.log(error);
      });
    });
  });

  document.getElementById('add-logo').addEventListener('click', function() {
    console.log("dkfjksjfejsejefjsj")
    document.querySelector('.new-task-form-div').style.display = 'flex';
  });

  const cancel_buttons = document.querySelectorAll('.cancel');
  cancel_buttons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      console.log("dsjfjsdl")
      document.querySelector('.new-task-form-div').style.display = 'none';
      document.querySelector('.view-task-div-div').style.display = 'none';
      document.querySelector('.edit-task-form-div').style.display = 'none';
      window.history.replaceState(null, null, '/home');
    });
  });


  document.querySelector('#search').addEventListener('click', function(e) {
    let search_text = document.querySelector('#search-text').value;
    console.log("searching")
    e.preventDefault();
    if(search_text == "") {
      document.querySelectorAll('.task').forEach(element => {
          element.style.display = 'grid';
      });
      return;
    }
    console.log(search_text)
    url = '/search/' + search_text + '/';
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
         console.log(data)
         document.querySelectorAll('.task').forEach(element => {
          console.log(element.id, data.includes(parseInt(element.id)))
          if(data.includes(parseInt(element.id))){
            element.style.display = 'grid';
            window.history.replaceState(null, null, '/home');
          }
          else{
            element.style.display = 'none';
          }
        });
      });
    
    
  });

  //view edit page
  document.querySelectorAll('.edit-logo').forEach(element => {
    element.addEventListener('click', async function() {
      const id = this.id.split('-')[1];
      document.querySelector('.edit-task-form-div').style.display = 'flex';
      document.querySelector('.edit-task-form-div').style.display = 'flex';
      document.querySelector('.edit-task-form').action = '/update/' + id + '/';
      const data = await get_data(id);
      document.querySelector('#edit-title').value = data.title;
      document.querySelector('#edit-description').value = data.description;
      document.querySelector('#edit-date').value = data.due_date;
    });
  })


  //view page
  document.querySelectorAll('.view-logo').forEach(element => {
    element.addEventListener('click', async function() {
      const id = this.id.split('-')[1];
      const data = await get_data(id);
      console.log(data)
      document.querySelector('.view-task-div-div').style.display = 'flex';

      document.querySelector('#view-title').innerHTML = data.title;
      document.querySelector('#view-description').innerHTML = data.description;
      document.querySelector('#view-date').innerHTML = data.due_date;
    });
  });


  //select all form to avoid back button
  document.querySelector('form').addEventListener('submit', function(e) {
    window.history.replaceState(null, null, '/home');
  });
}


//code helpt to avoid the back button after logout
function clearHistory() {
  console.log("clearing history");
  window.location.replace('/logout'); // Redirect to the logout page
  window.history.replaceState(null, null, '/logout'); // Replace the current history state with the logout page
}

history.pushState(null, null, location.href);
        window.onpopstate = function () {
            history.go(1);
        };