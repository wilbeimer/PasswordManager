async function connect_to_api() {
   // Define the API URL 
   const apiUrl = 'http://localhost:5000/status';

   // Make a GET request
   const response = await fetch(apiUrl)
   if (!response.ok) {
      throw new Error('Network response was not ok');
   }

   const data = await response.json()
   return data;
}

async function get_credentials() {
   site = window.location.hostname;
   const apiUrl = 'http://localhost:5000/get/' + site

   const response = await fetch(apiUrl);

   if (!response.ok) {
      throw new Error('Network response was not ok');
   }

   const data = await response.json()
   return data;
}

function getVisibleField() {
   // --- Define High-Priority Selectors ---
    
    // 1. Username/Email: Target the known specific ID first, then fall back to robust attributes
    const usernameSelector = [
        '#username', // <-- Tries to find your exact element first (by ID)
        'input[id*="email"]', 
        'input[autocomplete*="username"]',
        'input[autocomplete*="email"]'
    ].join(', ');
    
    // 2. Password: Target standard high-confidence fields
    const passwordSelector = [
        'input[autocomplete*="password"]',
        'input[id*="password"]',
        'input[id*="pass"]'
    ].join(', ');

    // --- Find the Best Match ---
    
    // Use querySelector to find the *first* matching element for each
    // (This is okay if we rely on a strong ID selector like #username first)
    const usernameField = document.querySelector(usernameSelector);
    const passwordField = document.querySelector(passwordSelector);

    // --- Check for Visibility and Interactivity ---
    
    const isVisibleAndInteractive = (el) => {
        if (!el) return false;
        // Check for basic hidden properties
        if (el.type === 'hidden' || el.disabled || el.readOnly) return false;
        // Check for basic visibility (if dimensions are zero, it's likely hidden)
        if (el.offsetWidth === 0 && el.offsetHeight === 0) return false;
        return true;
    };

    const finalUsername = isVisibleAndInteractive(usernameField) ? usernameField : null;
    const finalPassword = isVisibleAndInteractive(passwordField) ? passwordField : null;

    return {
        usernameField: finalUsername,
        passwordField: finalPassword,
    };
}


function find_fields_continuously() {
   let lastSeenId = null;

   const observer = new MutationObserver(async () => {
      const { usernameField, passwordField } = getVisibleField();

    const { username, password } = await get_credentials(); // Fetch credentials once

    // --- Username Field Logic ---
    if (usernameField && usernameField.id !== lastSeenId) {
        lastSeenId = usernameField.id;

        // 1. Simulate Interaction: Focus the field to activate listeners
        usernameField.focus(); 
        
        // 2. Set Value
        usernameField.value = username;

        // 3. Dispatch Events: Tell the framework the value changed
        usernameField.dispatchEvent(new Event('input', { bubbles: true }));
        usernameField.dispatchEvent(new Event('change', { bubbles: true }));

        // 4. Simulate Interaction: Blur the field (unfocus)
        usernameField.blur();
        
        console.log(`Username field filled and activated: ${usernameField.type}`);
    };

    // --- Password Field Logic ---
    if (passwordField && passwordField.id !== lastSeenId) {
        lastSeenId = passwordField.id;

        // 1. Simulate Interaction: Focus the field to activate listeners
        passwordField.focus(); 
        
        // 2. Set Value
        passwordField.value = password;

        // 3. Dispatch Events: Tell the framework the value changed
        passwordField.dispatchEvent(new Event('input', { bubbles: true }));
        passwordField.dispatchEvent(new Event('change', { bubbles: true }));

        // 4. Simulate Interaction: Blur the field (unfocus)
        passwordField.blur();

        console.log(`Password field filled and activated: ${passwordField.type}`);
    };
   });

   observer.observe(document.body, { childList: true, subtree: true });
}

find_fields_continuously();
