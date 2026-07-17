import Fastify from "fastify";
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

const app = Fastify();

const PORT = Number(process.env.PORT);
const OLLAMA_URL = process.env.OLLAMA_URL;
const MODEL = process.env.OLLAMA_MODEL;


app.post("/ai/chat", async (request, reply) => {

  const body = request.body as {
    message:string;
  };


  const response = await axios.post(
    `${OLLAMA_URL}/api/generate`,
    {
      model: MODEL,
      prompt: body.message,
      stream:false
    }
  );


  return {
    model: MODEL,
    response: response.data.response
  };

});


app.listen({
  port: PORT,
  host:"0.0.0.0"
})
.then(()=>{
  console.log(
    `LN-NeU AI Gateway running : ${PORT}`
  );
});

