import app from "./app.js";
import { env } from "./env.js";
const start = async () => {
    try {
        await app.listen({
            port: env.PORT,
            host: env.HOST,
        });
        console.log(`LN-NeU API running on port ${env.PORT}`);
    }
    catch (error) {
        app.log.error(error);
        process.exit(1);
    }
};
start();
//# sourceMappingURL=server.js.map