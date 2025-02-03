# app/response_generator.py
from langgraph.graph import Graph
from ollama import Client

class ResponseGenerator:
    def __init__(self):
        self.client = Client(host="http://localhost:11434")
        self.graph = self._build_graph()

    def _build_graph(self):
        # Define LangGraph workflow
        graph = Graph()
        graph.add_node("generate_response", self._generate_response)
        graph.set_entry_point("generate_response")
        return graph.compile()

    def _generate_response(self, transcription):
        if not transcription:
            return "No audio input detected"
        
        try:
            response = self.client.generate(
                model="llama2", 
                prompt=f"Your task is to respond to the question {transcription}" # Ensure string type
            )
            return response["response"]
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def generate_response(self, transcription):
        return self.graph.invoke({"transcription": transcription})