const BACKEND_API = 'http://127.0.0.1:4000';

export async function Login(loginData){
    const response = await fetch(`${BACKEND_API}/login`, {
        method: 'POST',
        body: JSON.stringify(loginData),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || 'could not fetch login');
    }

    return null;
};
