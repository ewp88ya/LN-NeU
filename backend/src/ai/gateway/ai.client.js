import axios from "axios";
const AI_URL = process.env.AI_ENGINE_URL ||
    "http://ai:8000";
export class AIClient {
    async execute(payload) {
        const response = await axios.post(`${AI_URL}/execute`, payload);
        return response.data;
    }
}
//# sourceMappingURL=ai.client.js.map