document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('password-form');
    const passwordOutput = document.getElementById('password-output');

    form.addEventListener('submit', async (event) => {
        // Stop the default browser action. We're handling this via Fetch.
        event.preventDefault(); 

        const lengthInput = form.querySelector('input[name="length"]');

        passwordOutput.textContent = 'Generating... hold on.';

        try {
            // Must use POST and FormData so Flask populates request.form, 
            // matching the server-side code structure.
            const formData = new FormData(form);

            const response = await fetch('/generate', {
                method: 'POST',
                body: formData 
            });
            
            const data = await response.json();

            // Check if the HTTP status was successful (200-299 range).
            if (response.ok) { 
                passwordOutput.textContent = data.password;
            } else {
                // If the server returns an error (401, 400), display the message from the JSON body.
                passwordOutput.textContent = `Error: ${data.message || 'Server returned an error.'}`;
                console.error('API Error:', data.message);
            }
        } catch (error) {
            // Catch network or execution errors.
            passwordOutput.textContent = 'Network error. Check your connection.';
            console.error('Fetch Failed:', error);
        }
    });
});
