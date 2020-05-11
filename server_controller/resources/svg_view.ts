const HOST: string = "127.0.0.1:8080";

function makeUrl(host, path) {
    return `http://${host}/${path}`;
}

async function getRequest(url) {
    const response = await fetch(url);
    return response.json();
}

async function postRequest(url: string, data: object) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return response.json();
}
