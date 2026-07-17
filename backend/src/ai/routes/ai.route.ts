import type { FastifyInstance } from "fastify";
import { AIClient } from "../gateway/ai.client";

const aiClient = new AIClient();

export async function aiRoute(app: FastifyInstance) {
  app.post("/ai/execute", async (request) => {
    const task = request.body as any;

    const result = await aiClient.execute(task);

    return result;
  });
}
