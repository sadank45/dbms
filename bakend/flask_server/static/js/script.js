document.getElementById('registrationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const userData = {
                username: document.getElementById('username').value,
                email: document.getElementById('email').value,
                password: document.getElementById('password').value
            };

            try {
                const response = await fetch('/db/write', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ data: userData })
                });

                const result = await response.json();
                const messageDiv = document.getElementById('message');
                
                if (result.status === 'success') {
                    messageDiv.className = 'success';
                    messageDiv.textContent = 'User registered successfully!';
                    document.getElementById('registrationForm').reset();
                } else {
                    messageDiv.className = 'error';
                    messageDiv.textContent = 'Error: ' + (result.error || 'Registration failed');
                }
            } catch (error) {
                const messageDiv = document.getElementById('message');
                messageDiv.className = 'error';
                messageDiv.textContent = 'Error: ' + error.message;
            }
        });
