import Fastify from "fastify";
import cors from "@fastify/cors";
import helmet from "@fastify/helmet";
import rateLimit from "@fastify/rate-limit";

import { aiRoute } from "./routes/v1/ai.route";


const app = Fastify({
  logger: {
    transport:
      process.env.NODE_ENV === "development"
        ? {
            target: "pino-pretty",
            options: {
              translateTime: "HH:MM:ss",
            },
          }
        : undefined,
  },
});


await app.register(cors, {
  origin: true,
});


await app.register(helmet);


await app.register(rateLimit, {
  max: 100,
  timeWindow: "1 minute",
});


await app.register(aiRoute);


app.get("/health", async () => {
  return {
    status: "ok",
    service: "LN-NeU API",
    timestamp: new Date().toISOString(),
  };
});


export default app;
