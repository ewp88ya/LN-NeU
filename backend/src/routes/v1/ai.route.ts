import type { FastifyInstance } from "fastify";

type ExecuteTask = {
  taskId: string;
  action: string;
  input: string;
  context?: Record<string, unknown>;
};

export async function aiRoute(app: FastifyInstance) {
  app.post("/api/v1/ai/execute", async (request, reply) => {
    const body = request.body as ExecuteTask;
    const apiKey = request.headers["x-ln-neu-api-key"];

    if (typeof apiKey !== "string" || apiKey.length < 32) {
      return reply.code(401).send({ detail: "Invalid service credentials" });
    }

    let response: Response;
    try {
      response = await fetch(
        process.env.LN_NEU_AI_EXECUTE_URL ?? "http://ln-neu-ai:8000/execute",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-LN-NeU-API-Key": apiKey,
          },
          body: JSON.stringify(body),
          signal: AbortSignal.timeout(30_000),
        },
      );
    } catch {
      return reply.code(502).send({ detail: "AI engine unavailable" });
    }

    const contentType = response.headers.get("content-type");
    reply.code(response.status);
    if (contentType) reply.header("content-type", contentType);
    return reply.send(await response.text());
  });
}
