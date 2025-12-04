function connect_to_api() {
   // Define the API URL 
   const apiUrl = 'http://localhost:5000/';

   // Make a GET request
   fetch(apiUrl)
      .then(response => {
         if (!response.ok) {
            throw new Error('Network response was not ok');
         }
         return response.json();
      })
      .then(data => {
         console.log(data);
      })
      .catch(error => {
         console.error('Error:', error);
      });
}

connect_to_api()
