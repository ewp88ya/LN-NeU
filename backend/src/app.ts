import Fastify from "fastify";
import cors from "@fastify/cors";
import helmet from "@fastify/helmet";
import rateLimit from "@fastify/rate-limit";

import { aiRoute } from "./routes/v1/ai.route.js";


const app = Fastify({
  logger:
    process.env.NODE_ENV === "development"
      ? {
          transport: {
            target: "pino-pretty",
            options: {
              translateTime: "HH:MM:ss",
            },
          },
        }
      : true,
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
    service: "LN-NeU Core API",
    version: "1.0.0",
    timestamp: new Date().toISOString(),
  };
});


export default app;
