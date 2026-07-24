class ContextBuilder:


    def build(
        self,
        results,
        max_items=5
    ):


        context = []


        for item in results[:max_items]:


            context.append(

                {

                    "text":
                    item.text,


                    "score":
                    item.score,


                    "metadata":
                    item.metadata

                }

            )


        return {


            "memory_context":

            context,


            "count":

            len(context)

        }
