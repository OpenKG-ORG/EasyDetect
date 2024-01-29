import asyncio
import aiohttp

class GoogleSerperAPIWrapper():
    """Wrapper around the Serper.dev Google Search API.
    You can create a free API key at https://serper.dev.
    To use, you should have the environment variable ``SERPER_API_KEY``
    set with your API key, or pass `serper_api_key` as a named parameter
    to the constructor.
    Example:
        .. code-block:: python
            from langchain import GoogleSerperAPIWrapper
            google_serper = GoogleSerperAPIWrapper()
    """
    def __init__(self, config):
        self.config = config
        self.k = self.config["tool"]["google_serper"]["snippet_cnt"]
        self.gl = "us"
        self.hl = "en"
        self.serper_api_key = self.config["tool"]["google_serper"]["serper_api_key"]
        assert self.serper_api_key is not None, "Please set the SERPER_API_KEY environment variable."
        assert self.serper_api_key != '', "Please set the SERPER_API_KEY environment variable."

    async def _google_serper_search_results(self, session, search_term: str, gl: str, hl: str) -> dict:
        headers = {
            "X-API-KEY": self.serper_api_key,
            "Content-Type": "application/json",
        }
        params = {"q": search_term, "gl": gl, "hl": hl}
        async with session.post(
            "https://google.serper.dev/search", headers=headers, params=params, raise_for_status=True
        ) as response:
            return await response.json()
    
    def _parse_results(self, results):
        snippets = []
        if results.get("answerBox"):
            answer_box = results.get("answerBox", {})
            if answer_box.get("answer"):
                element = {"content":answer_box.get("answer"),"source":"None"}
                return [element]
            elif answer_box.get("snippet"):
                element = {"content":answer_box.get("snippet").replace("\n", " "),"source":"None"}
                return [element]
            elif answer_box.get("snippetHighlighted"):
                element = {"content":answer_box.get("snippetHighlighted"),"source":"None"}
                return [element]
            
        if results.get("knowledgeGraph"):
            kg = results.get("knowledgeGraph", {})
            title = kg.get("title")
            entity_type = kg.get("type")
            if entity_type:
                element = {"content":f"{title}: {entity_type}","source":"None"}
                snippets.append(element)
            description = kg.get("description")
            if description:
                element = {"content":description,"source":"None"}
                snippets.append(element)
            for attribute, value in kg.get("attributes", {}).items():
                element = {"content":f"{attribute}: {value}","source":"None"}
                snippets.append(element)

        for result in results["organic"][: self.k]:
            if "snippet" in result:
                if result["snippet"].find("Missing") != -1:
                    continue
                element = {"content":result["snippet"],"source":result["link"]}
                snippets.append(element)
            for attribute, value in result.get("attributes", {}).items():
                element = {"content":f"{attribute}: {value}","source":result["link"]}
                if element["content"].find("Missing") != -1:
                    continue
                snippets.append(element)

        if len(snippets) == 0:
            element = {"content":"No good Google Search Result was found","source":"None"}
            return [element]
        
        snippets = snippets[:int(self.k / 2)]

        return snippets
    
    async def parallel_searches(self, search_queries, gl, hl):
        async with aiohttp.ClientSession() as session:
            tasks = [self._google_serper_search_results(session, query, gl, hl) for query in search_queries]
            search_results = await asyncio.gather(*tasks, return_exceptions=True)
            return search_results


    async def run(self, queries):
        """Run query through GoogleSearch and parse result."""
        flattened_queries = []

        for sublist in queries:
            if sublist is None:
                sublist = ['None', 'None']
            for item in sublist:
                flattened_queries.append(item)

        results = await self.parallel_searches(flattened_queries, gl=self.gl, hl=self.hl)
        snippets_list = []
        for i in range(len(results)):
            snippets_list.append(self._parse_results(results[i]))
        snippets_split = [snippets_list[i] + snippets_list[i+1] for i in range(0, len(snippets_list), 2)]
        return snippets_split
    
    
    def execute(self, content):
        query_list = [content.split(",")[0][2:-1],content.split(",")[1][2:-2]]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        search_outputs_for_claims = loop.run_until_complete(self.run([query_list]))
        evidences = [[output['content'] for output in search_outputs_for_claim] for search_outputs_for_claim in
                  search_outputs_for_claims]
        return evidences[0]