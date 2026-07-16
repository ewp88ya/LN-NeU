export interface AITaskRequest {
  taskId: string;
  action: string;
  input: string;
  context?: Record<string, unknown>;
}

export interface AIResponse {
  taskId: string;
  status: string;
  result: unknown;
}

export class AIClient {
  async execute(
    task: AITaskRequest
  ): Promise<AIResponse> {

    // bridge Fastify -> AI Engine
    throw new Error("AI Engine bridge not connected");
  }
}
