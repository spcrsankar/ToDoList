

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

  document.getElementById('cancel').addEventListener('click', function(e) {
    e.preventDefault();
    console.log("dsjfjsdl")
    document.querySelector('.new-task-form-div').style.display = 'none';
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
          }
          else{
            element.style.display = 'none';
          }
        });
      });
    
    
  });

}


//code helpt to avoid the back button after logout
function clearHistory() {
  console.log("clearing history");
  window.location.replace('/logout'); // Redirect to the logout page
  window.history.replaceState(null, null, '/logout'); // Replace the current history state with the logout page
}