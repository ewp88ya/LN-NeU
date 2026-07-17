import type { FastifyInstance } from "fastify";


export async function aiRoute(
  app: FastifyInstance
) {

  app.post("/api/v1/ai/execute", async (request) => {

    const body = request.body as {
      taskId: string;
      action: string;
      input: string;
    };


    const response = await fetch(
      "http://localhost:8000/execute",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }
    );


    return response.json();
  });

}
