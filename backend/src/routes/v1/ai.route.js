export async function aiRoute(app) {
    app.post("/api/v1/ai/execute", async (request) => {
        const body = request.body;
        const response = await fetch("http://localhost:8000/execute", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        });
        return response.json();
    });
}
//# sourceMappingURL=ai.route.js.map