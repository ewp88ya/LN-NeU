import axios from "axios";

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
  private readonly url = "http://localhost:8000";

  async execute(task: AITaskRequest): Promise<AIResponse> {
    const response = await axios.post(
      `${this.url}/execute`,
      task
    );

    return response.data;
  }
}
